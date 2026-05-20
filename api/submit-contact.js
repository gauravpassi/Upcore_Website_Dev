// POST /api/submit-contact
// Handles the contact page form. Sends team notification + prospect confirmation via Resend.

const { notifyTeam, confirmProspect } = require('./_email');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { name, company, email, industry, message } = req.body || {};

  if (!name || !email || !message) {
    return res.status(400).json({ error: 'name, email and message are required' });
  }

  try {
    // 1 — Team notification
    await notifyTeam({
      subject: `📩 New Contact Form — ${name} · ${company || 'Unknown Co.'}`,
      fields: {
        'Name':     name,
        'Company':  company || '—',
        'Email':    email,
        'Industry': industry || '—',
        'Message':  message,
        'Source':   'Contact Page Form'
      }
    });

    // 2 — Prospect confirmation (fire-and-forget)
    confirmProspect({
      to: email,
      name,
      subject: 'Your message to Upcore — we\'ll be in touch',
      heading: 'Message received ✓',
      lines: [
        'A member of our team will reply to this email <strong>within 4 hours</strong> on business days.',
        `Your message: <em>"${message.slice(0, 120)}${message.length > 120 ? '…' : ''}"</em>`,
        'You can also reach us on WhatsApp for a faster response.'
      ]
    }).catch(err => console.error('Contact confirmation email failed:', err));

    return res.status(200).json({ ok: true });

  } catch (err) {
    console.error('submit-contact error:', err);
    return res.status(500).json({ error: err.message });
  }
};
