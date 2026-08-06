(function () {
  'use strict';

  // ── Shared behavior engine for the two lead-magnet landing pages ──────────
  // One mechanical engine, two content configs (see NICHE_CONFIG in each
  // page). This file owns flow control, scoring, chart rendering, PDF
  // generation, GTM events, and UTM capture. It never touches colors —
  // it only emits fixed class names (.lm-*); each page's own <style>
  // block decides what those classes look like (dark console vs light
  // scorecard). See docs/STRUCTURE.md for why this is a shared global
  // file (same precedent tier as chat-widget.js / cta-tracking.js).

  function slugify(text) {
    return String(text).trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  }

  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'html') { e.innerHTML = attrs[k]; }
      else if (k === 'text') { e.textContent = attrs[k]; }
      else if (k.indexOf('on') === 0 && typeof attrs[k] === 'function') { e.addEventListener(k.slice(2), attrs[k]); }
      else if (attrs[k] === null || attrs[k] === false || typeof attrs[k] === 'undefined') { /* skip — avoids setAttribute('disabled','null') leaving boolean attrs stuck "on" */ }
      else { e.setAttribute(k, attrs[k]); }
    });
    if (children) children.forEach(function (c) { if (c) e.appendChild(c); });
    return e;
  }

  function escapeHtml(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // ── UTM / click-ID capture ─────────────────────────────────────────────
  function captureUTM() {
    var params = new URLSearchParams(window.location.search);
    var utm = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'li_fat_id'].forEach(function (k) {
      var v = params.get(k);
      if (v) utm[k] = v;
    });
    return utm;
  }

  // ── Scoring ──────────────────────────────────────────────────────────────
  function allQuestions(config) {
    var out = [];
    config.screens.forEach(function (screen) {
      screen.questions.forEach(function (q) { out.push(q); });
    });
    return out;
  }

  function findQuestion(config, id) {
    var qs = allQuestions(config);
    for (var i = 0; i < qs.length; i++) if (qs[i].id === id) return qs[i];
    return null;
  }

  function computeScore(config, answers) {
    var dims = {}; // dimId -> {raw, maxRaw, label}
    var order = [];
    allQuestions(config).forEach(function (q) {
      if (q.type === 'multiselect') return; // handled as a modifier below
      if (!dims[q.dimId]) { dims[q.dimId] = { raw: 0, maxRaw: 0, label: q.dimLabel }; order.push(q.dimId); }
      var ans = answers[q.id];
      var raw = ans && typeof ans.index === 'number' ? ans.index : 0;
      dims[q.dimId].raw += raw;
      dims[q.dimId].maxRaw += 3;
    });
    allQuestions(config).forEach(function (q) {
      if (q.type !== 'multiselect' || !q.modifierFor) return;
      var target = findQuestion(config, q.modifierFor);
      if (!target || !dims[target.dimId]) return;
      var ans = answers[q.id];
      var count = ans && ans.indices ? Math.min(ans.indices.length, q.capValue || 3) : 0;
      dims[target.dimId].raw += count;
      dims[target.dimId].maxRaw += q.capValue || 3;
    });
    var dimScores = {}, sum = 0, n = 0;
    order.forEach(function (id) {
      var d = dims[id];
      var pct = d.maxRaw ? Math.round((d.raw / d.maxRaw) * 100) : 0;
      dimScores[id] = { pct: pct, label: d.label };
      sum += pct; n++;
    });
    var overall = n ? Math.round(sum / n) : 0;
    var tier = null;
    for (var i = 0; i < config.tierTable.length; i++) {
      var t = config.tierTable[i];
      if (overall >= t.min && overall <= t.max) { tier = t; break; }
    }
    return { overall: overall, dims: dimScores, dimOrder: order, tier: tier };
  }

  function weakestDim(score) {
    var weakest = null;
    score.dimOrder.forEach(function (id) {
      if (!weakest || score.dims[id].pct < score.dims[weakest].pct) weakest = id;
    });
    return weakest;
  }

  // ── Soft-disqualify / routing signals (client-side mirror; server re-verifies) ──
  function checkSoftSignals(config, answers, score) {
    var flags = { lighterTrack: false };
    if (score.tier && score.tier.lighterCTA) flags.lighterTrack = true;
    (config.softDisqualifyQuestions || []).forEach(function (qid) {
      var ans = answers[qid];
      var q = findQuestion(config, qid);
      if (ans && q && q.softDisqualifyIndex === ans.index) flags.lighterTrack = true;
    });
    return flags;
  }

  // ── Engine instance ──────────────────────────────────────────────────────
  function LeadMagnetEngine(config) {
    this.config = config;
    this.root = document.getElementById('lm-root');
    this.state = {
      screen: 'hero',
      qIndex: 0,
      pendingInsight: null,
      answers: {},
      score: null,
      apiResult: null,
      utm: captureUTM(),
      insightsShown: {}
    };
    this._lastQuizRenderKey = null;
    this._buildStickyCTA();
    this._bindKeyboard();
    this._render();
  }

  // Fires both to the dataLayer (for anyone who later wants to build GTM
  // triggers/tags off it) AND directly via gtag() — this page already loads
  // gtag.js straight for GA4 (G-TVRF5M70ES), so a direct gtag('event',...)
  // call lands in GA4 immediately with no GTM trigger/tag configuration
  // required. Same reasoning as the Google Ads conversion calls elsewhere
  // on this site (assessment.html, chat-widget.js).
  LeadMagnetEngine.prototype.pushEvent = function (key, payload) {
    var eventName = this.config.events[key];
    if (!eventName) return;
    var params = { niche: this.config.niche };
    if (payload) Object.keys(payload).forEach(function (k) { params[k] = payload[k]; });

    window.dataLayer = window.dataLayer || [];
    var dlData = { event: eventName };
    Object.keys(params).forEach(function (k) { dlData[k] = params[k]; });
    window.dataLayer.push(dlData);

    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, params);
    }
  };

  LeadMagnetEngine.prototype._render = function () {
    this.root.innerHTML = '';
    if (this.state.screen === 'hero') this._renderHero();
    else if (this.state.screen === 'intro') this._renderIntro();
    else if (this.state.screen === 'quiz') this._renderQuiz();
    else if (this.state.screen === 'teaser') this._renderTeaser();
    else if (this.state.screen === 'full') this._renderFull();
    this._updateStickyCTA();
    window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });
  };

  // ── HERO ─────────────────────────────────────────────────────────────────
  LeadMagnetEngine.prototype._renderHero = function () {
    var self = this, c = this.config, h = c.copy.hero;
    var wrap = el('div', { class: 'lm-hero' });

    wrap.appendChild(el('div', { class: 'lm-eyebrow' }, [
      el('span', { class: 'lm-eyebrow-dot' }), el('span', { text: h.eyebrow })
    ]));
    wrap.appendChild(el('h1', { class: 'lm-h1', html: h.headline }));
    wrap.appendChild(el('p', { class: 'lm-sub', html: h.subhead }));

    var ctaRow = el('div', { class: 'lm-cta-row' });
    var primaryBtn = el('button', {
      class: 'lm-btn lm-btn-primary', text: h.primaryCta,
      'data-gtm-cta': slugify(h.primaryCta), 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'hero',
      onclick: function () { self._startQuiz(); }
    });
    var secondaryLink = el('a', {
      class: 'lm-link-secondary', text: h.secondaryCta, href: c.bookingHref || '/assessment',
      'data-gtm-cta': slugify(h.secondaryCta), 'data-gtm-cta-type': 'secondary', 'data-gtm-cta-section': 'hero'
    });
    ctaRow.appendChild(primaryBtn);
    ctaRow.appendChild(secondaryLink);
    wrap.appendChild(ctaRow);

    if (h.guaranteeLine) {
      wrap.appendChild(el('p', { class: 'lm-guarantee-line', text: h.guaranteeLine }));
    }

    if (c.chart && c.chart.type === 'maturityCurve') {
      var curveCard = el('div', { class: 'lm-hero-visual-card' });
      if (h.heroVisualLabel) curveCard.appendChild(el('div', { class: 'lm-hero-visual-label', text: h.heroVisualLabel }));
      curveCard.appendChild(this._buildMaturityCurve(null));
      wrap.appendChild(curveCard);
    } else if (h.dashboardWidget) {
      wrap.appendChild(this._buildHeroWidget());
    }

    var proof = el('div', { class: 'lm-proof-bar' });
    (h.proofBar || []).forEach(function (item) { proof.appendChild(el('span', { class: 'lm-proof-item', html: item })); });
    wrap.appendChild(proof);

    if (h.whyNow) {
      var why = el('div', { class: 'lm-why-now' });
      why.appendChild(el('h2', { class: 'lm-h2', text: h.whyNow.headline }));
      var whyBody = h.whyNow.body;
      if (c.healthcareUtmMatchers && c.healthcareUtmMatchers.length && this._isHealthcareTraffic()) {
        whyBody += ' ' + h.whyNow.healthcareExtra;
      }
      why.appendChild(el('p', { class: 'lm-body', text: whyBody }));
      wrap.appendChild(why);
    }

    if (h.icpMirror && h.icpMirror.length) {
      var icp = el('div', { class: 'lm-icp' });
      icp.appendChild(el('h2', { class: 'lm-h2', text: 'Is this you?' }));
      var list = el('div', { class: 'lm-icp-list' });
      h.icpMirror.forEach(function (line) { list.appendChild(el('p', { class: 'lm-icp-line', text: '"' + line + '"' })); });
      icp.appendChild(list);
      if (h.icpClosing) icp.appendChild(el('p', { class: 'lm-icp-closing', text: h.icpClosing }));
      wrap.appendChild(icp);
    }

    if (h.howItWorks && h.howItWorks.length) {
      var hiw = el('div', { class: 'lm-how' });
      hiw.appendChild(el('h2', { class: 'lm-h2', text: 'How it works' }));
      var steps = el('div', { class: 'lm-how-steps' });
      h.howItWorks.forEach(function (step, i) {
        steps.appendChild(el('div', { class: 'lm-how-step' }, [
          el('div', { class: 'lm-how-num', text: String(i + 1) }),
          el('p', { text: step })
        ]));
      });
      hiw.appendChild(steps);
      wrap.appendChild(hiw);
    }

    if (h.faq && h.faq.length) {
      var faqWrap = el('div', { class: 'lm-faq' });
      faqWrap.appendChild(el('h2', { class: 'lm-h2', text: 'Frequently asked' }));
      h.faq.forEach(function (item) {
        var q = el('button', { class: 'lm-faq-q', text: item.q, onclick: function (e) {
          var body = e.currentTarget.nextElementSibling;
          var open = body.style.maxHeight;
          document.querySelectorAll('.lm-faq-a').forEach(function (b) { b.style.maxHeight = ''; });
          if (!open) body.style.maxHeight = body.scrollHeight + 'px';
        } });
        var a = el('div', { class: 'lm-faq-a' }, [el('p', { text: item.a })]);
        faqWrap.appendChild(q);
        faqWrap.appendChild(a);
      });
      wrap.appendChild(faqWrap);
    }

    var footerCta = el('div', { class: 'lm-footer-strip' });
    var footerBtn = el('button', {
      class: 'lm-btn lm-btn-primary', text: h.primaryCta,
      'data-gtm-cta': slugify(h.primaryCta), 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'footer',
      onclick: function () { self._startQuiz(); }
    });
    footerCta.appendChild(footerBtn);
    footerCta.appendChild(el('p', { class: 'lm-legal', html: 'By continuing you agree to our <a href="/privacy">Privacy Policy</a>.' }));
    wrap.appendChild(footerCta);

    this.root.appendChild(wrap);
  };

  LeadMagnetEngine.prototype._isHealthcareTraffic = function () {
    var matchers = this.config.healthcareUtmMatchers || [];
    if (!matchers.length) return false;
    var utm = this.state.utm;
    var haystack = ((utm.utm_campaign || '') + ' ' + (utm.utm_content || '') + ' ' + (utm.utm_source || '')).toLowerCase();
    return matchers.some(function (m) { return haystack.indexOf(m) !== -1; });
  };

  LeadMagnetEngine.prototype._buildHeroWidget = function () {
    var c = this.config;
    var box = el('div', { class: 'lm-hero-widget' });
    box.appendChild(el('div', { class: 'lm-hero-widget-header', text: c.copy.hero.dashboardWidgetHeader || 'Overview — Example' }));
    var body = el('div', { class: 'lm-hero-widget-body' });
    (c.copy.hero.dashboardWidget || []).forEach(function (row) {
      body.appendChild(el('div', { class: 'lm-hero-widget-row' }, [
        el('span', { class: 'lm-mono', text: row.label }),
        el('span', { class: 'lm-hero-widget-status', text: row.status })
      ]));
    });
    box.appendChild(body);
    return box;
  };

  // ── Intro screen (between Hero and the first question) ─────────────────
  LeadMagnetEngine.prototype._startQuiz = function () {
    this.state.screen = 'intro';
    this._render();
  };

  LeadMagnetEngine.prototype._renderIntro = function () {
    var self = this, intro = this.config.copy.intro;
    var wrap = el('div', { class: 'lm-intro' });
    wrap.appendChild(el('h1', { class: 'lm-h1', text: intro.headline }));
    wrap.appendChild(el('p', { class: 'lm-sub', text: intro.subhead }));
    wrap.appendChild(el('button', {
      class: 'lm-btn lm-btn-primary', text: intro.cta,
      'data-gtm-cta': slugify(intro.cta), 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'intro',
      onclick: function () { self._beginQuestions(); }
    }));
    this.root.appendChild(wrap);
  };

  LeadMagnetEngine.prototype._beginQuestions = function () {
    this.state.screen = 'quiz';
    this.state.qIndex = 0;
    this.state.pendingInsight = null;
    this.pushEvent('start');
    this._render();
  };

  // Flat, ordered list of every question across every screen — the quiz now
  // shows exactly one question per view (Typeform-style), so screens are
  // only used as metadata (category label, insight-interrupt triggers).
  LeadMagnetEngine.prototype._findScreenForQuestion = function (q) {
    var screens = this.config.screens;
    for (var i = 0; i < screens.length; i++) {
      if (screens[i].questions.indexOf(q) !== -1) return screens[i];
    }
    return null;
  };

  LeadMagnetEngine.prototype._bindKeyboard = function () {
    var self = this;
    document.addEventListener('keydown', function (e) {
      if (self.state.screen !== 'quiz') return;
      if (e.target && /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) return;

      if (self.state.pendingInsight) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); self._dismissInsight(); }
        else if (e.key === 'Backspace') { e.preventDefault(); self.state.pendingInsight = null; self._render(); }
        return;
      }

      var flat = allQuestions(self.config);
      var q = flat[self.state.qIndex];
      if (!q) return;

      if (e.key === 'Backspace') {
        e.preventDefault();
        self._goBack();
        return;
      }
      if (e.key === 'Enter' && q.type === 'multiselect') {
        e.preventDefault();
        self._afterQuestionAnswered(q);
        return;
      }
      var num = parseInt(e.key, 10);
      if (!isNaN(num) && num >= 1 && num <= q.options.length) {
        e.preventDefault();
        if (q.type === 'multiselect') self._toggleMultiselect(q, num - 1);
        else self._answerQuestion(q, num - 1);
      }
    });
  };

  // Re-rendering the quiz screen (e.g. to show a selected option, or to
  // toggle a multiselect checkbox) must NOT replay the entrance animation —
  // only an actual navigation (a new question, going back, or an insight
  // interrupt) should slide in. Tracked via a render-key comparison.
  LeadMagnetEngine.prototype._quizAnimClass = function (key) {
    var isNew = key !== this._lastQuizRenderKey;
    this._lastQuizRenderKey = key;
    return isNew ? ' lm-quiz-anim' : '';
  };

  LeadMagnetEngine.prototype._renderQuiz = function () {
    if (this.state.pendingInsight) { this._renderInsightScreen(); return; }

    var self = this, c = this.config;
    var flat = allQuestions(c);
    var q = flat[this.state.qIndex];
    var screen = this._findScreenForQuestion(q);
    var total = flat.length;

    var wrap = el('div', { class: 'lm-quiz' + this._quizAnimClass('q' + this.state.qIndex) });

    var topbar = el('div', { class: 'lm-quiz-topbar' });
    topbar.appendChild(el('button', {
      class: 'lm-quiz-back' + (this.state.qIndex === 0 ? ' lm-quiz-back-hidden' : ''),
      html: '&larr;', 'aria-label': 'Previous question',
      onclick: function () { self._goBack(); }
    }));
    var track = el('div', { class: 'lm-quiz-progress-track' });
    track.appendChild(el('div', { class: 'lm-quiz-progress-fill', style: 'width:' + Math.round((this.state.qIndex / total) * 100) + '%' }));
    topbar.appendChild(track);
    topbar.appendChild(el('span', { class: 'lm-quiz-count', text: (this.state.qIndex + 1) + ' / ' + total }));
    wrap.appendChild(topbar);

    var body = el('div', { class: 'lm-quiz-body' });
    if (screen) body.appendChild(el('div', { class: 'lm-quiz-eyebrow', text: screen.chipLabel || screen.theme || '' }));
    body.appendChild(this._buildQuestionBlock(q));

    if (q.type === 'multiselect') {
      var continueBtn = el('button', {
        class: 'lm-btn lm-btn-primary lm-continue-btn', text: 'Continue',
        'data-gtm-cta': 'continue', 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'quiz',
        onclick: function () { self._afterQuestionAnswered(q); }
      });
      body.appendChild(continueBtn);
      body.appendChild(el('p', { class: 'lm-quiz-hint', text: 'Select any that apply, then press Enter or click Continue.' }));
    } else {
      body.appendChild(el('p', { class: 'lm-quiz-hint', text: 'Click an answer, or press 1–9 on your keyboard.' }));
    }

    wrap.appendChild(body);
    this.root.appendChild(wrap);
  };

  LeadMagnetEngine.prototype._buildQuestionBlock = function (q) {
    var self = this;
    var block = el('div', { class: 'lm-question' });
    block.appendChild(el('p', { class: 'lm-question-text', text: q.text }));
    var opts = el('div', { class: 'lm-options' });
    q.options.forEach(function (optText, idx) {
      if (q.type === 'multiselect') {
        var selected = self.state.answers[q.id] && self.state.answers[q.id].indices.indexOf(idx) !== -1;
        var btn = el('button', {
          class: 'lm-option lm-option-multi' + (selected ? ' lm-option-selected' : ''),
          onclick: function () { self._toggleMultiselect(q, idx); }
        }, [
          el('span', { class: 'lm-opt-num', text: String(idx + 1) }),
          el('span', { class: 'lm-opt-text', text: optText }),
          el('span', { class: 'lm-opt-check', html: selected ? '&check;' : '' })
        ]);
        opts.appendChild(btn);
      } else {
        var isSelected = self.state.answers[q.id] && self.state.answers[q.id].index === idx;
        opts.appendChild(el('button', {
          class: 'lm-option' + (isSelected ? ' lm-option-selected' : ''),
          onclick: function () { self._answerQuestion(q, idx); }
        }, [
          el('span', { class: 'lm-opt-num', text: String(idx + 1) }),
          el('span', { class: 'lm-opt-text', text: optText })
        ]));
      }
    });
    block.appendChild(opts);
    return block;
  };

  LeadMagnetEngine.prototype._answerQuestion = function (q, idx) {
    this.state.answers[q.id] = { index: idx };
    this.pushEvent('questionAnswered', { question_id: q.id, dimension: q.dimId });
    this._render(); // show the selected state immediately, then advance
    var self = this;
    setTimeout(function () { self._afterQuestionAnswered(q); }, 280);
  };

  LeadMagnetEngine.prototype._toggleMultiselect = function (q, idx) {
    var ans = this.state.answers[q.id] || { indices: [] };
    var pos = ans.indices.indexOf(idx);
    if (pos === -1) ans.indices.push(idx); else ans.indices.splice(pos, 1);
    this.state.answers[q.id] = ans;
    this._render();
  };

  // Called once a question has a final answer — checks for an insight
  // interrupt tied to this question before moving to the next one.
  LeadMagnetEngine.prototype._afterQuestionAnswered = function (q) {
    var screen = this._findScreenForQuestion(q);
    var insight = screen && screen.insightAfter;
    if (insight && insight.afterQuestionId === q.id && !this.state.insightsShown[screen.id]) {
      this.state.insightsShown[screen.id] = true;
      this.state.pendingInsight = insight;
      this._render();
      return;
    }
    this._advanceQuestion();
  };

  LeadMagnetEngine.prototype._advanceQuestion = function () {
    var total = allQuestions(this.config).length;
    if (this.state.qIndex < total - 1) {
      this.state.qIndex++;
      this._render();
    } else {
      this._goToTeaser();
    }
  };

  LeadMagnetEngine.prototype._goBack = function () {
    if (this.state.pendingInsight) { this.state.pendingInsight = null; this._render(); return; }
    if (this.state.qIndex > 0) { this.state.qIndex--; this._render(); }
  };

  LeadMagnetEngine.prototype._dismissInsight = function () {
    this.state.pendingInsight = null;
    this._advanceQuestion();
  };

  LeadMagnetEngine.prototype._renderInsightScreen = function () {
    var self = this;
    var wrap = el('div', { class: 'lm-quiz' + this._quizAnimClass('insight' + this.state.qIndex) });
    var body = el('div', { class: 'lm-quiz-body lm-insight-screen' });
    body.appendChild(el('div', { class: 'lm-insight-badge', text: 'Quick insight' }));
    body.appendChild(el('p', { class: 'lm-insight-copy', text: this.state.pendingInsight.copy }));
    body.appendChild(el('button', {
      class: 'lm-btn lm-btn-primary', text: 'Continue',
      'data-gtm-cta': 'insight-continue', 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'quiz',
      onclick: function () { self._dismissInsight(); }
    }));
    wrap.appendChild(body);
    this.root.appendChild(wrap);
  };

  // ── Teaser (email gate) ─────────────────────────────────────────────────
  LeadMagnetEngine.prototype._goToTeaser = function () {
    this.state.score = computeScore(this.config, this.state.answers);
    this.state.screen = 'teaser';
    this.pushEvent('teaserView', { tier: this.state.score.tier ? this.state.score.tier.label : null });
    this._render();
  };

  LeadMagnetEngine.prototype._renderTeaser = function () {
    var self = this, c = this.config, score = this.state.score;
    var wrap = el('div', { class: 'lm-teaser' });

    wrap.appendChild(el('h2', { class: 'lm-h2', text: 'Your ' + c.indexLabel + ': ' + (score.tier ? score.tier.label : '') }));
    wrap.appendChild(el('div', { class: 'lm-score-blur', text: score.overall + '/100' }));
    wrap.appendChild(this._buildChart(score, true));

    var weakest = weakestDim(score);
    if (weakest && c.weakLineTemplates && c.weakLineTemplates[weakest]) {
      wrap.appendChild(el('p', { class: 'lm-weak-line', text: c.weakLineTemplates[weakest] }));
    }
    wrap.appendChild(el('p', { class: 'lm-peer-line', text: 'Enterprise buyers are already asking vendors for a score like this one. See yours before they ask you.' }));

    var gate = el('div', { class: 'lm-email-gate' });
    gate.appendChild(el('p', { class: 'lm-gate-copy', text: 'Enter your work email to unlock your full ' + c.indexLabel + ', breakdown, peer comparison, and PDF report.' }));
    var form = el('form', { class: 'lm-gate-form' });
    var fName = el('input', { type: 'text', placeholder: 'First name', required: 'required', class: 'lm-input' });
    var fEmail = el('input', { type: 'email', placeholder: 'Work email', required: 'required', class: 'lm-input' });
    var fCompany = el('input', { type: 'text', placeholder: 'Company', required: 'required', class: 'lm-input' });
    form.appendChild(fName);
    form.appendChild(fEmail);
    form.appendChild(fCompany);
    var submitBtn = el('button', {
      type: 'submit', class: 'lm-btn lm-btn-primary', text: 'Unlock My ' + c.indexLabel,
      'data-gtm-cta': 'unlock-my-index', 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'teaser'
    });
    form.appendChild(submitBtn);
    form.appendChild(el('p', { class: 'lm-legal', text: "We'll use this to generate your report. We won't share it, and you can unsubscribe from any follow-up at any time." }));
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      self._submitContact({ firstName: fName.value.trim(), email: fEmail.value.trim(), company: fCompany.value.trim() });
    });
    gate.appendChild(form);
    wrap.appendChild(gate);

    this.root.appendChild(wrap);
  };

  LeadMagnetEngine.prototype._submitContact = function (contact) {
    var self = this, c = this.config;
    this.state.contact = contact;
    this.pushEvent('emailCaptured', { email_domain: (contact.email.split('@')[1] || '') });

    // "Assessment complete" — the primary conversion: every question
    // answered AND contact info handed over. Distinct from emailCaptured
    // above so it reads unambiguously as THE conversion event in GA4/Ads
    // reporting, not just a generic form-fill analytics event.
    this.pushEvent('assessmentComplete', { tier: this.state.score.tier ? this.state.score.tier.label : null });
    if (c.googleAdsConversionLabel && typeof window.gtag === 'function') {
      window.gtag('event', 'conversion', {
        send_to: c.googleAdsConversionLabel,
        value: c.googleAdsConversionValue,
        currency: c.googleAdsConversionCurrency
      });
    }

    var body = {
      niche: c.niche,
      answers: this._serializeAnswers(),
      contact: contact,
      utm: this.state.utm,
      consent: true
    };

    if (!c.api || !c.api.submit) {
      // Phase A stub — no backend wired yet
      console.warn('[lead-magnet] Phase A stub — no backend wired, using client-only score');
      this._onSubmitResult({
        ok: true, tier: this.state.score.tier ? this.state.score.tier.label : null,
        overallScore: this.state.score.overall,
        peer: { sufficientData: false },
        routing: { crossRouted: false, lighterTrack: checkSoftSignals(c, this.state.answers, this.state.score).lighterTrack }
      });
      return;
    }

    fetch(c.api.submit, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body)
    }).then(function (r) { return r.json(); }).then(function (data) {
      self._onSubmitResult(data);
    }).catch(function () {
      self._onSubmitResult({
        ok: false, tier: self.state.score.tier ? self.state.score.tier.label : null,
        overallScore: self.state.score.overall, peer: { sufficientData: false }, routing: {}
      });
    });
  };

  LeadMagnetEngine.prototype._serializeAnswers = function () {
    var out = [];
    var answers = this.state.answers;
    Object.keys(answers).forEach(function (qid) {
      var a = answers[qid];
      out.push({ questionId: qid, index: a.index, indices: a.indices });
    });
    return out;
  };

  LeadMagnetEngine.prototype._onSubmitResult = function (apiResult) {
    this.state.apiResult = apiResult;
    this.state.screen = 'full';
    this.pushEvent('resultView', { tier: apiResult.tier });
    this._sendTeamNotification(apiResult);
    this._render();
  };

  // Fires the team-notification email client-side (browser fetch — same
  // pattern as contact.html/chat-widget.js). api/lead-magnet-submit.js
  // deliberately does NOT send this itself: Cloudflare (fronting
  // FormSubmit.co) returns a 403 bot-detection challenge to Vercel's
  // serverless outbound IPs regardless of headers, so the request has to
  // come from a real browser. Uses apiResult's server-verified
  // tier/overallScore/dims/weakestDim, not the client-computed score.
  LeadMagnetEngine.prototype._sendTeamNotification = function (apiResult) {
    var c = this.config, contact = this.state.contact || {};
    if (!apiResult || apiResult.ok === false) return;
    var dims = apiResult.dims || {};
    var dimLines = Object.keys(dims).map(function (id) { return id + ': ' + dims[id]; }).join(', ');

    fetch('https://formsubmit.co/gaurav@upcoretechnologies.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        _subject: 'New Lead-Magnet Submission — ' + (contact.firstName || contact.email) + ' · ' + c.indexLabel,
        _template: 'table',
        _captcha: 'false',
        _cc: 'saswata@upcoretechnologies.com',
        'Index': c.indexLabel,
        'Tier': apiResult.tier + ' (' + apiResult.overallScore + '/100)',
        'Weakest Dimension': apiResult.weakestDim || '',
        'Dimension Breakdown': dimLines,
        'Lighter-Track Signal': apiResult.routing && apiResult.routing.lighterTrack ? 'Yes' : 'No',
        'Name': contact.firstName || 'Not provided',
        'Email': contact.email || '',
        'Company': contact.company || 'Not provided',
        'UTM Source': this.state.utm.utm_source || 'Not set',
        'UTM Campaign': this.state.utm.utm_campaign || 'Not set',
        'Submitted At': new Date().toISOString()
      })
    }).catch(function (err) { console.error('[lead-magnet] Team notification failed:', err); });
  };

  // Booking link with the visitor's tier/score appended once known, so the
  // booking page can show a personalized "we'll pick up from there" line
  // instead of a cold, context-free form. Only used post-quiz (the hero's
  // pre-quiz "skip to booking" link has no score yet, so stays plain).
  LeadMagnetEngine.prototype._bookingUrl = function () {
    var base = this.config.bookingHref || '/assessment';
    var score = this.state.score;
    if (!score) return base;
    var params = new URLSearchParams();
    if (score.tier) params.set('tier', score.tier.label);
    params.set('score', String(score.overall));
    return base + '?' + params.toString();
  };

  // ── Full result ──────────────────────────────────────────────────────────
  LeadMagnetEngine.prototype._renderFull = function () {
    var self = this, c = this.config, score = this.state.score, api = this.state.apiResult;
    var wrap = el('div', { class: 'lm-full-result' });

    wrap.appendChild(el('h2', { class: 'lm-h2', text: 'Your ' + c.indexLabel + ': ' + score.overall + '/100 — ' + (score.tier ? score.tier.label : '') }));
    if (score.tier && score.tier.description) wrap.appendChild(el('p', { class: 'lm-body', text: score.tier.description }));

    wrap.appendChild(this._buildChart(score, false));

    var peer = el('p', { class: 'lm-peer-line' });
    if (api.peer && api.peer.sufficientData) {
      peer.textContent = 'Teams assessed so far average ' + api.peer.avgOverall + '/100 — you scored ' + (score.overall >= api.peer.avgOverall ? 'above' : 'below') + ' that.';
    } else {
      peer.textContent = 'Not enough peer responses yet to show a reliable comparison — check back soon.';
    }
    wrap.appendChild(peer);

    var weakest = weakestDim(score);
    if (weakest && c.weakLineTemplates && c.weakLineTemplates[weakest]) {
      wrap.appendChild(el('div', { class: 'lm-weak-callout' }, [el('p', { text: c.weakLineTemplates[weakest] })]));
    }

    var ctaRow = el('div', { class: 'lm-cta-row' });
    var bookBtn = el('a', {
      class: 'lm-btn lm-btn-primary', text: c.copy.fullResult.primaryCta, href: this._bookingUrl(),
      'data-gtm-cta': slugify(c.copy.fullResult.primaryCta), 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'full_result',
      onclick: function () { self.pushEvent('callBooked'); }
    });
    var pdfBtn = el('button', {
      class: 'lm-btn lm-btn-ghost', text: 'Download PDF Report',
      'data-gtm-cta': 'download-pdf-report', 'data-gtm-cta-type': 'secondary', 'data-gtm-cta-section': 'full_result',
      onclick: function () { self._downloadPdf(); }
    });
    ctaRow.appendChild(bookBtn);
    ctaRow.appendChild(pdfBtn);
    wrap.appendChild(ctaRow);

    wrap.appendChild(el('p', { class: 'lm-legal', html: 'Your data is used only to generate this report and isn\'t shared. See our <a href="/privacy">Privacy Policy</a>.' }));

    this.root.appendChild(wrap);
  };

  LeadMagnetEngine.prototype._downloadPdf = function () {
    var self = this;
    if (typeof window.jspdf === 'undefined') { console.error('[lead-magnet] jsPDF not loaded'); return; }
    var blob = this._generatePdf();
    blob.save((this.config.niche + '-report.pdf'));
    this.pushEvent('pdfSent');
  };

  // ── PDF branding helpers ────────────────────────────────────────────────
  var PDF_TEAL = [10, 191, 204];
  var PDF_TEAL_DARK = [8, 154, 170];
  var PDF_INK = [10, 10, 10];
  var PDF_GREY = [110, 118, 128];
  var PDF_TRACK = [232, 235, 239];
  var PDF_CARD = [247, 248, 250];

  function pdfHeaderBand(doc, pageW, eyebrow, headline) {
    doc.setFillColor.apply(doc, PDF_TEAL);
    doc.rect(0, 0, pageW, 120, 'F');
    doc.setTextColor(7, 11, 16);
    doc.setFont('helvetica', 'bold'); doc.setFontSize(10);
    doc.text(eyebrow.toUpperCase(), 48, 44, { charSpace: 0.6 });
    doc.setFontSize(22);
    doc.text(headline, 48, 76);
    doc.setTextColor.apply(doc, PDF_INK);
  }

  function pdfFooter(doc, pageW, pageH, pageNum, totalPages) {
    doc.setDrawColor.apply(doc, PDF_TEAL);
    doc.setLineWidth(1);
    doc.line(48, pageH - 46, pageW - 48, pageH - 46);
    doc.setFont('helvetica', 'normal'); doc.setFontSize(9);
    doc.setTextColor.apply(doc, PDF_GREY);
    doc.text('Upcore Technologies  ·  upcoretech.com', 48, pageH - 30);
    doc.text('Page ' + pageNum + ' of ' + totalPages, pageW - 48, pageH - 30, { align: 'right' });
    doc.setTextColor.apply(doc, PDF_INK);
  }

  function pdfTierColor(tier) {
    // Rough good/ok/risk read on the tier position — purely visual, not scored.
    if (!tier) return PDF_TEAL;
    if (tier.lighterCTA) return [22, 163, 74];      // top tier — green
    if (tier.min >= 51) return PDF_TEAL;             // mid-high — brand teal
    if (tier.min >= 26) return [217, 119, 6];         // mid-low — amber
    return [220, 38, 38];                             // bottom tier — red
  }

  LeadMagnetEngine.prototype._generatePdf = function () {
    var c = this.config, score = this.state.score, contact = this.state.contact || {};
    var api = this.state.apiResult || {};
    var peer = api.peer || {};
    var jsPDF = window.jspdf.jsPDF;
    var doc = new jsPDF({ unit: 'pt', format: 'a4' });
    var pageW = doc.internal.pageSize.getWidth();
    var pageH = doc.internal.pageSize.getHeight();
    var margin = 48, contentW = pageW - margin * 2;
    var tierColor = pdfTierColor(score.tier);

    doc.setFont('helvetica', 'normal');

    // ── PAGE 1 — Cover ──────────────────────────────────────────────────
    pdfHeaderBand(doc, pageW, 'Upcore Technologies', c.indexLabel + ' Report');

    var y = 168;
    doc.setFont('helvetica', 'normal'); doc.setFontSize(10);
    doc.setTextColor.apply(doc, PDF_GREY);
    var metaLine = (contact.company ? contact.company + '  ·  ' : '') + new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    doc.text(metaLine, margin, y);
    doc.setTextColor.apply(doc, PDF_INK);
    y += 40;

    // Score card
    doc.setFillColor.apply(doc, PDF_CARD);
    doc.roundedRect(margin, y, contentW, 150, 10, 10, 'F');

    doc.setFont('helvetica', 'bold'); doc.setFontSize(46);
    doc.setTextColor.apply(doc, tierColor);
    var scoreStr = String(score.overall);
    doc.text(scoreStr, margin + 30, y + 78);
    var scoreW = doc.getTextWidth(scoreStr);
    doc.setFontSize(16);
    doc.text('/100', margin + 30 + scoreW + 4, y + 78);

    doc.setFillColor.apply(doc, tierColor);
    var tierLabel = score.tier ? score.tier.label : '';
    doc.roundedRect(margin + 30, y + 96, doc.getTextWidth(tierLabel) + 28, 26, 13, 13, 'F');
    doc.setFont('helvetica', 'bold'); doc.setFontSize(11);
    doc.setTextColor(255, 255, 255);
    doc.text(tierLabel, margin + 44, y + 113);
    doc.setTextColor.apply(doc, PDF_INK);

    if (score.tier && score.tier.description) {
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
      doc.setTextColor.apply(doc, PDF_GREY);
      var descLines = doc.splitTextToSize(score.tier.description, 190);
      doc.text(descLines, margin + contentW - 220, y + 40);
      doc.setTextColor.apply(doc, PDF_INK);
    }

    y += 150 + 36;
    doc.setFont('helvetica', 'bold'); doc.setFontSize(13);
    doc.text('What this score means', margin, y);
    y += 22;
    doc.setFont('helvetica', 'normal'); doc.setFontSize(11);
    var introBody = 'This report scores your organization across the ' + score.dimOrder.length + ' dimensions Upcore’s Fractional AI Officer framework governs against. The next page breaks down exactly where you’re strong and where the gaps are — the same lens we use in paying engagements.';
    var introLines = doc.splitTextToSize(introBody, contentW);
    doc.text(introLines, margin, y);
    y += introLines.length * 15 + 30;

    if (peer.sufficientData) {
      doc.setFillColor.apply(doc, PDF_CARD);
      doc.roundedRect(margin, y, contentW, 44, 8, 8, 'F');
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
      doc.text('Teams assessed so far average ' + peer.avgOverall + '/100 — you scored ' + (score.overall >= peer.avgOverall ? 'above' : 'below') + ' that.', margin + 16, y + 27);
    }

    pdfFooter(doc, pageW, pageH, 1, 3);

    // ── PAGE 2 — Dimension breakdown ────────────────────────────────────
    doc.addPage();
    pdfHeaderBand(doc, pageW, c.indexLabel, 'Your Breakdown');
    y = 168;

    doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
    doc.setTextColor.apply(doc, PDF_GREY);
    doc.text('Score out of 100 for each dimension.' + (peer.sufficientData ? ' The teal marker shows the peer average.' : ''), margin, y);
    doc.setTextColor.apply(doc, PDF_INK);
    y += 30;

    var barW = contentW - 70;
    score.dimOrder.forEach(function (id) {
      var d = score.dims[id];
      doc.setFont('helvetica', 'bold'); doc.setFontSize(11.5);
      doc.text(d.label, margin, y);
      doc.setFont('helvetica', 'bold'); doc.setFontSize(11.5);
      doc.setTextColor.apply(doc, tierColor);
      doc.text(String(d.pct), margin + contentW - 26, y, { align: 'right' });
      doc.setTextColor.apply(doc, PDF_INK);
      y += 8;

      doc.setFillColor.apply(doc, PDF_TRACK);
      doc.roundedRect(margin, y, barW, 9, 4.5, 4.5, 'F');
      if (d.pct > 0) {
        doc.setFillColor.apply(doc, PDF_TEAL);
        doc.roundedRect(margin, y, Math.max(barW * (d.pct / 100), 9), 9, 4.5, 4.5, 'F');
      }
      if (peer.sufficientData && peer.avgByDim && typeof peer.avgByDim[id] === 'number') {
        var markerX = margin + barW * (peer.avgByDim[id] / 100);
        doc.setDrawColor.apply(doc, PDF_TEAL_DARK);
        doc.setLineWidth(1.5);
        doc.line(markerX, y - 3, markerX, y + 12);
      }
      y += 30;
    });

    y += 10;
    if (score.weakestDim && c.weakLineTemplates && c.weakLineTemplates[score.weakestDim]) {
      doc.setFillColor.apply(doc, PDF_CARD);
      var weakLines = doc.splitTextToSize(c.weakLineTemplates[score.weakestDim], contentW - 40);
      var boxH = weakLines.length * 15 + 30;
      doc.roundedRect(margin, y, contentW, boxH, 8, 8, 'F');
      doc.setFillColor.apply(doc, PDF_TEAL);
      doc.rect(margin, y, 4, boxH, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(10);
      doc.text('WEAKEST AREA: ' + (score.dims[score.weakestDim] ? score.dims[score.weakestDim].label.toUpperCase() : ''), margin + 20, y + 20);
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
      doc.text(weakLines, margin + 20, y + 38);
    }

    pdfFooter(doc, pageW, pageH, 2, 3);

    // ── PAGE 3 — Next step ───────────────────────────────────────────────
    doc.addPage();
    pdfHeaderBand(doc, pageW, c.indexLabel, 'Your Next Step');
    y = 168;

    doc.setFont('helvetica', 'normal'); doc.setFontSize(11.5);
    var nextLines = doc.splitTextToSize(c.copy.fullResult.pdfNextStep || '', contentW);
    doc.text(nextLines, margin, y);
    y += nextLines.length * 16 + 34;

    doc.setFillColor.apply(doc, PDF_INK);
    doc.roundedRect(margin, y, contentW, 96, 10, 10, 'F');
    doc.setFont('helvetica', 'bold'); doc.setFontSize(14);
    doc.setTextColor(255, 255, 255);
    doc.text(c.copy.fullResult.primaryCta || 'Book a 45-minute review', margin + 24, y + 38);
    doc.setFont('helvetica', 'normal'); doc.setFontSize(11);
    doc.setTextColor.apply(doc, PDF_TEAL);
    doc.text('upcoretech.com' + (c.bookingHref || '/assessment'), margin + 24, y + 62);
    doc.setFont('helvetica', 'normal'); doc.setFontSize(9.5);
    doc.setTextColor(200, 205, 210);
    doc.text('No commitment required — we’ll walk through this exact report on the call.', margin + 24, y + 80);
    doc.setTextColor.apply(doc, PDF_INK);

    pdfFooter(doc, pageW, pageH, 3, 3);

    return doc;
  };

  // ── Charts (hand-rolled inline SVG, no external library) ────────────────
  LeadMagnetEngine.prototype._buildChart = function (score, blurred) {
    var c = this.config;
    if (c.chart.type === 'maturityCurve') return this._buildMaturityCurve(score, blurred);
    return this._buildRadar(score, blurred);
  };

  LeadMagnetEngine.prototype._buildRadar = function (score, blurred) {
    var axisLabels = this.config.chart.axisLabels;
    var n = axisLabels.length;
    var size = 280, cx = size / 2, cy = size / 2, r = size / 2 - 40;
    var svgNs = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(svgNs, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + size + ' ' + size);
    svg.setAttribute('class', 'lm-radar-svg' + (blurred ? ' lm-blurred' : ''));
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Score radar chart');

    // grid rings
    [0.25, 0.5, 0.75, 1].forEach(function (frac) {
      var pts = [];
      for (var i = 0; i < n; i++) {
        var ang = (Math.PI * 2 * i) / n - Math.PI / 2;
        pts.push((cx + Math.cos(ang) * r * frac) + ',' + (cy + Math.sin(ang) * r * frac));
      }
      var ring = document.createElementNS(svgNs, 'polygon');
      ring.setAttribute('points', pts.join(' '));
      ring.setAttribute('class', 'lm-radar-grid');
      svg.appendChild(ring);
    });

    // data polygon
    var dimOrder = score ? score.dimOrder : [];
    var dataPts = [];
    for (var i = 0; i < n; i++) {
      var ang2 = (Math.PI * 2 * i) / n - Math.PI / 2;
      var pct = score && dimOrder[i] ? score.dims[dimOrder[i]].pct : 0;
      var rr = r * (pct / 100);
      dataPts.push((cx + Math.cos(ang2) * rr) + ',' + (cy + Math.sin(ang2) * rr));
      var lx = cx + Math.cos(ang2) * (r + 18), ly = cy + Math.sin(ang2) * (r + 18);
      var label = document.createElementNS(svgNs, 'text');
      label.setAttribute('x', lx); label.setAttribute('y', ly);
      label.setAttribute('class', 'lm-radar-label');
      label.setAttribute('text-anchor', 'middle');
      label.textContent = axisLabels[i];
      svg.appendChild(label);
    }
    var poly = document.createElementNS(svgNs, 'polygon');
    poly.setAttribute('points', dataPts.join(' '));
    poly.setAttribute('class', 'lm-radar-data');
    svg.appendChild(poly);

    return svg;
  };

  LeadMagnetEngine.prototype._buildMaturityCurve = function (score, blurred) {
    var stages = this.config.chart.stages || ['Fragmented', 'Emerging', 'Aligning', 'Orchestrated'];
    var w = 560, h = 140, pad = 40;
    var svgNs = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(svgNs, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    svg.setAttribute('class', 'lm-maturity-curve-svg' + (blurred ? ' lm-blurred' : ''));
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Maturity stage progression');

    var line = document.createElementNS(svgNs, 'line');
    line.setAttribute('x1', pad); line.setAttribute('y1', h / 2);
    line.setAttribute('x2', w - pad); line.setAttribute('y2', h / 2);
    line.setAttribute('class', 'lm-curve-line');
    svg.appendChild(line);

    var step = (w - pad * 2) / (stages.length - 1);
    stages.forEach(function (label, i) {
      var x = pad + step * i;
      var dot = document.createElementNS(svgNs, 'circle');
      dot.setAttribute('cx', x); dot.setAttribute('cy', h / 2); dot.setAttribute('r', 6);
      dot.setAttribute('class', 'lm-curve-dot');
      svg.appendChild(dot);
      var t = document.createElementNS(svgNs, 'text');
      t.setAttribute('x', x); t.setAttribute('y', h / 2 + 28);
      t.setAttribute('text-anchor', 'middle'); t.setAttribute('class', 'lm-curve-label');
      t.textContent = label;
      svg.appendChild(t);
    });

    if (score) {
      var idx = Math.min(3, Math.floor(score.overall / 25));
      var mx = pad + step * idx;
      var marker = document.createElementNS(svgNs, 'text');
      marker.setAttribute('x', mx); marker.setAttribute('y', h / 2 - 18);
      marker.setAttribute('text-anchor', 'middle'); marker.setAttribute('class', 'lm-curve-marker');
      marker.textContent = 'You are here';
      svg.appendChild(marker);
      var markerDot = document.createElementNS(svgNs, 'circle');
      markerDot.setAttribute('cx', mx); markerDot.setAttribute('cy', h / 2); markerDot.setAttribute('r', 9);
      markerDot.setAttribute('class', 'lm-curve-dot lm-curve-dot-active');
      svg.appendChild(markerDot);
    }

    return svg;
  };

  // ── Sticky CTA ───────────────────────────────────────────────────────────
  LeadMagnetEngine.prototype._buildStickyCTA = function () {
    var self = this;
    var bar = el('div', { class: 'lm-sticky-cta' });
    var btn = el('button', {
      class: 'lm-btn lm-btn-primary', text: this.config.copy.hero.primaryCta,
      'data-gtm-cta': 'sticky-cta', 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'sticky',
      onclick: function () { if (self.state.screen === 'hero') self._startQuiz(); }
    });
    bar.appendChild(btn);
    document.body.appendChild(bar);
    this._stickyBar = bar;
    window.addEventListener('scroll', function () { self._updateStickyCTA(); }, { passive: true });
  };

  LeadMagnetEngine.prototype._updateStickyCTA = function () {
    if (!this._stickyBar) return;
    var show = this.state.screen === 'hero' && window.scrollY > 400;
    this._stickyBar.classList.toggle('lm-sticky-visible', show);
  };

  // ── Public init ──────────────────────────────────────────────────────────
  window.LeadMagnetEngine = {
    init: function (config) { return new LeadMagnetEngine(config); }
  };
})();
