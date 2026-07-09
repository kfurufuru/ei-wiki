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
  // 許容電流 [管路, 気中, ラック]（JIS C 3605 / 内線規程参考値）
  // CVTは撚合せにより気中・ラックでCV 3芯より若干有利だが保守的に同値を採用
  var CABLE_DB = {
    cv:  [
      { size: 2.0,  amp: [19,  26,  24],  R: 9.61  },
      { size: 3.5,  amp: [26,  36,  33],  R: 5.48  },
      { size: 5.5,  amp: [34,  47,  43],  R: 3.49  },
      { size: 8,    amp: [42,  58,  53],  R: 2.40  },
      { size: 14,   amp: [61,  84,  77],  R: 1.37  },
      { size: 22,   amp: [78,  107, 98],  R: 0.872 },
      { size: 38,   amp: [105, 144, 132], R: 0.505 },
      { size: 60,   amp: [135, 185, 170], R: 0.320 },
      { size: 100,  amp: [175, 240, 220], R: 0.193 },
    ],
    cvt: [
      { size: 14,   amp: [61,  88,  80],  R: 1.37  },
      { size: 22,   amp: [78,  112, 103], R: 0.872 },
      { size: 38,   amp: [105, 152, 139], R: 0.505 },
      { size: 60,   amp: [135, 194, 178], R: 0.320 },
      { size: 100,  amp: [175, 252, 231], R: 0.193 },
      { size: 150,  amp: [210, 302, 277], R: 0.128 },
      { size: 200,  amp: [240, 346, 317], R: 0.096 },
      { size: 250,  amp: [270, 385, 353], R: 0.077 },
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
      '⚠ このツールの許容電流は <b>40℃ 基準・単独条布設の基準値</b>です。' +
      '周囲温度補正・多条布設低減は<b>含まれていません</b>。' +
      '実際の許容電流は「実許容電流 = 基準許容電流 × 周囲温度補正係数 × 多条布設低減係数」で必ず補正してください。' +
      '係数はリファレンス「ケーブル許容電流と補正係数」を参照。';

    g('cc_result').style.display = 'block';
  };
})();
