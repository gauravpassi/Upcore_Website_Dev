/* CTA click tracking (v2, 2026-10-06).
   - Sends cta_click through gtag (GA4) when available; falls back to a dataLayer push.
     Do not also create a GA4 event tag for cta_click in GTM, or clicks are counted twice.
   - Captures first-touch attribution (gclid/gbraid/wbraid/utm_*) with the landing page
     into localStorage 'upc_attrib' for later lead/booking matching. */
(function () {
  'use strict';
  window.dataLayer = window.dataLayer || [];

  try {
    var q = new URLSearchParams(location.search), a = {};
    ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'].forEach(function (k) { if (q.get(k)) a[k] = q.get(k); });
    if (Object.keys(a).length) { a.landing_page = location.pathname; a.ts = Date.now(); localStorage.setItem('upc_attrib', JSON.stringify(a)); }
  } catch (e) { /* storage unavailable */ }

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-gtm-cta]');
    if (!el) return;
    var p = {
      cta_id: el.getAttribute('data-gtm-cta'),
      cta_type: el.getAttribute('data-gtm-cta-type') || '',
      cta_section: el.getAttribute('data-gtm-cta-section') || '',
      cta_text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 100),
      cta_url: el.getAttribute('href') || '',
      page_path: location.pathname
    };
    if (typeof gtag === 'function') gtag('event', 'cta_click', p);
    else window.dataLayer.push(Object.assign({ event: 'cta_click' }, p));
  }, true);
})();
