(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setStyles(el, styles) {
    for (var key in styles) {
      if (styles.hasOwnProperty(key)) el.style[key] = styles[key];
    }
  }

  /* ---- 1. HEADER SCROLL EFFECT ---- */

  function initHeaderScroll() {
    var header = document.querySelector('.header');
    if (!header) return;
    var scrollThreshold = 20;

    function onScroll() {
      if (window.scrollY > scrollThreshold) {
        header.classList.add('header--scrolled');
      } else {
        header.classList.remove('header--scrolled');
      }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---- 2. SCROLL REVEAL (Intersection Observer) ---- */

  function initScrollReveal() {
    if (reducedMotion) return;

    var els = document.querySelectorAll(
      '.feature-card, .step, .stat, .section__title, .section__subtitle, ' +
      '.auth__card, .cta__container, .profile__header, .profile__body, ' +
      '.doctor-card, .hero__badge, .hero__title, .hero__subtitle, ' +
      '.hero__actions, .hero__stats, .empty-state'
    );
    if (!els.length) return;

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          el.classList.add('reveal--visible');
          observer.unobserve(el);
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    );

    els.forEach(function (el, i) {
      if (el.classList.contains('hero__badge') ||
          el.classList.contains('hero__title') ||
          el.classList.contains('hero__subtitle') ||
          el.classList.contains('hero__actions') ||
          el.classList.contains('hero__stats') ||
          el.classList.contains('auth__card')) return;
      el.classList.add('reveal');
      el.style.transitionDelay = (i * 60) + 'ms';
      observer.observe(el);
    });
  }

  /* ---- 3. ANIMATED COUNTERS ---- */

  function initCounters() {
    if (reducedMotion) return;

    var counters = document.querySelectorAll('.stat__number, .hero__stat-number');
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
    var duration = 1500;
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

  /* ---- 4. FORM SUBMIT LOADING ---- */

  function setFormLoading(form) {
    var btn = form.querySelector('.btn--submit, button[type="submit"]');
    if (!btn || btn.disabled) return;
    btn.disabled = true;
    btn.dataset.loading = 'true';
    var text = btn.textContent;
    btn.innerHTML = '<span class="btn__spinner" aria-hidden="true"></span> ' + text;
  }

  function initFormLoading() {
    document.querySelectorAll('form').forEach(function (form) {
      form.addEventListener('submit', function () {
        setFormLoading(form);
      });
    });
  }

  /* ---- 5. HERO PARTICLE CANVAS ---- */

  function initHeroCanvas() {
    if (reducedMotion) return;

    var canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    var ctx = canvas.getContext('2d');
    var particles = [];
    var mouseX = -1000;
    var mouseY = -1000;
    var frameId;

    function resize() {
      var rect = canvas.parentElement.getBoundingClientRect();
      canvas.width = rect.width * window.devicePixelRatio;
      canvas.height = rect.height * window.devicePixelRatio;
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    }

    function createParticles() {
      var w = canvas.width / window.devicePixelRatio;
      var h = canvas.height / window.devicePixelRatio;
      var count = Math.min(Math.floor((w * h) / 12000), 60);
      particles = [];
      for (var i = 0; i < count; i++) {
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          r: Math.random() * 2 + 1,
          opacity: Math.random() * 0.5 + 0.2,
        });
      }
    }

    function draw() {
      var w = canvas.width / window.devicePixelRatio;
      var h = canvas.height / window.devicePixelRatio;
      ctx.clearRect(0, 0, w, h);

      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, ' + p.opacity + ')';
        ctx.fill();

        for (var j = i + 1; j < particles.length; j++) {
          var p2 = particles[j];
          var dx = p.x - p2.x;
          var dy = p.y - p2.y;
          var dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = 'rgba(255, 255, 255, ' + (0.08 * (1 - dist / 120)) + ')';
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }

        var dxM = p.x - mouseX;
        var dyM = p.y - mouseY;
        var distM = Math.sqrt(dxM * dxM + dyM * dyM);
        if (distM < 150) {
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r * 1.5, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(255, 255, 255, ' + (p.opacity * 0.3 * (1 - distM / 150)) + ')';
          ctx.fill();
        }
      }

      frameId = requestAnimationFrame(draw);
    }

    resize();
    createParticles();
    draw();

    canvas.addEventListener('mousemove', function (e) {
      var rect = canvas.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
    });

    canvas.addEventListener('mouseleave', function () {
      mouseX = -1000;
      mouseY = -1000;
    });

    window.addEventListener('resize', function () {
      resize();
      createParticles();
    });

    return function cleanup() {
      cancelAnimationFrame(frameId);
    };
  }

  /* ---- 6. FLOATING ORBS ANIMATION ---- */

  function initOrbs() {
    if (reducedMotion) return;
    var orbs = document.querySelectorAll('.animated-bg__orb');
    if (!orbs.length) return;

    orbs.forEach(function (orb, i) {
      var duration = 18 + i * 4;
      var delay = i * 3;
      orb.style.animationDuration = duration + 's';
      orb.style.animationDelay = delay + 's';
    });
  }

  /* ---- 7. MOBILE NAV OVERLAY CLOSE ON CLICK ---- */

  function initMobileNav() {
    var toggle = document.querySelector('.header__menu-toggle');
    var nav = document.getElementById('primary-nav');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
      var expanded = toggle.getAttribute('aria-expanded') === 'true' ? false : true;
      toggle.setAttribute('aria-expanded', expanded);
      nav.classList.toggle('header__nav--open');
      document.body.classList.toggle('nav-open');
    });

    document.addEventListener('click', function (e) {
      if (nav.classList.contains('header__nav--open') &&
          !nav.contains(e.target) &&
          !toggle.contains(e.target)) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('header__nav--open');
        document.body.classList.remove('nav-open');
      }
    });

    nav.querySelectorAll('.header__nav-link').forEach(function (link) {
      link.addEventListener('click', function () {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('header__nav--open');
        document.body.classList.remove('nav-open');
      });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('header__nav--open')) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('header__nav--open');
        document.body.classList.remove('nav-open');
        toggle.focus();
      }
    });
  }

  /* ---- 8. CARD TILT EFFECT ---- */

  function initCardTilt() {
    if (reducedMotion) return;
    if (!window.matchMedia('(hover: hover)').matches) return;

    var cards = document.querySelectorAll('.doctor-card, .feature-card');
    if (!cards.length) return;

    cards.forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        var centerX = rect.width / 2;
        var centerY = rect.height / 2;
        var rotateX = ((y - centerY) / centerY) * -4;
        var rotateY = ((x - centerX) / centerX) * 4;
        card.style.transform =
          'perspective(600px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) translateY(-6px)';
      });

      card.addEventListener('mouseleave', function () {
        card.style.transform = '';
      });
    });
  }

  /* ---- 9. SMOOTH SCROLL FOR ANCHOR LINKS ---- */

  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        var target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /* ---- INIT ---- */

  initHeaderScroll();
  initScrollReveal();
  initCounters();
  initFormLoading();
  initOrbs();
  initMobileNav();
  initCardTilt();
  initSmoothScroll();

  if (!reducedMotion) {
    var cleanupCanvas = initHeroCanvas();
    window.addEventListener('unload', function () {
      if (cleanupCanvas) cleanupCanvas();
    });
  }

})();
