// ─── Shared Resend email helper ───────────────────────────────────────────────
// Used by: chat.js, build-demo.js, submit-contact.js, submit-assessment.js
// Requires RESEND_API_KEY env var in Vercel.
// From address: noreply@upcoretech.com  (domain must be verified in Resend dashboard)

const FROM    = 'Upcore Technologies <noreply@upcoretech.com>';
const TEAM    = ['gaurav@upcoretechnologies.com', 'saswata@upcoretechnologies.com'];
const REPLY_TO = 'gaurav@upcoretechnologies.com';

/**
 * Send an email via Resend REST API (no SDK — plain fetch).
 * @param {{ to: string|string[], subject: string, html: string, replyTo?: string }} opts
 */
async function sendEmail({ to, subject, html, replyTo }) {
  const key = process.env.RESEND_API_KEY;
  if (!key) throw new Error('RESEND_API_KEY env var is not set');

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${key}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from: FROM,
      to: Array.isArray(to) ? to : [to],
      reply_to: replyTo || REPLY_TO,
      subject,
      html
    })
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Resend error ${res.status}: ${err}`);
  }
  return res.json();
}

/** Notification email to both Upcore inboxes */
async function notifyTeam({ subject, fields }) {
  const rows = Object.entries(fields)
    .map(([k, v]) => `
      <tr>
        <td style="padding:8px 12px;font-size:13px;color:#6b7280;width:35%;vertical-align:top;border-bottom:1px solid #f3f4f6;">${k}</td>
        <td style="padding:8px 12px;font-size:13px;color:#111827;font-weight:600;border-bottom:1px solid #f3f4f6;">${v || '—'}</td>
      </tr>`)
    .join('');

  const html = `
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#111827;">
      <div style="background:#07101e;padding:20px 24px;border-radius:8px 8px 0 0;">
        <p style="margin:0;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#0abfcc;">Upcore Technologies</p>
        <h2 style="margin:6px 0 0;font-size:18px;color:#ffffff;">${subject}</h2>
      </div>
      <div style="background:#ffffff;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 8px 8px;overflow:hidden;">
        <table style="width:100%;border-collapse:collapse;">${rows}</table>
      </div>
      <p style="font-size:11px;color:#9ca3af;margin:12px 0 0;text-align:center;">
        ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', dateStyle: 'medium', timeStyle: 'short' })} IST · upcoretech.com
      </p>
    </div>`;

  return sendEmail({ to: TEAM, subject, html });
}

/** Confirmation email to the prospect */
async function confirmProspect({ to, name, subject, heading, lines }) {
  const listItems = lines
    .map(l => `<li style="margin-bottom:8px;font-size:14px;color:#374151;">${l}</li>`)
    .join('');

  const html = `
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#111827;">
      <div style="background:#07101e;padding:20px 24px;border-radius:8px 8px 0 0;">
        <p style="margin:0;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#0abfcc;">Upcore Technologies</p>
        <h2 style="margin:6px 0 0;font-size:18px;color:#ffffff;">${heading}</h2>
      </div>
      <div style="background:#ffffff;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 8px 8px;padding:24px;">
        <p style="font-size:15px;margin:0 0 16px;">Hi ${name},</p>
        <ul style="padding-left:20px;margin:0 0 24px;">${listItems}</ul>
        <p style="font-size:13px;color:#6b7280;margin:0;">
          Questions? Reply to this email or WhatsApp us at <strong>+91 99881 35327</strong>.
        </p>
      </div>
      <p style="font-size:11px;color:#9ca3af;margin:12px 0 0;text-align:center;">
        Upcore Technologies · <a href="https://www.upcoretech.com" style="color:#0abfcc;">upcoretech.com</a>
      </p>
    </div>`;

  return sendEmail({ to, subject, html, replyTo: REPLY_TO });
}

module.exports = { sendEmail, notifyTeam, confirmProspect, TEAM };
