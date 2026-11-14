// 目录抽屉、深浅色切换、阅读进度与当前段落高亮。无依赖。
(function () {
  var html = document.documentElement;
  var toc = document.getElementById('toc');
  var scrim = document.getElementById('scrim');
  var tocBtn = document.getElementById('tocBtn');
  var tocClose = document.getElementById('tocClose');
  var themeBtn = document.getElementById('themeBtn');
  var toTop = document.getElementById('toTop');

  /* ---- 主题：跟随系统，手动切换后记住选择 ---- */
  try {
    var saved = localStorage.getItem('theme');
    if (saved === 'light' || saved === 'dark') html.setAttribute('data-theme', saved);
  } catch (e) {}
  themeBtn.addEventListener('click', function () {
    var isDark = html.getAttribute('data-theme')
      ? html.getAttribute('data-theme') === 'dark'
      : window.matchMedia('(prefers-color-scheme: dark)').matches;
    var next = isDark ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  /* ---- 目录抽屉 ---- */
  function openToc() {
    toc.classList.add('open');
    scrim.hidden = false;
    tocBtn.setAttribute('aria-expanded', 'true');
  }
  function closeToc() {
    toc.classList.remove('open');
    scrim.hidden = true;
    tocBtn.setAttribute('aria-expanded', 'false');
  }
  tocBtn.addEventListener('click', function () {
    toc.classList.contains('open') ? closeToc() : openToc();
  });
  tocClose.addEventListener('click', closeToc);
  scrim.addEventListener('click', closeToc);
  toc.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') closeToc();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeToc();
  });

  /* ---- 当前段落高亮 + 回到顶部按钮 ---- */
  var links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
  var sections = Array.prototype.slice.call(document.querySelectorAll('section.seg[id]'));

  function setActive(id) {
    links.forEach(function (a) { a.classList.remove('active'); });
    if (byId[id]) byId[id].classList.add('active');
  }

  if ('IntersectionObserver' in window) {
    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting ? en.intersectionRatio : 0; });
      var best = null, ratio = 0;
      Object.keys(visible).forEach(function (id) {
        if (visible[id] > ratio) { ratio = visible[id]; best = id; }
      });
      if (best) setActive(best);
    }, { rootMargin: '-12% 0px -60% 0px', threshold: [0, 0.15, 0.4, 0.75] });
    var current = null;
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) current = en.target.id;
      });
      if (current) setActive(current);
    }, { rootMargin: '-12% 0px -70% 0px' });
    sections.forEach(function (s) { io.observe(s); spy.observe(s); });
  }

  window.addEventListener('scroll', function () {
    if (window.scrollY > 600) toTop.hidden = false; else toTop.hidden = true;
  }, { passive: true });
  toTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();
