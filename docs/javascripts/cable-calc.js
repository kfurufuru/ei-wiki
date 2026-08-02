// 許容電流表 CV/CVT 切り替え
window.switchAmpTable = function (type) {
  var cv  = document.getElementById('amp-table-cv');
  var cvt = document.getElementById('amp-table-cvt');
  var btnCv  = document.getElementById('amp-btn-cv');
  var btnCvt = document.getElementById('amp-btn-cvt');
  if (!cv || !cvt) return;
  var primary = 'var(--md-primary-fg-color,#00897b)';
  if (type === 'cv') {
    cv.style.display  = '';
    cvt.style.display = 'none';
    btnCv.style.background  = primary;
    btnCv.style.color        = '#fff';
    btnCvt.style.background = 'transparent';
    btnCvt.style.color       = primary;
  } else {
    cv.style.display  = 'none';
    cvt.style.display = '';
    btnCvt.style.background = primary;
    btnCvt.style.color       = '#fff';
    btnCv.style.background  = 'transparent';
    btnCv.style.color        = primary;
  }
};

// CV/CVT ケーブルサイズ選定ツール（600V）
(function () {
  // 許容電流 [電線管布設, 気中・暗渠布設, ケーブルラック単条]
  // JCS 0168-2（日本電線工業会規格）の 600V CV・CVT 許容電流。周囲温度40℃・
  // 絶縁体許容温度90℃・1条布設。JCS 原本は有償のため未照合だが、2026-08-02 に
  // 同規格を出典として明記したメーカー技術資料・カタログで全値を照合した:
  //   気中・暗渠 … フジクラ・ダイヤ カタログ / SWCC 技術資料 / 電材商社カタログ附録（3資料一致）
  //   電線管    … SWCC 技術資料 / 矢崎エナジーシステム 許容電流表（2社一致）
  // CV は「3心1条」、CVT は「単心3個より1条」の列。CVT は撚合せにより CV 3心より
  // 有利で、規格上も別値（14mm² 気中 86A vs 76A）。旧データの「保守的に同値」は取りやめ。
  // ラックは JCS に独立した列が無い。ラック上の単条は気中・暗渠と同一条件のため
  // 同値とし（JCS の気中多条布設低減率も1条=1.00）、多条・多段の低減は
  // docs/reference/ampacity.md の低減率表で別途乗じる。
  // 法定値ではないため調達・施工の判断にはメーカーカタログ値と補正係数を使うこと。
  // 表示側の表（docs/02-teiatsu/lv-cable.md）とはこの配列が唯一の正典。
  //
  // R: 導体抵抗（20℃、Ω/km）。JIS C 3605 に基づく最大導体抵抗の規格値で、
  // 2026-08-02 にメーカーカタログ3社（フジクラ・ダイヤ／矢崎／古河電工産業電線）で
  // 全サイズ照合し一致を確認した（8mm² のみ矢崎が円形圧縮で 2.34、他2社は 7/1.2 構成で
  // 2.36。2社一致かつ保守側の 2.36 を採用）。多心（2/3/4心）と CVT は同値で、
  // 単心はこれより低い（14mm² で 1.31）。単心の並列布設には本ツールを使わないこと。
  // docs/04-sekkei/voltage-drop.md の R 表と同一値。片方だけ書き換えないこと。
  var CABLE_DB = {
    cv:  [
      { size: 2.0,  amp: [19,  23,  23],  R: 9.42   },
      { size: 3.5,  amp: [26,  33,  33],  R: 5.30   },
      { size: 5.5,  amp: [35,  44,  44],  R: 3.40   },
      { size: 8,    amp: [43,  54,  54],  R: 2.36   },
      { size: 14,   amp: [59,  76,  76],  R: 1.34   },
      { size: 22,   amp: [77,  100, 100], R: 0.849  },
      { size: 38,   amp: [110, 140, 140], R: 0.491  },
      { size: 60,   amp: [150, 190, 190], R: 0.311  },
      { size: 100,  amp: [210, 260, 260], R: 0.187  },
    ],
    cvt: [
      { size: 14,   amp: [63,  86,  86],  R: 1.34   },
      { size: 22,   amp: [82,  110, 110], R: 0.849  },
      { size: 38,   amp: [110, 155, 155], R: 0.491  },
      { size: 60,   amp: [150, 210, 210], R: 0.311  },
      { size: 100,  amp: [215, 290, 290], R: 0.187  },
      { size: 150,  amp: [275, 380, 380], R: 0.124  },
      { size: 200,  amp: [340, 465, 465], R: 0.0933 },
      { size: 250,  amp: [395, 535, 535], R: 0.0754 },
    ]
  };
  var X = 0.09; // Ω/km（固定）

  function g(id) { return document.getElementById(id); }

  // 入力エラーを結果欄に表示（サイレント失敗を防ぐ）
  function showError(msg) {
    var wrap       = g('cc_result');
    var resultMain = g('cc_result_main');
    var resultSize = g('cc_result_size');
    var resultSub  = g('cc_result_sub');
    var tbody      = g('cc_result_tbody');
    if (tbody) tbody.innerHTML = '';
    if (resultMain) {
      resultMain.style.borderLeftColor = '#e53935';
      resultMain.style.background       = '#ffebee';
    }
    if (resultSize) {
      resultSize.style.color   = '#b71c1c';
      resultSize.style.fontSize = '1rem';
      resultSize.textContent   = '入力エラー';
    }
    if (resultSub) resultSub.textContent = msg;
    if (wrap) wrap.style.display = 'block';
  }

  window.calcCable = function () {
    var I      = parseFloat(g('cc_current').value);
    var Lraw   = parseFloat(g('cc_length').value);
    var L      = Lraw / 1000;
    var vSel   = g('cc_voltage').value;
    var inst   = g('cc_install').value;
    var pf     = parseFloat(g('cc_pf').value);
    var vdLim  = parseFloat(g('cc_vd_limit').value);
    var ctype  = g('cc_ctype').value;

    // 入力バリデーション（空・0・不正値は無反応にせずメッセージ表示）
    if (isNaN(I) || I <= 0)       { showError('負荷電流を 1 以上の数値で入力してください。'); return; }
    if (isNaN(Lraw) || Lraw <= 0) { showError('ケーブル長を 1 以上の数値で入力してください。'); return; }
    if (isNaN(pf) || pf <= 0 || pf > 1) { showError('負荷力率 cosθ は 0 超〜1.0 の範囲で入力してください。'); return; }
    if (isNaN(vdLim) || vdLim <= 0) { showError('許容電圧降下率を 1 以上の数値で入力してください。'); return; }

    // 結果欄の枠色を通常に戻す（前回エラー表示のリセット）
    g('cc_result_size').style.fontSize = '1.4rem';

    var CABLE_DATA = CABLE_DB[ctype];
    var instIdx    = { conduit: 0, air: 1, rack: 2 }[inst];
    var isSingle   = (vSel === '200s' || vSel === '100');
    var V0         = parseFloat(vSel) || 200;
    var factor     = isSingle ? 2 : Math.sqrt(3);
    var sinθ       = Math.sqrt(Math.max(0, 1 - pf * pf));

    var tbody = g('cc_result_tbody');
    tbody.innerHTML = '';

    var recommended = null;

    for (var i = 0; i < CABLE_DATA.length; i++) {
      var d         = CABLE_DATA[i];
      var allowable = d.amp[instIdx];
      var currentOK = allowable >= I;
      var vd        = factor * I * (d.R * pf + X * sinθ) * L;
      var vdRate    = vd / V0 * 100;
      var vdOK      = vdRate <= vdLim;
      var both      = currentOK && vdOK;

      if (both && recommended === null) {
        recommended = { d: d, allowable: allowable, vd: vd, vdRate: vdRate };
      }

      var sizeLabel = d.size < 10 ? d.size.toFixed(1) : String(d.size);
      var margin    = ((allowable / I - 1) * 100).toFixed(0);
      var tr = document.createElement('tr');
      if (both && recommended && recommended.d.size === d.size) {
        tr.style.background = '#e8f5e9';
        tr.style.fontWeight = 'bold';
      }
      tr.innerHTML =
        '<td>' + sizeLabel + '</td>' +
        '<td style="color:' + (currentOK ? '#2e7d32' : '#c62828') + '">' + allowable + '</td>' +
        '<td style="color:' + (currentOK ? '#2e7d32' : '#c62828') + '">' + (currentOK ? '+' + margin + '%' : '不足') + '</td>' +
        '<td style="color:' + (vdOK ? '#2e7d32' : '#c62828') + '">' + vd.toFixed(2) + '</td>' +
        '<td style="color:' + (vdOK ? '#2e7d32' : '#c62828') + '">' + vdRate.toFixed(2) + '</td>' +
        '<td>' + (both ? '✓ OK' : '✗ NG') + '</td>';
      tbody.appendChild(tr);
    }

    var resultMain = g('cc_result_main');
    var resultSize = g('cc_result_size');
    var resultSub  = g('cc_result_sub');
    var label      = ctype === 'cvt' ? 'CVT' : 'CV';

    if (recommended) {
      var s = recommended.d.size < 10 ? recommended.d.size.toFixed(1) : String(recommended.d.size);
      resultMain.style.borderLeftColor = '#43a047';
      resultMain.style.background      = '#e8f5e9';
      resultSize.style.color           = '#1b5e20';
      resultSize.textContent = label + ' ' + s + ' mm²';
      resultSub.textContent  =
        '許容電流 ' + recommended.allowable + ' A（負荷の ' +
        ((recommended.allowable / I) * 100).toFixed(0) + '%）、電圧降下率 ' +
        recommended.vdRate.toFixed(2) + '%';
    } else {
      resultMain.style.borderLeftColor = '#fb8c00';
      resultMain.style.background      = '#fff8e1';
      resultSize.style.color           = '#e65100';
      resultSize.textContent = '最大サイズ超 — 要別途検討';
      resultSub.textContent  = '表内サイズで条件を満たせません。並列敷設または電圧昇圧を検討してください。';
    }

    // 補正係数の警告（許容電流は基準値。温度補正・多条低減は未考慮）
    var warn = g('cc_result_warn');
    if (!warn) {
      warn = document.createElement('div');
      warn.id = 'cc_result_warn';
      warn.style.cssText = 'border-left:4px solid #fb8c00;background:#fff8e1;border-radius:4px;padding:0.6rem 0.9rem;margin-top:0.8rem;font-size:0.8rem;line-height:1.5';
      g('cc_result').appendChild(warn);
    }
    warn.innerHTML =
      '⚠ このツールの許容電流は <b>JCS 0168-2 の 40℃ 基準・1条布設</b>の値です' +
      '（ケーブルラックは「単条」＝気中・暗渠と同値）。' +
      '周囲温度補正・多条布設低減は<b>含まれていません</b>。' +
      '実際の許容電流は「実許容電流 = 基準許容電流 × 周囲温度補正係数 × 多条布設低減係数」で必ず補正してください。' +
      '係数はリファレンス「ケーブル許容電流と補正係数」を参照。';

    g('cc_result').style.display = 'block';
  };
})();
