// ── Upcore assistant (chat) ─────────────────────────────────────────────────
// Rebuilt 2026-10-07. Answers come from /api/chat (a free-tier model behind an OpenAI-compatible API,
// grounded in the site's facts; see api/chat.js). If the API is not configured, rate-limited or down,
// the widget answers from the built-in FAQ below instead, so it always works.
// "Talk to a person" sends the visitor's question and the recent transcript to the team via FormSubmit
// (same inboxes as before). The conversation is kept in sessionStorage so it survives page changes.
// Events (dataLayer on GTM pages, gtag elsewhere; no message text or personal data):
//   chat_open, chat_question {source, mode}, chat_action {action}, generate_lead {lead_source: chat_widget}.
(function () {
  'use strict';
  if (window.__upcChat) return;
  window.__upcChat = true;

  var LEAD_TO = 'gaurav@upcoretechnologies.com';
  var LEAD_CC = 'saswata@upcoretechnologies.com';
  var STORE = 'upc_chat_v2';
  var FONT = 'Geist,"DM Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif';
  var MONO = '"Geist Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace';
  var path = location.pathname.replace(/\.html$/, '').replace(/\/index$/, '/').replace(/\/$/, '') || '/';

  // ── Starter questions (page-aware) ──────────────────────────────────────
  var STARTERS = {
    '/': ['What is AI-native engineering?', 'How does a pilot work?', 'What does it cost?', 'Is our code and data secure?'],
    '/ai-native-engineering': ['How is this different from Copilot or Cursor?', 'What happens in a pilot?', 'Who decides what merges?', 'What does it cost?'],
    '/ai-engineering-governance': ['What does AI Governance include?', 'What happens in the first 30 days?', 'Can we see our AI spend by team?', 'What does it cost?'],
    '/platform': ['Which workflows can you automate?', 'How fast can a first agent go live?', 'Do agents act on their own?', 'Which systems do you connect to?'],
    '/fractional-ai-officer': ['What does a Fractional AI Officer do?', 'How is it different from a full-time hire?', 'What happens in 90 days?', 'What does it cost?'],
    '/security': ['Does our code leave our environment?', 'Which AI providers process our data?', 'Can you sign a BAA?', 'Can we use our own model?'],
    '/results': ['Which result is closest to an ecommerce brand?', 'What did you build for Woolworths?', 'Do you have healthcare examples?', 'Can we speak to a reference?'],
    '/contact': ['What happens on a discovery call?', 'Can we sign an NDA first?', 'Which time zones do you work in?'],
    '/about': ['Who leads Upcore?', 'Where is your team based?', 'What certifications do you hold?']
  };
  function starters() {
    if (STARTERS[path]) return STARTERS[path];
    if (path.indexOf('/who-we-help/') === 0) return ['What would you automate for a business like ours?', 'Do you have results in our industry?', 'How does a pilot work?', 'What does it cost?'];
    return STARTERS['/'];
  }

  // ── Built-in FAQ (used when the AI is unavailable) ──────────────────────
  var FAQ = [
    { k: ['ai-native', 'ai native', 'pipeline', 'copilot', 'cursor', 'claude code', 'delivery', 'merge', 'pull request', 'cto', 'engineering'],
      a: 'AI-Native Engineering is a governed delivery pipeline for AI-written code, installed inside your Jira or Linear, GitHub and CI/CD: specs from templates, architecture checks, automated pull-request checks, risk-scored merges and feature-flagged releases, with every rule deviation logged. A Claude Certified Architect runs it with your team. [See the nine stages](/ai-native-engineering)' },
    { k: ['pilot', 'start', 'begin', 'get started', 'trial', 'engagement', 'how does it work', 'first step'],
      a: 'Everything starts with a 45-minute discovery call and a written plan. Engineering work then begins with a pilot on one team and one service, measured against your current process; automation starts with one workflow. You see results before committing further.', act: ['book'] },
    { k: ['cost', 'price', 'pricing', 'how much', 'fee', 'budget', 'expensive', 'quote', '$'],
      a: 'The only price we publish is the Fractional AI Officer: **from $1,999 a month**. Everything else is scoped after a discovery call, and you get a written proposal with a fixed scope and price before any build starts. [Fractional AI Officer](/fractional-ai-officer#economics)', act: ['book', 'person'] },
    { k: ['secure', 'security', 'data', 'privacy', 'iso', 'soc', 'gdpr', 'hipaa', 'baa', 'nda', 'train', 'confidential'],
      a: 'Code stays in your repositories, access is scoped to what the work needs, and no code is copied to our servers. Model providers are named in your contract and do not train on your data. We hold ISO 27001, ISO 9001 and CMMI Level 3, and a Security Review Pack is available on request. [Security details](/security)' },
    { k: ['governance', 'spend', 'audit', 'policy', 'compliance', 'eu ai act', 'inventory', 'shadow ai'],
      a: 'AI Governance gives you an inventory of every AI tool with an owner, AI spend by team, data controls, AI-aware security checks on every commit and an audit trail. It is installed in 90 days, with a risk report at Day 30 when you can walk away. [AI Governance](/ai-engineering-governance)' },
    { k: ['automate', 'automation', 'agent', 'workflow', 'operations', 'crm', 'whatsapp', 'support', 'follow-up', 'follow up', 'invoice', 'documents'],
      a: 'We build AI agents that run repetitive support, operations, finance and sales work inside your CRM, ERP, helpdesk, email and WhatsApp, with people approving what matters. Our standard is a first agent live within 30 days of design sign-off. [Business Process Automation](/platform)' },
    { k: ['fractional', 'officer', 'caio', 'chief ai', 'strategy', 'roadmap', 'portfolio', 'pilots'],
      a: 'A Fractional AI Officer is an embedded AI lead on retainer, from $1,999 a month. They inventory every AI pilot and tool, pick the two or three worth scaling and stay accountable until they are live and used, with a Day-30 walk-away. [Fractional AI Officer](/fractional-ai-officer)' },
    { k: ['result', 'case', 'client', 'example', 'proof', 'reference', 'woolworths', 'worked with'],
      a: 'A few examples: Woolworths South Africa cut delivery-support tickets by more than 60%; Global PCCS replaced about $210K a year of licensed tooling; a residential developer cut time to first installment from 6–10 weeks to about 3. [All ten case studies](/results)' },
    { k: ['how fast', 'timeline', 'how long', 'weeks', 'days', 'quickly', 'when can'],
      a: 'Our standard for automation is a first agent live within 30 days of design sign-off. AI Governance is visible within 72 hours of access and runs as a 90-day plan. Engineering pilots start with one team, with duration agreed on the discovery call.' },
    { k: ['contact', 'call', 'talk', 'human', 'person', 'email', 'phone', 'meeting', 'book', 'speak'],
      a: 'The quickest way is a 45-minute discovery call; you get a written plan afterwards either way. You can also email gaurav@upcoretechnologies.com or WhatsApp +91 99881 35327 (Monday to Saturday, 9am to 7pm IST).', act: ['book', 'person'] },
    { k: ['industry', 'industries', 'who do you', 'work with', 'ecommerce', 'retail', 'accounting', 'law', 'wealth', 'staffing', 'healthcare', 'health', 'clinic', 'dental', 'hospital', 'real estate', 'property', 'bank', 'finance', 'insurance', 'logistics', 'manufacturing', 'saas', 'hospitality'],
      a: 'We work with tech and software companies, ecommerce and retail brands, operations-heavy businesses and professional services firms such as accounting, law, wealth and staffing. [Who we help](/#who-we-help)' },
    { k: ['who are you', 'company', 'team', 'founder', 'where', 'india', 'located', 'based', 'leadership', 'about'],
      a: 'Upcore Technologies has delivered for clients since 2020, in the US, UK, South Africa, Australia, Mauritius and India, from a delivery team in Mohali, India. It is led by Gaurav Passi (Co-Founder & CEO), Shrikant Maniar (Executive Director) and Shanker Dhand (Technical Head). [About Upcore](/about)' }
  ];
  function faqAnswer(q) {
    var t = ' ' + q.toLowerCase().replace(/[^\w$\s-]/g, ' ') + ' ', best = null, score = 0;
    FAQ.forEach(function (f) {
      var s = 0;
      f.k.forEach(function (k) { if (t.indexOf(k.length < 5 ? ' ' + k : k) > -1) s += k.length > 6 ? 2 : 1; });
      if (s > score) { score = s; best = f; }
    });
    if (best) return { reply: best.a, actions: best.act || [] };
    return { reply: "I can help with questions about Upcore's services, pricing, security and results. For anything specific to your situation, the team can answer directly.", actions: ['book', 'person'] };
  }

  // ── State ───────────────────────────────────────────────────────────────
  var st = load(), open = false, busy = false, mode = 'ai';
  function load() { try { var v = JSON.parse(sessionStorage.getItem(STORE) || 'null'); if (v && v.msgs) return v; } catch (e) { /* storage unavailable */ } return { msgs: [], teased: false }; }
  function save() { try { st.msgs = st.msgs.slice(-24); sessionStorage.setItem(STORE, JSON.stringify(st)); } catch (e) { /* storage unavailable */ } }
  function track(n, p) {
    p = p || {}; p.page_path = location.pathname;
    if (window.upcGTM || typeof gtag !== 'function') { window.dataLayer = window.dataLayer || []; window.dataLayer.push({ event_params: null }); window.dataLayer.push({ event: n, event_params: p }); }
    else gtag('event', n, p);
  }

  // ── Styles ──────────────────────────────────────────────────────────────
  var CSS = [
    '#upcore-chat-btn,#ucw-panel,#ucw-tease{font-family:' + FONT + ';box-sizing:border-box;-webkit-font-smoothing:antialiased;}',
    '#ucw-panel *,#ucw-panel *::before,#ucw-panel *::after,#upcore-chat-btn *,#ucw-tease *{box-sizing:border-box;}',
    '#upcore-chat-btn{position:fixed;right:22px;bottom:22px;z-index:9990;display:flex;align-items:center;gap:10px;height:54px;padding:0 20px 0 8px;border:0;border-radius:999px;background:#071A26;color:#EEF5F7;font:600 14.5px/1 ' + FONT + ';letter-spacing:-.01em;cursor:pointer;box-shadow:0 18px 40px -14px rgba(7,26,38,.65),inset 0 1px 0 rgba(255,255,255,.08);transition:transform .35s cubic-bezier(.16,1,.3,1),box-shadow .35s,opacity .3s;}',
    '#upcore-chat-btn:hover{transform:translateY(-2px);box-shadow:0 24px 48px -14px rgba(7,26,38,.7),inset 0 1px 0 rgba(255,255,255,.1);}',
    '#upcore-chat-btn:focus-visible{outline:2px solid #0A84FF;outline-offset:3px;}',
    '#upcore-chat-btn.is-open{opacity:0;pointer-events:none;transform:scale(.9);}',
    '.ucw-orb{position:relative;width:38px;height:38px;border-radius:50%;flex-shrink:0;background:radial-gradient(circle at 32% 30%,#7DE6F6,#21D2ED 40%,#0A6F82 75%);box-shadow:0 0 0 3px rgba(33,210,237,.16),0 0 18px rgba(33,210,237,.45);overflow:hidden;}',
    '.ucw-orb::after{content:"";position:absolute;inset:-40%;background:conic-gradient(from 0deg,transparent 0 70%,rgba(255,255,255,.55) 80%,transparent 90%);animation:ucwSpin 3.6s linear infinite;}',
    '.ucw-orb svg{position:absolute;inset:0;margin:auto;width:18px;height:18px;color:#071A26;z-index:1;}',
    '.ucw-dot{position:absolute;top:6px;left:36px;width:11px;height:11px;border-radius:50%;background:#F2A93B;border:2px solid #071A26;display:none;}',
    '#upcore-chat-btn.has-dot .ucw-dot{display:block;animation:ucwPing 1.8s ease-out infinite;}',
    '@keyframes ucwSpin{to{transform:rotate(1turn)}}',
    '@keyframes ucwPing{0%{box-shadow:0 0 0 0 rgba(242,169,59,.6)}100%{box-shadow:0 0 0 10px rgba(242,169,59,0)}}',
    '#ucw-tease{position:fixed;right:22px;bottom:88px;z-index:9990;width:280px;padding:14px 38px 14px 16px;border-radius:16px;background:#fff;color:#0A1419;font:400 14px/1.45 ' + FONT + ';box-shadow:0 24px 50px -20px rgba(7,26,38,.45),0 0 0 1px rgba(10,20,25,.06);cursor:pointer;animation:ucwUp .5s cubic-bezier(.16,1,.3,1);}',
    '#ucw-tease b{display:block;font-weight:600;margin-bottom:2px;}',
    '#ucw-tease button{position:absolute;top:8px;right:8px;width:24px;height:24px;border:0;border-radius:50%;background:transparent;color:#5D6B73;font:400 14px/1 ' + FONT + ';cursor:pointer;}',
    '#ucw-tease button:hover{background:#EEF2F4;color:#0A1419;}',
    '#ucw-panel{position:fixed;right:22px;bottom:22px;z-index:9991;width:404px;height:min(640px,calc(100vh - 44px));display:flex;flex-direction:column;border-radius:22px;background:#fff;color:#0A1419;box-shadow:0 40px 90px -30px rgba(7,26,38,.55),0 0 0 1px rgba(10,20,25,.07);overflow:hidden;opacity:0;visibility:hidden;transform:translateY(16px) scale(.97);transform-origin:100% 100%;transition:opacity .3s cubic-bezier(.16,1,.3,1),transform .45s cubic-bezier(.16,1,.3,1),visibility 0s linear .45s;}',
    '#ucw-panel.is-open{opacity:1;visibility:visible;transform:none;transition-delay:0s;}',
    '.ucw-head{display:flex;align-items:center;gap:12px;padding:14px 12px 14px 16px;background:#071A26;color:#EEF5F7;flex-shrink:0;}',
    '.ucw-head .ucw-orb{width:34px;height:34px;}',
    '.ucw-ht{flex:1;min-width:0;}',
    '.ucw-ht b{display:block;font:600 15px/1.2 ' + FONT + ';letter-spacing:-.01em;color:#fff;}',
    '.ucw-ht span{display:flex;align-items:center;gap:6px;margin-top:3px;font:400 12px/1.2 ' + FONT + ';color:#9AAEB8;}',
    '.ucw-ht span i{width:7px;height:7px;border-radius:50%;background:#3DDC97;box-shadow:0 0 0 3px rgba(61,220,151,.18);}',
    '.ucw-ht span i.is-faq{background:#F2A93B;box-shadow:0 0 0 3px rgba(242,169,59,.18);}',
    '.ucw-hb{width:34px;height:34px;display:grid;place-items:center;border:0;border-radius:50%;background:transparent;color:#C9D5DA;cursor:pointer;transition:background .2s,color .2s;}',
    '.ucw-hb:hover{background:rgba(255,255,255,.08);color:#fff;}',
    '.ucw-hb:focus-visible,.ucw-send:focus-visible,.ucw-chip:focus-visible,.ucw-act:focus-visible{outline:2px solid #0A84FF;outline-offset:2px;}',
    '.ucw-hb svg{width:17px;height:17px;}',
    '.ucw-log{flex:1;overflow-y:auto;overscroll-behavior:contain;padding:18px 16px 8px;scroll-behavior:smooth;}',
    '.ucw-log::-webkit-scrollbar{width:6px;}.ucw-log::-webkit-scrollbar-thumb{background:#DFE5E8;border-radius:3px;}',
    '.ucw-hi{padding:6px 2px 4px;animation:ucwUp .5s cubic-bezier(.16,1,.3,1);}',
    '.ucw-hi h3{margin:0;font:600 21px/1.2 ' + FONT + ';letter-spacing:-.025em;color:#0A1419;}',
    '.ucw-hi p{margin:8px 0 0;font:400 14px/1.55 ' + FONT + ';color:#5D6B73;}',
    '.ucw-k{margin:18px 0 8px;font:500 10.5px/1 ' + MONO + ';letter-spacing:.1em;text-transform:uppercase;color:#5D6B73;}',
    '.ucw-chips{display:flex;flex-direction:column;gap:6px;}',
    '.ucw-chip{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;padding:11px 14px;border:1px solid #DFE5E8;border-radius:12px;background:#fff;color:#0A1419;font:500 14px/1.35 ' + FONT + ';text-align:left;cursor:pointer;transition:border-color .2s,background .2s,transform .25s cubic-bezier(.16,1,.3,1);}',
    '.ucw-chip::after{content:"\\2192";color:#0A6F82;transition:transform .25s;}',
    '.ucw-chip:hover{border-color:#21D2ED;background:#F4FCFE;}',
    '.ucw-chip:hover::after{transform:translateX(3px);}',
    '.ucw-row{display:flex;gap:10px;margin:14px 0;animation:ucwUp .45s cubic-bezier(.16,1,.3,1);}',
    '.ucw-row.is-user{justify-content:flex-end;}',
    '.ucw-av{width:24px;height:24px;border-radius:50%;flex-shrink:0;margin-top:2px;background:radial-gradient(circle at 32% 30%,#7DE6F6,#21D2ED 45%,#0A6F82 80%);}',
    '.ucw-msg{max-width:85%;font:400 14.5px/1.6 ' + FONT + ';color:#1F2D35;word-wrap:break-word;}',
    '.ucw-row.is-user .ucw-msg{padding:10px 14px;border-radius:16px 16px 4px 16px;background:#071A26;color:#EEF5F7;}',
    '.ucw-row.is-bot .ucw-msg{padding:2px 0;}',
    '.ucw-msg p{margin:0;}.ucw-msg p+p,.ucw-msg ul+p,.ucw-msg p+ul{margin-top:8px;}',
    '.ucw-msg ul{margin:0;padding-left:18px;}.ucw-msg li{margin:3px 0;}',
    '.ucw-msg b{font-weight:600;color:#0A1419;}',
    '.ucw-msg a{color:#0A6F82;font-weight:500;text-decoration:underline;text-decoration-color:rgba(10,111,130,.35);text-underline-offset:3px;}',
    '.ucw-msg a:hover{text-decoration-color:#0A6F82;}',
    '.ucw-note{font:400 12px/1.45 ' + FONT + ';color:#5D6B73;margin-top:6px;}',
    '.ucw-acts{display:flex;flex-wrap:wrap;gap:8px;margin:2px 0 6px 34px;animation:ucwUp .45s cubic-bezier(.16,1,.3,1);}',
    '.ucw-act{display:inline-flex;align-items:center;gap:8px;padding:9px 14px;border-radius:999px;border:1px solid #DFE5E8;background:#fff;color:#0A1419;font:500 13.5px/1 ' + FONT + ';text-decoration:none;cursor:pointer;transition:background .2s,border-color .2s,color .2s;}',
    '.ucw-act.is-main{background:#21D2ED;border-color:#21D2ED;color:#071A26;}',
    '.ucw-act:hover{border-color:#0A1419;}.ucw-act.is-main:hover{background:#0A1419;border-color:#0A1419;color:#fff;}',
    '.ucw-typing{display:inline-flex;gap:4px;padding:10px 0;}',
    '.ucw-typing i{width:7px;height:7px;border-radius:50%;background:#21D2ED;animation:ucwBounce 1.1s ease-in-out infinite;}',
    '.ucw-typing i:nth-child(2){animation-delay:.15s}.ucw-typing i:nth-child(3){animation-delay:.3s}',
    '@keyframes ucwBounce{0%,80%,100%{transform:translateY(0);opacity:.4}40%{transform:translateY(-5px);opacity:1}}',
    '@keyframes ucwUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}',
    '.ucw-form{margin:6px 0 10px 34px;padding:14px;border-radius:14px;background:#F6F8F9;border:1px solid #ECF0F2;animation:ucwUp .45s cubic-bezier(.16,1,.3,1);}',
    '.ucw-form p{margin:0 0 10px;font:500 13.5px/1.45 ' + FONT + ';color:#0A1419;}',
    '.ucw-form input{display:block;width:100%;margin:0 0 8px;padding:10px 12px;border:1px solid #C9D3D8;border-radius:10px;background:#fff;color:#0A1419;font:400 14.5px/1.3 ' + FONT + ';outline:none;}',
    '.ucw-form input:focus{border-color:#0A6F82;box-shadow:0 0 0 3px rgba(33,210,237,.18);}',
    '.ucw-form .ucw-err{min-height:16px;margin:0 0 6px;font:400 12.5px/1.3 ' + FONT + ';color:#C2361F;}',
    '.ucw-form button{width:100%;padding:11px;border:0;border-radius:999px;background:#071A26;color:#fff;font:600 14px/1 ' + FONT + ';cursor:pointer;}',
    '.ucw-form button[disabled]{opacity:.6;cursor:progress;}',
    '.ucw-foot{flex-shrink:0;padding:10px 12px 12px;border-top:1px solid #ECF0F2;background:#fff;}',
    '.ucw-box{display:flex;align-items:flex-end;gap:8px;padding:6px 6px 6px 14px;border:1px solid #DFE5E8;border-radius:16px;background:#fff;transition:border-color .2s,box-shadow .2s;}',
    '.ucw-box:focus-within{border-color:#0A6F82;box-shadow:0 0 0 3px rgba(33,210,237,.16);}',
    '.ucw-in{flex:1;min-height:24px;max-height:120px;margin:0;padding:7px 0;border:0;outline:none;resize:none;background:transparent;color:#0A1419;font:400 15px/1.45 ' + FONT + ';}',
    '.ucw-in::placeholder{color:#8696A0;}',
    '.ucw-send{width:38px;height:38px;flex-shrink:0;display:grid;place-items:center;border:0;border-radius:12px;background:#0A1419;color:#21D2ED;cursor:pointer;transition:background .2s,opacity .2s,transform .2s;}',
    '.ucw-send:hover{background:#0A6F82;color:#fff;}',
    '.ucw-send[disabled]{opacity:.35;cursor:default;}',
    '.ucw-send svg{width:17px;height:17px;}',
    '.ucw-legal{margin:8px 4px 0;font:400 11.5px/1.45 ' + FONT + ';color:#5D6B73;}',
    '.ucw-legal a{color:#5D6B73;text-decoration:underline;text-underline-offset:2px;}',
    '@media (max-width:600px){',
    '#upcore-chat-btn{right:14px;bottom:14px;height:56px;width:56px;padding:0;justify-content:center;}',
    '#upcore-chat-btn .ucw-lt{display:none;}',
    '#upcore-chat-btn .ucw-orb{width:44px;height:44px;}',
    '.ucw-dot{left:40px;top:4px;}',
    '#ucw-panel{inset:0;right:0;bottom:0;width:100%;height:100%;border-radius:0;transform:translateY(24px);}',
    '.ucw-head{padding-top:max(14px,env(safe-area-inset-top));}',
    '.ucw-foot{padding-bottom:max(12px,env(safe-area-inset-bottom));}',
    '.ucw-in{font-size:16px;}',
    '#ucw-tease{display:none;}',
    'html.consent-open #upcore-chat-btn{display:none;}',
    '}',
    '@media (prefers-reduced-motion:reduce){#ucw-panel,#upcore-chat-btn,.ucw-row,.ucw-acts,.ucw-hi,.ucw-form,#ucw-tease{transition:none!important;animation:none!important;}.ucw-orb::after,.ucw-typing i{animation:none!important;}}'
  ].join('\n');

  // ── DOM helpers ─────────────────────────────────────────────────────────
  function h(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function safeHref(u) { u = String(u || '').trim(); if (/^\/[\w\-\/#.?=&]*$/.test(u)) return u; if (/^https:\/\/(www\.)?upcoretech\.com\//.test(u)) return u; return ''; }
  function md(text) {
    var lines = esc(text).split(/\n/), out = '', list = false;
    lines.forEach(function (raw) {
      var l = raw.trim();
      var inl = function (s) {
        return s.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, t, u) {
          var href = safeHref(u.replace(/&amp;/g, '&'));
          return href ? '<a href="' + esc(href) + '">' + t + '</a>' : t;
        });
      };
      if (/^[-*•]\s+/.test(l)) { if (!list) { out += '<ul>'; list = true; } out += '<li>' + inl(l.replace(/^[-*•]\s+/, '')) + '</li>'; return; }
      if (list) { out += '</ul>'; list = false; }
      if (l) out += '<p>' + inl(l) + '</p>';
    });
    if (list) out += '</ul>';
    return out;
  }
  var ICON = {
    spark: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M12 2.5c.5 4.6 2.4 6.9 7 7.5-4.6.6-6.5 2.9-7 7.5-.5-4.6-2.4-6.9-7-7.5 4.6-.6 6.5-2.9 7-7.5zM19 15.5c.2 1.8 1 2.6 2.8 2.8-1.8.2-2.6 1-2.8 2.8-.2-1.8-1-2.6-2.8-2.8 1.8-.2 2.6-1 2.8-2.8z"/></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    reset: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>',
    send: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
  };

  var btn, panel, log, input, send, statusEl, statusDot, tease;

  function init() {
    if (document.getElementById('upcore-chat-btn')) return;
    var style = document.createElement('style'); style.id = 'ucw-style'; style.textContent = CSS; document.head.appendChild(style);

    btn = h('button', '', '<span class="ucw-orb">' + ICON.spark + '</span><span class="ucw-lt">Ask Upcore</span><span class="ucw-dot"></span>');
    btn.id = 'upcore-chat-btn'; btn.type = 'button';
    btn.setAttribute('aria-label', 'Ask the Upcore assistant'); btn.setAttribute('aria-expanded', 'false'); btn.setAttribute('aria-controls', 'ucw-panel');
    btn.addEventListener('click', function () { setOpen(true); });

    panel = h('div'); panel.id = 'ucw-panel';
    panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'Upcore assistant'); panel.setAttribute('aria-modal', 'false');
    var head = h('div', 'ucw-head', '<span class="ucw-orb">' + ICON.spark + '</span><div class="ucw-ht"><b>Upcore assistant</b><span><i></i><em style="font-style:normal">AI answers from Upcore&rsquo;s own material</em></span></div>');
    statusDot = head.querySelector('.ucw-ht i'); statusEl = head.querySelector('.ucw-ht em');
    var rb = h('button', 'ucw-hb', ICON.reset); rb.type = 'button'; rb.setAttribute('aria-label', 'Start a new conversation'); rb.title = 'New conversation';
    rb.addEventListener('click', function () { st.msgs = []; save(); render(); input.focus(); });
    var cb = h('button', 'ucw-hb', ICON.close); cb.type = 'button'; cb.setAttribute('aria-label', 'Close the assistant');
    cb.addEventListener('click', function () { setOpen(false); });
    head.appendChild(rb); head.appendChild(cb);

    log = h('div', 'ucw-log'); log.setAttribute('role', 'log'); log.setAttribute('aria-live', 'polite'); log.setAttribute('aria-relevant', 'additions');

    var foot = h('div', 'ucw-foot');
    var box = h('div', 'ucw-box');
    input = h('textarea', 'ucw-in'); input.rows = 1; input.maxLength = 1000;
    input.placeholder = 'Ask about services, pricing, security…'; input.setAttribute('aria-label', 'Your question');
    send = h('button', 'ucw-send', ICON.send); send.type = 'button'; send.setAttribute('aria-label', 'Send'); send.disabled = true;
    input.addEventListener('input', function () { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 120) + 'px'; send.disabled = !input.value.trim() || busy; });
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit(); } });
    send.addEventListener('click', submit);
    box.appendChild(input); box.appendChild(send);
    foot.appendChild(box);
    foot.appendChild(h('p', 'ucw-legal', 'AI answers can be wrong; anything binding goes in a written proposal. Please don&rsquo;t share personal data here. <a href="/privacy">Privacy</a>'));

    panel.appendChild(head); panel.appendChild(log); panel.appendChild(foot);
    document.body.appendChild(btn); document.body.appendChild(panel);

    panel.addEventListener('keydown', function (e) { if (e.key === 'Escape') { e.stopPropagation(); setOpen(false); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && open && !document.getElementById('_gov_cal_overlay')) setOpen(false); });
    // Booking from inside the chat: the booking modal takes over; close the chat behind it.
    panel.addEventListener('click', function (e) { if (e.target.closest('a[href="#book-governance"]')) { track('chat_action', { action: 'book' }); setTimeout(function () { setOpen(false, true); }, 0); } });

    render();
    if (st.open && !matchMedia('(max-width: 600px)').matches) setOpen(true, true);
    scheduleTease();
  }

  function setOpen(v, quiet) {
    open = v; st.open = v; save();
    panel.classList.toggle('is-open', v);
    btn.classList.toggle('is-open', v);
    btn.setAttribute('aria-expanded', v ? 'true' : 'false');
    btn.classList.remove('has-dot');
    if (tease) { tease.remove(); tease = null; }
    var small = matchMedia('(max-width: 600px)').matches;
    document.documentElement.style.overflow = v && small ? 'hidden' : '';
    if (v) {
      if (!quiet) track('chat_open');
      setTimeout(function () { (st.msgs.length ? input : (log.querySelector('.ucw-chip') || input)).focus(); scrollEnd(); }, 220);
    } else if (!quiet) btn.focus();
  }

  function scheduleTease() {
    if (st.teased || st.msgs.length) return;
    setTimeout(function () {
      if (open || st.teased) return;
      st.teased = true; save();
      btn.classList.add('has-dot');
      if (matchMedia('(max-width: 600px)').matches) return;
      tease = h('div', '', '<b>Questions about your AI plans?</b>Ask about services, pricing, security or results. Answers in seconds.<button type="button" aria-label="Dismiss">✕</button>');
      tease.id = 'ucw-tease'; tease.setAttribute('role', 'status');
      tease.addEventListener('click', function (e) { if (e.target.closest('button')) { tease.remove(); tease = null; return; } setOpen(true); });
      document.body.appendChild(tease);
      setTimeout(function () { if (tease) { tease.remove(); tease = null; } }, 14000);
    }, 12000);
  }

  // ── Rendering ───────────────────────────────────────────────────────────
  function scrollEnd() { log.scrollTop = log.scrollHeight; }
  function render() {
    log.innerHTML = '';
    if (!st.msgs.length) { welcome(); return; }
    st.msgs.forEach(function (m) { bubble(m.r, m.t, true); if (m.a && m.a.length) actions(m.a, true); });
    scrollEnd();
  }
  function welcome() {
    var w = h('div', 'ucw-hi', '<h3>Hi, how can we help?</h3><p>Ask anything about AI-native engineering, governance, automation, pricing, security or our results. I answer from Upcore&rsquo;s own material, and a person is one click away.</p>');
    log.appendChild(w);
    log.appendChild(h('p', 'ucw-k', 'Try asking'));
    var c = h('div', 'ucw-chips');
    starters().forEach(function (q) {
      var b = h('button', 'ucw-chip'); b.type = 'button'; b.textContent = q;
      b.addEventListener('click', function () { ask(q, 'starter'); });
      c.appendChild(b);
    });
    log.appendChild(c);
    var a = h('div', 'ucw-acts'); a.style.margin = '16px 0 4px';
    a.innerHTML = '<a class="ucw-act is-main" href="#book-governance" data-gtm-cta="book-a-discovery-call" data-gtm-cta-type="primary" data-gtm-cta-section="chat_welcome">Book a 45-minute call</a>';
    var p = h('button', 'ucw-act', 'Talk to a person'); p.type = 'button'; p.addEventListener('click', function () { personForm(''); });
    a.appendChild(p);
    log.appendChild(a);
  }
  function bubble(role, text, instant) {
    var row = h('div', 'ucw-row ' + (role === 'u' ? 'is-user' : 'is-bot'));
    if (instant) row.style.animation = 'none';
    if (role !== 'u') row.appendChild(h('span', 'ucw-av'));
    var m = h('div', 'ucw-msg', role === 'u' ? '<p>' + esc(text).replace(/\n/g, '<br>') + '</p>' : md(text));
    row.appendChild(m); log.appendChild(row);
    return row;
  }
  function actions(list, instant) {
    var a = h('div', 'ucw-acts'); if (instant) a.style.animation = 'none';
    if (list.indexOf('book') > -1) a.innerHTML = '<a class="ucw-act is-main" href="#book-governance" data-gtm-cta="book-a-discovery-call" data-gtm-cta-type="primary" data-gtm-cta-section="chat_answer">Book a 45-minute call</a>';
    if (list.indexOf('person') > -1) {
      var p = h('button', 'ucw-act', 'Talk to a person'); p.type = 'button';
      p.addEventListener('click', function () { var q = ''; for (var i = st.msgs.length - 1; i >= 0; i--) if (st.msgs[i].r === 'u') { q = st.msgs[i].t; break; } personForm(q); });
      a.appendChild(p);
    }
    log.appendChild(a);
  }
  function typing() { var r = h('div', 'ucw-row is-bot'); r.appendChild(h('span', 'ucw-av')); r.appendChild(h('div', 'ucw-msg', '<span class="ucw-typing" aria-label="Typing"><i></i><i></i><i></i></span>')); log.appendChild(r); scrollEnd(); return r; }
  function setMode(m) {
    mode = m;
    statusDot.classList.toggle('is-faq', m === 'faq');
    statusEl.textContent = m === 'faq' ? 'Answering from our FAQ right now' : 'AI answers from Upcore’s own material';
  }

  // ── Asking ──────────────────────────────────────────────────────────────
  function submit() { var q = input.value.trim(); if (!q || busy) return; input.value = ''; input.style.height = 'auto'; send.disabled = true; ask(q, 'typed'); }
  function ask(q, source) {
    if (busy) return;
    if (!st.msgs.length) log.innerHTML = '';
    busy = true;
    st.msgs.push({ r: 'u', t: q }); save();
    bubble('u', q); scrollEnd();
    var t = typing(), started = Date.now();
    var hist = st.msgs.slice(-12).map(function (m) { return { role: m.r === 'u' ? 'user' : 'assistant', content: m.t }; });
    var done = function (res, m) {
      var wait = Math.max(0, 450 - (Date.now() - started));
      setTimeout(function () {
        t.remove();
        setMode(m);
        st.msgs.push({ r: 'b', t: res.reply, a: res.actions || [] }); save();
        bubble('b', res.reply);
        if (res.actions && res.actions.length) actions(res.actions);
        scrollEnd(); busy = false; send.disabled = !input.value.trim();
        track('chat_question', { source: source, mode: m });
      }, wait);
    };
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 28000);
    fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ messages: hist, page: path }), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (x) {
        clearTimeout(timer);
        if (x.ok && x.j && x.j.reply) done({ reply: x.j.reply, actions: x.j.actions }, 'ai');
        else done(faqAnswer(q), 'faq');
      })
      .catch(function () { clearTimeout(timer); done(faqAnswer(q), 'faq'); });
  }

  // ── Talk to a person ────────────────────────────────────────────────────
  function personForm(q) {
    if (log.querySelector('.ucw-form')) { log.querySelector('.ucw-form input').focus(); return; }
    track('chat_action', { action: 'person' });
    if (!st.msgs.length) log.innerHTML = '';
    var f = h('form', 'ucw-form'); f.noValidate = true;
    f.innerHTML = '<p>Leave your details and a member of the team will reply by email within 4 business hours.</p>' +
      '<input name="name" type="text" autocomplete="name" placeholder="Your name" aria-label="Your name" required>' +
      '<input name="email" type="email" autocomplete="email" placeholder="Work email" aria-label="Work email" required>' +
      '<input name="q" type="text" placeholder="What would you like to ask?" aria-label="Your question" value="' + esc(q || '') + '">' +
      '<p class="ucw-err" role="alert"></p><button type="submit">Send to the team</button>';
    log.appendChild(f); scrollEnd();
    f.elements.name.focus();
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var n = f.elements.name.value.trim(), em = f.elements.email.value.trim(), qq = f.elements.q.value.trim(), err = f.querySelector('.ucw-err');
      if (!n) { err.textContent = 'Please add your name.'; f.elements.name.focus(); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) { err.textContent = 'Please enter a valid email.'; f.elements.email.focus(); return; }
      err.textContent = '';
      var b = f.querySelector('button'); b.disabled = true; b.textContent = 'Sending…';
      var transcript = st.msgs.slice(-10).map(function (m) { return (m.r === 'u' ? 'Visitor: ' : 'Assistant: ') + m.t.replace(/\s+/g, ' ').slice(0, 600); }).join('\n\n');
      fetch('https://formsubmit.co/' + LEAD_TO, {
        method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ _captcha: 'false', _template: 'table', _subject: 'New Chat Question — ' + n, _cc: LEAD_CC,
          'Name': n, 'Email': em, 'Question': qq || '(see conversation)', 'Conversation': transcript || '(none)', 'Page': location.href, 'Source': 'Website assistant: talk to a person' })
      }).then(function (r) { return r.ok ? r.json().catch(function () { return {}; }) : Promise.reject(); })
        .then(function (j) {
          if (j && (j.success === false || j.success === 'false')) throw new Error('not sent');
          f.remove();
          var msg = 'Thanks, ' + n.split(' ')[0] + '. Your question is with the team, and you will get a reply at ' + em + ' within 4 business hours.';
          st.msgs.push({ r: 'b', t: msg }); save(); bubble('b', msg); scrollEnd();
          track('generate_lead', { lead_source: 'chat_widget' });
        })
        .catch(function () { b.disabled = false; b.textContent = 'Send to the team'; err.textContent = 'That did not send. Please email ' + LEAD_TO + '.'; });
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

// ── Discovery-call booking modal (Google Calendar Appointment Scheduling) ───
// Google Calendar's scheduling iframe exposes no "booking completed" event, so
// booking conversions are measured server-side instead (2026-10-06):
//   1. Before the calendar, the modal asks for a work email (one field, skippable).
//   2. That email + first-touch attribution (gclid/utm from cta-tracking.js's
//      'upc_attrib') + the GA client ID go to /api/booking-intent, which writes
//      them to the booking Google Sheet (BOOKING_SHEETS_WEBHOOK_URL).
//   3. tools/booking-conversions.gs watches the booking calendar, matches new
//      bookings to intents by attendee email, then sends GA4 'booking_completed'
//      (Measurement Protocol) and writes a Google Ads offline-conversion row.
// The team also gets a FormSubmit notification so a started-but-unbooked call
// can be followed up. No email or other PII is ever pushed to dataLayer/gtag.
// The old AW-16546427858/_Q5SCO7LodgcENLn-dE9 label is deliberately not fired
// here: a modal open is not a booking. See docs/TRACKING.md.
(function () {
  var CAL_URL = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ1_obz6QaD_10QlHvG7azfJ3015e7AdPmNiUtAgdK99p_9msqj5vR6pEnHV4KsEzNBRevBOFtPn?gv=true';
  var NOTIFY_TO = 'gaurav@upcoretechnologies.com';
  var NOTIFY_CC = 'saswata@upcoretechnologies.com';
  var DONE_KEY = 'upc_book_gate';
  var FONT = 'Geist,"DM Sans",system-ui,sans-serif';

  var overlay = null, calIframe = null, closeBtn = null, gate = null, emailIn = null, errEl = null;
  var returnFocus = null, ctx = {}, openedAt = 0, engaged = false, loads = 0, baseLoads = 0, srcSetAt = 0, focusing = false;

  function track(n, p) {
    p = Object.assign({ page_path: location.pathname }, ctx, p || {});
    if (window.upcGTM || typeof gtag !== 'function') {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event_params: null });
      window.dataLayer.push({ event: n, event_params: p });
    } else gtag('event', n, p);
    if (typeof clarity === 'function') clarity('event', n);
  }
  function setInert(on) { [].forEach.call(document.body.children, function (el) { if (el !== overlay) el.inert = on; }); }
  function gateDone() { try { return sessionStorage.getItem(DONE_KEY) === '1'; } catch (e) { return false; } }
  function markGateDone() { try { sessionStorage.setItem(DONE_KEY, '1'); } catch (e) { /* storage unavailable */ } }
  function attrib() { try { return JSON.parse(localStorage.getItem('upc_attrib') || '{}') || {}; } catch (e) { return {}; } }
  // Ad-consent state travels with the intent so the Ads upload can respect it.
  function consentState() {
    var c = null;
    try { c = localStorage.getItem('upc_consent'); } catch (e) { /* storage unavailable */ }
    if (c === 'granted' || c === 'denied') return c;
    var tz = '';
    try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) { /* old browser */ }
    return /^Europe\//.test(tz) ? 'unknown_eu' : 'default_granted';
  }
  function cookie(re) { var m = document.cookie.match(re); return m ? m[1] : ''; }

  function el(tag, css, text) {
    var e = document.createElement(tag);
    if (css) e.style.cssText = css;
    if (text) e.textContent = text;
    return e;
  }

  function buildGate() {
    gate = el('form', 'flex:1;overflow:auto;display:flex;align-items:center;justify-content:center;padding:28px 22px;box-sizing:border-box;background:#fff;');
    gate.noValidate = true;
    var card = el('div', 'width:min(440px,100%);font-family:' + FONT + ';color:#0A1419;');
    var k = el('div', 'font:500 11px/1 "Geist Mono",ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:#0A6F82;margin-bottom:12px;', 'Step 1 of 2');
    var h = el('h2', 'font:600 22px/1.25 ' + FONT + ';margin:0 0 8px;letter-spacing:-.01em;', 'Where should we send the call plan?');
    h.id = '_book_gate_h';
    var p = el('p', 'font:400 15px/1.55 ' + FONT + ';color:#34434B;margin:0 0 20px;', 'Pick a time on the next screen. We send the agenda before the call and a written plan after it, whether or not we work together.');
    var lab = el('label', 'display:block;font:600 13px/1.3 ' + FONT + ';margin-bottom:6px;', 'Work email');
    lab.setAttribute('for', '_book_email');
    emailIn = el('input', 'width:100%;box-sizing:border-box;font:400 16px/1.3 ' + FONT + ';padding:12px 14px;border:1px solid #C9D3D8;border-radius:10px;color:#0A1419;background:#fff;');
    emailIn.type = 'email'; emailIn.id = '_book_email'; emailIn.name = 'email';
    emailIn.autocomplete = 'email'; emailIn.required = true; emailIn.placeholder = 'you@company.com';
    emailIn.setAttribute('aria-describedby', '_book_err _book_note');
    errEl = el('div', 'min-height:18px;font:400 13px/1.4 ' + FONT + ';color:#C2361F;margin:6px 0 10px;');
    errEl.id = '_book_err'; errEl.setAttribute('role', 'alert');
    var go = el('button', 'width:100%;font:600 15px/1 ' + FONT + ';padding:14px 18px;border:0;border-radius:999px;background:#071A26;color:#fff;cursor:pointer;');
    go.type = 'submit'; go.innerHTML = 'Continue to the calendar &rarr;';
    var note = el('p', 'font:400 12px/1.5 ' + FONT + ';color:#5D6B73;margin:14px 0 0;');
    note.id = '_book_note';
    note.innerHTML = 'We use this email only for your booking and the call plan. <a href="/privacy" style="color:#0A6F82;">Privacy policy</a>';
    var skip = el('button', 'background:none;border:0;padding:0;margin-top:14px;font:500 13px/1.4 ' + FONT + ';color:#5D6B73;text-decoration:underline;text-underline-offset:2px;cursor:pointer;', 'Skip and go straight to the calendar');
    skip.type = 'button';
    skip.onclick = function () { track('booking_email_skipped'); showCalendar(); };
    card.appendChild(k); card.appendChild(h); card.appendChild(p); card.appendChild(lab); card.appendChild(emailIn);
    card.appendChild(errEl); card.appendChild(go); card.appendChild(note); card.appendChild(skip);
    gate.appendChild(card);
    gate.setAttribute('aria-labelledby', '_book_gate_h');
    gate.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = (emailIn.value || '').trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
        errEl.textContent = 'Please enter a valid email address.';
        emailIn.setAttribute('aria-invalid', 'true');
        emailIn.focus();
        return;
      }
      emailIn.removeAttribute('aria-invalid'); errEl.textContent = '';
      sendIntent(v);
      markGateDone();
      track('generate_lead', { lead_source: 'booking_modal' });
      showCalendar();
    });
    return gate;
  }

  function sendIntent(email) {
    var a = attrib();
    var payload = {
      email: email,
      page: location.pathname,
      cta_id: ctx.cta_id || '', cta_section: ctx.cta_section || '',
      attrib: a,
      ga_client_id: cookie(/(?:^|;\s*)_ga=GA\d\.\d\.(\d+\.\d+)/),
      ga_session_id: cookie(/(?:^|;\s*)_ga_TVRF5M70ES=GS\d\.\d\.s?(\d+)/),
      consent: consentState(),
      referrer: document.referrer || ''
    };
    try {
      fetch('/api/booking-intent', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload), keepalive: true }).catch(function () {});
    } catch (e) { /* network unavailable */ }
    try {
      fetch('https://formsubmit.co/' + NOTIFY_TO, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          _subject: 'Discovery call started: ' + email,
          _template: 'table',
          _captcha: 'false',
          _cc: NOTIFY_CC,
          'Email': email,
          'Page': location.href,
          'Button': (ctx.cta_section || '') + ' / ' + (ctx.cta_id || ''),
          'Source / medium / campaign': [a.utm_source, a.utm_medium, a.utm_campaign].filter(Boolean).join(' / ') || 'direct or unknown',
          'Google Ads click': a.gclid || a.gbraid || a.wbraid ? 'Yes' : 'No',
          'Next step': 'They are now choosing a time in the calendar. If no booking arrives for this email within a day, follow up.',
          'Source': 'Website booking modal (email step)'
        })
      }).catch(function () {});
    } catch (e) { /* network unavailable */ }
  }

  function showCalendar() {
    if (calIframe && !calIframe.src) { srcSetAt = Date.now(); calIframe.src = CAL_URL; }
    if (gate) gate.style.display = 'none';
    calIframe.style.display = 'block';
    focusing = true; calIframe.focus(); setTimeout(function () { focusing = false; }, 60);
    track('booking_calendar_view');
  }

  function buildModal() {
    overlay = document.createElement('div');
    overlay.id = '_gov_cal_overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Book a Discovery Call');
    overlay.style.cssText = 'position:fixed;inset:0;z-index:999999;background:rgba(7,26,38,.72);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);display:none;align-items:center;justify-content:center;padding:16px;box-sizing:border-box;';
    var box = el('div', 'background:#fff;border-radius:16px;overflow:hidden;width:min(820px,100%);height:min(720px,92vh);display:flex;flex-direction:column;box-shadow:0 24px 80px rgba(0,0,0,.45);');
    var hdr = el('div', 'background:#071A26;padding:12px 16px 12px 18px;flex-shrink:0;display:flex;align-items:center;gap:12px;');
    var dot = el('span', 'width:7px;height:7px;border-radius:50%;background:#21D2ED;flex-shrink:0;');
    var txt = el('div', 'flex:1;min-width:0;');
    var lbl = el('div', 'color:#fff;font:600 14px/1.3 ' + FONT + ';', 'Book a Discovery Call');
    var sub = el('div', 'color:#9AAEB8;font:400 12px/1.4 ' + FONT + ';margin-top:2px;', '45 minutes · a written plan, whether or not we work together');
    txt.appendChild(lbl); txt.appendChild(sub);
    closeBtn = el('button', 'background:none;border:1px solid rgba(255,255,255,.18);border-radius:999px;cursor:pointer;width:32px;height:32px;color:#E6EEF1;font-size:15px;line-height:1;flex-shrink:0;');
    closeBtn.type = 'button';
    closeBtn.innerHTML = '&#x2715;';
    closeBtn.setAttribute('aria-label', 'Close booking');
    closeBtn.onclick = closeModal;
    hdr.appendChild(dot); hdr.appendChild(txt); hdr.appendChild(closeBtn);
    calIframe = document.createElement('iframe');
    calIframe.setAttribute('title', 'Book a Discovery Call: Google Calendar scheduling');
    calIframe.setAttribute('frameborder', '0');
    calIframe.style.cssText = 'flex:1;width:100%;border:none;display:none;';
    // Google's scheduler reloads itself while it first loads; only later loads are real navigation.
    calIframe.addEventListener('load', function () {
      loads++;
      if (Date.now() - srcSetAt < 6000) { baseLoads = loads; return; }
      if (loads > baseLoads) track('booking_iframe_navigated', { load_count: loads - baseLoads });
    });
    box.appendChild(hdr); box.appendChild(buildGate()); box.appendChild(calIframe);
    overlay.appendChild(box);
    document.body.appendChild(overlay);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
  }

  function openModal(trigger) {
    if (!overlay) buildModal();
    returnFocus = trigger || document.activeElement;
    ctx = { cta_id: (trigger && trigger.getAttribute('data-gtm-cta')) || 'book-a-discovery-call', cta_section: (trigger && trigger.getAttribute('data-gtm-cta-section')) || 'unknown' };
    engaged = false; openedAt = Date.now();
    // Preload the calendar behind the email step so it appears instantly.
    if (!calIframe.src) { srcSetAt = Date.now(); calIframe.src = CAL_URL; }
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    setInert(true);
    track('booking_modal_open');
    if (gateDone()) { gate.style.display = 'none'; calIframe.style.display = 'block'; closeBtn.focus(); }
    else { gate.style.display = 'flex'; calIframe.style.display = 'none'; errEl.textContent = ''; emailIn.focus(); }
  }

  function closeModal() {
    if (!overlay || overlay.style.display !== 'flex') return;
    overlay.style.display = 'none';
    document.body.style.overflow = '';
    setInert(false);
    track('booking_modal_close', { open_seconds: Math.round((Date.now() - openedAt) / 1000), iframe_engaged: engaged ? 'yes' : 'no' });
    var f = returnFocus && document.contains(returnFocus) ? returnFocus : (document.getElementById('upcore-chat-btn') || document.body);
    if (f && f.focus) f.focus();
  }

  window.addEventListener('blur', function () {
    setTimeout(function () {
      if (!engaged && !focusing && overlay && overlay.style.display === 'flex' && document.activeElement === calIframe) {
        engaged = true;
        track('booking_iframe_engaged', { seconds_to_engage: Math.round((Date.now() - openedAt) / 1000) });
      }
    }, 0);
  });

  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });

  document.addEventListener('click', function (e) {
    var anchor = e.target.closest('a[href="#book-governance"]');
    if (!anchor) return;
    e.preventDefault();
    openModal(anchor);
  });
})();
