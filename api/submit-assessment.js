// POST /api/submit-assessment
// Handles the assessment / Discovery Call booking form. Sends team notification + confirmation via Resend.

const { notifyTeam, confirmProspect } = require('./_email');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const {
    firstName, lastName, email, company, phone,
    industry, teamSize, challenge, aiStatus
  } = req.body || {};

  if (!firstName || !email || !challenge) {
    return res.status(400).json({ error: 'firstName, email and challenge are required' });
  }

  const fullName = `${firstName} ${lastName || ''}`.trim();

  try {
    // 1 — Team notification
    await notifyTeam({
      subject: `📋 New Discovery Call Request — ${fullName} · ${company || 'Unknown Co.'}`,
      fields: {
        'Name':       fullName,
        'Company':    company    || '—',
        'Email':      email,
        'Phone':      phone      || '—',
        'Industry':   industry   || '—',
        'Team Size':  teamSize   || '—',
        'Challenge':  challenge,
        'AI Status':  aiStatus   || '—',
        'Source':     'Assessment / Discovery Call Form'
      }
    });

    // 2 — Prospect confirmation (fire-and-forget)
    confirmProspect({
      to: email,
      name: firstName,
      subject: 'Your Discovery Call Request — Upcore Technologies',
      heading: 'Discovery Call Requested ✓',
      lines: [
        'We\'ll reach out within <strong>24 hours</strong> to confirm your session time.',
        'Your session will cover:',
        '&nbsp;&nbsp;&nbsp;① Current AI posture audit',
        '&nbsp;&nbsp;&nbsp;② Your top 3 agent opportunities',
        '&nbsp;&nbsp;&nbsp;③ Draft architecture blueprint',
        '&nbsp;&nbsp;&nbsp;④ ROI estimate',
        `We\'ll be discussing: <em>"${challenge.slice(0, 120)}${challenge.length > 120 ? '…' : ''}"</em>`
      ]
    }).catch(err => console.error('Assessment confirmation email failed:', err));

    return res.status(200).json({ ok: true });

  } catch (err) {
    console.error('submit-assessment error:', err);
    return res.status(500).json({ error: err.message });
  }
};
