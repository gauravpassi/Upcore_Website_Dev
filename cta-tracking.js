/* CTA click tracking (v3, 2026-10-06).
   - Pages that load gtag.js directly send cta_click through gtag.
   - GTM pages (window.upcGTM, the V4 pages) push {event:'cta_click', event_params} to dataLayer;
     the GTM GA4 event tag only fires where the page also pushed {tagging:'gtm'}, so a click is
     never counted twice.
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
    if (!window.upcGTM && typeof gtag === 'function') gtag('event', 'cta_click', p);
    else { window.dataLayer.push({ event_params: null }); window.dataLayer.push({ event: 'cta_click', event_params: p }); }
  }, true);
})();
