/*
 * a11y-fixups.js — Material テーマ既定の軽微なアクセシビリティ欠落を補修する。
 * axe-core 検出: aria-dialog-name / aria-progressbar-name / region / landmark-unique。
 * instant navigation 後も document$ で再適用する。
 */
(function () {
  'use strict';

  function fix() {
    // 1. サイト内検索ダイアログに accessible name を付与
    var search = document.querySelector('[data-md-component="search"]');
    if (search && !search.getAttribute('aria-label')) {
      search.setAttribute('aria-label', 'サイト内検索');
    }
    var searchBox = document.querySelector('.md-search');
    if (searchBox && !searchBox.getAttribute('aria-label')) {
      searchBox.setAttribute('aria-label', 'サイト内検索');
    }

    // 2. instant-loading のプログレスバーは装飾。a11y ツリーから除外し
    //    aria-progressbar-name / region 警告を解消
    document.querySelectorAll('.md-progress').forEach(function (p) {
      p.setAttribute('aria-hidden', 'true');
    });

    // 3a. セクション nav は aria-labelledby がアイコンのみの <label> を指し
    //     アクセシブル名が空になる（navigation.indexes の仕様）。nav 直下の
    //     .md-nav__title のテキストで明示的に命名する。
    document.querySelectorAll('nav.md-nav[aria-labelledby]').forEach(function (nav) {
      var title = nav.querySelector(':scope > .md-nav__title');
      var name = title ? title.textContent.trim() : '';
      if (name) { nav.setAttribute('aria-label', name); }
    });

    // 3b. landmark-unique: 同名の <nav> が残る場合、2 個目以降に連番を付け一意化。
    var nameCount = {};
    document.querySelectorAll('nav').forEach(function (n) {
      var name = n.getAttribute('aria-label');
      if (!name) {
        var lb = n.getAttribute('aria-labelledby');
        if (lb) {
          var el = document.getElementById(lb);
          name = el ? el.textContent.trim() : '';
        }
      }
      if (!name) { return; }
      if (nameCount[name] === undefined) {
        nameCount[name] = 1;
      } else {
        nameCount[name] += 1;
        n.setAttribute('aria-label', name + ' （' + nameCount[name] + '）');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fix);
  } else {
    fix();
  }

  // Material の instant navigation 後にも再適用
  if (window.document$ && typeof window.document$.subscribe === 'function') {
    try { window.document$.subscribe(fix); } catch (e) { /* noop */ }
  }
})();
