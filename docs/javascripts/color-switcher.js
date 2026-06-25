/*
 * ei-wiki color-switcher
 * MkDocs Material の primary 色を <body data-md-color-primary="<token>"> 切替で変更する。
 * パレットは自作せず Material 組込みの primary パレットを利用する（light/dark scheme は触らない）。
 *
 * 公開コントラクト:
 *   - マウント点: <span id="ei-theme-switcher"></span>（無ければ静かに return）
 *   - localStorage キー: 'ei-color-primary'
 *   - body 属性: data-md-color-primary
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'ei-color-primary';
  var DEFAULT_COLOR = 'teal';

  // value = Material primary token / hex = スウォッチ表示用代表色 / label = 日本語ラベル
  var COLORS = [
    { value: 'teal',        hex: '#009688', label: 'ティール（既定）' },
    { value: 'indigo',      hex: '#3f51b5', label: '藍' },
    { value: 'blue',        hex: '#2196f3', label: '青' },
    { value: 'green',       hex: '#4caf50', label: '緑' },
    { value: 'deep-orange', hex: '#ff5722', label: '橙' },
    { value: 'deep-purple', hex: '#673ab7', label: '紫' },
    { value: 'pink',        hex: '#e91e63', label: '桃' },
    { value: 'blue-grey',   hex: '#607d8b', label: '青灰' }
  ];

  function readStored() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function writeStored(value) {
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch (e) {
      /* localStorage 不可（プライベートモード等）でも動作継続 */
    }
  }

  function applyColor(value) {
    if (document.body) {
      document.body.setAttribute('data-md-color-primary', value);
    }
  }

  function init() {
    // 1. 起動時に保存色（無ければ既定）を適用
    var current = readStored() || DEFAULT_COLOR;
    applyColor(current);

    // 2. マウント点を探す。無ければ静かに終了（色適用だけは済んでいる）
    var mount = document.getElementById('ei-theme-switcher');
    if (!mount) {
      return;
    }

    // 既に描画済みなら二重描画しない
    if (mount.getAttribute('data-ei-initialized') === 'true') {
      return;
    }
    mount.setAttribute('data-ei-initialized', 'true');

    // 3. UI 構築
    var root = document.createElement('div');
    root.className = 'ei-cs-root';

    // トグルボタン
    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'ei-cs-toggle';
    toggle.setAttribute('aria-label', '配色を変更');
    toggle.setAttribute('aria-haspopup', 'true');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.textContent = '🎨';

    // ポップオーバー
    var popover = document.createElement('div');
    popover.className = 'ei-cs-popover';
    popover.setAttribute('role', 'menu');
    popover.hidden = true;

    var swatchByValue = {};

    function updateSelected(value) {
      for (var key in swatchByValue) {
        if (Object.prototype.hasOwnProperty.call(swatchByValue, key)) {
          var btn = swatchByValue[key];
          var isSel = key === value;
          if (isSel) {
            btn.classList.add('ei-cs-selected');
            btn.setAttribute('aria-checked', 'true');
          } else {
            btn.classList.remove('ei-cs-selected');
            btn.setAttribute('aria-checked', 'false');
          }
        }
      }
    }

    COLORS.forEach(function (c) {
      var sw = document.createElement('button');
      sw.type = 'button';
      sw.className = 'ei-cs-swatch';
      sw.setAttribute('role', 'menuitemradio');
      sw.setAttribute('title', c.label);
      sw.setAttribute('aria-label', c.label);
      sw.style.background = c.hex;
      sw.setAttribute('data-color', c.value);

      sw.addEventListener('click', function () {
        applyColor(c.value);     // (1) body 属性適用
        writeStored(c.value);    // (2) localStorage 保存
        updateSelected(c.value); // (3) 選択スウォッチ強調
        closePopover();          // (4) ポップオーバーを閉じる
      });

      swatchByValue[c.value] = sw;
      popover.appendChild(sw);
    });

    function openPopover() {
      popover.hidden = false;
      toggle.setAttribute('aria-expanded', 'true');
      root.classList.add('ei-cs-open');
      document.addEventListener('click', onOutsideClick, true);
      document.addEventListener('keydown', onKeydown, true);
    }

    function closePopover() {
      popover.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      root.classList.remove('ei-cs-open');
      document.removeEventListener('click', onOutsideClick, true);
      document.removeEventListener('keydown', onKeydown, true);
    }

    function onOutsideClick(ev) {
      if (!root.contains(ev.target)) {
        closePopover();
      }
    }

    function onKeydown(ev) {
      if (ev.key === 'Escape') {
        closePopover();
        toggle.focus();
      }
    }

    toggle.addEventListener('click', function (ev) {
      ev.stopPropagation();
      if (popover.hidden) {
        openPopover();
      } else {
        closePopover();
      }
    });

    updateSelected(current);

    root.appendChild(toggle);
    root.appendChild(popover);
    mount.appendChild(root);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
