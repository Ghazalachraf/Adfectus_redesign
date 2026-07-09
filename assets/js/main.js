// Adfectus — interactions minimales
(function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Menu mobile
  var burger = document.querySelector('.burger');
  var links = document.querySelector('.nav-links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      burger.classList.toggle('open');
      links.classList.toggle('open');
      document.body.style.overflow = links.classList.contains('open') ? 'hidden' : '';
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        burger.classList.remove('open');
        links.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  // Header transparent en haut, verre blanc dès qu'on scrolle
  var header = document.querySelector('.site-header');

  // Footer « curtain reveal » : hauteur du révélateur + progression
  var footerReveal = document.querySelector('.footer-reveal');
  var footer = document.querySelector('.site-footer');
  function sizeFooter() {
    if (!footer || !footerReveal) return;
    footer.style.height = 'auto';
    var h = Math.min(footer.scrollHeight, window.innerHeight);
    document.documentElement.style.setProperty('--footer-h', h + 'px');
    footer.style.height = '';
  }
  function onScroll() {
    header.classList.toggle('scrolled', window.scrollY > 30);
    if (footerReveal) {
      var r = footerReveal.getBoundingClientRect();
      var visible = Math.min(Math.max(window.innerHeight - r.top, 0), r.height);
      var progress = r.height > 0 ? visible / r.height : 0;
      footer.style.setProperty('--reveal', progress.toFixed(3));
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { sizeFooter(); onScroll(); });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { sizeFooter(); onScroll(); });
  }
  sizeFooter();
  onScroll();

  // Lien actif dans la navigation
  var current = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(function (a) {
    if (a.getAttribute('href') === current) a.classList.add('active');
  });

  // Apparition douce au scroll
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('visible'); });
  }

  // Lightbox vidéo
  var cards = document.querySelectorAll('.video-card[data-video]');
  if (cards.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.innerHTML =
      '<button class="lightbox-close" aria-label="Fermer">×</button>' +
      '<div class="lightbox-inner"><video controls playsinline></video><p class="lightbox-title"></p></div>';
    document.body.appendChild(lb);
    var lbVideo = lb.querySelector('video');
    var lbTitle = lb.querySelector('.lightbox-title');

    function openLb(card) {
      lbVideo.src = card.getAttribute('data-video');
      lbTitle.textContent = card.getAttribute('data-title') || '';
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
      lbVideo.play().catch(function () {});
    }
    function closeLb() {
      lb.classList.remove('open');
      lbVideo.pause();
      lbVideo.removeAttribute('src');
      lbVideo.load();
      document.body.style.overflow = '';
    }
    cards.forEach(function (card) {
      card.addEventListener('click', function () { openLb(card); });
      card.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLb(card); }
      });
    });
    lb.addEventListener('click', function (e) {
      if (e.target === lb || e.target.classList.contains('lightbox-close')) closeLb();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && lb.classList.contains('open')) closeLb();
    });
  }

  // Lecteur audio minimal (spot Adfectus)
  var player = document.querySelector('.audio-player');
  if (player) {
    var audio = new Audio(player.getAttribute('data-src'));
    audio.preload = 'metadata';
    var toggle = player.querySelector('.audio-toggle');
    var track = player.querySelector('.audio-track');
    var bar = player.querySelector('.audio-bar');
    var time = player.querySelector('.audio-time');

    function fmt(s) {
      s = Math.floor(s || 0);
      return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
    }
    toggle.addEventListener('click', function () {
      if (audio.paused) { audio.play(); } else { audio.pause(); }
    });
    audio.addEventListener('play', function () { player.classList.add('playing'); });
    audio.addEventListener('pause', function () { player.classList.remove('playing'); });
    audio.addEventListener('timeupdate', function () {
      if (audio.duration) bar.style.width = (audio.currentTime / audio.duration * 100) + '%';
      time.textContent = fmt(audio.currentTime);
    });
    audio.addEventListener('ended', function () {
      player.classList.remove('playing');
      bar.style.width = '0';
      time.textContent = fmt(0);
    });
    track.addEventListener('click', function (e) {
      if (!audio.duration) return;
      var r = track.getBoundingClientRect();
      audio.currentTime = ((e.clientX - r.left) / r.width) * audio.duration;
    });
  }

  // Transition de page en fondu sur les liens internes
  if (!reduceMotion) {
    document.querySelectorAll('a[href$=".html"]:not([target])').forEach(function (a) {
      var href = a.getAttribute('href');
      if (/^https?:/i.test(href)) return;
      a.addEventListener('click', function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        document.body.classList.add('page-out');
        setTimeout(function () { location.href = href; }, 240);
      });
    });
  }
})();
