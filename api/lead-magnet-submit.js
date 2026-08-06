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
//
// The team-notification EMAIL is deliberately NOT sent from here — see
// the note above sendTeamNotification's old location (now removed):
// Cloudflare (fronting FormSubmit.co) returns a 403 bot-detection
// challenge to Vercel's serverless outbound IPs no matter what headers
// are set. lp/lead-magnet-engine.js sends it client-side instead, using
// this function's own server-verified tier/overallScore/dims/weakestDim.
// ═══════════════════════════════════════════════════════════════════════

const GOOGLE_SHEETS_WEBHOOK_URL = process.env.GOOGLE_SHEETS_WEBHOOK_URL;

const PEER_MIN_SAMPLE = 30; // matches the client's honest-FOMO rule — no fabricated averages below this

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
      // q8 is a segmentation multiselect (which regulations apply) — it is
      // deliberately UNSCORED: counting ticked frameworks scored regulatory
      // exposure as if it were audit-readiness, and gave "None yet" a point.
      { id: 'q8', dimId: 'comply', type: 'multiselect' },
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
      { id: 'd9', dimId: 'adoption', maxIndex: 4 }, // 5 options — "haven't rolled out yet" added as a true zero
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
    if (q.type === 'multiselect') return; // segmentation only — never scored
    const ans = answerById[q.id];
    const max = q.maxIndex || 3;
    const raw = ans && typeof ans.index === 'number' ? Math.min(ans.index, max) : 0;
    dims[q.dimId].raw += raw;
    dims[q.dimId].maxRaw += max;
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

// ─── Team notification ─────────────────────────────────────────────────────
// NOTE: the team-notification email is sent CLIENT-SIDE by lead-magnet-engine.js
// after this function returns, not from here. Cloudflare (fronting FormSubmit.co)
// returns a 403 "Just a moment..." bot-detection challenge to Vercel's serverless
// IPs regardless of headers — it cannot be solved from a Node.js fetch() call.
// Browser-side calls (this exact pattern already works in contact.html,
// chat-widget.js, and assessment.html) aren't challenged, so the notification
// is built from this function's own server-verified score/tier/dims and fired
// from the visitor's browser instead. Confirmed via direct testing 2026-08-05.

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

    let peer = { sufficientData: false };
    try {
      peer = await writeToGoogleSheetAndGetPeerStats(row);
    } catch (err) {
      console.error('[lead-magnet-submit] Sheet write failed:', err);
    }

    return res.status(200).json({
      ok: true,
      tier: score.tier ? score.tier.label : null,
      overallScore: score.overall,
      dims: score.dims,
      weakestDim: score.weakestDim,
      peer,
      routing: { lighterTrack }
    });

  } catch (err) {
    console.error('[lead-magnet-submit] error:', err);
    return res.status(500).json({ error: 'Failed to process submission. Please try again.', detail: err.message });
  }
}
