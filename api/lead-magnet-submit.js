// ═══════════════════════════════════════════════════════════════════════
// Upcore · Lead-Magnet Submit API
// POST /api/lead-magnet-submit
//
// Called by lp/governance-index.html + lp/ai-maturity-index.html at the
// email-gate step (see lp/lead-magnet-engine.js _submitContact).
//
// 1. Recomputes the score server-side (never trust a client-submitted
//    score/tier — it's trivially spoofable in devtools).
// 2. Writes the lead as one row to a Google Sheet via a Google Apps
//    Script Web App webhook (no Apollo, no Vercel KV — this account has
//    no Vercel Pro plan, so the Sheet itself is also the peer-benchmark
//    store: the Apps Script computes and returns the niche aggregate in
//    its response, no separate database needed).
// 3. Notifies the team by email via FormSubmit.co — the same service
//    already used by assessment.html / contact.html / chat-widget.js /
//    api/build-demo.js, so this needs no new API key.
// ═══════════════════════════════════════════════════════════════════════

const GOOGLE_SHEETS_WEBHOOK_URL = process.env.GOOGLE_SHEETS_WEBHOOK_URL;

const PEER_MIN_SAMPLE = 30; // matches the client's honest-FOMO rule — no fabricated averages below this
const NOTIFY_TO = 'gaurav@upcoretechnologies.com';
const NOTIFY_CC = 'saswata@upcoretechnologies.com';
const SITE_URL = 'https://www.upcoretech.com/';

// ─── Rate limit store (in-memory, resets on cold start — same pattern as build-demo.js) ───
const rateLimitStore = {};
const RATE_LIMIT_WINDOW_MS = 30 * 60 * 1000; // 30 min
const RATE_LIMIT_MAX       = 5;               // max 5 submissions per IP per window

function getClientIP(req) {
  return (req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown').split(',')[0].trim();
}

function checkRateLimit(ip) {
  const now = Date.now();
  if (!rateLimitStore[ip]) rateLimitStore[ip] = [];
  rateLimitStore[ip] = rateLimitStore[ip].filter(t => now - t < RATE_LIMIT_WINDOW_MS);
  if (rateLimitStore[ip].length >= RATE_LIMIT_MAX) {
    return { allowed: false, reason: 'Too many submissions from your IP. Please wait a while and try again.' };
  }
  rateLimitStore[ip].push(now);
  return { allowed: true };
}

// ─── Per-niche scoring config ──────────────────────────────────────────────
// Mirrors NICHE_CONFIG.screens[].questions in lp/governance-index.html and
// lp/ai-maturity-index.html — id/dimId/type/modifierFor/capValue only
// (no copy text needed server-side). Keep in sync if questions change.

const NICHE_SCORING = {
  'governance-index': {
    label: 'Governance Index',
    questions: [
      { id: 'q1', dimId: 'align' },
      { id: 'q2', dimId: 'align' },
      { id: 'q3', dimId: 'accelerate' },
      { id: 'q4', dimId: 'accelerate' },
      { id: 'q5', dimId: 'protect' },
      { id: 'q6', dimId: 'protect' },
      { id: 'q7', dimId: 'comply' },
      { id: 'q8', dimId: 'comply', type: 'multiselect', modifierFor: 'q7', capValue: 3 },
      { id: 'q9', dimId: 'optimise' },
      { id: 'q10', dimId: 'optimise' }
    ],
    dimOrder: ['align', 'accelerate', 'protect', 'comply', 'optimise'],
    tierTable: [
      { min: 0, max: 25, label: 'Ungoverned' },
      { min: 26, max: 50, label: 'Reactive' },
      { min: 51, max: 75, label: 'Structured' },
      { min: 76, max: 100, label: 'Governed', lighterCTA: true }
    ],
    softDisqualifyQuestions: []
  },
  'ai-maturity-index': {
    label: 'AI Maturity Index',
    questions: [
      { id: 'd1', dimId: 'vision' },
      { id: 'd2', dimId: 'ownership', softDisqualifyIndex: 3 },
      { id: 'd3', dimId: 'inventory' },
      { id: 'd4', dimId: 'coordination' },
      { id: 'd5', dimId: 'roi' },
      { id: 'd6', dimId: 'budget' },
      { id: 'd7', dimId: 'visibility' },
      { id: 'd8', dimId: 'tooling' },
      { id: 'd9', dimId: 'adoption' },
      { id: 'd10', dimId: 'oversight' }
    ],
    dimOrder: ['vision', 'ownership', 'inventory', 'coordination', 'roi', 'budget', 'visibility', 'tooling', 'adoption', 'oversight'],
    tierTable: [
      { min: 0, max: 25, label: 'Fragmented' },
      { min: 26, max: 50, label: 'Emerging' },
      { min: 51, max: 75, label: 'Aligning' },
      { min: 76, max: 100, label: 'Orchestrated', lighterCTA: true }
    ],
    softDisqualifyQuestions: ['d2']
  }
};

// answers: [{questionId, index, indices}] as sent by _serializeAnswers() in lead-magnet-engine.js
function computeScore(niche, answers) {
  const cfg = NICHE_SCORING[niche];
  const answerById = {};
  answers.forEach(a => { answerById[a.questionId] = a; });

  const dims = {}; // dimId -> {raw, maxRaw}
  cfg.dimOrder.forEach(id => { dims[id] = { raw: 0, maxRaw: 0 }; });

  cfg.questions.forEach(q => {
    if (q.type === 'multiselect') return; // handled as a modifier below
    const ans = answerById[q.id];
    const raw = ans && typeof ans.index === 'number' ? ans.index : 0;
    dims[q.dimId].raw += raw;
    dims[q.dimId].maxRaw += 3;
  });

  cfg.questions.forEach(q => {
    if (q.type !== 'multiselect' || !q.modifierFor) return;
    const target = cfg.questions.find(tq => tq.id === q.modifierFor);
    if (!target) return;
    const ans = answerById[q.id];
    const count = ans && Array.isArray(ans.indices) ? Math.min(ans.indices.length, q.capValue || 3) : 0;
    dims[target.dimId].raw += count;
    dims[target.dimId].maxRaw += q.capValue || 3;
  });

  const dimScores = {};
  let sum = 0, n = 0;
  cfg.dimOrder.forEach(id => {
    const d = dims[id];
    const pct = d.maxRaw ? Math.round((d.raw / d.maxRaw) * 100) : 0;
    dimScores[id] = pct;
    sum += pct; n++;
  });
  const overall = n ? Math.round(sum / n) : 0;

  let tier = null;
  for (const t of cfg.tierTable) {
    if (overall >= t.min && overall <= t.max) { tier = t; break; }
  }

  let weakestDim = null;
  cfg.dimOrder.forEach(id => {
    if (!weakestDim || dimScores[id] < dimScores[weakestDim]) weakestDim = id;
  });

  return { overall, dims: dimScores, dimOrder: cfg.dimOrder, tier, weakestDim, answerById };
}

function checkSoftDisqualify(niche, score) {
  const cfg = NICHE_SCORING[niche];
  if (score.tier && score.tier.lighterCTA) return true;
  return cfg.softDisqualifyQuestions.some(qid => {
    const q = cfg.questions.find(x => x.id === qid);
    const ans = score.answerById[qid];
    return q && ans && q.softDisqualifyIndex === ans.index;
  });
}

// ─── Google Sheets webhook (Apps Script Web App — see docs/ARCHITECTURE.md §5) ──
// The Apps Script both appends the row AND returns the niche's running
// aggregate (count/avgOverall/avgByDim) in its response — the Sheet is the
// only store this needs, no Vercel KV / database required.
async function writeToGoogleSheetAndGetPeerStats(row) {
  if (!GOOGLE_SHEETS_WEBHOOK_URL) {
    console.warn('[lead-magnet-submit] GOOGLE_SHEETS_WEBHOOK_URL not set — skipping sheet write');
    return { sufficientData: false };
  }
  const res = await fetch(GOOGLE_SHEETS_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(row)
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Google Sheets webhook error ${res.status}: ${text}`);
  }
  const data = await res.json();
  const peer = (data && data.peer) || {};
  const count = Number(peer.count) || 0;
  if (count < PEER_MIN_SAMPLE) return { sufficientData: false, count };
  return {
    sufficientData: true,
    count,
    avgOverall: peer.avgOverall,
    avgByDim: peer.avgByDim
  };
}

// ─── Team notification (FormSubmit.co — same service as every other lead form on this site) ──
async function sendTeamNotification(row, niche) {
  const cfg = NICHE_SCORING[niche];
  const dimLines = cfg.dimOrder.map(id => `${id}: ${row.dims[id]}`).join(', ');

  const payload = {
    _subject: `New Lead-Magnet Submission — ${row.firstName || row.email} · ${cfg.label}`,
    _template: 'table',
    _captcha: 'false',
    _cc: NOTIFY_CC,
    'Index': cfg.label,
    'Tier': `${row.tier} (${row.overallScore}/100)`,
    'Weakest Dimension': row.weakestDim,
    'Dimension Breakdown': dimLines,
    'Lighter-Track Signal': row.lighterTrack ? 'Yes' : 'No',
    'Name': row.firstName || 'Not provided',
    'Email': row.email,
    'Company': row.company || 'Not provided',
    'UTM Source': row.utmSource || 'Not set',
    'UTM Campaign': row.utmCampaign || 'Not set',
    'Submitted At': row.timestamp
  };

  const res = await fetch(`https://formsubmit.co/${NOTIFY_TO}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      // FormSubmit requires a Referer/Origin identifying a real website —
      // without one it silently rejects the submission (still HTTP 200,
      // with an "Unable to submit form... browsed as HTML files" error
      // page as the body). Server-side fetch() calls don't send a browser
      // Referer automatically, so it must be set explicitly here.
      Referer: SITE_URL,
      Origin: SITE_URL
    },
    body: JSON.stringify(payload)
  });
  const text = await res.text();
  if (!res.ok || text.indexOf('Unable to submit form') !== -1) {
    throw new Error(`FormSubmit error ${res.status}: ${text.slice(0, 300)}`);
  }
}

// ─── MAIN HANDLER ─────────────────────────────────────────────────────────────

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const ip = getClientIP(req);
  const rl = checkRateLimit(ip);
  if (!rl.allowed) return res.status(429).json({ error: rl.reason });

  let body;
  try { body = req.body; }
  catch (e) { return res.status(400).json({ error: 'Invalid request body' }); }

  const { niche, answers, contact, utm = {}, consent } = body || {};

  if (!niche || !NICHE_SCORING[niche]) {
    return res.status(400).json({ error: 'Invalid or missing niche.' });
  }
  if (!Array.isArray(answers) || !answers.length) {
    return res.status(400).json({ error: 'Answers are required.' });
  }
  if (!contact || !contact.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact.email)) {
    return res.status(400).json({ error: 'A valid email address is required.' });
  }
  if (!consent) {
    return res.status(400).json({ error: 'Consent is required.' });
  }

  try {
    const score = computeScore(niche, answers);
    const lighterTrack = checkSoftDisqualify(niche, score);

    const row = {
      timestamp: new Date().toISOString(),
      niche,
      tier: score.tier ? score.tier.label : '',
      overallScore: score.overall,
      dims: score.dims,
      weakestDim: score.weakestDim,
      lighterTrack,
      firstName: contact.firstName || '',
      email: contact.email,
      company: contact.company || '',
      utmSource: utm.utm_source || '',
      utmMedium: utm.utm_medium || '',
      utmCampaign: utm.utm_campaign || '',
      utmContent: utm.utm_content || '',
      utmTerm: utm.utm_term || '',
      gclid: utm.gclid || '',
      liFatId: utm.li_fat_id || ''
    };

    // Sheet write (+ peer stats in its response) and the team email run in
    // parallel; neither blocks the other, and either one failing shouldn't
    // stop the visitor from getting their score.
    const [sheetResult, notifyResult] = await Promise.allSettled([
      writeToGoogleSheetAndGetPeerStats(row),
      sendTeamNotification(row, niche)
    ]);

    const peer = sheetResult.status === 'fulfilled' ? sheetResult.value : { sufficientData: false };
    if (sheetResult.status === 'rejected') {
      console.error('[lead-magnet-submit] Sheet write failed:', sheetResult.reason);
    }
    if (notifyResult.status === 'rejected') {
      console.error('[lead-magnet-submit] Team notification failed:', notifyResult.reason);
    }

    return res.status(200).json({
      ok: true,
      tier: score.tier ? score.tier.label : null,
      overallScore: score.overall,
      dims: score.dims,
      peer,
      routing: { lighterTrack },
      // TEMPORARY diagnostic field — remove once email delivery is confirmed working.
      _debug: {
        sheetWrite: sheetResult.status,
        teamNotify: notifyResult.status,
        teamNotifyError: notifyResult.status === 'rejected' ? String(notifyResult.reason && notifyResult.reason.message || notifyResult.reason) : null
      }
    });

  } catch (err) {
    console.error('[lead-magnet-submit] error:', err);
    return res.status(500).json({ error: 'Failed to process submission. Please try again.', detail: err.message });
  }
}
