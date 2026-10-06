// ═══════════════════════════════════════════════════════════════════════
// Upcore · Booking Intent API
// POST /api/booking-intent
//
// Called by the booking modal in chat-widget.js when a visitor enters their
// work email before the Google Calendar scheduler. Writes one "intent" row to
// the booking Google Sheet through an Apps Script Web App
// (BOOKING_SHEETS_WEBHOOK_URL, script: tools/booking-conversions.gs).
//
// The Apps Script later matches calendar bookings to these rows by attendee
// email and records the conversion (GA4 Measurement Protocol + a Google Ads
// offline-conversion row using the stored gclid). See docs/TRACKING.md.
//
// Deliberately separate from /api/lead-magnet-submit: that webhook writes the
// LP lead CRM and returns peer benchmarks; bookings must not mix into it.
// The team-notification email is sent client-side (FormSubmit is behind a
// Cloudflare challenge that blocks Vercel's serverless IPs).
// ═══════════════════════════════════════════════════════════════════════

const BOOKING_SHEETS_WEBHOOK_URL = process.env.BOOKING_SHEETS_WEBHOOK_URL;
const BOOKING_WEBHOOK_TOKEN = process.env.BOOKING_WEBHOOK_TOKEN || ''; // must match WEBHOOK_TOKEN in the Apps Script

// ─── Rate limit store (in-memory, resets on cold start — same pattern as lead-magnet-submit.js) ───
const rateLimitStore = {};
const RATE_LIMIT_WINDOW_MS = 30 * 60 * 1000; // 30 min
const RATE_LIMIT_MAX       = 8;               // max 8 intents per IP per window

function getClientIP(req) {
  return (req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown').split(',')[0].trim();
}

function checkRateLimit(ip) {
  const now = Date.now();
  if (!rateLimitStore[ip]) rateLimitStore[ip] = [];
  rateLimitStore[ip] = rateLimitStore[ip].filter(t => now - t < RATE_LIMIT_WINDOW_MS);
  if (rateLimitStore[ip].length >= RATE_LIMIT_MAX) return false;
  rateLimitStore[ip].push(now);
  return true;
}

const clip = (v, n = 200) => (typeof v === 'string' ? v.trim().slice(0, n) : '');

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  if (!checkRateLimit(getClientIP(req))) return res.status(429).json({ error: 'Too many requests.' });

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (e) { return res.status(400).json({ error: 'Invalid request body' }); }
  }
  body = body || {};

  const email = clip(body.email, 254).toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    return res.status(400).json({ error: 'A valid email address is required.' });
  }
  const a = body.attrib && typeof body.attrib === 'object' ? body.attrib : {};

  const consent = ['granted', 'denied', 'default_granted', 'unknown_eu'].includes(body.consent) ? body.consent : '';

  const row = {
    type: 'intent',
    token: BOOKING_WEBHOOK_TOKEN,
    timestamp: new Date().toISOString(),
    email,
    page: clip(body.page),
    ctaId: clip(body.cta_id, 80),
    ctaSection: clip(body.cta_section, 80),
    gclid: clip(a.gclid),
    gbraid: clip(a.gbraid),
    wbraid: clip(a.wbraid),
    utmSource: clip(a.utm_source, 120),
    utmMedium: clip(a.utm_medium, 120),
    utmCampaign: clip(a.utm_campaign, 120),
    utmTerm: clip(a.utm_term, 120),
    utmContent: clip(a.utm_content, 120),
    landingPage: clip(a.landing_page),
    firstTouchAt: a.ts ? new Date(Number(a.ts)).toISOString() : '',
    gaClientId: /^\d+\.\d+$/.test(body.ga_client_id || '') ? body.ga_client_id : '',
    gaSessionId: /^\d+$/.test(body.ga_session_id || '') ? body.ga_session_id : '',
    consent,
    referrer: clip(body.referrer, 300),
    country: clip(req.headers['x-vercel-ip-country'], 4)
  };

  if (!BOOKING_SHEETS_WEBHOOK_URL) {
    console.warn('[booking-intent] BOOKING_SHEETS_WEBHOOK_URL not set — skipping sheet write');
    return res.status(202).json({ ok: true, stored: false });
  }

  try {
    const r = await fetch(BOOKING_SHEETS_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(row)
    });
    if (!r.ok) throw new Error(`Booking sheet webhook error ${r.status}: ${(await r.text()).slice(0, 200)}`);
    return res.status(200).json({ ok: true, stored: true });
  } catch (err) {
    console.error('[booking-intent] Sheet write failed:', err);
    return res.status(502).json({ ok: false, error: 'Could not record the booking intent.' });
  }
}
