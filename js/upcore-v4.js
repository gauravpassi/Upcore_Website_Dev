/* Upcore V4.1 motion + interaction layer. Vanilla JS, no dependencies.
   Every effect degrades to a static, fully readable page when the visitor
   prefers reduced motion or JS fails. */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hover = window.matchMedia('(hover:hover)').matches;
  var hasIO = 'IntersectionObserver' in window;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var onView = function (el, fn, opts) {
    if (!hasIO) { fn(); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { fn(); io.disconnect(); } });
    }, opts || { threshold: 0.25 });
    io.observe(el);
  };

  /* ---------------- Scroll: nav state, progress bar, mobile CTA ---------------- */
  var nav = $('.nav'), mcta = $('.mcta'), prog = $('.progress');
  var onScroll = function () {
    var y = window.scrollY, h = doc.scrollHeight - window.innerHeight;
    if (nav) nav.classList.toggle('is-scrolled', y > 8);
    if (mcta) mcta.classList.toggle('show', y > window.innerHeight * 0.8);
    if (prog) prog.style.setProperty('--p', h > 0 ? (y / h).toFixed(4) : 0);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------- Nav dropdowns + mobile menu ---------------- */
  $$('.nav-menu > li').forEach(function (li) {
    var btn = li.querySelector('button');
    if (!btn) return;
    var open = function (v) { li.classList.toggle('open', v); btn.setAttribute('aria-expanded', v ? 'true' : 'false'); };
    btn.addEventListener('click', function (e) { e.stopPropagation(); open(!li.classList.contains('open')); });
    if (hover) {
      li.addEventListener('mouseenter', function () { if (window.innerWidth > 1100) open(true); });
      li.addEventListener('mouseleave', function () { if (window.innerWidth > 1100) open(false); });
    }
    li.addEventListener('keydown', function (e) { if (e.key === 'Escape') { open(false); btn.focus(); } });
    li.addEventListener('focusout', function (e) { if (!li.contains(e.relatedTarget) && window.innerWidth > 1100) open(false); });
  });
  document.addEventListener('click', function () { $$('.nav-menu > li.open').forEach(function (li) { li.classList.remove('open'); }); });
  var burger = $('.nav-burger');
  if (burger) burger.addEventListener('click', function () {
    var v = !nav.classList.contains('menu-open');
    nav.style.setProperty('--navb', nav.getBoundingClientRect().bottom + 'px');
    nav.classList.toggle('menu-open', v);
    burger.setAttribute('aria-expanded', v ? 'true' : 'false');
    document.body.style.overflow = v ? 'hidden' : '';
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav && nav.classList.contains('menu-open')) { nav.classList.remove('menu-open'); document.body.style.overflow = ''; if (burger) { burger.setAttribute('aria-expanded', 'false'); burger.focus(); } }
  });
  $$('.nav-menu a').forEach(function (a) { a.addEventListener('click', function () { if (nav) nav.classList.remove('menu-open'); document.body.style.overflow = ''; }); });

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
  });

  /* ---------------- Reveal on view ---------------- */
  var revealTargets = $$('[data-reveal], .hero, .ul-draw, .media-card, .console');
  if (reduce || !hasIO) revealTargets.forEach(function (el) { el.classList.add('is-in'); });
  else {
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); rio.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealTargets.forEach(function (el) { rio.observe(el); });
  }

  /* ---------------- Count-up numbers ---------------- */
  var fmt = function (n, d) { return n.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); };
  $$('[data-count]').forEach(function (el) {
    var to = parseFloat(el.getAttribute('data-count')), dec = parseInt(el.getAttribute('data-dec') || '0', 10);
    if (reduce) return;
    el.textContent = fmt(0, dec);
    onView(el, function () {
      var t0 = null;
      var tick = function (t) {
        if (!t0) t0 = t;
        var p = Math.min(1, (t - t0) / 1500), e = 1 - Math.pow(1 - p, 4);
        el.textContent = fmt(to * e, dec);
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }, { threshold: 0.6 });
  });

  /* ---------------- Spotlight, magnetic buttons, tilt ---------------- */
  if (!reduce && hover) {
    $$('.band').forEach(function (b) {
      var spot = b.querySelector('.spot');
      if (!spot) return;
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        spot.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        spot.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
    $$('[data-magnetic]').forEach(function (btn) {
      btn.addEventListener('pointermove', function (e) {
        var r = btn.getBoundingClientRect();
        btn.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.16) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.26) + 'px)';
      });
      btn.addEventListener('pointerleave', function () { btn.style.transform = ''; });
    });
    $$('[data-tilt]').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(1400px) rotateY(' + (x * 4) + 'deg) rotateX(' + (-y * 4) + 'deg)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------------- Agent console: scripted workflow loop ---------------- */
  var con = $('[data-console]');
  if (con) {
    var chat = $('.chat-msgs', con), cSteps = $$('.step', con), counter = $('[data-console-count]', con);
    var base = 0, script = JSON.parse($('script[type="application/json"]', con).textContent), timers = [];
    var later = function (fn, ms) { timers.push(setTimeout(fn, ms)); };
    var addMsg = function (m) {
      var d = document.createElement('div');
      d.className = 'msg ' + m.side;
      d.innerHTML = m.html + (m.meta ? '<small>' + m.meta + '</small>' : '');
      chat.appendChild(d);
      requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('show'); }); });
      while (chat.children.length > 4) chat.removeChild(chat.firstChild);
    };
    var typing = function (on) {
      var t = $('.typing', chat);
      if (on && !t) { t = document.createElement('div'); t.className = 'msg in show typing'; t.innerHTML = '<i></i><i></i><i></i>'; chat.appendChild(t); }
      if (!on && t) t.remove();
    };
    var run = function (k) {
      chat.innerHTML = '';
      cSteps.forEach(function (s) { s.classList.remove('run', 'done'); });
      var conv = script[k % script.length], t = 300;
      addMsg(conv.q); t += 700;
      cSteps.forEach(function (s, i) {
        later(function () { if (i === 0) typing(true); s.classList.add('run'); }, t); t += 620;
        later(function () { s.classList.remove('run'); s.classList.add('done'); }, t);
      });
      later(function () { typing(false); addMsg(conv.a); if (counter) counter.textContent = String(++base); }, t + 250);
      later(function () { run(k + 1); }, t + 3600);
    };
    if (reduce) { addMsg(script[0].q); addMsg(script[0].a); cSteps.forEach(function (s) { s.classList.add('done'); }); }
    else onView(con, function () { run(0); }, { threshold: 0.3 });
  }

  /* ---------------- System story (sticky diagram) ---------------- */
  var sys = $('[data-sys]');
  if (sys) {
    var panels = $$('.sys-panel', sys), sNodes = $$('.sys-node', sys), spokes = $$('.spoke', sys), pm = $('.pulse-motion', sys);
    var setActive = function (i) {
      panels.forEach(function (p, j) { p.classList.toggle('on', j === i); });
      sNodes.forEach(function (n, j) { n.classList.toggle('on', j === i); });
      spokes.forEach(function (s, j) { s.classList.toggle('on', j === i); });
      if (pm && spokes[i]) pm.setAttribute('path', spokes[i].getAttribute('d'));
    };
    setActive(0);
    if (hasIO) {
      var pio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) setActive(panels.indexOf(e.target)); }); }, { rootMargin: '-45% 0px -45% 0px' });
      panels.forEach(function (p) { pio.observe(p); });
    }
  }

  /* ---------------- Process line ---------------- */
  var proc = $('[data-proc]');
  if (proc) {
    var line = $('.proc-line', proc), pSteps = $$('.proc-step', proc);
    var upd = function () {
      var r = proc.getBoundingClientRect(), vh = window.innerHeight;
      var p = reduce ? 1 : Math.max(0, Math.min(1, (vh * 0.75 - r.top) / (r.height + vh * 0.25)));
      line.style.setProperty('--p', (p * 100).toFixed(1) + '%');
      pSteps.forEach(function (s, i) { s.classList.toggle('on', p >= (i + 0.5) / pSteps.length - 0.08); });
    };
    window.addEventListener('scroll', function () { requestAnimationFrame(upd); }, { passive: true });
    upd();
  }

  /* ---------------- Pipeline rail: fills and lights stages as you scroll ---------------- */
  $$('[data-pipe]').forEach(function (pl) {
    var st = $$('.pipe-stage', pl);
    var upd = function () {
      var r = pl.getBoundingClientRect(), vh = window.innerHeight;
      var p = reduce ? 1 : Math.max(0, Math.min(1, (vh * 0.62 - r.top) / r.height));
      pl.style.setProperty('--pp', (p * 100).toFixed(1) + '%');
      st.forEach(function (s) { s.classList.toggle('on', reduce || s.getBoundingClientRect().top < vh * 0.62); });
    };
    window.addEventListener('scroll', function () { requestAnimationFrame(upd); }, { passive: true });
    upd();
  });

  /* ---------------- Marquee duplication ---------------- */
  $$('.marquee').forEach(function (m) {
    var tr = $('.marquee-track', m);
    if (!tr || reduce) return;
    var clone = tr.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    $$('a,button', clone).forEach(function (el) { el.setAttribute('tabindex', '-1'); });
    m.appendChild(clone);
  });

  /* ---------------- FAQ smooth open ---------------- */
  if (!reduce) $$('.faq details').forEach(function (d) {
    var s = d.querySelector('summary'), a = d.querySelector('.ans');
    s.addEventListener('click', function (e) {
      e.preventDefault();
      if (d.open) {
        a.animate([{ height: a.offsetHeight + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 300, easing: 'cubic-bezier(.16,1,.3,1)' }).onfinish = function () { d.open = false; };
      } else {
        d.open = true;
        a.animate([{ height: '0px', opacity: 0 }, { height: a.offsetHeight + 'px', opacity: 1 }], { duration: 400, easing: 'cubic-bezier(.16,1,.3,1)' });
      }
    });
  });

  /* ---------------- Workflow panels (segment hero) ---------------- */
  $$('[data-flow]').forEach(function (f) {
    var steps = $$('.step', f), out = $('.flow-out', f), tm = [];
    if (reduce || !hasIO) { steps.forEach(function (s) { s.classList.add('done'); }); if (out) out.classList.add('show'); return; }
    var run = function () {
      tm.forEach(clearTimeout); tm = [];
      steps.forEach(function (s) { s.classList.remove('run', 'done'); });
      if (out) out.classList.remove('show');
      var t = 400;
      steps.forEach(function (s) {
        tm.push(setTimeout(function () { s.classList.add('run'); }, t)); t += 680;
        tm.push(setTimeout(function () { s.classList.remove('run'); s.classList.add('done'); }, t));
      });
      tm.push(setTimeout(function () { if (out) out.classList.add('show'); }, t + 200));
      tm.push(setTimeout(run, t + 4200));
    };
    onView(f, run, { threshold: 0.3 });
  });

  /* ---------------- Generic tabs (segment pages) ---------------- */
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
  });

  /* ---------------- Frameworks ---------------- */
  // Autonomy ladder: evidence fills, the agent earns the next level, then resets.
  var ladder = function (ld, panel) {
    var cols = $$('.ld-col', ld), fill = $('.ld-meter .fill', panel), next = $('.ld-meter .next', panel);
    if (ld._t) clearInterval(ld._t);
    var lvl = 2, ev = 0;
    var paint = function () {
      cols.forEach(function (c, i) { c.classList.toggle('cur', i === lvl); c.classList.toggle('done', i < lvl); });
      if (fill) fill.style.setProperty('--ev', ev.toFixed(1) + '%');
      if (next) next.textContent = lvl < 4 ? 'earns L' + (lvl + 1) : 'sampled audit';
    };
    if (reduce) { ev = 100; paint(); return; }
    paint();
    ld._t = setInterval(function () {
      if (!panel.classList.contains('play')) return;
      ev += 1.6;
      if (ev >= 100) { ev = 0; lvl = lvl >= 4 ? 2 : lvl + 1; }
      paint();
    }, 60);
  };
  var replay = function (panel) {
    panel.classList.remove('play');
    void panel.offsetWidth;
    requestAnimationFrame(function () { panel.classList.add('play'); });
    var ld = $('.ld', panel);
    if (ld) ladder(ld, panel);
  };
  $$('[data-fw]').forEach(function (fw) {
    var tabs = $$('.fw-tab', fw), panels = $$('.fw-panel', fw), idx = 0, timer = null, manual = !!reduce, inView = false, DUR = 10000;
    fw.style.setProperty('--fw-dur', DUR / 1000 + 's');
    if (manual) fw.classList.add('manual');
    var schedule = function () {
      clearTimeout(timer);
      if (manual || !inView) return;
      timer = setTimeout(function () { select((idx + 1) % panels.length); }, DUR);
    };
    var select = function (i, focus) {
      idx = i;
      tabs.forEach(function (t, j) { t.setAttribute('aria-selected', j === i ? 'true' : 'false'); t.tabIndex = j === i ? 0 : -1; });
      panels.forEach(function (p, j) { p.classList.toggle('on', j === i); if (j !== i) p.classList.remove('play'); });
      replay(panels[i]);
      if (focus) tabs[i].focus();
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
    fw.addEventListener('pointerenter', function () { if (!manual) { clearTimeout(timer); fw.classList.add('paused'); } });
    fw.addEventListener('pointerleave', function () { if (!manual) { fw.classList.remove('paused'); schedule(); } });
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
  $$('.fw-single').forEach(function (s) {
    var p = $('.fw-panel', s);
    onView(s, function () { replay(p); }, { threshold: 0.3 });
  });
})();
