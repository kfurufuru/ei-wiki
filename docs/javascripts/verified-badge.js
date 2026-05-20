/* last_verified バッジ描画
   閲覧時の実日付を基準に記事の鮮度を判定してバッジを描画する。
   しきい値は scripts/check_last_verified.py と統一（DUE_SOON 300日 / EXPIRED 365日）。
   MkDocs Material の instant navigation に対応するため document$ で購読する。 */
(function () {
  function render() {
    var badges = document.querySelectorAll(".last-verified-badge[data-last-verified]");
    badges.forEach(function (el) {
      if (el.dataset.rendered === "1") return;
      var lv = (el.dataset.lastVerified || "").trim();
      var d = new Date(lv + "T00:00:00");
      if (isNaN(d.getTime())) {
        el.dataset.rendered = "1";
        return;
      }
      var days = Math.floor((Date.now() - d.getTime()) / 86400000);
      var cls, label;
      if (days > 365) {
        cls = "expired";
        label = "🔴 最終確認 " + lv + "（" + days + "日経過 — 内容を再確認のうえ参照）";
      } else if (days >= 300) {
        cls = "due-soon";
        label = "🟠 最終確認 " + lv + "（" + days + "日経過 — まもなく要再確認）";
      } else {
        cls = "ok";
        label = "✅ 最終確認 " + lv;
      }
      el.classList.add(cls);
      el.textContent = label;
      el.dataset.rendered = "1";
    });
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(render);
  } else {
    document.addEventListener("DOMContentLoaded", render);
  }
})();
