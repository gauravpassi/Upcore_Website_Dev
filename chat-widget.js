(function () {
  'use strict';

  // ── Config ───────────────────────────────────────────────────────────────
  var LEAD_EMAIL = 'gaurav@upcoretechnologies.com';
  var LEAD_CC = 'saswata@upcoretechnologies.com';
  var BOT_NAME = 'Kai';
  var BOT_SUBTITLE = 'Upcore AI Assistant';
  var INITIAL_MESSAGE = "Hi there! I'm Kai. Tap a question below for an instant answer, or type your own and I'll pass it straight to our team for a personal reply.";

  // ── Knowledge base ───────────────────────────────────────────────────────
  var CATEGORIES = [
    { id: 'start', icon: '🚀', label: 'Getting Started' },
    { id: 'gov', icon: '🛡️', label: 'AI Governance' },
    { id: 'agents', icon: '🤖', label: 'Agents & Delivery' },
    { id: 'pricing', icon: '💰', label: 'Pricing' },
    { id: 'trust', icon: '🔒', label: 'Trust & Security' },
    { id: 'talk', icon: '📞', label: 'Talk to a Human' }
  ];

  var FAQ = [
    { id: 'gov-what', cat: 'gov', popular: true,
      q: 'What is AI Governance (the FAO)?',
      a: 'A Fractional AI Officer (FAO) is an AI-certified governance specialist embedded directly in your engineering org — accountable for the risk of AI-generated code across security, budget, and compliance. Embeds in 72 hours, no recruiting cycle. <a href="/ai-engineering-governance" target="_blank" rel="noopener">See the full framework &rarr;</a>' },
    { id: 'gov-why', cat: 'gov',
      q: 'Why do I need AI governance?',
      a: "Because your engineers are already shipping AI-generated code, and most orgs have zero review process for it. Roughly 45% of AI-generated code carries security vulnerabilities (Veracode, 2025), and most teams have no audit trail ready for the EU AI Act, HIPAA, or SOX. Your FAO owns that risk end to end." },
    { id: 'fde-what', cat: 'agents', popular: true,
      q: 'What is a Forward Deployed Engineer?',
      a: 'A dedicated engineer embedded in your workflow to build, integrate, and maintain custom AI agents against your real systems — not a demo, not a project-and-vanish agency engagement. Starting from $2,499/month. <a href="/fde-engineers" target="_blank" rel="noopener">Meet the FDE Engineers &rarr;</a>' },
    { id: 'studio-vs-nocode', cat: 'agents',
      q: 'How is Studio different from a no-code tool?',
      a: 'A no-code tool hands you a config UI and leaves integration to you. Studio is a managed service — describe a workflow in plain English, and your Forward Deployed Engineer builds, integrates, and deploys it into your actual CRM, ERP, or channels, governed by your FAO. <a href="/agent-builder" target="_blank" rel="noopener">Explore Studio &rarr;</a>' },
    { id: 'industries', cat: 'agents', popular: true,
      q: 'What industries do you work with?',
      a: 'We serve 12+ verticals, including Manufacturing, SaaS, Ecommerce/D2C, Banking &amp; Finance, Healthcare, Real Estate, Logistics, Legal &amp; Compliance, EdTech, Government, NBFC/Loans, and Marketing Agencies. <a href="/industries" target="_blank" rel="noopener">See all industries &rarr;</a>' },
    { id: 'pricing-how-much', cat: 'pricing', popular: true,
      q: 'How much does this cost?',
      a: 'AI Governance (the FAO) starts from $1,999/month. Studio and Forge agents start from $799. A dedicated FDE Engineer retainer starts from $2,499/month. Exact pricing depends on scope — confirmed for free on your Discovery Call. <a href="/pricing" target="_blank" rel="noopener">See full pricing &rarr;</a>' },
    { id: 'pricing-lockin', cat: 'pricing',
      q: 'Is there a minimum commitment?',
      a: "No lock-in on the FAO engagement. You get your first AI risk report at Day 30 — if it doesn't justify continuing, you walk away. No exit fee, no minimum term after that." },
    { id: 'start-how', cat: 'start', popular: true,
      q: 'How do I get started?',
      a: 'Book a free 45-minute Discovery Call. We\'ll audit your current setup, map your top 3 opportunities, and hand you a written action plan — no pitch, no pressure. <a href="/assessment" target="_blank" rel="noopener">Book a Discovery Call &rarr;</a>' },
    { id: 'start-speed', cat: 'start',
      q: 'How fast can you deploy?',
      a: 'AI Governance embeds in 72 hours. A single Studio agent goes live in 48 hours. Full multi-agent build-outs typically take 30&ndash;90 days depending on scope.' },
    { id: 'start-call', cat: 'start',
      q: 'What happens on the Discovery Call?',
      a: "30&ndash;45 minutes, completely free. We audit your current AI/ops posture, map your top 3 opportunities, and give you a written blueprint you can act on &mdash; with or without us." },
    { id: 'trust-security', cat: 'trust', popular: true,
      q: 'Is my code and data secure?',
      a: 'Yes &mdash; we operate under ISO 27001 and CMMI Level 3 practices, and every engagement runs under your FAO\'s governance framework from day one. <a href="/security" target="_blank" rel="noopener">See our Security page &rarr;</a>' },
    { id: 'trust-certs', cat: 'trust',
      q: 'What certifications do you hold?',
      a: 'ISO 27001, ISO 9001, and CMMI Level 3 &mdash; plus a 5.0 rating on Clutch. <a href="/security" target="_blank" rel="noopener">Full details on our Security page &rarr;</a>' }
  ];

  function faqById(id) { for (var i = 0; i < FAQ.length; i++) if (FAQ[i].id === id) return FAQ[i]; return null; }
  function faqByCat(catId) { return FAQ.filter(function (f) { return f.cat === catId; }); }
  function popularFaq() { return FAQ.filter(function (f) { return f.popular; }); }

  // ── State ────────────────────────────────────────────────────────────────
  var isOpen = false;
  var isBusy = false;
  var hasGreeted = false;
  var unreadCount = 0;
  var leadStage = null; // null | 'name' | 'email'
  var pendingQuestion = '', pendingName = '', pendingEmail = '';

  // ── Styles ───────────────────────────────────────────────────────────────
  var css = `
    #upcore-chat-btn {
      position: fixed;
      bottom: 28px;
      right: 28px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: #0a0a0a;
      border: none;
      cursor: pointer;
      z-index: 9998;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 20px rgba(0,0,0,0.28);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      outline: none;
    }
    #upcore-chat-btn:hover {
      transform: scale(1.06);
      box-shadow: 0 6px 28px rgba(10,191,204,0.32);
    }
    #upcore-chat-btn svg { transition: opacity 0.2s; }
    #upcore-chat-badge {
      position: absolute;
      top: -4px;
      right: -4px;
      width: 20px;
      height: 20px;
      background: #0ABFCC;
      border-radius: 50%;
      font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
      font-size: 11px;
      font-weight: 700;
      color: #fff;
      display: none;
      align-items: center;
      justify-content: center;
      border: 2px solid #ffffff;
    }
    #upcore-chat-window {
      position: fixed;
      bottom: 96px;
      right: 28px;
      width: 392px;
      max-width: calc(100vw - 40px);
      height: 600px;
      max-height: calc(100vh - 120px);
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 22px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      box-shadow: 0 24px 70px rgba(0,0,0,0.16), 0 4px 16px rgba(0,0,0,0.06);
      transform: translateY(16px) scale(0.97);
      opacity: 0;
      pointer-events: none;
      transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1), opacity 0.2s ease;
      font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
      overflow: hidden;
    }
    #upcore-chat-window.open {
      transform: translateY(0) scale(1);
      opacity: 1;
      pointer-events: all;
    }
    #upcore-chat-header {
      padding: 16px 16px;
      background: linear-gradient(135deg, #0a0a0a 0%, #0d1f22 65%, #0f2b2e 100%);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }
    #upcore-chat-avatar {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: #0ABFCC;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      flex-shrink: 0;
      box-shadow: 0 0 0 4px rgba(10,191,204,0.14);
    }
    #upcore-chat-info { flex: 1; min-width: 0; }
    #upcore-chat-name {
      font-size: 14.5px;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: -0.2px;
    }
    #upcore-chat-status {
      font-size: 11px;
      color: #3ddcc4;
      display: flex;
      align-items: center;
      gap: 5px;
      margin-top: 2px;
    }
    #upcore-chat-status::before {
      content: '';
      width: 5px;
      height: 5px;
      background: #3ddcc4;
      border-radius: 50%;
      display: inline-block;
    }
    #upcore-chat-close {
      background: rgba(255,255,255,0.08);
      border: none;
      color: rgba(255,255,255,0.5);
      width: 30px;
      height: 30px;
      border-radius: 7px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.15s, color 0.15s;
      flex-shrink: 0;
      outline: none;
    }
    #upcore-chat-close:hover { background: rgba(255,255,255,0.15); color: #fff; }
    #upcore-chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      scroll-behavior: smooth;
      background: #ffffff;
    }
    #upcore-chat-messages::-webkit-scrollbar { width: 4px; }
    #upcore-chat-messages::-webkit-scrollbar-track { background: transparent; }
    #upcore-chat-messages::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 2px; }
    .uc-msg-wrap { display: flex; flex-direction: column; gap: 2px; animation: ucFadeIn 0.28s ease; }
    .uc-msg-wrap.user { align-items: flex-end; }
    .uc-msg-wrap.bot { align-items: flex-start; }
    @keyframes ucFadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }
    .uc-msg {
      max-width: 88%;
      padding: 10px 14px;
      border-radius: 16px;
      font-size: 13.5px;
      line-height: 1.6;
      word-wrap: break-word;
    }
    .uc-msg.user {
      background: #0a0a0a;
      color: #ffffff;
      font-weight: 500;
      border-bottom-right-radius: 4px;
    }
    .uc-msg.bot {
      background: #f7f8fa;
      color: #2d3748;
      border-bottom-left-radius: 4px;
      border: 1px solid #e5e7eb;
    }
    .uc-msg a { color: #0ABFCC; font-weight: 600; text-decoration: none; }
    .uc-msg a:hover { text-decoration: underline; }
    #upcore-typing {
      display: none;
      align-items: flex-start;
      gap: 8px;
      padding: 0 4px;
    }
    #upcore-typing.show { display: flex; }
    .uc-typing-dots {
      background: #f7f8fa;
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      border-bottom-left-radius: 4px;
      padding: 12px 16px;
      display: flex;
      gap: 4px;
      align-items: center;
    }
    .uc-dot {
      width: 6px;
      height: 6px;
      background: #c4c9d4;
      border-radius: 50%;
      animation: ucPulse 1.2s ease-in-out infinite;
    }
    .uc-dot:nth-child(2) { animation-delay: 0.2s; }
    .uc-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes ucPulse { 0%,60%,100% { opacity:0.4; transform:scale(1); } 30% { opacity:1; transform:scale(1.2); } }

    /* Topic cards (category grid) */
    .uc-topics-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      max-width: 100%;
      width: 100%;
    }
    .uc-topic-card {
      background: #f7f8fa;
      border: 1px solid #e5e7eb;
      border-radius: 14px;
      padding: 14px 8px;
      text-align: center;
      cursor: pointer;
      transition: border-color 0.15s, background 0.15s, transform 0.15s;
      font-family: inherit;
    }
    .uc-topic-card:hover {
      border-color: #0ABFCC;
      background: #ffffff;
      transform: translateY(-2px);
    }
    .uc-topic-icon { font-size: 21px; display: block; margin-bottom: 5px; }
    .uc-topic-label { font-size: 11.5px; font-weight: 700; color: #2d3748; line-height: 1.3; }

    /* Suggestion / action chips */
    #upcore-suggestions {
      padding: 6px 16px 12px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      background: #ffffff;
      border-top: 1px solid #f2f3f5;
    }
    .uc-suggestion {
      background: #f7f8fa;
      border: 1px solid #e5e7eb;
      color: #45515e;
      font-size: 12px;
      font-family: inherit;
      padding: 6px 12px;
      border-radius: 9999px;
      cursor: pointer;
      transition: background 0.15s, border-color 0.15s, color 0.15s;
      white-space: nowrap;
      outline: none;
    }
    .uc-suggestion:hover { background: #0a0a0a; border-color: #0a0a0a; color: #ffffff; }
    .uc-suggestion.accent { border-color: rgba(10,191,204,0.35); color: #089aaa; font-weight: 600; }
    .uc-suggestion.accent:hover { background: #0ABFCC; border-color: #0ABFCC; color: #ffffff; }
    .uc-suggestion.ask-else { border-style: dashed; }

    #upcore-chat-input-area {
      padding: 10px 14px 12px;
      border-top: 1px solid #e5e7eb;
      display: flex;
      gap: 8px;
      align-items: flex-end;
      background: #ffffff;
      flex-shrink: 0;
    }
    #upcore-chat-input {
      flex: 1;
      background: #f7f8fa;
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      padding: 10px 14px;
      color: #0a0a0a;
      font-size: 13.5px;
      font-family: inherit;
      resize: none;
      outline: none;
      line-height: 1.5;
      max-height: 100px;
      transition: border-color 0.15s, background 0.15s;
    }
    #upcore-chat-input::placeholder { color: #8e8e93; }
    #upcore-chat-input:focus { border-color: #0ABFCC; background: #ffffff; }
    #upcore-chat-send {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      background: #0a0a0a;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: background 0.15s, transform 0.15s;
      outline: none;
    }
    #upcore-chat-send:hover { background: #222222; transform: scale(1.05); }
    #upcore-chat-send:disabled { opacity: 0.35; cursor: not-allowed; transform: none; }
    #upcore-chat-footer {
      text-align: center;
      font-size: 10px;
      color: #c4c9d4;
      padding: 0 16px 10px;
      background: #ffffff;
      flex-shrink: 0;
    }
    #upcore-chat-footer a { color: #c4c9d4; text-decoration: none; }
    .uc-banner {
      background: rgba(10,191,204,0.06);
      border: 1px solid rgba(10,191,204,0.2);
      border-radius: 12px;
      padding: 14px;
      text-align: center;
      margin: 4px 0;
      max-width: 100%;
    }
    .uc-banner .uc-banner-icon { font-size: 28px; margin-bottom: 6px; }
    .uc-banner .uc-banner-title { font-size: 14px; font-weight: 700; color: #0ABFCC; margin-bottom: 4px; }
    .uc-banner .uc-banner-sub { font-size: 12px; color: #45515e; line-height: 1.5; }
    @media (max-width: 440px) {
      #upcore-chat-window { right: 16px; left: 16px; width: auto; bottom: 88px; }
      #upcore-chat-btn { right: 20px; bottom: 20px; }
    }
  `;

  // ── DOM helpers ──────────────────────────────────────────────────────────
  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'html') { e.innerHTML = attrs[k]; }
      else if (k === 'text') { e.textContent = attrs[k]; }
      else if (k.startsWith('on')) { e.addEventListener(k.slice(2), attrs[k]); }
      else { e.setAttribute(k, attrs[k]); }
    });
    if (children) children.forEach(function (c) { if (c) e.appendChild(c); });
    return e;
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatUserMessage(text) {
    return escapeHtml(text).replace(/\n/g, '<br>');
  }

  // ── Render ───────────────────────────────────────────────────────────────
  var messagesEl, typingEl, suggestionsEl, inputEl, sendBtn, badgeEl, windowEl, btnEl;

  function init() {
    // Inject styles
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    // Chat toggle button
    btnEl = el('button', { id: 'upcore-chat-btn', 'aria-label': 'Open chat', onclick: toggleChat });
    badgeEl = el('span', { id: 'upcore-chat-badge' });
    btnEl.appendChild(badgeEl);
    btnEl.insertAdjacentHTML('afterbegin', chatIcon());

    // Chat window
    windowEl = el('div', { id: 'upcore-chat-window', role: 'dialog', 'aria-label': 'Chat with Kai' });

    // Header
    var header = el('div', { id: 'upcore-chat-header' });
    header.appendChild(el('div', { id: 'upcore-chat-avatar', html: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="14" rx="2"/><rect x="8" y="10" width="2" height="2"/><rect x="14" y="10" width="2" height="2"/><path d="M8 17h8"/><path d="M12 6V2"/><circle cx="12" cy="2" r="1"/></svg>' }));
    var info = el('div', { id: 'upcore-chat-info' });
    info.appendChild(el('div', { id: 'upcore-chat-name', text: BOT_NAME }));
    info.appendChild(el('div', { id: 'upcore-chat-status', text: BOT_SUBTITLE }));
    header.appendChild(info);
    header.appendChild(el('button', {
      id: 'upcore-chat-close', 'aria-label': 'Close chat',
      html: '<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
      onclick: toggleChat
    }));

    // Messages
    messagesEl = el('div', { id: 'upcore-chat-messages' });
    typingEl = el('div', { id: 'upcore-typing' });
    typingEl.insertAdjacentHTML('beforeend', '<div class="uc-typing-dots"><div class="uc-dot"></div><div class="uc-dot"></div><div class="uc-dot"></div></div>');
    messagesEl.appendChild(typingEl);

    // Suggestions
    suggestionsEl = el('div', { id: 'upcore-suggestions' });

    // Input area
    inputEl = el('textarea', {
      id: 'upcore-chat-input',
      placeholder: 'Ask me anything…',
      rows: '1',
      onkeydown: function (e) {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
      },
      oninput: function () {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
      }
    });
    sendBtn = el('button', {
      id: 'upcore-chat-send', 'aria-label': 'Send',
      html: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
      onclick: sendMessage
    });
    var inputArea = el('div', { id: 'upcore-chat-input-area' });
    inputArea.appendChild(inputEl);
    inputArea.appendChild(sendBtn);

    var footer = el('div', { id: 'upcore-chat-footer' });
    footer.innerHTML = 'Powered by <a href="https://upcoretech.com" target="_blank">Upcore AI</a>';

    windowEl.appendChild(header);
    windowEl.appendChild(messagesEl);
    windowEl.appendChild(suggestionsEl);
    windowEl.appendChild(inputArea);
    windowEl.appendChild(footer);

    document.body.appendChild(btnEl);
    document.body.appendChild(windowEl);
  }

  function chatIcon() {
    return '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2v10z" stroke="rgba(255,255,255,0.95)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="rgba(255,255,255,0.15)"/><circle cx="8.5" cy="10" r="1.3" fill="rgba(255,255,255,0.9)"/><circle cx="12" cy="10" r="1.3" fill="rgba(255,255,255,0.9)"/><circle cx="15.5" cy="10" r="1.3" fill="rgba(255,255,255,0.9)"/></svg>';
  }

  // ── Message rendering ───────────────────────────────────────────────────
  function addMessage(role, text) {
    var wrap = el('div', { class: 'uc-msg-wrap ' + role });
    var bubble = el('div', { class: 'uc-msg ' + role, html: role === 'user' ? formatUserMessage(text) : text });
    wrap.appendChild(bubble);
    messagesEl.insertBefore(wrap, typingEl);
    scrollToBottom();
  }

  function addBanner(icon, title, sub) {
    var wrap = el('div', { class: 'uc-msg-wrap bot' });
    var banner = el('div', { class: 'uc-banner' });
    banner.innerHTML = '<div class="uc-banner-icon">' + icon + '</div><div class="uc-banner-title">' + escapeHtml(title) + '</div><div class="uc-banner-sub">' + escapeHtml(sub) + '</div>';
    wrap.appendChild(banner);
    messagesEl.insertBefore(wrap, typingEl);
    scrollToBottom();
  }

  function addTopicGrid() {
    var wrap = el('div', { class: 'uc-msg-wrap bot' });
    var grid = el('div', { class: 'uc-topics-grid' });
    CATEGORIES.forEach(function (cat) {
      var card = el('button', {
        class: 'uc-topic-card',
        onclick: function () { handleCategoryClick(cat); }
      });
      card.innerHTML = '<span class="uc-topic-icon">' + cat.icon + '</span><span class="uc-topic-label">' + escapeHtml(cat.label) + '</span>';
      grid.appendChild(card);
    });
    wrap.appendChild(grid);
    messagesEl.insertBefore(wrap, typingEl);
    scrollToBottom();
  }

  function scrollToBottom() {
    setTimeout(function () { messagesEl.scrollTop = messagesEl.scrollHeight; }, 50);
  }

  function showTyping() {
    typingEl.classList.add('show');
    isBusy = true;
    sendBtn.disabled = true;
    scrollToBottom();
  }

  function hideTyping() {
    typingEl.classList.remove('show');
    isBusy = false;
    sendBtn.disabled = false;
  }

  function think(fn, delay) {
    showTyping();
    setTimeout(function () { hideTyping(); fn(); }, delay || 550);
  }

  function toggleChat() {
    isOpen = !isOpen;
    if (isOpen) {
      windowEl.classList.add('open');
      unreadCount = 0;
      badgeEl.style.display = 'none';
      setTimeout(function () { inputEl.focus(); }, 300);
      if (!hasGreeted) {
        hasGreeted = true;
        setTimeout(function () { greet(); }, 400);
      }
    } else {
      windowEl.classList.remove('open');
    }
  }

  function greet() {
    think(function () {
      addMessage('bot', INITIAL_MESSAGE);
      setTimeout(renderPopular, 300);
    }, 700);
  }

  // ── Quick-reply chip rendering ──────────────────────────────────────────
  function renderChips(items) {
    suggestionsEl.innerHTML = '';
    items.forEach(function (item) {
      var btn = el('button', {
        class: 'uc-suggestion' + (item.cls ? ' ' + item.cls : ''),
        text: item.label,
        onclick: item.onClick
      });
      suggestionsEl.appendChild(btn);
    });
  }

  function askElseChip() {
    return {
      label: '🙋 Ask us something else', cls: 'ask-else',
      onClick: function () {
        suggestionsEl.innerHTML = '';
        think(function () {
          addMessage('bot', "Sure — type your question in the box below and I'll pass it straight to our team for a personal reply.");
        }, 400);
      }
    };
  }

  function bookChip() {
    return {
      label: '📅 Book a Governance Review', cls: 'accent',
      onClick: function () {
        var a = document.createElement('a');
        a.href = '#book-governance';
        document.body.appendChild(a);
        a.click();
        a.remove();
      }
    };
  }

  function renderPopular() {
    var chips = popularFaq().map(function (f) {
      return { label: f.q, onClick: function () { handleQuestionClick(f); } };
    });
    chips.push({ label: '📂 Browse All Topics', onClick: function () { addTopicGrid(); suggestionsEl.innerHTML = ''; } });
    renderChips(chips);
  }

  function handleCategoryClick(cat) {
    if (cat.id === 'talk') {
      addMessage('user', cat.label);
      think(function () {
        addMessage('bot', "Here's how to reach the team directly:");
        renderChips([bookChip(), askElseChip(), { label: '⬅ Back to Popular', onClick: renderPopular }]);
      });
      return;
    }
    addMessage('user', cat.label);
    think(function () {
      addMessage('bot', 'Here are common questions about ' + cat.label + ':');
      var qs = faqByCat(cat.id).map(function (f) {
        return { label: f.q, onClick: function () { handleQuestionClick(f); } };
      });
      qs.push({ label: '⬅ Back to Popular', onClick: renderPopular });
      renderChips(qs);
    });
  }

  function handleQuestionClick(item) {
    addMessage('user', item.q);
    suggestionsEl.innerHTML = '';
    think(function () {
      addMessage('bot', item.a);
      var related = faqByCat(item.cat).filter(function (f) { return f.id !== item.id; }).slice(0, 3);
      var chips = related.map(function (f) {
        return { label: f.q, onClick: function () { handleQuestionClick(f); } };
      });
      chips.push({ label: '⬅ More Topics', onClick: function () { addTopicGrid(); suggestionsEl.innerHTML = ''; } });
      chips.push(askElseChip());
      renderChips(chips);
    });
  }

  // ── Free-text input → lead capture ──────────────────────────────────────
  function sendMessage() {
    var text = inputEl.value.trim();
    if (!text || isBusy) return;
    inputEl.value = '';
    inputEl.style.height = 'auto';
    handleUserInput(text);
  }

  function handleUserInput(text) {
    addMessage('user', text);
    suggestionsEl.innerHTML = '';

    if (leadStage === 'name') {
      pendingName = text;
      leadStage = 'email';
      think(function () {
        addMessage('bot', 'Thanks, ' + escapeHtml(text.split(' ')[0]) + '! And what\'s the best email to reach you at?');
      });
      return;
    }

    if (leadStage === 'email') {
      if (text.indexOf('@') === -1 || text.indexOf('.') === -1) {
        think(function () {
          addMessage('bot', "That doesn't look like a valid email — mind double-checking it?");
        }, 400);
        return;
      }
      pendingEmail = text;
      leadStage = null;
      submitLead();
      return;
    }

    // Idle — any typed message becomes a question for the team
    pendingQuestion = text;
    leadStage = 'name';
    think(function () {
      addMessage('bot', "Great question — I'll pass this straight to our team so you get a real, specific answer, not a canned one. What's your name?");
    }, 600);
  }

  function submitLead() {
    showTyping();
    fetch('https://formsubmit.co/' + LEAD_EMAIL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        _captcha: 'false',
        _template: 'table',
        _subject: 'New Chat Question — ' + pendingName,
        _cc: LEAD_CC,
        'Name': pendingName,
        'Email': pendingEmail,
        'Question': pendingQuestion,
        'Page': window.location.href,
        'Source': 'Website Chat Widget (Kai) — Custom Question'
      })
    }).catch(function () {}).then(function () {
      hideTyping();
      addBanner('📨', 'Message Sent!', "We'll reply to your question by email within 24 hours.");
      var q = pendingQuestion, n = pendingName, e = pendingEmail;
      pendingQuestion = ''; pendingName = ''; pendingEmail = '';
      if (!isOpen) { unreadCount++; badgeEl.style.display = 'flex'; badgeEl.textContent = unreadCount; }
      setTimeout(function () {
        addMessage('bot', 'Anything else I can help with?');
        renderPopular();
      }, 700);
    });
  }

  // ── Boot ─────────────────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Show badge after 8 seconds on page to draw attention
  setTimeout(function () {
    if (!isOpen && !hasGreeted) {
      unreadCount = 1;
      badgeEl.style.display = 'flex';
      badgeEl.textContent = '1';
    }
  }, 8000);

})();

// ── Governance Calendar (Calendly modal) ──────────────────────────────────
// Calendly is embedded in our own modal chrome (not their popup widget) so
// the "Book a Governance Review" experience looks identical everywhere. Its
// postMessage API (unlike Google Calendar's appointment scheduler) exposes a
// real "calendly.event_scheduled" event, letting us fire the Google Ads
// primary conversion only on an actually-completed booking.
(function () {
  var CAL_URL = 'https://calendly.com/saswata-upcoretechnologies/ai-governance-review';

  var overlay = null;
  var calIframe = null;

  window.addEventListener('message', function (e) {
    if (e.origin !== 'https://calendly.com') return;
    if (!e.data || e.data.event !== 'calendly.event_scheduled') return;
    if (typeof gtag === 'function') {
      gtag('event', 'conversion', { send_to: 'AW-16546427858/_Q5SCO7LodgcENLn-dE9' });
    }
  });

  function buildModal() {
    overlay = document.createElement('div');
    overlay.id = '_gov_cal_overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-label', 'Book a Governance Review');
    overlay.style.cssText = [
      'position:fixed;inset:0;z-index:999999;',
      'background:rgba(10,10,10,.75);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);',
      'display:none;align-items:center;justify-content:center;',
      'padding:16px;box-sizing:border-box;'
    ].join('');

    var box = document.createElement('div');
    box.style.cssText = [
      'background:#fff;border-radius:14px;overflow:hidden;',
      'width:min(820px,100%);height:min(700px,90vh);',
      'display:flex;flex-direction:column;',
      'box-shadow:0 24px 80px rgba(0,0,0,.5);'
    ].join('');

    var hdr = document.createElement('div');
    hdr.style.cssText = [
      'background:#0a0a0a;padding:13px 18px;flex-shrink:0;',
      'display:flex;align-items:center;justify-content:space-between;gap:12px;'
    ].join('');

    var dot = document.createElement('span');
    dot.style.cssText = 'width:7px;height:7px;border-radius:50%;background:#0ABFCC;flex-shrink:0;';

    var lbl = document.createElement('span');
    lbl.textContent = 'Book a Governance Review';
    lbl.style.cssText = 'color:#fff;font:600 13px/1 "DM Sans",system-ui,sans-serif;flex:1;';

    var cls = document.createElement('button');
    cls.innerHTML = '&#x2715;';
    cls.setAttribute('aria-label', 'Close');
    cls.style.cssText = [
      'background:none;border:none;cursor:pointer;padding:2px 8px;',
      'color:rgba(255,255,255,.5);font-size:20px;line-height:1;'
    ].join('');
    cls.onclick = closeModal;

    hdr.appendChild(dot);
    hdr.appendChild(lbl);
    hdr.appendChild(cls);

    calIframe = document.createElement('iframe');
    calIframe.setAttribute('title', 'Book a Governance Review');
    calIframe.setAttribute('frameborder', '0');
    calIframe.style.cssText = 'flex:1;width:100%;border:none;display:block;';

    box.appendChild(hdr);
    box.appendChild(calIframe);
    overlay.appendChild(box);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeModal();
    });
  }

  function openModal() {
    if (!overlay) buildModal();
    if (calIframe && !calIframe.src) {
      calIframe.src = CAL_URL + '?embed_domain=' + window.location.hostname + '&embed_type=Inline';
    }
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    if (!overlay) return;
    overlay.style.display = 'none';
    document.body.style.overflow = '';
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });

  document.addEventListener('click', function (e) {
    var anchor = e.target.closest('a[href="#book-governance"]');
    if (!anchor) return;
    e.preventDefault();
    openModal();
  });
})();
