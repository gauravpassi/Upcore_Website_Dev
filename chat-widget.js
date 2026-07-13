(function () {
  'use strict';

  // ── Config ───────────────────────────────────────────────────────────────
  var API_URL = '/api/chat';
  var BOT_NAME = 'Kai';
  var BOT_SUBTITLE = 'Upcore AI Assistant';
  var INITIAL_MESSAGE = "Hi there! I'm Kai, Upcore's AI assistant.\n\nI can help you understand how AI agents can transform your operations, answer any questions about Upcore, or help you get started.\n\nWhat brings you here today?";
  var SUGGESTED_PROMPTS = [
    'Who governs our AI-generated code?',
    'How can AI agents help my business?',
    'What industries do you work with?',
    'Book a Discovery Call'
  ];

  // ── State ────────────────────────────────────────────────────────────────
  var messages = [];
  var isOpen = false;
  var isTyping = false;
  var hasGreeted = false;
  var booked = false;
  var unreadCount = 0;

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
      box-shadow: 0 6px 28px rgba(0,0,0,0.36);
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
      width: 380px;
      max-width: calc(100vw - 40px);
      height: 560px;
      max-height: calc(100vh - 120px);
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 60px rgba(0,0,0,0.14), 0 4px 16px rgba(0,0,0,0.06);
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
      padding: 14px 16px;
      background: #0a0a0a;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }
    #upcore-chat-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #0ABFCC;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      flex-shrink: 0;
    }
    #upcore-chat-info { flex: 1; min-width: 0; }
    #upcore-chat-name {
      font-size: 14px;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: -0.2px;
    }
    #upcore-chat-status {
      font-size: 11px;
      color: #0ABFCC;
      display: flex;
      align-items: center;
      gap: 5px;
      margin-top: 2px;
    }
    #upcore-chat-status::before {
      content: '';
      width: 5px;
      height: 5px;
      background: #0ABFCC;
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
    .uc-msg-wrap { display: flex; flex-direction: column; gap: 2px; }
    .uc-msg-wrap.user { align-items: flex-end; }
    .uc-msg-wrap.bot { align-items: flex-start; }
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
    .uc-msg a { color: #0ABFCC; text-decoration: underline; }
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
    .uc-booked-banner {
      background: rgba(10,191,204,0.06);
      border: 1px solid rgba(10,191,204,0.2);
      border-radius: 12px;
      padding: 14px;
      text-align: center;
      margin: 4px 0;
    }
    .uc-booked-banner .uc-booked-icon { font-size: 28px; margin-bottom: 6px; }
    .uc-booked-banner .uc-booked-title { font-size: 14px; font-weight: 700; color: #0ABFCC; margin-bottom: 4px; }
    .uc-booked-banner .uc-booked-sub { font-size: 12px; color: #45515e; line-height: 1.5; }
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

  function formatMessage(text) {
    return escapeHtml(text)
      .replace(/\n/g, '<br>')
      .replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
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
    renderSuggestions(SUGGESTED_PROMPTS);

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

  function renderSuggestions(prompts) {
    suggestionsEl.innerHTML = '';
    prompts.forEach(function (p) {
      var btn = el('button', {
        class: 'uc-suggestion', text: p,
        onclick: function () { sendUserMessage(p); }
      });
      suggestionsEl.appendChild(btn);
    });
  }

  function addMessage(role, text, isBookingConfirm) {
    var wrap = el('div', { class: 'uc-msg-wrap ' + role });

    if (isBookingConfirm) {
      var banner = el('div', { class: 'uc-booked-banner' });
      banner.innerHTML = '<div class="uc-booked-icon">✅</div><div class="uc-booked-title">Discovery Call Requested!</div><div class="uc-booked-sub">Check your inbox for confirmation. The Upcore team will reach out within 24 hours.</div>';
      wrap.appendChild(banner);
    } else {
      var bubble = el('div', { class: 'uc-msg ' + role, html: formatMessage(text) });
      wrap.appendChild(bubble);
    }

    // Insert before typing indicator
    messagesEl.insertBefore(wrap, typingEl);
    scrollToBottom();
  }

  function scrollToBottom() {
    setTimeout(function () { messagesEl.scrollTop = messagesEl.scrollHeight; }, 50);
  }

  function showTyping() {
    typingEl.classList.add('show');
    scrollToBottom();
  }

  function hideTyping() {
    typingEl.classList.remove('show');
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
    showTyping();
    setTimeout(function () {
      hideTyping();
      addMessage('bot', INITIAL_MESSAGE);
    }, 900);
  }

  // ── Messaging ────────────────────────────────────────────────────────────
  function sendUserMessage(text) {
    if (!text || !text.trim() || isTyping) return;
    text = text.trim();
    suggestionsEl.innerHTML = '';
    addMessage('user', text);
    messages.push({ role: 'user', content: text });
    fetchBotReply();
  }

  function sendMessage() {
    var text = inputEl.value.trim();
    if (!text || isTyping) return;
    inputEl.value = '';
    inputEl.style.height = 'auto';
    sendUserMessage(text);
  }

  function fetchBotReply() {
    if (booked) return;
    isTyping = true;
    sendBtn.disabled = true;
    showTyping();

    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: messages })
    })
      .then(function (r) { return r.json().then(function(d) { return { status: r.status, data: d }; }); })
      .then(function (res) {
        hideTyping();
        isTyping = false;
        sendBtn.disabled = false;

        var data = res.data;
        // Log error detail to console for debugging
        if (!data.reply && data.error) {
          console.warn('[Kai] API error:', data.error, data.detail || '');
        }
        var reply = data.reply || "I'm having trouble connecting. Please try again or email gaurav@upcoretechnologies.com";
        messages.push({ role: 'assistant', content: reply });

        if (data.booked) {
          booked = true;
          addMessage('bot', reply);
          setTimeout(function () { addMessage('bot', '', true); }, 600);
          // Hide input, show final CTA
          setTimeout(function () {
            suggestionsEl.innerHTML = '';
            var cta = el('button', {
              class: 'uc-suggestion',
              text: 'View Discovery Call Page →',
              onclick: function () { window.open('/assessment', '_blank'); }
            });
            suggestionsEl.appendChild(cta);
          }, 1500);
        } else {
          addMessage('bot', reply);
          // Show contextual follow-up suggestions after first exchange
          if (messages.length === 2) {
            setTimeout(function () {
              renderSuggestions(['Tell me about pricing', 'See industries →', 'Build a free demo', 'Book a call now']);
            }, 500);
          }
        }

        if (!isOpen) {
          unreadCount++;
          badgeEl.style.display = 'flex';
          badgeEl.textContent = unreadCount;
        }
      })
      .catch(function () {
        hideTyping();
        isTyping = false;
        sendBtn.disabled = false;
        addMessage('bot', "Hmm, something went wrong on my end. You can email us at gaurav@upcoretechnologies.com and we'll get back to you within a few hours.");
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

// ── Governance Calendar (iframe modal) ────────────────────────────────────
// Google's appointment scheduling page (?gv=true) is iframe-embeddable.
// We show it in our own modal — no dependency on Google's button-click
// mechanics, no popup-blocker risk, opens reliably on every click.
(function () {
  var CAL_URL = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ1_obz6QaD_10QlHvG7azfJ3015e7AdPmNiUtAgdK99p_9msqj5vR6pEnHV4KsEzNBRevBOFtPn?gv=true';

  var overlay = null;
  var calIframe = null;

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
    calIframe.setAttribute('allowfullscreen', '');
    calIframe.style.cssText = 'flex:1;width:100%;border:none;display:block;';
    calIframe.allow = 'payment camera microphone';

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
    if (calIframe && !calIframe.src) calIframe.src = CAL_URL;
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
