/* V4.1 engagement analytics. No-ops until gtag/clarity are present (they are omitted on previews).
   Events: scroll_depth, section_view, framework_tab_select, content_tab_select, nav_menu_open, faq_open. */
(function () {
  'use strict';
  function send(n, p) { if (typeof gtag === 'function') gtag('event', n, p || {}); if (typeof clarity === 'function') clarity('event', n); }

  var hit = {}, q = false;
  function sc() {
    if (q) return; q = true;
    requestAnimationFrame(function () {
      q = false;
      var h = document.documentElement.scrollHeight - innerHeight, pc = h > 0 ? Math.round(scrollY / h * 100) : 100;
      [25, 50, 75, 90].forEach(function (m) { if (pc >= m && !hit[m]) { hit[m] = 1; send('scroll_depth', { percent_scrolled: m }); } });
      if (hit[90]) removeEventListener('scroll', sc);
    });
  }
  addEventListener('scroll', sc, { passive: true });

  if ('IntersectionObserver' in window) {
    var seen = {}, io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var id = e.target.getAttribute('aria-labelledby');
        if (!id || seen[id]) return; seen[id] = 1; io.unobserve(e.target);
        var h = document.getElementById(id);
        send('section_view', { section_id: id, section_title: h ? h.textContent.replace(/\s+/g, ' ').trim().slice(0, 80) : '' });
      });
    }, { rootMargin: '0px 0px -50% 0px' });
    document.querySelectorAll('main section[aria-labelledby]').forEach(function (s) { io.observe(s); });
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[role="tab"]');
    if (t) send(t.classList.contains('fw-tab') ? 'framework_tab_select' : 'content_tab_select', { tab_id: t.id, method: 'click' });
    var b = e.target.closest('.nav-menu > li > button');
    if (b && b.getAttribute('aria-expanded') !== 'true') send('nav_menu_open', { menu: b.textContent.trim() });
  }, true);

  document.addEventListener('toggle', function (e) {
    var d = e.target;
    if (d.tagName === 'DETAILS' && d.open && d.closest('.faq')) {
      var s = d.querySelector('summary');
      send('faq_open', { faq_question: s ? s.textContent.trim().slice(0, 100) : '' });
    }
  }, true);
})();
