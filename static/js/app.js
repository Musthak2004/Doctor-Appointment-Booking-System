(function () {
  'use strict';

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  /* ---- Shared ---- */

  function setStyles(el, styles) {
    for (var key in styles) {
      if (styles.hasOwnProperty(key)) el.style[key] = styles[key];
    }
  }

  /* ---- 1. Scroll reveal (fade + slide-up) ---- */

  function initScrollReveal() {
    var els = document.querySelectorAll(
      '.feature-card, .step, .stat, .section__title, .section__subtitle, .auth__card, .cta__container'
    );
    if (!els.length) return;

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
          observer.unobserve(el);
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -32px 0px' }
    );

    els.forEach(function (el, i) {
      setStyles(el, {
        opacity: '0',
        transform: 'translateY(24px)',
        transition: 'opacity 0.5s ease-out, transform 0.5s ease-out',
        transitionDelay: i * 50 + 'ms',
      });
      observer.observe(el);
    });
  }

  /* ---- 2. Counter animation (stats) ---- */

  function initCounters() {
    var counters = document.querySelectorAll('.stat__number');
    if (!counters.length) return;

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.5 }
    );

    counters.forEach(function (c) {
      return observer.observe(c);
    });
  }

  function animateCounter(el) {
    var text = el.textContent;
    var match = text.match(/[\d,]+/);
    if (!match) return;

    var target = parseInt(match[0].replace(/,/g, ''), 10);
    var suffix = text.replace(match[0], '');
    var duration = 1200;
    var start = performance.now();

    function update(now) {
      var elapsed = now - start;
      var progress = Math.min(elapsed / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = Math.round(eased * target);
      el.textContent = current.toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
  }

  /* ---- 3. Form submit loading spinner ---- */

  function setFormLoading(form) {
    var btn = form.querySelector('.btn--submit, button[type="submit"]');
    if (!btn || btn.disabled) return;
    btn.disabled = true;
    btn.dataset.loading = 'true';
    var text = btn.textContent;
    btn.innerHTML =
      '<span class="btn__spinner" aria-hidden="true"></span> ' + text;
  }

  function initFormLoading() {
    document.querySelectorAll('form').forEach(function (form) {
      form.addEventListener('submit', function () {
        setFormLoading(form);
      });
    });
  }

  /* ---- 4. Auth card entrance (scale + fade) ---- */

  function initAuthEntrance() {
    var card = document.querySelector('.auth__card');
    if (!card) return;
    setStyles(card, {
      opacity: '0',
      transform: 'scale(0.96) translateY(12px)',
      transition: 'opacity 0.35s ease-out, transform 0.35s ease-out',
    });
    requestAnimationFrame(function () {
      card.style.opacity = '1';
      card.style.transform = 'scale(1) translateY(0)';
    });
  }

  /* ---- Init ---- */

  initScrollReveal();
  initCounters();
  initFormLoading();
  initAuthEntrance();
})();
