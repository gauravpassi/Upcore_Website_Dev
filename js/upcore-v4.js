/* Upcore V4.1 motion + interaction layer. Vanilla JS, no dependencies.
   Principles: transform/opacity only, pause when off-screen or hidden, settle instead of
   looping forever, user can pause long loops (WCAG 2.2.2), full static fallback for
   reduced motion. */
(function () {
  'use strict';
  window.__v4 = true;
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hover = window.matchMedia('(hover:hover)').matches;
  var hasIO = 'IntersectionObserver' in window;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var onView = function (el, fn, opts) {
    if (!hasIO) { fn(); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { fn(); io.disconnect(); } }); }, opts || { threshold: 0.25 });
    io.observe(el);
  };
  var visible = function (el) { return !el.classList.contains('is-off') && !document.hidden; };

  /* ---------------- Fonts ready: hero words animate in the real font ---------------- */
  var fontsGo = function () { doc.classList.add('fonts-ready'); };
  if (reduce || !document.fonts) fontsGo();
  else Promise.race([document.fonts.ready, new Promise(function (r) { setTimeout(r, 700); })]).then(fontsGo);

  /* ---------------- Off-screen pause for every animated region ---------------- */
  if (hasIO) {
    var offIO = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('is-off', !e.isIntersecting); }); });
    $$('.band, .hero, .fw, .fw-single, .flow, .run').forEach(function (el) { offIO.observe(el); });
  }

  /* ---------------- Scroll: nav state, progress, sticky mobile CTA ---------------- */
  var nav = $('.nav'), mcta = $('.mcta'), prog = $('.progress');
  var endZone = false, ticking = false, scrollFns = [];
  var onScroll = function () {
    var y = window.scrollY, h = doc.scrollHeight - window.innerHeight;
    if (nav) nav.classList.toggle('is-scrolled', y > 8);
    if (mcta) mcta.classList.toggle('show', y > window.innerHeight * 0.8 && !endZone && !(nav && nav.classList.contains('menu-open')));
    if (prog) prog.style.transform = 'scaleX(' + (h > 0 ? (y / h).toFixed(4) : 0) + ')';
    scrollFns.forEach(function (f) { f(); });
    ticking = false;
  };
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  if (hasIO && mcta) {
    var ends = $$('.cta-band, .foot');
    var endIO = new IntersectionObserver(function () {
      endZone = ends.some(function (el) { var r = el.getBoundingClientRect(); return r.top < window.innerHeight && r.bottom > 0; });
      onScroll();
    });
    ends.forEach(function (el) { endIO.observe(el); });
  }

  /* ---------------- Nav: disclosure dropdowns + mobile menu ---------------- */
  var items = $$('.nav-menu > li');
  var closeAll = function (except) {
    items.forEach(function (li) { if (li === except) return; li.classList.remove('open'); var b = li.querySelector('button'); if (b) b.setAttribute('aria-expanded', 'false'); });
  };
  items.forEach(function (li) {
    var btn = li.querySelector('button');
    if (!btn) return;
    var t = 0;
    var open = function (v) { li.classList.toggle('open', v); btn.setAttribute('aria-expanded', v ? 'true' : 'false'); if (v) closeAll(li); };
    btn.addEventListener('click', function (e) { e.stopPropagation(); open(!li.classList.contains('open')); });
    if (hover) {
      li.addEventListener('mouseenter', function () { if (window.innerWidth > 1100) { clearTimeout(t); open(true); } });
      li.addEventListener('mouseleave', function () { if (window.innerWidth > 1100) { t = setTimeout(function () { open(false); }, 140); } });
    }
    li.addEventListener('keydown', function (e) { if (e.key === 'Escape') { open(false); btn.focus(); } });
    li.addEventListener('focusout', function (e) { if (!li.contains(e.relatedTarget) && window.innerWidth > 1100) open(false); });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.nav-menu')) closeAll(); });
  var burger = $('.nav-burger');
  var setMenu = function (v) {
    if (!nav) return;
    nav.style.setProperty('--navb', nav.getBoundingClientRect().bottom + 'px');
    nav.classList.toggle('menu-open', v);
    if (burger) { burger.setAttribute('aria-expanded', v ? 'true' : 'false'); burger.setAttribute('aria-label', v ? 'Close menu' : 'Open menu'); }
    document.body.style.overflow = v ? 'hidden' : '';
    onScroll();
  };
  if (burger) burger.addEventListener('click', function () { setMenu(!nav.classList.contains('menu-open')); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav && nav.classList.contains('menu-open')) { setMenu(false); burger.focus(); } });
  $$('.nav-menu a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  /* ---------------- Headline word split ---------------- */
  $$('[data-split]').forEach(function (h) {
    var i = 0;
    h.setAttribute('aria-label', h.textContent.replace(/\s+/g, ' ').trim());
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            var w = document.createElement('span'); w.className = 'w'; w.setAttribute('aria-hidden', 'true');
            var s = document.createElement('span'); s.textContent = part; s.style.setProperty('--i', i++);
            w.appendChild(s); frag.appendChild(w);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1) walk(n);
      });
    };
    walk(h);
    h.classList.add('is-split');
  });

  /* ---------------- Reveal on view ---------------- */
  var revealTargets = $$('[data-reveal], .ul-draw');
  if (reduce || !hasIO) revealTargets.forEach(function (el) { el.classList.add('is-in'); });
  else {
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); rio.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealTargets.forEach(function (el) { rio.observe(el); });
  }

  /* ---------------- Spotlight (transform, rAF-throttled) + magnetic buttons ---------------- */
  if (!reduce && hover) {
    $$('.band').forEach(function (b) {
      var spot = b.querySelector('.spot');
      if (!spot) return;
      var raf = 0, lx = 0, ly = 0;
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect(); lx = e.clientX - r.left; ly = e.clientY - r.top;
        if (!raf) raf = requestAnimationFrame(function () { raf = 0; spot.style.transform = 'translate3d(' + lx + 'px,' + ly + 'px,0)'; });
      }, { passive: true });
    });
    $$('[data-magnetic]').forEach(function (btn) {
      btn.addEventListener('pointermove', function (e) {
        var r = btn.getBoundingClientRect();
        btn.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.14) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.22) + 'px)';
      });
      btn.addEventListener('pointerleave', function () { btn.style.transform = ''; });
    });
  }

  /* ---------------- Workflow panels ([data-flow]) ----------------
     Generic: steps tick through, status settles, result shows, graceful rewind.
     data-flow="handoff" (home hero): cycles three tickets with different outcomes and
     writes each decision into the deviation log beside it. */
  var wait = function (el, ms) {
    return new Promise(function (res) {
      var left = ms, last = performance.now();
      (function tick(now) {
        if (el._paused || !visible(el)) { last = now; return requestAnimationFrame(tick); }
        left -= now - last; last = now;
        if (left <= 0) res(); else requestAnimationFrame(tick);
      })(last);
    });
  };
  var TICKETS = [
    { id: 'PAY-418', title: 'Add partial refunds to checkout', branch: 'main &larr; feat/refunds', hold: -1, status: 'Released', out: ['Logged', 'Low risk &middot; auto-merged and released behind a flag'],
      row: ['PAY-418', 'Partial refunds within the payments API conventions', 'lo', 'Low', 'Gates passed &middot; auto-merged'] },
    { id: 'ORD-190', title: 'Add delivery-window field to orders', branch: 'main &larr; feat/windows', hold: -1, status: 'Released', out: ['Logged', 'Medium risk &middot; spec amended, then approved'],
      row: ['ORD-190', 'Migration changes a column the schema record marks required', 'md', 'Med', 'Spec amended &middot; approved'] },
    { id: 'AUTH-77', title: 'Refactor session handling', branch: 'main &larr; chore/sessions', hold: 2, status: 'Held &middot; architect review', out: ['Held', 'High risk &middot; stopped at plan sign-off for an architect'],
      row: ['AUTH-77', 'Plan touches a shared auth module outside the spec&rsquo;s scope', 'hi', 'High', 'Held for architect review'] },
  ];
  var insertRow = function (log, r) {
    if (!log) return;
    var rows = $('.dlog-rows', log); if (!rows) return;
    var old = $$('.dlog-row', rows), first = old.map(function (n) { return n.getBoundingClientRect().top; });
    var el = document.createElement('div'); el.className = 'dlog-row is-new';
    el.innerHTML = '<code>' + r[0] + '</code><p>' + r[1] + '</p><div class="dec"><span class="risk ' + r[2] + '">' + r[3] + '</span>' + r[4] + '</div>';
    rows.insertBefore(el, rows.firstChild);
    if (old.length >= 4) old[old.length - 1].remove();
    if (reduce || !el.animate) return;
    $$('.dlog-row', rows).slice(1).forEach(function (n, i) {
      var d = first[i] - n.getBoundingClientRect().top;
      if (d) n.animate([{ transform: 'translateY(' + d + 'px)' }, { transform: 'none' }], { duration: 600, easing: 'cubic-bezier(.65,0,.35,1)' });
    });
    el.animate([{ opacity: 0, transform: 'translateY(-12px)' }, { opacity: 1, transform: 'none' }], { duration: 600, easing: 'cubic-bezier(.16,1,.3,1)' });
    setTimeout(function () { el.classList.remove('is-new'); }, 1800);
  };
  $$('[data-flow]').forEach(function (f) {
    var steps = $$('.step', f), out = $('.flow-out', f), live = $('.live', f), toggle = $('.run-toggle', f);
    var handoff = f.getAttribute('data-flow') === 'handoff', log = handoff ? $('.dlog', f.parentNode) : null;
    var outB = out && $('b', out), outS = out && $('span', out), outDefault = out ? [outB.innerHTML, outS.innerHTML] : null;
    var setLive = function (txt, cls) { if (!live) return; live.innerHTML = txt; live.classList.remove('is-done', 'is-held'); if (cls) live.classList.add(cls); };
    var clear = function () { steps.forEach(function (s) { s.classList.remove('is-run', 'done', 'held'); }); if (out) out.classList.remove('show'); };
    if (reduce || !hasIO) { steps.forEach(function (s) { s.classList.add('done'); }); if (out) out.classList.add('show'); setLive('Released', 'is-done'); if (toggle) toggle.hidden = true; return; }
    if (toggle) toggle.addEventListener('click', function () {
      f._paused = !f._paused;
      toggle.textContent = f._paused ? 'Play' : 'Pause';
      toggle.setAttribute('aria-label', f._paused ? 'Play animation' : 'Pause animation');
      f.classList.toggle('is-paused', f._paused);
    });
    var k = 0;
    var cycle = async function () {
      var t = handoff ? TICKETS[k % TICKETS.length] : null;
      if (t) {
        var pr = $('.run-pr', f);
        if (pr) { $('code', pr).textContent = t.id; $('b', pr).textContent = t.title; $('span', pr).innerHTML = t.branch; }
        if (out) { outB.innerHTML = 'Pending'; outS.innerHTML = 'Writing decision record&hellip;'; }
      }
      setLive('Running');
      for (var i = 0; i < steps.length; i++) {
        var s = steps[i];
        s.classList.add('is-run');
        await wait(f, s.classList.contains('human') ? 1100 : 560);
        s.classList.remove('is-run');
        if (t && t.hold === i) { s.classList.add('held'); break; }
        s.classList.add('done');
      }
      if (t) { outB.innerHTML = t.out[0]; outS.innerHTML = t.out[1]; setLive(t.status, t.hold >= 0 ? 'is-held' : 'is-done'); }
      else { if (outDefault) { outB.innerHTML = outDefault[0]; outS.innerHTML = outDefault[1]; } setLive('Complete', 'is-done'); }
      if (out) out.classList.add('show');
      if (t) { await wait(f, 500); insertRow(log, t.row); }
      await wait(f, 3800);
      var st = $('.steps', f);
      if (st && st.animate) st.animate([{ opacity: 1 }, { opacity: 0.25 }, { opacity: 1 }], { duration: 700, easing: 'cubic-bezier(.65,0,.35,1)' });
      await wait(f, 350);
      clear(); k++;
      await wait(f, 400);
      cycle();
    };
    onView(f, function () { setTimeout(cycle, handoff ? 900 : 300); }, { threshold: 0.3 });
  });

  /* ---------------- Pipeline rail: fill, numbered stages, governed packet ---------------- */
  $$('[data-pipe]').forEach(function (pl) {
    var st = $$('.pipe-stage', pl), tops = [], H = 0, humans = [], cur = 0, target = 0, raf = 0;
    var packet = null;
    if (!reduce) { packet = document.createElement('span'); packet.className = 'pipe-packet'; packet.setAttribute('aria-hidden', 'true'); pl.appendChild(packet); }
    var measure = function () {
      var base = pl.getBoundingClientRect().top + window.scrollY;
      tops = st.map(function (s) { return s.getBoundingClientRect().top + window.scrollY - base; });
      H = pl.offsetHeight - 24;
      humans = st.map(function (s, i) { return s.classList.contains('is-human') ? tops[i] : -1; }).filter(function (v) { return v >= 0; });
    };
    var paint = function (y) {
      var p = H > 0 ? Math.max(0, Math.min(1, y / H)) : 1;
      pl.style.setProperty('--pp', p.toFixed(4));
      var lastOn = -1, waiting = -1;
      st.forEach(function (s, i) { var on = reduce || y >= tops[i] - 4; s.classList.toggle('on', on); if (on) lastOn = i; });
      st.forEach(function (s, i) {
        var isWait = !reduce && s.classList.contains('is-human') && Math.abs(y - tops[i]) < 6;
        s.classList.toggle('is-waiting', isWait); if (isWait) waiting = i;
        s.classList.toggle('head', i === lastOn);
      });
      if (packet) { packet.style.setProperty('--py', y.toFixed(1) + 'px'); packet.classList.toggle('wait', waiting >= 0); }
    };
    var compute = function () {
      var r = pl.getBoundingClientRect();
      var s = Math.max(0, Math.min(H, window.innerHeight * 0.55 - r.top - 12));
      var y = s;
      humans.forEach(function (h) { if (y > h) y = Math.max(h, y - 70); });
      target = Math.min(y, H);
      if (reduce) { paint(H); return; }
      if (!raf) raf = requestAnimationFrame(function step() {
        cur += (target - cur) * 0.16;
        if (Math.abs(target - cur) < 0.3) cur = target;
        paint(cur);
        raf = cur === target ? 0 : requestAnimationFrame(step);
      });
    };
    measure(); compute();
    window.addEventListener('resize', function () { measure(); compute(); });
    window.addEventListener('load', function () { measure(); compute(); });
    scrollFns.push(compute);
  });

  /* ---------------- FAQ: native animation where supported, guarded JS fallback ---------------- */
  var nativeDetails = window.CSS && CSS.supports && CSS.supports('interpolate-size', 'allow-keywords');
  if (!reduce && !nativeDetails) $$('.faq details').forEach(function (d) {
    var s = d.querySelector('summary'), a = d.querySelector('.ans');
    s.addEventListener('click', function (e) {
      e.preventDefault();
      if (a._busy) return; a._busy = true;
      var done = function () { a._busy = false; };
      if (d.open) {
        var an = a.animate([{ height: a.offsetHeight + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 260, easing: 'cubic-bezier(.4,0,1,1)' });
        an.onfinish = function () { d.open = false; done(); };
      } else {
        d.open = true;
        a.animate([{ height: '0px', opacity: 0 }, { height: a.offsetHeight + 'px', opacity: 1 }], { duration: 360, easing: 'cubic-bezier(.16,1,.3,1)' }).onfinish = done;
      }
    });
  });

  /* ---------------- Generic tabs (segment pages) + chip deep links ---------------- */
  $$('[role="tablist"]:not(.fw-tabs)').forEach(function (list) {
    var tabs = $$('[role="tab"]', list);
    var select = function (t, focus) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1;
        var p = document.getElementById(x.getAttribute('aria-controls')); if (p) p.classList.toggle('on', on);
      });
      if (focus) t.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') select(tabs[(i + 1) % tabs.length], true);
        if (e.key === 'ArrowLeft') select(tabs[(i - 1 + tabs.length) % tabs.length], true);
      });
    });
    $$('a[data-tab]').forEach(function (a) {
      a.addEventListener('click', function () { var t = document.getElementById('t-' + a.getAttribute('data-tab')); if (t) select(t); });
    });
    var hash = (location.hash || '').replace('#', '');
    if (hash) { var ht = document.getElementById('t-' + hash); if (ht) select(ht); }
  });

  /* ---------------- Frameworks ---------------- */
  var ladder = function (ld, panel) {
    var cols = $$('.ld-col', ld), fill = $('.ld-meter .fill', panel), next = $('.ld-meter .next', panel);
    if (ld._t) cancelAnimationFrame(ld._t);
    var lvl = 2, ev = 0, last = performance.now();
    var paint = function () {
      cols.forEach(function (c, i) { c.classList.toggle('cur', i === lvl); c.classList.toggle('done', i < lvl); });
      if (fill) fill.style.setProperty('--ev', (ev / 100).toFixed(3));
      if (next) next.textContent = lvl < 4 ? 'earns L' + (lvl + 1) : 'sampled audit';
    };
    if (reduce) { ev = 100; paint(); return; }
    paint();
    var host = panel.closest('.fw, .fw-single') || panel;
    (function tick(now) {
      var dt = now - last; last = now;
      if (panel.classList.contains('play') && visible(host)) {
        ev += dt * 0.027;
        if (ev >= 100) { ev = 0; lvl = lvl >= 4 ? 2 : lvl + 1; }
        paint();
      }
      ld._t = requestAnimationFrame(tick);
    })(last);
  };
  var replay = function (panel) {
    panel.classList.remove('play');
    void panel.offsetWidth;
    requestAnimationFrame(function () { panel.classList.add('play'); });
    var ld = $('.ld', panel);
    if (ld) ladder(ld, panel);
  };
  $$('[data-fw]').forEach(function (fw) {
    var tabs = $$('.fw-tab', fw), panels = $$('.fw-panel', fw), idx = 0, timer = null, manual = !!reduce || !hover, inView = false, DUR = 10000;
    var list = $('.fw-tabs', fw);
    fw.style.setProperty('--fw-dur', DUR / 1000 + 's');
    if (manual) fw.classList.add('manual');
    var schedule = function () { clearTimeout(timer); if (manual || !inView) return; timer = setTimeout(function () { select((idx + 1) % panels.length); }, DUR); };
    var select = function (i, focus) {
      idx = i;
      tabs.forEach(function (t, j) { t.setAttribute('aria-selected', j === i ? 'true' : 'false'); t.tabIndex = j === i ? 0 : -1; });
      panels.forEach(function (p, j) { p.classList.toggle('on', j === i); p.setAttribute('aria-hidden', j === i ? 'false' : 'true'); if (j !== i) p.classList.remove('play'); });
      replay(panels[i]);
      if (focus) tabs[i].focus();
      if (list && list.scrollWidth > list.clientWidth) list.scrollTo({ left: tabs[i].offsetLeft - 16, behavior: reduce ? 'auto' : 'smooth' });
      schedule();
    };
    var takeOver = function () { manual = true; fw.classList.add('manual'); clearTimeout(timer); };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { takeOver(); select(i); });
      t.addEventListener('keydown', function (e) {
        var k = e.key;
        if (k === 'ArrowDown' || k === 'ArrowRight') { e.preventDefault(); takeOver(); select((i + 1) % tabs.length, true); }
        if (k === 'ArrowUp' || k === 'ArrowLeft') { e.preventDefault(); takeOver(); select((i - 1 + tabs.length) % tabs.length, true); }
      });
    });
    fw.addEventListener('focusin', takeOver);
    fw.addEventListener('pointerenter', function () { if (!manual) { clearTimeout(timer); fw.classList.add('paused'); } });
    fw.addEventListener('pointerleave', function () { if (!manual) { fw.classList.remove('paused'); schedule(); } });
    panels.forEach(function (p, j) { p.setAttribute('aria-hidden', j === 0 ? 'false' : 'true'); });
    if (hasIO) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          var was = inView; inView = e.isIntersecting;
          if (inView && !was) { if (!panels[idx].classList.contains('play')) replay(panels[idx]); schedule(); }
          if (!inView) clearTimeout(timer);
        });
      }, { threshold: 0.25 }).observe(fw);
    } else { inView = true; replay(panels[0]); }
  });
  $$('.fw-single').forEach(function (s) { var p = $('.fw-panel', s); onView(s, function () { replay(p); }, { threshold: 0.3 }); });

  onScroll();
})();
