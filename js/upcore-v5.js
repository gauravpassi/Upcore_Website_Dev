/* Upcore V5 "Flow" motion layer (2026-10-06). Runs after js/upcore-v4.js on V4 pages.
   Modules: spine (scroll thread + stage dots), flowline (hero pipeline animation),
   heading word reveal, count-up numbers, pipeline scrollytelling counter, quote carousel,
   marquee off-screen pause, hero glow parallax. Everything respects prefers-reduced-motion,
   pauses off-screen and degrades to the server-rendered content without JS. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var onView = function (el, fn, opts) {
    if (!hasIO) { fn(); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { fn(e); io.unobserve(e.target); } }); }, opts || { threshold: 0.2 });
    io.observe(el);
  };
  var offWatch = function (el) {
    if (!hasIO) return;
    new IntersectionObserver(function (es) { es.forEach(function (e) { el.classList.toggle('is-off', !e.isIntersecting); }); }, { rootMargin: '80px' }).observe(el);
  };

  /* ------------------------------------------------------------ heading word reveal */
  function splitWords(h) {
    var i = 0;
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var parts = n.textContent.split(/(\s+)/), frag = document.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            var w = document.createElement('span'); w.className = 'w';
            var inner = document.createElement('span'); inner.style.setProperty('--i', i++); inner.textContent = p;
            w.appendChild(inner); frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && !n.classList.contains('sr')) {
          if (n.classList.contains('ul-draw')) {           // keep the underline phrase whole
            var w2 = document.createElement('span'); w2.className = 'w';
            var in2 = document.createElement('span'); in2.style.setProperty('--i', i++);
            n.parentNode.replaceChild(w2, n); in2.appendChild(n); w2.appendChild(in2);
          } else walk(n);
        }
      });
    };
    walk(h);
    h.classList.add('wr');
  }
  if (!reduce && hasIO) {
    $$('.flow-main .sec-head .t-h2, .flow-main .pipe-intro .t-h2, .flow-main .subhead .t-h2, .flow-main .pod-head .t-h2, .cta-band .t-display, .is-calm .h-h2').forEach(function (h) {
      splitWords(h);
      onView(h, function () { h.classList.add('is-in'); }, { threshold: 0.3 });
    });
  }

  /* ------------------------------------------------------------ spine */
  var main = $('.flow-main'), spine = $('.spine'), fill = $('.spine-fill');
  var dots = [], mTop = 0, mH = 1;
  function layoutSpine() {
    if (!main || !spine || getComputedStyle(spine).display === 'none') { dots = []; return; }
    var r = main.getBoundingClientRect(), base = r.top + scrollY;
    $$('.spine-dot', spine).forEach(function (d) { d.remove(); });
    var ebs = $$('.sec-head .eyebrow, .pipe-intro .eyebrow, .sec--dash .split .eyebrow', main);
    var first = ebs.length ? ebs[0].getBoundingClientRect().top + scrollY - base - 120 : 0;
    first = Math.max(0, first);
    spine.style.setProperty('--spine-top', first + 'px');
    mTop = base + first; mH = Math.max(1, main.offsetHeight - first);
    dots = ebs.map(function (eb) {
      var y = eb.getBoundingClientRect().top + scrollY - mTop + eb.offsetHeight / 2 - 4;
      var d = document.createElement('i'); d.className = 'spine-dot' + (eb.closest('.band') ? ' dark' : ''); d.style.top = y + 'px';
      spine.appendChild(d); return { el: d, y: y };
    });
  }
  function paintSpine() {
    if (!dots.length || !fill) return;
    var p = clamp((scrollY + innerHeight * 0.55 - mTop) / mH, 0, 1);
    fill.style.setProperty('--p', p.toFixed(4));
    var at = p * mH;
    dots.forEach(function (d) { d.el.classList.toggle('on', d.y <= at); });
  }

  /* ------------------------------------------------------------ hero glow parallax */
  var glow = $('.hero--flow .hero-glow');
  function paintGlow() { if (glow && !reduce && scrollY < innerHeight * 1.5) glow.style.setProperty('--gy', (scrollY * 0.18).toFixed(1) + 'px'); }

  var ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () { ticking = false; paintSpine(); paintGlow(); });
  }
  addEventListener('scroll', onScroll, { passive: true });
  var rs; addEventListener('resize', function () { clearTimeout(rs); rs = setTimeout(function () { layoutSpine(); paintSpine(); }, 150); });
  var spineInit = function () { layoutSpine(); paintSpine(); };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(spineInit); else addEventListener('load', spineInit);
  addEventListener('load', spineInit);
  setTimeout(spineInit, 1200);

  /* ------------------------------------------------------------ count-up */
  $$('[data-count]').forEach(function (el) {
    var txt = el.textContent, m = txt.match(/^([^\d]*?)(\d+(?:\.\d+)?)([^\d]*)$/);
    if (!m || reduce) return;
    var pre = m[1], num = parseFloat(m[2]), suf = m[3], dec = (m[2].split('.')[1] || '').length;
    if (num < 2 && !dec) return;
    el.textContent = pre + (0).toFixed(dec) + suf;
    onView(el, function () {
      var t0 = performance.now(), dur = 1500;
      (function step(t) {
        var k = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - k, 3);
        el.textContent = pre + (num * e).toFixed(dec) + suf;
        if (k < 1) requestAnimationFrame(step); else el.textContent = txt;
      })(t0);
    }, { threshold: 0.6 });
  });

  /* ------------------------------------------------------------ open-grid icon draw (controls) */
  $$('.flow-main .ctrl').forEach(function (c) { onView(c, function () { c.classList.add('is-in'); }); });

  /* ------------------------------------------------------------ pipeline scrollytelling */
  $$('.sec--pipe').forEach(function (sec) {
    var pipe = $('.pipe', sec), count = $('.pipe-count b', sec), label = $('.pipe-count em', sec);
    var stages = $$('.pipe-stage', sec);
    if (!pipe || !stages.length || !hasIO) return;
    var cur = -1;
    var set = function (i) {
      if (i === cur) return; cur = i;
      pipe.classList.add('has-cur');
      stages.forEach(function (s, j) { s.classList.toggle('is-cur', j === i); });
      if (count) { count.textContent = (i + 1 < 10 ? '0' : '') + (i + 1); count.classList.remove('tick'); void count.offsetWidth; if (!reduce) count.classList.add('tick'); }
      if (label) { var h = $('h3', stages[i]); label.textContent = h ? h.textContent.replace(/^Stage \d+:\s*/, '') : ''; }
    };
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) set(stages.indexOf(e.target)); });
    }, { rootMargin: '-46% 0px -50% 0px' });
    stages.forEach(function (s) { io.observe(s); });
  });

  /* ------------------------------------------------------------ quote carousel */
  $$('[data-quotes]').forEach(function (qc) {
    var items = $$('.qc-item', qc), dots = $$('.qc-dot', qc), i = 0, timer = 0, held = false, off = false, DUR = 8000;
    if (items.length < 2) { $('.qc-nav', qc) && ($('.qc-nav', qc).hidden = true); return; }
    qc.style.setProperty('--qc-dur', DUR / 1000 + 's');
    var show = function (n) {
      i = (n + items.length) % items.length;
      items.forEach(function (it, j) { it.classList.toggle('is-on', j === i); });
      dots.forEach(function (d, j) { d.classList.remove('is-on'); d.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
      void qc.offsetWidth;
      if (dots[i]) dots[i].classList.add('is-on');
      schedule();
    };
    var schedule = function () { clearTimeout(timer); if (reduce || held || off) return; timer = setTimeout(function () { show(i + 1); }, DUR); };
    if (reduce) qc.classList.add('no-auto');
    dots.forEach(function (d, j) { d.addEventListener('click', function () { show(j); }); });
    var hold = function (v) { held = v; qc.classList.toggle('is-held', v); if (!v) show(i); else clearTimeout(timer); };
    qc.addEventListener('mouseenter', function () { hold(true); });
    qc.addEventListener('mouseleave', function () { hold(false); });
    qc.addEventListener('focusin', function () { hold(true); });
    qc.addEventListener('focusout', function (e) { if (!qc.contains(e.relatedTarget)) hold(false); });
    if (hasIO) new IntersectionObserver(function (es) { es.forEach(function (e) { off = !e.isIntersecting; if (off) clearTimeout(timer); else schedule(); }); }).observe(qc);
    show(0);
  });

  /* ------------------------------------------------------------ marquees + cta lines: pause off-screen */
  $$('[data-marquee]').forEach(offWatch);
  $$('.cta-band').forEach(offWatch);


  /* ------------------------------------------------------------ hero artifact: pull-request gate (homepage)
     Auto-plays two scenarios; the "Routine / Risky" switch takes over (manual mode). Tilts with the pointer,
     drifts with scroll, and a decision-log toast slides out after each decision. */
  $$('[data-gate]').forEach(function (fig) {
    var G = function (k) { return $('[data-g="' + k + '"]', fig); };
    var lis = $$('.gate-checks li', fig), meter = $('.meter i', fig), toggle = $('.gate-toggle', fig);
    var tabs = $$('.gate-tab', fig), ink = $('.gate-ink', fig), log = G('log'), stage = fig.closest('[data-tilt]');
    var SC = [
      { repo: 'Payments service', pr: 'Pull request #418', title: 'Add partial refunds to checkout', sub: 'Written with AI \u00b7 checked by your pipeline',
        c: [['ok', 'Template complete'], ['ok', 'Follows your API conventions'], ['ok', 'No issues found'], ['ok', '87% (minimum 80%)']],
        risk: 12, riskT: '12 / 100', hi: false, tag: 'Merged', out: 'Under your risk limit, so it merged automatically', log: '#418 merged automatically \u00b7 risk 12' },
      { repo: 'Sign-in service', pr: 'Pull request #77', title: 'Refactor session handling', sub: 'Written with AI \u00b7 checked by your pipeline',
        c: [['ok', 'Template complete'], ['fail', 'Changes a shared module outside the spec'], ['ok', 'No issues found'], ['ok', '91% (minimum 80%)']],
        risk: 78, riskT: '78 / 100', hi: true, tag: 'Held', out: 'Over your risk limit, so an architect must approve it', log: '#77 held for architect review \u00b7 risk 78' }
    ];
    var placeInk = function (i) {
      var t = tabs[i]; if (!t || !ink) return;
      ink.style.setProperty('--ink-x', t.offsetLeft + 'px'); ink.style.setProperty('--ink-w', t.offsetWidth + 'px');
      tabs.forEach(function (b, j) { b.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
    };
    placeInk(0);
    addEventListener('resize', function () { placeInk(cur); });
    var cur = 0, paused = false, off = false, manual = false, token = 0;
    var sleep = function (ms, tk) {
      return new Promise(function (res, rej) {
        var left = ms, last = performance.now();
        (function tick(now) {
          if (tk !== token) { rej('cancel'); return; }
          if (!paused && !off && !document.hidden) left -= now - last;
          last = now;
          if (left <= 0) res(); else requestAnimationFrame(tick);
        })(last);
      });
    };
    var setText = function (s) {
      G('repo').textContent = s.repo; G('pr').textContent = s.pr; G('title').textContent = s.title; G('sub').textContent = s.sub;
      lis.forEach(function (li, i) { G('c' + i).textContent = s.c[i][1]; });
    };
    var final = function (s) {
      setText(s);
      lis.forEach(function (li, i) { li.className = s.c[i][0]; });
      meter.style.setProperty('--v', s.risk + '%'); fig.classList.toggle('is-hi', s.hi); G('risk').textContent = s.riskT;
      G('tag').textContent = s.tag; G('out').textContent = s.out;
      var ow = G('outwrap'); ow.classList.toggle('hold', s.hi); ow.classList.toggle('ok', !s.hi); ow.classList.remove('is-hidden');
      if (log) { G('logt').textContent = s.log; }
    };
    async function play(idx, tk) {
      var s = SC[idx]; cur = idx; placeInk(idx);
      setText(s);
      lis.forEach(function (li) { li.className = 'wait'; });
      meter.style.setProperty('--v', '0%'); fig.classList.toggle('is-hi', s.hi); G('risk').textContent = '\u2014';
      var ow = G('outwrap'); ow.classList.add('is-hidden'); if (log) log.classList.remove('show');
      await sleep(450, tk);
      for (var i = 0; i < lis.length; i++) { lis[i].className = 'run'; await sleep(560, tk); lis[i].className = s.c[i][0]; await sleep(150, tk); }
      meter.style.setProperty('--v', s.risk + '%'); await sleep(950, tk);
      G('risk').textContent = s.riskT; G('tag').textContent = s.tag; G('out').textContent = s.out;
      ow.classList.toggle('hold', s.hi); ow.classList.toggle('ok', !s.hi); ow.classList.remove('is-hidden');
      await sleep(500, tk);
      if (log) { G('logt').textContent = s.log; log.classList.add('show'); }
    }
    async function loop() {
      var tk = ++token;
      try {
        await sleep(900, tk);
        for (var n = 0; ; n++) { await play(n % SC.length, tk); await sleep(SC[n % SC.length].hi ? 3800 : 3200, tk); }
      } catch (e) { /* cancelled by the user switching scenario */ }
    }
    tabs.forEach(function (b, i) {
      b.addEventListener('click', function () {
        manual = true; var tk = ++token;
        if (reduce) { placeInk(i); cur = i; final(SC[i]); return; }
        play(i, tk).catch(function () {});
      });
    });
    if (reduce) { if (toggle) toggle.hidden = true; final(SC[0]); return; }
    if (hasIO) new IntersectionObserver(function (es) { es.forEach(function (e) { off = !e.isIntersecting; }); }).observe(fig);
    if (toggle) toggle.addEventListener('click', function () {
      paused = !paused; toggle.textContent = paused ? 'Play' : 'Pause'; toggle.setAttribute('aria-label', paused ? 'Play animation' : 'Pause animation');
      if (!paused && manual) { manual = false; loop(); }
    });
    loop();
    // pointer tilt (fine pointers only) and a slow drift while the hero scrolls away
    var hover = matchMedia('(hover: hover) and (pointer: fine)').matches;
    var hero = fig.closest('.h-hero') || fig.parentNode;
    if (hover && stage) {
      var raf = 0, px = 0, py = 0;
      hero.addEventListener('pointermove', function (e) {
        var r = stage.getBoundingClientRect();
        px = clamp((e.clientX - (r.left + r.width / 2)) / r.width, -1, 1); py = clamp((e.clientY - (r.top + r.height / 2)) / r.height, -1, 1);
        if (!raf) raf = requestAnimationFrame(function () { raf = 0; fig.classList.add('is-tracking'); fig.style.setProperty('--ry', (px * 6).toFixed(2) + 'deg'); fig.style.setProperty('--rx', (-py * 5).toFixed(2) + 'deg'); });
      }, { passive: true });
      hero.addEventListener('pointerleave', function () { fig.classList.remove('is-tracking'); fig.style.setProperty('--rx', '0deg'); fig.style.setProperty('--ry', '0deg'); });
    }
    addEventListener('scroll', function () {
      var y = scrollY; if (y > innerHeight * 1.2) return;
      fig.style.setProperty('--py', (-y * 0.08).toFixed(1) + 'px');
    }, { passive: true });
  });

  /* ------------------------------------------------------------ how it works: scroll story (homepage) */
  $$('[data-story]').forEach(function (story) {
    var steps = $$('.story-step', story), panels = $$('.sv-panel', story), pips = $$('.sv-pip', story), track = $('.sv-track i', story);
    var cur = -1;
    var set = function (i) {
      if (i === cur || i < 0) return; cur = i;
      steps.forEach(function (s, j) { s.classList.toggle('is-on', j === i); });
      panels.forEach(function (p, j) { p.classList.toggle('on', j === i); });
      pips.forEach(function (p, j) { p.classList.toggle('on', j <= i); });
      if (track) track.style.setProperty('--sv', ((i + 1) / steps.length * 100) + '%');
    };
    if (hasIO) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) set(steps.indexOf(e.target)); }); }, { rootMargin: '-45% 0px -50% 0px' });
      steps.forEach(function (s) { io.observe(s); });
    }
    steps.forEach(function (s, i) {
      var b = $('.story-btn', s);
      if (b) b.addEventListener('click', function () { set(i); s.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' }); });
    });
    set(0);
  });

  /* ------------------------------------------------------------ menu hides while reading down, returns on the way up */
  (function () {
    var nav = $('.nav'); if (!nav || reduce) return;
    var lastY = scrollY, acc = 0;
    addEventListener('scroll', function () {
      var y = scrollY, dy = y - lastY; lastY = y;
      if (nav.classList.contains('menu-open') || nav.matches(':focus-within') || $('.nav [aria-expanded="true"]')) { nav.classList.remove('is-hidden'); return; }
      acc = (dy > 0) === (acc > 0) ? acc + dy : dy;
      if (y < 400) nav.classList.remove('is-hidden');
      else if (acc > 60) nav.classList.add('is-hidden');
      else if (acc < -30) nav.classList.remove('is-hidden');
    }, { passive: true });
  })();


  /* ------------------------------------------------------------ homepage estimator: visitor sets the inputs, numbers ease to the result */
  $$('[data-calc]').forEach(function (c) {
    var ins = $$('input[type=range]', c), out = {};
    $$('[data-o]', c).forEach(function (o) { out[o.getAttribute('data-o')] = o; });
    var sr = document.createElement('p'); sr.className = 'sr'; sr.setAttribute('aria-live', 'polite'); c.appendChild(sr);
    var shown = {}, raf = 0, used = false;
    var val = function (k) { var i = $('#c-' + k, c); return i ? +i.value : 0; };
    var fill = function (i) {
      i.style.setProperty('--fill', ((i.value - i.min) / (i.max - i.min) * 100) + '%');
      var o = $('#o-' + i.getAttribute('data-k'), c); if (o) o.textContent = i.value + (i.getAttribute('data-u') || '');
    };
    var calc = function () { var today = val('eng') * val('prs') * val('mins') / 60, freed = today * val('routine') / 100; return { today: today, freed: freed, fte: freed / 40 }; };
    var fmt = function (k, v) { return k === 'fte' ? v.toFixed(1) : Math.round(v).toLocaleString('en-US'); };
    var render = function (animate) {
      var t = calc();
      if (reduce || !animate) { Object.keys(t).forEach(function (k) { shown[k] = t[k]; if (out[k]) out[k].textContent = fmt(k, t[k]); }); return; }
      var from = Object.assign({}, shown), t0 = performance.now(); cancelAnimationFrame(raf);
      (function step(now) {
        var e = clamp((now - t0) / 420, 0, 1); e = 1 - Math.pow(1 - e, 3);
        Object.keys(t).forEach(function (k) { shown[k] = from[k] + (t[k] - from[k]) * e; if (out[k]) out[k].textContent = fmt(k, shown[k]); });
        if (e < 1) raf = requestAnimationFrame(step);
      })(t0);
    };
    var announce = function () { var t = calc(); sr.textContent = 'About ' + fmt('today', t.today) + ' hours of senior review a week, ' + fmt('freed', t.freed) + ' of them on routine changes, roughly ' + fmt('fte', t.fte) + ' full-time senior engineers.'; };
    ins.forEach(function (i) {
      fill(i);
      i.addEventListener('input', function () {
        fill(i); render(true);
        if (!used) { used = true; window.dataLayer = window.dataLayer || []; window.dataLayer.push({ event_params: null }); window.dataLayer.push({ event: 'estimator_used', event_params: { page_path: location.pathname } }); }
      });
      i.addEventListener('change', announce);
    });
    render(false);
  });


  /* ------------------------------------------------------------ AI-Native Engineering: leadership view (hero)
     Rows rotate: the oldest deviation slides out, a "new" one arrives on top; the change count ticks up. */
  $$('[data-dash]').forEach(function (fig) {
    var list = $('.dv', fig), toggle = $('.dash-toggle', fig), shipped = $('.dash-kpis b', fig);
    var hero = fig.closest('.h-hero') || fig.parentNode;
    if (reduce || !list) { if (toggle) toggle.hidden = true; return; }
    var paused = false, off = false, timer = 0;
    var cycle = function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (!paused && !off && !document.hidden) {
          var rows = $$('.dv-row', list), pos = new Map();
          rows.forEach(function (r) { pos.set(r, r.getBoundingClientRect().top); });
          var last = rows[rows.length - 1];
          list.insertBefore(last, list.firstChild);
          rows = $$('.dv-row', list);
          rows.forEach(function (r) {
            if (r === last) { r.animate([{ opacity: 0, transform: 'translateY(-10px)' }, { opacity: 1, transform: 'none' }], { duration: 600, easing: 'cubic-bezier(.16,1,.3,1)' }); return; }
            var dy = pos.get(r) - r.getBoundingClientRect().top;
            if (dy) r.animate([{ transform: 'translateY(' + dy + 'px)' }, { transform: 'none' }], { duration: 600, easing: 'cubic-bezier(.16,1,.3,1)' });
          });
          rows.forEach(function (r) { r.classList.remove('is-new'); }); last.classList.add('is-new');
          if (shipped && /^\d+$/.test(shipped.textContent)) { shipped.textContent = (+shipped.textContent + 1); shipped.classList.add('bump'); setTimeout(function () { shipped.classList.remove('bump'); }, 900); }
        }
        cycle();
      }, 3400);
    };
    if (hasIO) new IntersectionObserver(function (es) { es.forEach(function (e) { off = !e.isIntersecting; }); }).observe(fig);
    if (toggle) toggle.addEventListener('click', function () {
      paused = !paused; toggle.textContent = paused ? 'Play' : 'Pause'; toggle.setAttribute('aria-label', paused ? 'Play animation' : 'Pause animation');
    });
    cycle();
    var hov = matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (hov) {
      var raf = 0, px = 0, py = 0;
      hero.addEventListener('pointermove', function (e) {
        var r = fig.getBoundingClientRect();
        px = clamp((e.clientX - (r.left + r.width / 2)) / r.width, -1, 1); py = clamp((e.clientY - (r.top + r.height / 2)) / r.height, -1, 1);
        if (!raf) raf = requestAnimationFrame(function () { raf = 0; fig.classList.add('is-tracking'); fig.style.setProperty('--ry', (px * 5).toFixed(2) + 'deg'); fig.style.setProperty('--rx', (-py * 4).toFixed(2) + 'deg'); });
      }, { passive: true });
      hero.addEventListener('pointerleave', function () { fig.classList.remove('is-tracking'); fig.style.setProperty('--rx', '0deg'); fig.style.setProperty('--ry', '0deg'); });
    }
    addEventListener('scroll', function () { var y = scrollY; if (y > innerHeight * 1.2) return; fig.style.setProperty('--py', (-y * 0.06).toFixed(1) + 'px'); }, { passive: true });
  });

  /* ------------------------------------------------------------ AI-Native Engineering: nine-stage explorer (tabs on desktop, list on phones) */
  $$('[data-stages]').forEach(function (stx) {
    var tabs = $$('.stx-tab', stx), panels = $$('.stx-panel', stx), rail = $('.stx-rail', stx), cur = 0;
    var mq = matchMedia('(max-width: 900px)');
    var moveRail = function () { var t = tabs[cur]; if (!rail || !t) return; rail.style.setProperty('--ry', t.offsetTop + 'px'); rail.style.setProperty('--rh', t.offsetHeight + 'px'); };
    var show = function (i, focus) {
      cur = (i + tabs.length) % tabs.length;
      tabs.forEach(function (t, j) { var on = j === cur; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); t.tabIndex = on ? 0 : -1; });
      panels.forEach(function (pn, j) { var on = j === cur; pn.classList.toggle('is-on', on); if (!mq.matches) pn.hidden = !on; });
      moveRail();
      if (focus) tabs[cur].focus();
    };
    var mode = function () {
      stx.classList.toggle('is-list', mq.matches);
      panels.forEach(function (pn, j) { pn.hidden = mq.matches ? false : j !== cur; });
      moveRail();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(i); });
      t.addEventListener('keydown', function (e) {
        var k = e.key;
        if (k === 'ArrowDown' || k === 'ArrowRight') { e.preventDefault(); show(cur + 1, true); }
        else if (k === 'ArrowUp' || k === 'ArrowLeft') { e.preventDefault(); show(cur - 1, true); }
        else if (k === 'Home') { e.preventDefault(); show(0, true); }
        else if (k === 'End') { e.preventDefault(); show(tabs.length - 1, true); }
      });
    });
    if (mq.addEventListener) mq.addEventListener('change', mode); else mq.addListener(mode);
    addEventListener('resize', moveRail);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(moveRail);
    mode(); show(0);
  });

  /* ------------------------------------------------------------ About: statement lights up word by word as it scrolls through */
  $$('[data-lit]').forEach(function (el) {
    if (reduce) return;
    var words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(function (w) { return '<span class="lw">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>'; }).join(' ');
    var spans = $$('.lw', el), raf = 0;
    el.classList.add('is-live');
    var upd = function () {
      raf = 0;
      var r = el.getBoundingClientRect(), vh = innerHeight;
      var n = Math.round(clamp((vh * 0.88 - r.top) / (r.height + vh * 0.38), 0, 1) * spans.length);
      spans.forEach(function (s, i) { s.classList.toggle('on', i < n); });
    };
    addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(upd); }, { passive: true });
    addEventListener('resize', upd);
    upd();
  });

  /* ------------------------------------------------------------ About: the conviction nearest the middle of the screen is the one in focus */
  $$('[data-beliefs]').forEach(function (ol) {
    if (reduce || !hasIO) return;
    var items = $$('li', ol);
    var set = function (li) { items.forEach(function (x) { x.classList.toggle('is-cur', x === li); }); };
    ol.classList.add('is-live');
    set(items[0]);
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) set(e.target); }); }, { rootMargin: '-42% 0px -42% 0px' });
    items.forEach(function (li) { io.observe(li); li.addEventListener('mouseenter', function () { set(li); }); });
  });

  /* ------------------------------------------------------------ About: hovering a country (list or map) highlights its route */
  $$('[data-map]').forEach(function (fig) {
    var sec = fig.closest('section');
    var on = function (c) { if (c && c !== 'in') fig.setAttribute('data-hl', c); };
    var off = function () { fig.removeAttribute('data-hl'); };
    $$('.ab-places li[data-c]', sec || document).forEach(function (li) {
      li.addEventListener('mouseenter', function () { on(li.getAttribute('data-c')); });
      li.addEventListener('mouseleave', off);
    });
    $$('.ab-node', fig).forEach(function (g) {
      var c = (g.getAttribute('class').match(/c-(\w+)/) || [])[1];
      g.addEventListener('mouseenter', function () { on(c); });
      g.addEventListener('mouseleave', off);
    });
  });

  /* @block security */
  /* ------------------------------------------------------------ Security: data-path explorer (three setups, text swaps in place) */
  $$('[data-dpath]').forEach(function (fig) {
    var tabs = $$('.dp-tab', fig), swaps = $$('[data-std]', fig), cur = 0;
    var show = function (i, focus) {
      cur = (i + tabs.length) % tabs.length;
      var m = tabs[cur].getAttribute('data-mode');
      tabs.forEach(function (t, j) { var on = j === cur; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); t.tabIndex = on ? 0 : -1; });
      fig.classList.toggle('is-eu', m === 'eu'); fig.classList.toggle('is-prem', m === 'prem');
      swaps.forEach(function (el) {
        var v = el.getAttribute('data-' + m);
        if (v !== null && el.textContent !== v) { el.textContent = v; el.classList.remove('is-swap'); void el.offsetWidth; el.classList.add('is-swap'); }
      });
      if (focus) tabs[cur].focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(i); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); show(cur + 1, true); }
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); show(cur - 1, true); }
      });
    });
  });
  /* @end security */

  /* @block contact */
  /* ------------------------------------------------------------ Contact: message form (FormSubmit, same endpoint and recipients as the old page) */
  $$('[data-contact]').forEach(function (form) {
    var wrap = form.parentNode, done = $('.ct-done', wrap), err = $('.ct-err', form), btn = $('.ct-send', form), bt = $('.ct-send-t', form);
    var val = function (n) { var el = form.elements[n]; return el ? String(el.value || '').trim() : ''; };
    var fail = function () {
      btn.disabled = false; bt.textContent = 'Send message';
      err.innerHTML = 'Something went wrong. Please email us at <a href="mailto:gaurav@upcoretechnologies.com">gaurav@upcoretechnologies.com</a>.';
      err.hidden = false;
    };
    form.addEventListener('input', function (e) { var f = e.target.closest('.ct-f, .ct-topics'); if (f) f.classList.remove('is-bad'); });
    form.addEventListener('change', function (e) { var f = e.target.closest('.ct-topics'); if (f) f.classList.remove('is-bad'); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (val('_honey')) return;
      var bad = [];
      ['name', 'company', 'email'].forEach(function (n) {
        var el = form.elements[n], v = el.value.trim();
        var ok = n === 'email' ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) : !!v;
        el.parentNode.classList.toggle('is-bad', !ok);
        if (!ok) bad.push(el);
      });
      var picked = form.querySelector('input[name="topic"]:checked'), topic = picked ? picked.value : '';
      $('.ct-topics', form).classList.toggle('is-bad', !topic);
      if (!topic) bad.push(form.querySelector('input[name="topic"]'));
      if (bad.length) { err.textContent = 'Please complete the highlighted fields.'; err.hidden = false; bad[0].focus(); return; }
      err.hidden = true; btn.disabled = true; bt.textContent = 'Sending…';
      fetch('https://formsubmit.co/gaurav@upcoretechnologies.com', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          _captcha: 'false', _template: 'table',
          _subject: 'New Contact Form - ' + val('name') + ' · ' + val('company'),
          _cc: 'saswata@upcoretechnologies.com',
          'Name': val('name'), 'Company': val('company'), 'Email': val('email'),
          'Interest': topic, 'Message': val('message'), 'Source': 'Contact Page Form'
        })
      }).then(function (r) {
        if (!r.ok) throw new Error('status ' + r.status);
        return r.json().catch(function () { return {}; });
      }).then(function (j) {
        if (j && (j.success === false || j.success === 'false')) throw new Error(j.message || 'not sent');
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({ event_params: null });
        window.dataLayer.push({ event: 'generate_lead', event_params: { lead_source: 'contact_form', topic: topic } });
        form.hidden = true; done.hidden = false; done.focus();
      }).catch(fail);
    });
  });
  /* @end contact */

  /* @block gov */
  /* ------------------------------------------------------------ Segmented views (AI Governance hero, others): tabs swap panels; bars draw on show */
  $$('[data-seg]').forEach(function (fig) {
    var tabs = $$('.dp-tab', fig), panels = $$('.gv-p, [data-seg-panel]', fig), cur = 0;
    var draw = function (p) { if (!p) return; requestAnimationFrame(function () { requestAnimationFrame(function () { p.classList.add('is-drawn'); }); }); };
    var show = function (i, focus) {
      cur = (i + tabs.length) % tabs.length;
      tabs.forEach(function (t, j) { var on = j === cur; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); t.tabIndex = on ? 0 : -1; });
      panels.forEach(function (p, j) { var on = j === cur; p.hidden = !on; p.classList.toggle('is-on', on); p.classList.remove('is-drawn'); });
      draw(panels[cur]);
      if (focus) tabs[cur].focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(i); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); show(cur + 1, true); }
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); show(cur - 1, true); }
      });
    });
    if (reduce) { panels.forEach(function (p) { p.classList.add('is-drawn'); }); return; }
    onView(fig, function () { draw(panels[cur]); }, { threshold: 0.3 });
  });

  /* ------------------------------------------------------------ AI Governance: five-layer stack (accordion drives the isometric plates) */
  $$('[data-layers]').forEach(function (root) {
    var items = $$('.gv-l', root), plates = $$('.gv-plate', root);
    var set = function (i) {
      items.forEach(function (li, j) {
        var on = j === i, b = $('button', li), p = $('.gv-lp', li);
        li.classList.toggle('is-on', on); b.setAttribute('aria-expanded', on ? 'true' : 'false'); p.hidden = !on;
      });
      plates.forEach(function (g) { g.classList.toggle('is-on', +g.getAttribute('data-i') === i); });
    };
    items.forEach(function (li, i) {
      $('button', li).addEventListener('click', function () { set(li.classList.contains('is-on') ? -1 : i); });
    });
    plates.forEach(function (g) {
      g.addEventListener('click', function () { set(+g.getAttribute('data-i')); });
      g.addEventListener('mouseenter', function () { if (!reduce) g.style.transform = g.classList.contains('is-on') ? '' : 'translateY(-6px)'; });
      g.addEventListener('mouseleave', function () { g.style.transform = ''; });
    });
    set(0);
  });
  /* @end gov */

  /* @block bpa */
  /* ------------------------------------------------------------ Automation: Autonomy Ladder (choose a level; detail swaps from <template>s) */
  $$('[data-ladder]').forEach(function (root) {
    var btns = $$('.bp-lv', root), det = $('.bp-det', root), tpl = $$('template[data-lv]', root), cur = 2;
    var set = function (i, focus, quiet) {
      cur = clamp(i, 0, btns.length - 1);
      btns.forEach(function (b, j) {
        b.classList.toggle('is-on', j === cur); b.classList.toggle('is-below', j < cur);
        b.setAttribute('aria-selected', j === cur ? 'true' : 'false'); b.tabIndex = j === cur ? 0 : -1;
      });
      if (!quiet && tpl[cur]) { det.innerHTML = tpl[cur].innerHTML; det.classList.remove('is-swap'); void det.offsetWidth; det.classList.add('is-swap'); }
      if (focus) btns[cur].focus();
    };
    btns.forEach(function (b, i) {
      b.addEventListener('click', function () { set(i); });
      b.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowUp') { e.preventDefault(); set(cur + 1, true); }
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') { e.preventDefault(); set(cur - 1, true); }
      });
    });
    set(2, false, true);
  });
  /* @end bpa */

  /* @block fao */
  /* ------------------------------------------------------------ Fractional AI Officer: portfolio verdicts stamp in when seen; Replay restarts */
  $$('[data-portfolio]').forEach(function (fig) {
    var btn = $('.fo-toggle', fig);
    var run = function () { fig.classList.remove('is-run'); void fig.offsetWidth; fig.classList.add('is-run'); };
    if (reduce) { if (btn) btn.hidden = true; return; }
    onView(fig, run, { threshold: 0.35 });
    if (btn) btn.addEventListener('click', run);
  });
  /* @end fao */

  /* ------------------------------------------------------------ flowline (hero pipeline) */
  var NS = 'http://www.w3.org/2000/svg', uid = 0;
  function mk(n, a, p) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
  function segs(pts) {
    var out = [];
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      out.push(' C' + (p1[0] + (p2[0] - p0[0]) / 6).toFixed(1) + ' ' + (p1[1] + (p2[1] - p0[1]) / 6).toFixed(1) + ',' +
               (p2[0] - (p3[0] - p1[0]) / 6).toFixed(1) + ' ' + (p2[1] - (p3[1] - p1[1]) / 6).toFixed(1) + ',' + p2[0].toFixed(1) + ' ' + p2[1].toFixed(1));
    }
    return out;
  }

  $$('[data-flowline]').forEach(function (root) {
    var data; try { data = JSON.parse(root.getAttribute('data-flowline')); } catch (e) { return; }
    var stage = $('.fl-stage', root), log = $('.fl-log', root), toggle = $('.fl-toggle', root);
    var id = 'fl' + (uid++), n = data.steps.length, bi = -1;
    data.steps.forEach(function (s, i) { if (s.h && bi < 0) bi = i; });
    var svg, main, branch = null, nodes = [], nodeLen = [], total = 0, bLen = 0, W = 0, vertical = false;
    var tks = [], paused = false, off = false, started = false, last = 0, nextLaunch = 0, k = 0;

    function build() {
      W = stage.clientWidth || root.clientWidth; vertical = W < 760;
      if (svg) svg.remove();
      nodes = []; nodeLen = []; tks = [];
      var pts = [], H, np = [];
      if (!vertical) {
        H = 300; var yc = 128, x0 = Math.max(60, W * 0.075), x1 = W - x0;
        pts.push([-40, yc]);
        for (var i = 0; i < n; i++) { var x = x0 + (x1 - x0) * i / (n - 1), y = yc + (i % 2 ? 24 : -24); np.push([x, y]); pts.push([x, y]); }
        pts.push([W + 40, yc]);
      } else {
        var rowH = 70; H = 36 + rowH * (n - 1) + 56; var xc = 30;
        pts.push([xc, -20]);
        for (var j = 0; j < n; j++) { var yy = 30 + rowH * j, xx = xc + (j % 2 ? 7 : -7); np.push([xx, yy]); pts.push([xx, yy]); }
        pts.push([xc, H + 20]);
      }
      svg = mk('svg', { 'class': 'fl-svg', viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, 'aria-hidden': 'true', focusable: 'false' });
      var defs = mk('defs', {}, svg);
      var lg = mk('linearGradient', { id: id + 'g', x1: '0', y1: '0', x2: vertical ? '0' : '1', y2: vertical ? '1' : '0' }, defs);
      [[0, 0], [0.12, 0.95], [0.88, 0.95], [1, 0]].forEach(function (s) { mk('stop', { offset: s[0], 'stop-color': '#21D2ED', 'stop-opacity': s[1] }, lg); });
      var S = segs(pts), d = 'M' + pts[0][0] + ' ' + pts[0][1] + S.join('');
      var base = mk('path', { d: d, 'class': 'fl-base fl-draw' }, svg);
      main = mk('path', { d: d, 'class': 'fl-run', stroke: 'url(#' + id + 'g)' }, svg);
      total = main.getTotalLength();
      for (var a = 0; a < n; a++) {
        var tmp = mk('path', { d: 'M' + pts[0][0] + ' ' + pts[0][1] + S.slice(0, a + 1).join('') }, svg);
        nodeLen.push(tmp.getTotalLength()); tmp.remove();
      }
      var bl = base.getTotalLength();
      base.style.strokeDasharray = bl; base.style.strokeDashoffset = reduce ? 0 : bl;
      // branch to "held" lane (horizontal layout only)
      if (bi >= 0 && !vertical) {
        var bx = np[bi][0], by = np[bi][1], ly = H - 28, ex = Math.min(W - 24, bx + Math.max(260, W * 0.3));
        var bd = 'M' + bx + ' ' + by + ' C' + bx + ' ' + (by + 70) + ',' + (bx + 30) + ' ' + ly + ',' + (bx + 110) + ' ' + ly + ' L' + ex + ' ' + ly;
        branch = mk('path', { d: bd, 'class': 'fl-branch' }, svg);
        bLen = branch.getTotalLength();
        mk('circle', { cx: ex, cy: ly, r: 4, 'class': 'fl-enddot' }, svg);
        var et = mk('text', { x: ex - 12, y: ly - 10, 'text-anchor': 'end', 'class': 'fl-end' }, svg); et.textContent = data.branchLabel;
      } else branch = null;
      // nodes + labels
      np.forEach(function (p, i) {
        var s = data.steps[i], up = !vertical && i % 2 === 0;
        var g = mk('g', { 'class': 'fl-node' + (s.h ? ' h' : ''), transform: 'translate(' + p[0] + ' ' + p[1] + ')', style: '--i:' + i }, svg);
        mk('circle', { r: 6.5, 'class': 'fl-ring' }, g);
        mk('circle', { r: 6.5, 'class': 'fl-dot' }, g);
        var t, e;
        if (vertical) {
          t = mk('text', { x: 26, y: -1, 'class': 'fl-t' }, g);
          e = mk('text', { x: 26, y: 15, 'class': 'fl-e' }, g);
        } else if (up) {
          t = mk('text', { x: 0, y: -34, 'text-anchor': 'middle', 'class': 'fl-t' }, g);
          e = mk('text', { x: 0, y: -19, 'text-anchor': 'middle', 'class': 'fl-e' }, g);
        } else {
          t = mk('text', { x: 0, y: 30, 'text-anchor': 'middle', 'class': 'fl-t' }, g);
          e = mk('text', { x: 0, y: 45, 'text-anchor': 'middle', 'class': 'fl-e' }, g);
        }
        t.textContent = s.t; e.textContent = s.e + (s.h ? ' · a person decides' : '');
        nodes.push(g);
      });
      stage.appendChild(svg);
      root.classList.add('is-ready');
      if (reduce) { root.classList.add('is-drawn'); return; }
      if (started) { base.style.strokeDashoffset = 0; root.classList.add('is-drawn'); }
    }

    function hit(i, cls) {
      var g = nodes[i]; if (!g) return;
      g.classList.remove('hit'); void g.getBBox(); g.classList.add(cls || 'hit');
      setTimeout(function () { g.classList.remove(cls || 'hit'); }, cls === 'warn' ? 900 : 700);
    }
    function addLog(t) {
      if (!log) return;
      $$('li', log).forEach(function (li) { li.classList.add('is-old'); });
      var li = document.createElement('li'); li.className = 'is-new r-' + t.risk;
      var c = document.createElement('code'); c.textContent = t.id;
      var sp = document.createElement('span'); sp.textContent = t.title;
      var em = document.createElement('em'); em.textContent = t.out;
      li.appendChild(c); li.appendChild(sp); li.appendChild(em);
      log.insertBefore(li, log.firstChild);
      var all = $$('li', log); while (all.length > 3) { all.pop().remove(); }
    }
    function launch() {
      var t = data.tickets[k++ % data.tickets.length];
      var g = mk('g', { 'class': 'fl-tk' + (t.risk === 'hi' ? ' hi' : '') }, svg);
      mk('circle', { r: 11, 'class': 'halo' }, g); mk('circle', { r: 4.5, 'class': 'core' }, g);
      if (!vertical) { var tx = mk('text', { x: 15, y: 4 }, g); tx.textContent = t.id; }
      tks.push({ t: t, g: g, s: 0, next: 0, wait: 0, onBranch: false, done: false });
    }
    function place(tk) {
      var p = (tk.onBranch ? branch : main).getPointAtLength(tk.s);
      tk.g.setAttribute('transform', 'translate(' + p.x.toFixed(1) + ' ' + p.y.toFixed(1) + ')');
    }
    function tickFrame(now) {
      requestAnimationFrame(tickFrame);
      if (paused || off || document.hidden || !svg) { last = now; return; }
      var dt = Math.min(64, now - (last || now)); last = now;
      var speed = (vertical ? 70 : 125) * clamp(W / 1200, 0.75, 1.15) / 1000;
      if (now >= nextLaunch && tks.filter(function (x) { return !x.done; }).length < 3) { launch(); nextLaunch = now + 2900; }
      tks.forEach(function (tk) {
        if (tk.done) return;
        if (tk.wait > 0) { tk.wait -= dt; return; }
        if (tk.onBranch) {
          tk.s = Math.min(bLen, tk.s + speed * dt); place(tk);
          if (tk.s >= bLen) { tk.done = true; addLog(tk.t); tk.g.classList.add('out'); setTimeout(function () { tk.g.remove(); }, 600); }
          return;
        }
        var target = tk.next < n ? nodeLen[tk.next] : total;
        tk.s = Math.min(target, tk.s + speed * dt); place(tk);
        if (tk.s >= target) {
          if (tk.next >= n) { tk.done = true; addLog(tk.t); tk.g.classList.add('out'); setTimeout(function () { tk.g.remove(); }, 600); return; }
          var i = tk.next, s = data.steps[i];
          var warn = tk.t.risk === 'md' && i === 1;
          hit(i, warn ? 'warn' : 'hit');
          tk.wait = s.h ? 1250 : (warn ? 950 : 380);
          tk.next++;
          if (tk.t.branch && i === bi) {
            if (branch) { tk.onBranch = true; tk.s = 0; tk.wait = 1400; }
            else { tk.wait = 1500; tk.next = n + 1; setTimeout(function () { tk.done = true; addLog(tk.t); tk.g.classList.add('out'); setTimeout(function () { tk.g.remove(); }, 600); }, 1500); }
          }
        }
      });
      tks = tks.filter(function (x) { return !x.done || x.g.isConnected; });
    }

    build();
    if (reduce) { if (toggle) toggle.hidden = true; return; }
    $$('li', log).forEach(function (li) { li.classList.add('is-old'); });
    onView(root, function () {
      started = true;
      var base = $('.fl-base', root); if (base) base.style.strokeDashoffset = 0;
      root.classList.add('is-drawn');
      nextLaunch = performance.now() + 900;
      requestAnimationFrame(tickFrame);
    }, { threshold: 0.25 });
    if (hasIO) new IntersectionObserver(function (es) { es.forEach(function (e) { off = !e.isIntersecting; root.classList.toggle('is-off', off); }); }).observe(root);
    if (toggle) toggle.addEventListener('click', function () {
      paused = !paused; root.classList.toggle('is-paused', paused);
      toggle.textContent = paused ? 'Play' : 'Pause'; toggle.setAttribute('aria-label', paused ? 'Play animation' : 'Pause animation');
    });
    var lw = W, rt;
    addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () { var w = stage.clientWidth; if (Math.abs(w - lw) > 24) { lw = w; $$('.fl-tk', svg).forEach(function (g) { g.remove(); }); build(); } }, 200);
    });
  });
})();
