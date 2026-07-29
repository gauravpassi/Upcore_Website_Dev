(function () {
  'use strict';

  window.dataLayer = window.dataLayer || [];

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-gtm-cta]');
    if (!el) return;

    window.dataLayer.push({
      event: 'cta_click',
      cta_id: el.getAttribute('data-gtm-cta'),
      cta_type: el.getAttribute('data-gtm-cta-type') || '',
      cta_section: el.getAttribute('data-gtm-cta-section') || '',
      cta_text: (el.textContent || '').trim(),
      cta_url: el.getAttribute('href') || '',
      page_path: window.location.pathname
    });
  }, true);
})();
