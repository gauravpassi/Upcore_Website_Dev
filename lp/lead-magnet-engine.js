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
      if (q.type === 'multiselect') return; // segmentation only — never scored
      if (!dims[q.dimId]) { dims[q.dimId] = { raw: 0, maxRaw: 0, label: q.dimLabel }; order.push(q.dimId); }
      var ans = answers[q.id];
      var max = q.options.length - 1;
      var raw = ans && typeof ans.index === 'number' ? Math.min(ans.index, max) : 0;
      dims[q.dimId].raw += raw;
      dims[q.dimId].maxRaw += max;
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
    // Per-pageview token — dedupes the Ads conversion if the gate is ever
    // double-submitted, and ties dataLayer events to one session.
    this.sessionId = 'lm-' + Math.random().toString(36).slice(2, 10) + '-' + Math.random().toString(36).slice(2, 6);
    this._lastQuizRenderKey = null;
    this._submitting = false;
    this._advancing = false;
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
    var params = { niche: this.config.niche, lm_session: this.sessionId };
    var utm = this.state.utm || {};
    Object.keys(utm).forEach(function (k) { params[k] = utm[k]; });
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
    this._advancing = false;
    document.body.classList.toggle('lm-on-hero', this.state.screen === 'hero');
    if (this.state.screen === 'hero') this._renderHero();
    else if (this.state.screen === 'quiz') this._renderQuiz();
    else if (this.state.screen === 'teaser') this._renderTeaser();
    else if (this.state.screen === 'full') this._renderFull();
    this._updateStickyCTA();
    // Literal 'instant' — anything else falls back to the page's
    // scroll-behavior:smooth and animates on every question advance.
    window.scrollTo({ top: 0, behavior: 'instant' });
  };

  // ── HERO ─────────────────────────────────────────────────────────────────
  LeadMagnetEngine.prototype._renderHero = function () {
    var self = this, c = this.config, h = c.copy.hero;
    var wrap = el('div', { class: 'lm-hero' });

    // Company identity above the fold — opens in a new tab so a cold ad
    // click can vet who's asking for their data without losing the funnel.
    wrap.appendChild(el('a', {
      class: 'lm-wordmark', href: 'https://www.upcoretech.com', target: '_blank', rel: 'noopener',
      'aria-label': 'Upcore Technologies — company site'
    }, [
      el('span', { class: 'lm-wordmark-name', text: 'UPCORE' }),
      el('span', { class: 'lm-wordmark-domain', text: 'upcoretech.com' })
    ]));

    wrap.appendChild(el('div', { class: 'lm-eyebrow' }, [
      el('span', { class: 'lm-eyebrow-dot' }), el('span', { text: h.eyebrow })
    ]));
    wrap.appendChild(el('h1', { class: 'lm-h1', html: h.headline }));
    wrap.appendChild(el('p', { class: 'lm-sub', html: h.subhead }));

    var ctaRow = el('div', { class: 'lm-cta-row' });
    var primaryBtn = el('button', {
      class: 'lm-btn lm-btn-primary', text: h.primaryCta,
      'data-gtm-cta': slugify(h.primaryCta), 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'hero',
      onclick: function () { self._startQuiz('hero'); }
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

    // Proof directly under the CTA — credibility shouldn't hide below a
    // 300px decorative visual. Stats read as lines, certifications as chips.
    var proof = el('div', { class: 'lm-proof-bar' });
    (h.proofBar || []).forEach(function (item) {
      proof.appendChild(el('span', { class: 'lm-proof-item' }, [
        el('span', { class: 'lm-proof-icon', html: '&#10003;' }),
        el('span', { html: item })
      ]));
    });
    if (h.proofCerts && h.proofCerts.length) {
      var certs = el('div', { class: 'lm-proof-certs' });
      h.proofCerts.forEach(function (item) {
        certs.appendChild(el('span', { class: 'lm-proof-cert', text: item }));
      });
      proof.appendChild(certs);
    }
    wrap.appendChild(proof);

    if (h.frameworkPreview && h.frameworkPreview.length) {
      var fwCard = el('div', { class: 'lm-fw-preview-card lm-reveal' });
      if (h.heroVisualLabel) fwCard.appendChild(el('div', { class: 'lm-hero-visual-label', text: h.heroVisualLabel }));
      var fwPreview = this._buildFrameworkPreview();
      if (fwPreview) fwCard.appendChild(fwPreview);
      wrap.appendChild(fwCard);
    } else if (c.chart && c.chart.type === 'maturityCurve') {
      var curveCard = el('div', { class: 'lm-hero-visual-card lm-reveal' });
      if (h.heroVisualLabel) curveCard.appendChild(el('div', { class: 'lm-hero-visual-label', text: h.heroVisualLabel }));
      curveCard.appendChild(this._buildMaturityCurve(null));
      wrap.appendChild(curveCard);
    }

    var sampleReport = this._buildSampleReportPreview();
    if (sampleReport) {
      sampleReport.classList.add('lm-reveal');
      wrap.appendChild(sampleReport);
    }

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
      var hiw = el('div', { class: 'lm-how lm-reveal' });
      hiw.appendChild(el('h2', { class: 'lm-h2', text: 'How it works' }));
      var steps = el('div', { class: 'lm-how-steps' });
      h.howItWorks.forEach(function (step, i) {
        steps.appendChild(el('div', { class: 'lm-how-step' }, [
          el('div', { class: 'lm-how-num', text: String(i + 1) }),
          el('p', { text: step })
        ]));
      });
      hiw.appendChild(steps);
      var sampleQ = this._buildSampleQuestionTeaser();
      if (sampleQ) { sampleQ.classList.add('lm-reveal'); hiw.appendChild(sampleQ); }
      wrap.appendChild(hiw);
    }

    if (h.faq && h.faq.length) {
      var faqWrap = el('div', { class: 'lm-faq' });
      faqWrap.appendChild(el('h2', { class: 'lm-h2', text: 'Frequently asked' }));
      h.faq.forEach(function (item, fi) {
        var aId = 'lm-faq-a-' + fi;
        var q = el('button', {
          class: 'lm-faq-q', 'aria-expanded': 'false', 'aria-controls': aId,
          onclick: function (e) {
            var btn = e.currentTarget;
            var body = btn.nextElementSibling;
            var wasOpen = btn.getAttribute('aria-expanded') === 'true';
            faqWrap.querySelectorAll('.lm-faq-a').forEach(function (b) { b.style.maxHeight = ''; b.style.visibility = 'hidden'; });
            faqWrap.querySelectorAll('.lm-faq-q').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
            if (!wasOpen) {
              body.style.maxHeight = body.scrollHeight + 'px';
              body.style.visibility = 'visible';
              btn.setAttribute('aria-expanded', 'true');
            }
          }
        }, [
          el('span', { class: 'lm-faq-q-text', text: item.q }),
          el('span', { class: 'lm-faq-chevron', 'aria-hidden': 'true', html: '&#9662;' })
        ]);
        var a = el('div', { class: 'lm-faq-a', id: aId, style: 'visibility:hidden;' }, [el('p', { text: item.a })]);
        faqWrap.appendChild(q);
        faqWrap.appendChild(a);
      });
      wrap.appendChild(faqWrap);
    }

    var footerCta = el('div', { class: 'lm-footer-strip' });
    if (h.footerCtaHeadline) footerCta.appendChild(el('h2', { class: 'lm-h2', text: h.footerCtaHeadline }));
    var footerBtn = el('button', {
      class: 'lm-btn lm-btn-primary', text: h.primaryCta,
      'data-gtm-cta': slugify(h.primaryCta), 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'footer',
      onclick: function () { self._startQuiz('footer'); }
    });
    footerCta.appendChild(footerBtn);
    if (h.guaranteeLine) footerCta.appendChild(el('p', { class: 'lm-guarantee-line lm-footer-guarantee', text: h.guaranteeLine }));
    footerCta.appendChild(el('p', { class: 'lm-legal', html: 'By continuing you agree to our <a href="/privacy" target="_blank" rel="noopener">Privacy Policy</a>.' }));
    wrap.appendChild(footerCta);

    this.root.appendChild(wrap);
    this._footerCtaEl = footerBtn;
    this._observeReveals();
  };

  // ── Scroll reveal + count-up (purposeful motion only: one-time reveal on
  // first scroll into view, no loops, no gratuitous parallax) ──────────────
  LeadMagnetEngine.prototype._observeReveals = function () {
    // Bars/count-ups can live outside .lm-reveal wrappers too (e.g. the real
    // result card) — animate those immediately.
    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var loose = this.root.querySelectorAll('[data-fill], [data-countup]');
    loose.forEach(function (t) { if (!t.closest('.lm-reveal')) animateEl(t); });

    var els = this.root.querySelectorAll('.lm-reveal:not(.lm-revealed)');
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('lm-revealed'); runCountUps(el); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('lm-revealed');
        runCountUps(entry.target);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.2 });
    els.forEach(function (el) { io.observe(el); });

    function animateEl(t) {
      if (t.hasAttribute('data-fill')) {
        t.style.width = parseInt(t.getAttribute('data-fill'), 10) + '%';
        return;
      }
      var end = parseInt(t.getAttribute('data-countup'), 10);
      var suffix = t.getAttribute('data-countup-suffix') || '';
      if (isNaN(end)) return;
      if (reduceMotion) { t.textContent = end + suffix; return; }
      var t0 = null, dur = 900;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        t.textContent = Math.round(eased * end) + suffix;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    function runCountUps(scope) {
      var targets = (scope.hasAttribute('data-countup') || scope.hasAttribute('data-fill'))
        ? [scope]
        : Array.prototype.slice.call(scope.querySelectorAll('[data-countup], [data-fill]'));
      targets.forEach(animateEl);
    }
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

  // ── Framework preview — animated SVG pentagon with L1-L5 badges. Reuses
  // the sitewide numbered-badge convention (not invented icons). Draws in
  // via stroke-dasharray once scrolled into view (handled by _observeReveals
  // through the .lm-reveal wrapper, not a timed loop). ─────────────────────
  LeadMagnetEngine.prototype._buildFrameworkPreview = function () {
    var items = this.config.copy.hero.frameworkPreview || [];
    if (!items.length) return null;
    var n = items.length;
    var size = 280, cx = size / 2, cy = size / 2 - 6, r = 92;
    var SVG_NS = 'http://www.w3.org/2000/svg';
    var pts = [];
    for (var i = 0; i < n; i++) {
      var angle = (Math.PI * 2 * i) / n - Math.PI / 2;
      pts.push({ x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) });
    }
    var pathD = pts.map(function (p, i) { return (i === 0 ? 'M' : 'L') + p.x.toFixed(1) + ',' + p.y.toFixed(1); }).join(' ') + ' Z';

    var wrap = el('div', { class: 'lm-fw-preview' });
    var svgWrap = el('div', { class: 'lm-fw-svg-wrap' });
    var svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + size + ' ' + size);
    svg.setAttribute('class', 'lm-fw-svg');

    var fill = document.createElementNS(SVG_NS, 'path');
    fill.setAttribute('d', pathD);
    fill.setAttribute('class', 'lm-fw-fill');
    svg.appendChild(fill);

    var stroke = document.createElementNS(SVG_NS, 'path');
    stroke.setAttribute('d', pathD);
    stroke.setAttribute('class', 'lm-fw-stroke');
    svg.appendChild(stroke);

    pts.forEach(function (p) {
      var dot = document.createElementNS(SVG_NS, 'circle');
      dot.setAttribute('cx', p.x); dot.setAttribute('cy', p.y); dot.setAttribute('r', 4);
      dot.setAttribute('class', 'lm-fw-dot');
      svg.appendChild(dot);
    });
    svgWrap.appendChild(svg);

    // Badges positioned in HTML (outside the SVG viewBox scale) so labels stay crisp at any size
    pts.forEach(function (p, i) {
      var pct = { left: (p.x / size * 100).toFixed(1) + '%', top: (p.y / size * 100).toFixed(1) + '%' };
      var badge = el('div', { class: 'lm-fw-badge', style: 'left:' + pct.left + ';top:' + pct.top }, [
        el('span', { class: 'lm-fw-badge-num', text: items[i].badge }),
        el('span', { class: 'lm-fw-badge-label', text: items[i].label })
      ]);
      svgWrap.appendChild(badge);
    });

    wrap.appendChild(svgWrap);
    return wrap;
  };

  // ── Sample report preview — honestly-labeled "Example" mockup of the
  // gated report a visitor unlocks. Real tier/dimension data from config,
  // never fabricated. ────────────────────────────────────────────────────
  LeadMagnetEngine.prototype._buildSampleReportPreview = function () {
    var c = this.config, sr = c.copy.sampleReport;
    if (!sr) return null;
    var card = el('div', { class: 'lm-sample-report' });
    card.appendChild(el('div', { class: 'lm-sample-report-tag', text: 'Sample Report — Example' }));
    var head = el('div', { class: 'lm-sr-head' });
    head.appendChild(el('div', { class: 'lm-sr-score' }, [
      el('span', { class: 'lm-sr-score-num', 'data-countup': String(sr.score), text: String(sr.score) }),
      el('span', { class: 'lm-sr-score-max', text: '/100' })
    ]));
    head.appendChild(el('div', { class: 'lm-sr-tier', text: sr.tier }));
    card.appendChild(head);
    var dims = el('div', { class: 'lm-sr-dims' });
    (sr.dims || []).forEach(function (d) {
      var row = el('div', { class: 'lm-sr-dim-row' });
      row.appendChild(el('span', { class: 'lm-sr-dim-label', text: d.label }));
      var track = el('div', { class: 'lm-sr-dim-track' });
      // Width applied by _observeReveals so the bars animate in on reveal.
      track.appendChild(el('div', { class: 'lm-sr-dim-fill', 'data-fill': String(d.pct), style: 'width:0%' }));
      row.appendChild(track);
      row.appendChild(el('span', { class: 'lm-sr-dim-pct', text: d.pct + '%' }));
      dims.appendChild(row);
    });
    card.appendChild(dims);
    card.appendChild(el('p', { class: 'lm-sr-note', text: 'Illustrative scoring pattern — your real report is generated from your answers.' }));
    return card;
  };

  // ── Sample question — one REAL question from the quiz, fully live:
  // answering it starts the quiz with Q1 already recorded and drops the
  // visitor on Q2. An interactive on-ramp, not a dead mockup. ─────────────
  LeadMagnetEngine.prototype._buildSampleQuestionTeaser = function () {
    var self = this, c = this.config;
    var q = c.screens && c.screens[0] && c.screens[0].questions && c.screens[0].questions[0];
    if (!q || q.type === 'multiselect') return null;
    var card = el('div', { class: 'lm-sample-q' });
    card.appendChild(el('div', { class: 'lm-sample-q-tag', text: 'Or just start here — question 1 of ' + this._totalQuestions() }));
    card.appendChild(el('p', { class: 'lm-sample-q-text', text: q.text }));
    var opts = el('div', { class: 'lm-sample-q-opts' });
    (q.options || []).forEach(function (opt, i) {
      opts.appendChild(el('button', {
        class: 'lm-sample-q-opt',
        'data-gtm-cta': 'sample-question-answer', 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'sample_question',
        onclick: function () {
          self.state.answers[q.id] = { index: i };
          self.pushEvent('start', { cta_source: 'sample_question' });
          self.pushEvent('questionAnswered', { question_id: q.id, dimension: q.dimId });
          self.state.screen = 'quiz';
          self.state.qIndex = 1;
          self.state.pendingInsight = null;
          self._render();
        }
      }, [
        el('span', { class: 'lm-opt-num', text: String(i + 1) }),
        el('span', { class: 'lm-opt-text', text: opt })
      ]));
    });
    card.appendChild(opts);
    card.appendChild(el('p', { class: 'lm-sample-q-hint', text: 'Your answer counts — that\'s 1 of 10 done.' }));
    return card;
  };

  LeadMagnetEngine.prototype._totalQuestions = function () {
    var total = 0;
    (this.config.screens || []).forEach(function (s) { total += (s.questions || []).length; });
    return total;
  };

  // Hero CTA jumps straight into the first question — no separate intro
  // screen, which only repeated the hero's own headline/subhead.
  LeadMagnetEngine.prototype._startQuiz = function (source) {
    this._beginQuestions(source);
  };

  LeadMagnetEngine.prototype._beginQuestions = function (source) {
    this.state.screen = 'quiz';
    this.state.qIndex = 0;
    this.state.pendingInsight = null;
    this.pushEvent('start', { cta_source: source || 'unknown' });
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
    // (qIndex+1)/(total+1): never 0% on Q1, never claims done before the gate.
    var track = el('div', { class: 'lm-quiz-progress-track', role: 'progressbar', 'aria-valuemin': '0', 'aria-valuemax': String(total), 'aria-valuenow': String(this.state.qIndex + 1), 'aria-label': 'Quiz progress' });
    track.appendChild(el('div', { class: 'lm-quiz-progress-fill', style: 'width:' + Math.round(((this.state.qIndex + 1) / (total + 1)) * 100) + '%' }));
    topbar.appendChild(track);
    topbar.appendChild(el('span', { class: 'lm-quiz-count', text: (this.state.qIndex + 1) + ' / ' + total }));
    wrap.appendChild(topbar);

    var body = el('div', { class: 'lm-quiz-body', 'aria-live': 'polite' });
    if (screen) body.appendChild(el('div', { class: 'lm-quiz-eyebrow', text: screen.chipLabel || screen.theme || '' }));
    body.appendChild(this._buildQuestionBlock(q));

    if (q.type === 'multiselect') {
      var hasSelection = this.state.answers[q.id] && this.state.answers[q.id].indices.length > 0;
      body.appendChild(el('p', { class: 'lm-quiz-hint', text: 'Select every one that applies, then continue.' }));
      var continueBtn = el('button', {
        class: 'lm-btn lm-btn-primary lm-continue-btn', text: 'Continue',
        disabled: hasSelection ? null : 'disabled',
        'data-gtm-cta': 'continue', 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'quiz',
        onclick: function () { self._afterQuestionAnswered(q); }
      });
      body.appendChild(continueBtn);
    } else if (this.state.qIndex < 2) {
      body.appendChild(el('p', { class: 'lm-quiz-hint', text: 'Tap an answer, or press 1–' + q.options.length + ' on your keyboard. About 2 minutes total.' }));
    }

    wrap.appendChild(body);
    this.root.appendChild(wrap);
    var qText = wrap.querySelector('.lm-question-text');
    if (qText) { qText.setAttribute('tabindex', '-1'); try { qText.focus({ preventScroll: true }); } catch (e) { /* older browsers */ } }
  };

  LeadMagnetEngine.prototype._buildQuestionBlock = function (q) {
    var self = this;
    var block = el('div', { class: 'lm-question' });
    var qTextId = 'lm-q-' + q.id;
    block.appendChild(el('p', { class: 'lm-question-text', id: qTextId, text: q.text }));
    var opts = el('div', {
      class: 'lm-options',
      role: q.type === 'multiselect' ? 'group' : 'radiogroup',
      'aria-labelledby': qTextId
    });
    q.options.forEach(function (optText, idx) {
      if (q.type === 'multiselect') {
        var selected = self.state.answers[q.id] && self.state.answers[q.id].indices.indexOf(idx) !== -1;
        var btn = el('button', {
          class: 'lm-option lm-option-multi' + (selected ? ' lm-option-selected' : ''),
          'aria-pressed': selected ? 'true' : 'false',
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
          role: 'radio', 'aria-checked': isSelected ? 'true' : 'false',
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
    if (this._advancing) return; // rapid double-answer would skip a question
    this._advancing = true;
    var firstAnswer = !this.state.answers[q.id];
    this.state.answers[q.id] = { index: idx };
    if (firstAnswer) this.pushEvent('questionAnswered', { question_id: q.id, dimension: q.dimId });
    this._render(); // show the selected state immediately, then advance
    this._advancing = true; // _render resets it; re-arm for the timeout window
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
    if (q.type === 'multiselect') {
      var ans = this.state.answers[q.id];
      if (!ans || !ans.indices.length) return; // Continue is disabled, but guard Enter too
      if (!ans._eventSent) { ans._eventSent = true; this.pushEvent('questionAnswered', { question_id: q.id, dimension: q.dimId }); }
    }
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
    var total = allQuestions(this.config).length;
    var wrap = el('div', { class: 'lm-quiz' + this._quizAnimClass('insight' + this.state.qIndex) });

    // Keep the topbar so progress context survives the interrupt.
    var topbar = el('div', { class: 'lm-quiz-topbar' });
    topbar.appendChild(el('button', {
      class: 'lm-quiz-back', html: '&larr;', 'aria-label': 'Back to the question',
      onclick: function () { self.state.pendingInsight = null; self._render(); }
    }));
    var track = el('div', { class: 'lm-quiz-progress-track', role: 'progressbar', 'aria-valuemin': '0', 'aria-valuemax': String(total), 'aria-valuenow': String(this.state.qIndex + 1) });
    track.appendChild(el('div', { class: 'lm-quiz-progress-fill', style: 'width:' + Math.round(((this.state.qIndex + 1) / (total + 1)) * 100) + '%' }));
    topbar.appendChild(track);
    topbar.appendChild(el('span', { class: 'lm-quiz-count', text: (this.state.qIndex + 1) + ' / ' + total }));
    wrap.appendChild(topbar);

    if (!this._insightViewSent) { this._insightViewSent = true; this.pushEvent('questionAnswered', { question_id: 'insight_interrupt', dimension: 'insight' }); }
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
    this.state.score.weakestDim = weakestDim(this.state.score);
    this.state.screen = 'teaser';
    this.pushEvent('teaserView', { tier: this.state.score.tier ? this.state.score.tier.label : null });
    if (typeof window.clarity === 'function') { window.clarity('set', 'lm_step', 'teaser'); }
    this._render();
  };

  LeadMagnetEngine.prototype._renderTeaser = function () {
    var self = this, c = this.config, score = this.state.score;
    var wrap = el('div', { class: 'lm-teaser' });

    // Tier and score both stay hidden until the gate — revealing the tier
    // here gave away most of the value the email unlocks.
    wrap.appendChild(el('h1', { class: 'lm-h2', text: 'Your ' + c.indexLabel + ' is ready.' }));
    wrap.appendChild(el('div', { class: 'lm-score-blur', 'aria-hidden': 'true', text: '··/100' }));
    wrap.appendChild(this._buildChart(score, true));

    wrap.appendChild(el('p', { class: 'lm-weak-line', text: 'One of your ' + score.dimOrder.length + ' areas scored materially below the rest — your report names it, and what to do about it first.' }));
    if (c.copy.teaser && c.copy.teaser.urgencyLine) {
      wrap.appendChild(el('p', { class: 'lm-peer-line', text: c.copy.teaser.urgencyLine }));
    }

    var gate = el('div', { class: 'lm-email-gate' });
    gate.appendChild(el('p', { class: 'lm-gate-done', text: '10 of 10 answered — one step left.' }));
    gate.appendChild(el('p', { class: 'lm-gate-copy', text: 'You’re done. Enter your work email and your score, your weakest spot, and your PDF report unlock instantly — right here, no waiting on an inbox.' }));
    var form = el('form', { class: 'lm-gate-form' });
    function labeled(input, id, labelText) {
      input.setAttribute('id', id);
      input.setAttribute('name', id);
      var lab = el('label', { for: id, class: 'lm-visually-hidden', text: labelText });
      form.appendChild(lab);
      form.appendChild(input);
    }
    var fName = el('input', { type: 'text', placeholder: 'First name', required: 'required', class: 'lm-input', autocomplete: 'given-name' });
    var fEmail = el('input', { type: 'email', placeholder: 'Work email', required: 'required', class: 'lm-input', autocomplete: 'email', inputmode: 'email', autocapitalize: 'off' });
    var fCompany = el('input', { type: 'text', placeholder: 'Company', required: 'required', class: 'lm-input', autocomplete: 'organization' });
    labeled(fName, 'lm-first-name', 'First name');
    labeled(fEmail, 'lm-email', 'Work email');
    labeled(fCompany, 'lm-company', 'Company');
    form.appendChild(el('p', { class: 'lm-legal', text: "Your report generates instantly in your browser. We won't share your details, and there's no obligation." }));
    var submitBtn = el('button', {
      type: 'submit', class: 'lm-btn lm-btn-primary', text: 'Unlock My ' + c.indexLabel,
      'data-gtm-cta': 'unlock-my-index', 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'teaser'
    });
    form.appendChild(submitBtn);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (self._submitting) return;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Unlocking…';
      self._submitContact({ firstName: fName.value.trim(), email: fEmail.value.trim(), company: fCompany.value.trim() });
    });
    gate.appendChild(form);
    wrap.appendChild(gate);

    this.root.appendChild(wrap);
  };

  LeadMagnetEngine.prototype._submitContact = function (contact) {
    var self = this, c = this.config;
    if (this._submitting) return;
    this._submitting = true;
    this.state.contact = contact;
    this.pushEvent('emailCaptured', { email_domain: (contact.email.split('@')[1] || '') });

    // "Assessment complete" — the primary conversion: every question
    // answered AND contact info handed over. Distinct from emailCaptured
    // above so it reads unambiguously as THE conversion event in GA4/Ads
    // reporting, not just a generic form-fill analytics event.
    var tierLabel = this.state.score.tier ? this.state.score.tier.label : null;
    this.pushEvent('assessmentComplete', { tier: tierLabel });

    if (typeof window.gtag === 'function') {
      // Enhanced Conversions for Leads — gtag hashes this before sending.
      // Also requires the "Enhanced conversions" toggle ON for the conversion
      // action in Google Ads (Goals → Conversions → Settings).
      window.gtag('set', 'user_data', {
        email: contact.email,
        address: { first_name: contact.firstName }
      });
    }
    if (c.googleAdsConversionLabel && typeof window.gtag === 'function') {
      // Tier-weighted value so value-based bidding can tell a hot lead
      // (low-maturity tier = most in need of the engagement) from a cold one.
      var adsValue = (c.googleAdsTierValues && tierLabel && typeof c.googleAdsTierValues[tierLabel] === 'number')
        ? c.googleAdsTierValues[tierLabel]
        : c.googleAdsConversionValue;
      window.gtag('event', 'conversion', {
        send_to: c.googleAdsConversionLabel,
        value: adsValue,
        currency: c.googleAdsConversionCurrency,
        transaction_id: this.sessionId
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
    if (typeof window.clarity === 'function') {
      window.clarity('set', 'lm_step', 'full');
      if (apiResult.tier) window.clarity('set', 'lm_tier', apiResult.tier);
    }
    this._sendTeamNotification(apiResult);
    this._render();
  };

  // Fires the team-notification email client-side (browser fetch — same
  // pattern as contact.html/chat-widget.js). api/lead-magnet-submit.js
  // deliberately does NOT send this itself: Cloudflare (fronting
  // FormSubmit.co) returns a 403 bot-detection challenge to Vercel's
  // serverless outbound IPs regardless of headers, so the request has to
  // come from a real browser. Prefers apiResult's server-verified
  // tier/overallScore/dims/weakestDim, but ALWAYS fires — even when the API
  // call failed — falling back to the client-computed score, so a network
  // blip never silently destroys a fully-qualified lead.
  LeadMagnetEngine.prototype._sendTeamNotification = function (apiResult) {
    var c = this.config, contact = this.state.contact || {};
    if (!apiResult) apiResult = { ok: false };
    var apiFailed = apiResult.ok === false;
    var score = this.state.score || {};
    var tier = apiResult.tier || (score.tier ? score.tier.label : '');
    var overall = (typeof apiResult.overallScore === 'number') ? apiResult.overallScore : score.overall;
    var weakest = apiResult.weakestDim || score.weakestDim || '';
    var dims = apiResult.dims || {};
    if (!Object.keys(dims).length && score.dims) {
      Object.keys(score.dims).forEach(function (id) { dims[id] = score.dims[id].pct; });
    }
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
        'Tier': tier + ' (' + overall + '/100)',
        'Weakest Dimension': weakest,
        'Dimension Breakdown': dimLines,
        'Lighter-Track Signal': apiResult.routing && apiResult.routing.lighterTrack ? 'Yes' : 'No',
        'Delivery Note': apiFailed ? 'API failed — score is the client-side fallback, lead is NOT in the Sheet' : 'Server-verified',
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

    wrap.appendChild(el('h1', { class: 'lm-h2', text: 'Your ' + c.indexLabel }));

    // Real score card — same styled component as the hero's sample preview,
    // now with the reader's actual numbers.
    var card = el('div', { class: 'lm-sample-report lm-result-card' });
    var head = el('div', { class: 'lm-sr-head' });
    head.appendChild(el('div', { class: 'lm-sr-score' }, [
      el('span', { class: 'lm-sr-score-num', 'data-countup': String(score.overall), text: String(score.overall) }),
      el('span', { class: 'lm-sr-score-max', text: '/100' })
    ]));
    if (score.tier) head.appendChild(el('div', { class: 'lm-sr-tier', text: score.tier.label }));
    card.appendChild(head);
    var dims = el('div', { class: 'lm-sr-dims' });
    score.dimOrder.forEach(function (id) {
      var d = score.dims[id];
      var row = el('div', { class: 'lm-sr-dim-row' });
      row.appendChild(el('span', { class: 'lm-sr-dim-label', text: d.label }));
      var track = el('div', { class: 'lm-sr-dim-track' });
      track.appendChild(el('div', { class: 'lm-sr-dim-fill', 'data-fill': String(d.pct), style: 'width:0%' }));
      row.appendChild(track);
      row.appendChild(el('span', { class: 'lm-sr-dim-pct', text: d.pct + '%' }));
      dims.appendChild(row);
    });
    card.appendChild(dims);
    wrap.appendChild(card);

    if (score.tier && score.tier.description) wrap.appendChild(el('p', { class: 'lm-body lm-result-desc', text: score.tier.description }));

    var weakest = score.weakestDim || weakestDim(score);
    if (weakest && c.weakLineTemplates && c.weakLineTemplates[weakest]) {
      var weakKids = [el('p', { text: c.weakLineTemplates[weakest] })];
      if (c.nextStepTemplates && c.nextStepTemplates[weakest]) {
        weakKids.push(el('p', { class: 'lm-next-action', text: c.nextStepTemplates[weakest] }));
      }
      wrap.appendChild(el('div', { class: 'lm-weak-callout' }, weakKids));
    }

    // Booking CTA sits high, while motivation is peak — chart + sell copy follow.
    var lighter = api.routing && api.routing.lighterTrack;
    var ctaLabel = (lighter && c.copy.fullResult.primaryCtaLighter) || c.copy.fullResult.primaryCta;
    var ctaRow = el('div', { class: 'lm-cta-row' });
    var bookBtn = el('a', {
      class: 'lm-btn lm-btn-primary', text: ctaLabel, href: this._bookingUrl(),
      target: '_blank', rel: 'noopener',
      'data-gtm-cta': slugify(ctaLabel), 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'full_result',
      onclick: function () { self.pushEvent('callBooked'); }
    });
    var pdfBtn = el('button', {
      class: 'lm-btn lm-btn-ghost', text: 'Download PDF Report',
      'data-gtm-cta': 'download-pdf-report', 'data-gtm-cta-type': 'secondary', 'data-gtm-cta-section': 'full_result',
      onclick: function () { self._downloadPdf(this); }
    });
    ctaRow.appendChild(bookBtn);
    ctaRow.appendChild(pdfBtn);
    wrap.appendChild(ctaRow);
    wrap.appendChild(el('p', { class: 'lm-guarantee-line lm-result-guarantee', text: 'If the Day-30 report doesn’t justify continuing, you walk away — no lock-in, no exit fee.' }));

    wrap.appendChild(this._buildChart(score, false));

    if (api.peer && api.peer.sufficientData) {
      wrap.appendChild(el('p', { class: 'lm-peer-line', text: 'Teams assessed so far average ' + api.peer.avgOverall + '/100 — you scored ' + (score.overall >= api.peer.avgOverall ? 'above' : 'below') + ' that.' }));
    }

    if (c.copy.fullResult.pdfNextStep) {
      wrap.appendChild(el('div', { class: 'lm-weak-callout lm-next-step' }, [el('p', { text: c.copy.fullResult.pdfNextStep })]));
    }

    wrap.appendChild(el('p', { class: 'lm-legal', html: 'Your data is used only to generate this report and isn\'t shared. See our <a href="/privacy" target="_blank" rel="noopener">Privacy Policy</a>.' }));

    this.root.appendChild(wrap);
    this._observeReveals();
  };

  LeadMagnetEngine.prototype._downloadPdf = function (btn) {
    if (typeof window.jspdf === 'undefined') {
      console.error('[lead-magnet] jsPDF not loaded');
      if (btn) { btn.textContent = 'PDF blocked by your browser — book the call and we’ll bring it'; btn.disabled = true; }
      return;
    }
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

  // Radar diagram of the score's dimensions, drawn with jsPDF vector
  // primitives (the on-page SVG can't be reused inside the PDF).
  function pdfRadar(doc, cx, cy, r, score) {
    var n = score.dimOrder.length;
    function pt(i, radius) {
      var a = (Math.PI * 2 * i) / n - Math.PI / 2;
      return [cx + radius * Math.cos(a), cy + radius * Math.sin(a)];
    }
    function polySegs(radiusFn) {
      var start = pt(0, radiusFn(0)), segs = [], prev = start;
      for (var i = 1; i < n; i++) {
        var p = pt(i, radiusFn(i));
        segs.push([p[0] - prev[0], p[1] - prev[1]]);
        prev = p;
      }
      return { start: start, segs: segs };
    }
    doc.setDrawColor(223, 227, 232);
    doc.setLineWidth(0.75);
    [0.25, 0.5, 0.75, 1].forEach(function (f) {
      var g = polySegs(function () { return r * f; });
      doc.lines(g.segs, g.start[0], g.start[1], [1, 1], 'S', true);
    });
    for (var i = 0; i < n; i++) {
      var sp = pt(i, r);
      doc.line(cx, cy, sp[0], sp[1]);
    }
    var v = polySegs(function (i) {
      var d = score.dims[score.dimOrder[i]];
      return r * Math.max(d.pct, 4) / 100;
    });
    doc.setFillColor(200, 240, 244);
    doc.setDrawColor.apply(doc, PDF_TEAL);
    doc.setLineWidth(1.5);
    doc.lines(v.segs, v.start[0], v.start[1], [1, 1], 'FD', true);
    for (var j = 0; j < n; j++) {
      var d2 = score.dims[score.dimOrder[j]];
      var vp = pt(j, r * Math.max(d2.pct, 4) / 100);
      doc.setFillColor.apply(doc, PDF_TEAL_DARK);
      doc.circle(vp[0], vp[1], 2.4, 'F');
    }
    doc.setFont('helvetica', 'bold'); doc.setFontSize(8.5);
    doc.setTextColor.apply(doc, PDF_GREY);
    for (var k = 0; k < n; k++) {
      var lp = pt(k, r + 16);
      var lbl = score.dims[score.dimOrder[k]].label;
      doc.text(lbl, lp[0], lp[1] + 3, { align: 'center' });
    }
    doc.setTextColor.apply(doc, PDF_INK);
  }

  // Horizontal tier scale with a marker at the reader's exact score.
  function pdfTierBar(doc, x, y, w, tierTable, overall, tierColor) {
    var n = tierTable.length, gap = 3, segW = (w - gap * (n - 1)) / n, segH = 12;
    tierTable.forEach(function (t, i) {
      var active = overall >= t.min && overall <= t.max;
      var sx = x + i * (segW + gap);
      if (active) doc.setFillColor.apply(doc, tierColor);
      else doc.setFillColor.apply(doc, PDF_TRACK);
      doc.roundedRect(sx, y, segW, segH, 4, 4, 'F');
      doc.setFont('helvetica', active ? 'bold' : 'normal');
      doc.setFontSize(8.5);
      if (active) doc.setTextColor.apply(doc, tierColor);
      else doc.setTextColor.apply(doc, PDF_GREY);
      doc.text(t.label, sx + segW / 2, y + segH + 13, { align: 'center' });
    });
    var mx = x + w * (overall / 100);
    doc.setFillColor.apply(doc, PDF_INK);
    doc.triangle(mx - 4.5, y - 9, mx + 4.5, y - 9, mx, y - 2, 'F');
    doc.setFont('helvetica', 'bold'); doc.setFontSize(8.5);
    doc.setTextColor.apply(doc, PDF_INK);
    doc.text('You: ' + overall, mx, y - 14, { align: 'center' });
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
    var metaLine = (contact.firstName ? 'Prepared for ' + contact.firstName + '  ·  ' : '') +
      (contact.company ? contact.company + '  ·  ' : '') +
      new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
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

    y += 150 + 44;

    // Tier scale — where this score sits across all tiers
    if (c.tierTable && c.tierTable.length) {
      doc.setFont('helvetica', 'bold'); doc.setFontSize(13);
      doc.text('Where you sit', margin, y);
      y += 34;
      pdfTierBar(doc, margin, y, contentW, c.tierTable, score.overall, tierColor);
      y += 52;
    }

    doc.setFont('helvetica', 'bold'); doc.setFontSize(13);
    doc.setTextColor.apply(doc, PDF_INK);
    doc.text('What this score means', margin, y);
    y += 22;
    doc.setFont('helvetica', 'normal'); doc.setFontSize(11);
    var introBody = 'This report scores your organisation across the ' + score.dimOrder.length + ' dimensions Upcore’s Fractional AI Officer framework governs against. The following pages map your profile against the framework and break down exactly where you’re strong and where the gaps are — the same lens we use in paying engagements.';
    var introLines = doc.splitTextToSize(introBody, contentW);
    doc.text(introLines, margin, y);
    y += introLines.length * 15 + 26;

    if (peer.sufficientData) {
      doc.setFillColor.apply(doc, PDF_CARD);
      doc.roundedRect(margin, y, contentW, 44, 8, 8, 'F');
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
      doc.text('Teams assessed so far average ' + peer.avgOverall + '/100 — you scored ' + (score.overall >= peer.avgOverall ? 'above' : 'below') + ' that.', margin + 16, y + 27);
    }

    pdfFooter(doc, pageW, pageH, 1, 4);

    // ── PAGE 2 — Framework profile (radar diagram) ──────────────────────
    doc.addPage();
    pdfHeaderBand(doc, pageW, c.indexLabel, 'Your Framework Profile');
    y = 168;

    doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
    doc.setTextColor.apply(doc, PDF_GREY);
    doc.text('Your profile across all ' + score.dimOrder.length + ' framework dimensions. A balanced, wide shape is the goal.', margin, y);
    doc.setTextColor.apply(doc, PDF_INK);

    pdfRadar(doc, pageW / 2, y + 190, 130, score);
    y += 380;

    if (score.weakestDim && c.weakLineTemplates && c.weakLineTemplates[score.weakestDim]) {
      doc.setFillColor.apply(doc, PDF_CARD);
      var weakLines = doc.splitTextToSize(c.weakLineTemplates[score.weakestDim], contentW - 40);
      var nextLines2 = (c.nextStepTemplates && c.nextStepTemplates[score.weakestDim])
        ? doc.splitTextToSize(c.nextStepTemplates[score.weakestDim], contentW - 40)
        : [];
      var boxH = weakLines.length * 15 + 42 + (nextLines2.length ? nextLines2.length * 14 + 12 : 0);
      doc.roundedRect(margin, y, contentW, boxH, 8, 8, 'F');
      doc.setFillColor.apply(doc, PDF_TEAL);
      doc.rect(margin, y, 4, boxH, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(10);
      doc.text('WEAKEST AREA: ' + (score.dims[score.weakestDim] ? score.dims[score.weakestDim].label.toUpperCase() : ''), margin + 20, y + 22);
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
      doc.text(weakLines, margin + 20, y + 40);
      if (nextLines2.length) {
        doc.setFont('helvetica', 'bold'); doc.setFontSize(10);
        doc.setTextColor.apply(doc, PDF_TEAL_DARK);
        doc.text(nextLines2, margin + 20, y + 40 + weakLines.length * 15 + 8);
        doc.setTextColor.apply(doc, PDF_INK);
      }
    }

    pdfFooter(doc, pageW, pageH, 2, 4);

    // ── PAGE 3 — Dimension breakdown ────────────────────────────────────
    doc.addPage();
    pdfHeaderBand(doc, pageW, c.indexLabel, 'Dimension Breakdown');
    y = 168;

    doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
    doc.setTextColor.apply(doc, PDF_GREY);
    doc.text('Score out of 100 for each dimension.' + (peer.sufficientData ? ' The teal marker shows the peer average.' : ''), margin, y);
    doc.setTextColor.apply(doc, PDF_INK);
    y += 30;

    var barW = contentW - 70;
    var rowGap = score.dimOrder.length > 6 ? 26 : 34;
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
      y += rowGap;
    });

    pdfFooter(doc, pageW, pageH, 3, 4);

    // ── PAGE 4 — Next step ───────────────────────────────────────────────
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
    doc.textWithLink('www.upcoretech.com' + (c.bookingHref || '/assessment'), margin + 24, y + 62, {
      url: 'https://www.upcoretech.com' + (c.bookingHref || '/assessment') + '?utm_source=pdf_report&utm_medium=pdf&utm_campaign=' + c.niche
    });
    doc.setFont('helvetica', 'normal'); doc.setFontSize(9.5);
    doc.setTextColor(200, 205, 210);
    doc.text('No commitment required — we’ll walk through this exact report on the call.', margin + 24, y + 80);
    doc.setTextColor.apply(doc, PDF_INK);

    pdfFooter(doc, pageW, pageH, 4, 4);

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
    svg.setAttribute('class', 'lm-radar-svg');
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
    // Blur only the data polygon — the axis labels explain what the chart
    // is; hiding them made the teaser read as a broken image.
    poly.setAttribute('class', 'lm-radar-data' + (blurred ? ' lm-blurred' : ''));
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
  // Shows on the hero (start the quiz) AND on the full result (book the
  // call) — the two screens with real scroll depth. Hidden while the hero's
  // own footer CTA is on screen so the same button never appears twice.
  LeadMagnetEngine.prototype._buildStickyCTA = function () {
    var self = this;
    var bar = el('div', { class: 'lm-sticky-cta' });
    var btn = el('button', {
      class: 'lm-btn lm-btn-primary', text: this.config.copy.hero.primaryCta,
      'data-gtm-cta': 'sticky-cta', 'data-gtm-cta-type': 'primary', 'data-gtm-cta-section': 'sticky',
      onclick: function () {
        if (self.state.screen === 'hero') self._startQuiz('sticky');
        else if (self.state.screen === 'full') { self.pushEvent('callBooked'); window.open(self._bookingUrl(), '_blank', 'noopener'); }
      }
    });
    bar.appendChild(btn);
    document.body.appendChild(bar);
    this._stickyBar = bar;
    this._stickyBtn = btn;
    window.addEventListener('scroll', function () { self._updateStickyCTA(); }, { passive: true });
  };

  LeadMagnetEngine.prototype._updateStickyCTA = function () {
    if (!this._stickyBar) return;
    var screen = this.state.screen;
    var show = false;
    if (screen === 'hero' && window.scrollY > 400) {
      show = true;
      this._stickyBtn.textContent = this.config.copy.hero.primaryCta;
      // Suppress while the hero's own footer CTA is in view — identical
      // buttons stacked on screen read as a rendering bug.
      if (this._footerCtaEl) {
        var r = this._footerCtaEl.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) show = false;
      }
    } else if (screen === 'full' && window.scrollY > 300) {
      show = true;
      this._stickyBtn.textContent = this.config.copy.fullResult.primaryCta;
    }
    this._stickyBar.classList.toggle('lm-sticky-visible', show);
  };

  // ── Public init ──────────────────────────────────────────────────────────
  window.LeadMagnetEngine = {
    init: function (config) { return new LeadMagnetEngine(config); }
  };
})();
