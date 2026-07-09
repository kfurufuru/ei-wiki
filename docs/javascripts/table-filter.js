/*
 * table-filter.js — 症状逆引きインデックスのページ内インクリメンタル絞り込み。
 * <input class="ei-tablefilter"> があれば、同ページの全テーブル行を入力語で
 * 即時フィルタし、ヒット0のカテゴリ（直前の見出し含む）を隠す。
 * Material の instant navigation 後も document$ で再配線する。
 */
(function () {
  'use strict';

  function prevHeading(el) {
    var n = el.previousElementSibling;
    while (n) {
      if (/^H[2-3]$/.test(n.tagName)) { return n; }
      n = n.previousElementSibling;
    }
    return null;
  }

  function wire() {
    var input = document.querySelector('.ei-tablefilter');
    if (!input || input.dataset.eiWired === '1') { return; }
    input.dataset.eiWired = '1';
    // JS無効時は入力欄を隠しておき（HTMLに hidden 属性）、配線できた時のみ表示する。
    // これで非JS/印刷/オフラインでは死んだ入力欄が出ず、アンカーチップが主導線になる。
    input.hidden = false;

    var tables = Array.prototype.slice.call(
      document.querySelectorAll('.md-typeset table')
    );
    if (!tables.length) { return; }

    // ヒット0時の案内メッセージ
    var empty = document.createElement('p');
    empty.className = 'ei-filter-empty';
    empty.hidden = true;
    empty.textContent = '該当する症状が見つかりません。キーワードを短くするか、上部の検索もお試しください。';
    input.insertAdjacentElement('afterend', empty);

    function apply() {
      var q = input.value.trim().toLowerCase();
      var totalVisible = 0;
      tables.forEach(function (t) {
        var rows = t.querySelectorAll('tbody tr');
        var anyVisible = false;
        rows.forEach(function (r) {
          var match = !q || r.textContent.toLowerCase().indexOf(q) >= 0;
          r.style.display = match ? '' : 'none';
          if (match) { anyVisible = true; totalVisible++; }
        });
        var wrap = t.closest('.md-typeset__scrollwrap') || t;
        wrap.style.display = anyVisible ? '' : 'none';
        var h = prevHeading(wrap);
        if (h) { h.style.display = anyVisible ? '' : 'none'; }
      });
      empty.hidden = !(q && totalVisible === 0);
    }

    input.addEventListener('input', apply);
  }

  // カテゴリ早送りチップの scrollspy：表示中カテゴリのチップを塗りで明示
  function spy() {
    var jump = document.querySelector('.ei-jump');
    if (!jump || jump.dataset.eiSpy === '1' || !('IntersectionObserver' in window)) { return; }
    var links = Array.prototype.slice.call(jump.querySelectorAll('a'));
    if (!links.length) { return; }
    jump.dataset.eiSpy = '1';
    var map = {};
    links.forEach(function (a) {
      var h = a.getAttribute('href') || '';
      var id = h.indexOf('#') >= 0 ? h.substring(h.indexOf('#') + 1) : '';
      if (id) { map[id] = a; }
    });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && map[e.target.id]) {
          links.forEach(function (a) { a.classList.remove('ei-jump-active'); });
          map[e.target.id].classList.add('ei-jump-active');
        }
      });
    }, { rootMargin: '-12% 0px -60% 0px', threshold: 0 });
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) { obs.observe(el); }
    });
  }

  function init() { wire(); spy(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  if (window.document$ && typeof window.document$.subscribe === 'function') {
    try { window.document$.subscribe(init); } catch (e) { /* noop */ }
  }
})();
