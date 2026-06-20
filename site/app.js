/* ═══════════════════════════════════════════════════════
   TeamBrain 사이트 · 네비 스크롤스파이 · 모바일 메뉴 · 페이드인 · 복사
   빌드 단계 없는 순수 JS
   ═══════════════════════════════════════════════════════ */
(function () {
  'use strict';

  // reduced-motion 환경 감지 (모션은 끄되 콘텐츠는 절대 숨기지 않음)
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav__link'));
  var sections = navLinks
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);
  var linkById = {};
  navLinks.forEach(function (a) { linkById[a.getAttribute('href').slice(1)] = a; });

  /* ─── 모바일 오프캔버스 메뉴 ─────────────────────── */
  var menuBtn = document.querySelector('.nav__menu-btn');
  var menu = document.getElementById('nav-links');
  var backdrop = document.createElement('div');
  backdrop.className = 'nav-backdrop';
  document.body.appendChild(backdrop);

  function openMenu(open) {
    menu.classList.toggle('open', open);
    backdrop.classList.toggle('show', open);
    if (menuBtn) menuBtn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (menuBtn) menuBtn.addEventListener('click', function () { openMenu(!menu.classList.contains('open')); });
  backdrop.addEventListener('click', function () { openMenu(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') openMenu(false);
  });

  /* ─── 부드러운 앵커 스크롤 + 클릭 시 활성 잠금 ────── */
  var clickLockUntil = 0;
  navLinks.forEach(function (a) {
    a.addEventListener('click', function () {
      clickLockUntil = performance.now() + 700;
      activate(a.getAttribute('href').slice(1));
      openMenu(false); // 모바일에서 링크 클릭 시 메뉴 닫기
    });
  });
  // 브랜드 클릭도 닫기
  var brand = document.querySelector('.nav__brand');
  if (brand) brand.addEventListener('click', function () { openMenu(false); });

  /* ─── 스크롤스파이 (rect 기반, IO 불필요) ────────── */
  var LINE = 96;
  function activate(id) {
    navLinks.forEach(function (a) {
      a.classList.toggle('is-active', a.getAttribute('href').slice(1) === id);
    });
  }
  function pickActive() {
    if (performance.now() < clickLockUntil) return;
    var best = null, bestTop = -Infinity;
    for (var i = 0; i < sections.length; i++) {
      var top = sections[i].getBoundingClientRect().top - LINE;
      if (top <= 0 && top > bestTop) { bestTop = top; best = sections[i].id; }
    }
    if (!best && sections[0]) best = sections[0].id;
    // 페이지 끝에 닿으면 마지막 섹션 강제 활성
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 2 && sections.length) {
      best = sections[sections.length - 1].id;
    }
    if (best) activate(best);
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { pickActive(); ticking = false; });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  pickActive();

  /* ─── 스크롤 진입 페이드인 ───────────────────────── */
  var reveals = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  function showAll() { reveals.forEach(function (el) { el.classList.add('is-in'); }); }

  if (reduceMotion || !('IntersectionObserver' in window)) {
    showAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ─── 터미널 클립보드 복사 ───────────────────────── */
  document.querySelectorAll('.tb-copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var term = btn.closest('.terminal');
      if (!term) return;
      // .t-prompt가 있는 줄(명령어)만 골라 주석·프롬프트 제거 후 추출
      var cmds = Array.prototype.slice.call(term.querySelectorAll('.terminal-body .line'))
        .filter(function (line) { return line.querySelector('.t-prompt'); })
        .map(function (line) {
          var clone = line.cloneNode(true);
          clone.querySelectorAll('.t-cmt, .t-prompt').forEach(function (n) { n.remove(); });
          return clone.textContent.replace(/\s+/g, ' ').trim();
        })
        .filter(Boolean);
      if (!cmds.length) return;
      var text = cmds.join('\n');
      try {
        navigator.clipboard.writeText(text).then(function () {
          var orig = btn.innerHTML;
          btn.classList.add('copied');
          btn.textContent = '✓ 복사됨';
          setTimeout(function () { btn.innerHTML = orig; btn.classList.remove('copied'); }, 1600);
        });
      } catch (e) { /* 미지원 환경 무시 */ }
    });
  });
})();
