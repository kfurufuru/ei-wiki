// CV 3芯 600V ケーブルサイズ選定ツール
(function () {
  var CABLE_DATA = [
    { size: 2.0,  amp: [19,  26,  24],  R: 9.61  },
    { size: 3.5,  amp: [26,  36,  33],  R: 5.48  },
    { size: 5.5,  amp: [34,  47,  43],  R: 3.49  },
    { size: 8,    amp: [42,  58,  53],  R: 2.40  },
    { size: 14,   amp: [61,  84,  77],  R: 1.37  },
    { size: 22,   amp: [78,  107, 98],  R: 0.872 },
    { size: 38,   amp: [105, 144, 132], R: 0.505 },
    { size: 60,   amp: [135, 185, 170], R: 0.320 },
    { size: 100,  amp: [175, 240, 220], R: 0.193 },
  ];
  var X = 0.09; // Ω/km（固定）

  function g(id) { return document.getElementById(id); }

  window.calcCable = function () {
    var I      = parseFloat(g('cc_current').value);
    var L      = parseFloat(g('cc_length').value) / 1000;
    var vSel   = g('cc_voltage').value;
    var inst   = g('cc_install').value;
    var pf     = parseFloat(g('cc_pf').value);
    var vdLim  = parseFloat(g('cc_vd_limit').value);

    if (!I || !L || !pf || !vdLim) return;

    var instIdx  = { conduit: 0, air: 1, rack: 2 }[inst];
    var isSingle = (vSel === '200s' || vSel === '100');
    var V0       = parseFloat(vSel) || 200;
    var factor   = isSingle ? 2 : Math.sqrt(3);
    var sinθ     = Math.sqrt(Math.max(0, 1 - pf * pf));

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

    if (recommended) {
      var s = recommended.d.size < 10 ? recommended.d.size.toFixed(1) : String(recommended.d.size);
      resultMain.style.borderLeftColor = '#43a047';
      resultMain.style.background      = '#e8f5e9';
      resultSize.style.color           = '#1b5e20';
      resultSize.textContent = 'CV ' + s + ' mm²';
      resultSub.textContent  =
        '許容電流 ' + recommended.allowable + ' A（負荷の ' +
        ((recommended.allowable / I) * 100).toFixed(0) + '%）、電圧降下率 ' +
        recommended.vdRate.toFixed(2) + '%';
    } else {
      resultMain.style.borderLeftColor = '#fb8c00';
      resultMain.style.background      = '#fff8e1';
      resultSize.style.color           = '#e65100';
      resultSize.textContent = '100mm² 超 — 要別途検討';
      resultSub.textContent  = '表内サイズで条件を満たせません。並列敷設または電圧昇圧を検討してください。';
    }

    g('cc_result').style.display = 'block';
  };
})();
