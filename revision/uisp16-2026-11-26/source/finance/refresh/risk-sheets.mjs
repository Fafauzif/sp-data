/** Write auditable sensitivity and Monte Carlo results in native Excel sheets. */
const PALETTE = { green: "#185544", dark: "#15382C", ink: "#243D35", pale: "#EEF5F0", grey: "#DFE9E3" };
const MONEY = '#,##0.0;[Red](#,##0.0);0.0';
const INTEGER = '#,##0;[Red](#,##0);0';
const PERCENT = '0.0%;[Red](0.0%);0.0%';
const MULTIPLE = '0.00"x"';
const FONT = 'Aptos';

function put(sheet, row, column, records, property = 'values') {
  if (records.length) sheet.getRangeByIndexes(row-1, column-1, records.length, records[0].length)[property] = records;
}

function shade(sheet, range, dark = false) {
  sheet.getRange(range).format = {
    fill: dark ? PALETTE.dark : PALETTE.pale,
    font: { name: FONT, bold: true, color: dark ? '#FFFFFF' : PALETTE.ink },
    verticalAlignment: 'center',
    wrapText: true,
  };
}

function mergedText(sheet, range, copy, dark = false) {
  sheet.mergeCells(range);
  const area = sheet.getRange(range);
  area.values = [[copy]];
  area.format = {
    fill: dark ? PALETTE.dark : PALETTE.pale,
    font: { name: FONT, bold: dark, color: dark ? '#FFFFFF' : PALETTE.ink },
    verticalAlignment: 'center',
    wrapText: true,
  };
}

function makeSheet(wb, name) {
  const sheet = wb.worksheets.add(name);
  sheet.showGridLines = false;
  sheet.tabColor = PALETTE.green;
  return sheet;
}

function safeMoney(value, scale) {
  return Number.isFinite(value) ? value / scale : null;
}

function col(index) {
  let key = "";
  for (let i = index; i > 0; i = Math.floor((i-1)/26)) {
    key = String.fromCharCode(65 + (i-1)%26) + key;
  }
  return key;
}

function writeSensitivity(wb, analysis, {moneyScale, moneyUnit, refreshText, baseMeasureRef}) {
  const sheet = makeSheet(wb, 'Sensitivity');
  const n = analysis.levels.length;
  const end = col(n+1);
  const middle = Math.floor(n / 2);
  const center = col(middle+2);
  sheet.getRange('A:A').format.columnWidth = 28;
  sheet.getRange('B:I').format.columnWidth = 14;
  mergedText(sheet, 'A1:I1', 'Sensitivitas pendapatan dan nilai proyek', true);
  sheet.getRange('A1').format.rowHeight = 28;
  mergedText(sheet, 'A2:I2', `Kas proyek setelah pajak, sebelum pendanaan, Tahun 0 ${analysis.startYear} hingga ${analysis.assessmentYear}. CAPM Base tetap.`);
  mergedText(sheet, 'A3:I3', 'Baris mengubah permintaan yang memenuhi syarat. Kolom mengubah tarif biaya pembeli dan komisi. Seluruh kombinasi menjalankan kembali model dan batas kapasitasnya.');
  mergedText(sheet, 'A4:I4', refreshText);
  sheet.getRange('A2:A4').format.rowHeight = 30;

  const firstRow = 6;
  const irrRow = firstRow + n + 3;
  put(sheet, firstRow, 1, [[`NPV (${moneyUnit})`, ...analysis.levels]]);
  put(sheet, firstRow+1, 1, analysis.cells.map((row,i) => [analysis.levels[i], ...row.map(v=>safeMoney(v.npv,moneyScale))]));
  put(sheet, irrRow, 1, [['IRR proyek', ...analysis.levels]]);
  put(sheet, irrRow+1, 1, analysis.cells.map((row,i) => [analysis.levels[i], ...row.map(v=>v.irr)]));
  for(const [row, fmt] of [[firstRow, MONEY], [irrRow, PERCENT]]) {
    shade(sheet, `A${row}:${end}${row}`, true);
    shade(sheet, `A${row+1}:A${row+n}`);
    sheet.getRange(`B${row}:${end}${row}`).setNumberFormat(MULTIPLE);
    sheet.getRange(`A${row+1}:A${row+n}`).setNumberFormat(MULTIPLE);
    sheet.getRange(`B${row+1}:${end}${row+n}`).setNumberFormat(fmt);
    shade(sheet, `${center}${row+1+middle}:${center}${row+1+middle}`);
    sheet.getRange(`${center}${row+1+middle}`).setNumberFormat(fmt);
  }
  const check = irrRow+n+2;
  put(sheet, check, 1, [['Selisih NPV pusat dan Base']]);
  if (baseMeasureRef) {
    put(sheet, check, 2, [[`=${center}${firstRow+1+middle}-(${baseMeasureRef})/${moneyScale}`]], 'formulas');
  } else {
    put(sheet, check, 2, [[analysis.cells[middle][middle].npv/moneyScale-analysis.center.npv/moneyScale]]);
  }
  sheet.getRange(`B${check}`).setNumberFormat(MONEY);
  const thresholdRow = check+2;
  mergedText(sheet, `A${thresholdRow}:I${thresholdRow}`, 'Ambang tarif saat NPV berubah tanda');
  const thresholdBody = analysis.feeBreakEven.map(row => [
    row.demand,
    row.points.length ? row.points.map(value=>value.toFixed(3)+'x').join(' / ') : 'Di luar rentang uji',
    row.lowerNpv / moneyScale,
    row.upperNpv / moneyScale,
  ]);
  put(sheet, thresholdRow+1, 1, [['Permintaan', 'Tarif impas', `NPV tarif rendah (${moneyUnit})`, `NPV tarif tinggi (${moneyUnit})`], ...thresholdBody]);
  shade(sheet, `A${thresholdRow+1}:D${thresholdRow+1}`, true);
  sheet.getRange(`A${thresholdRow+1}`).format.rowHeight = 39;
  sheet.getRange(`A${thresholdRow+2}:A${thresholdRow+1+n}`).setNumberFormat(MULTIPLE);
  sheet.getRange(`C${thresholdRow+2}:D${thresholdRow+1+n}`).setNumberFormat(MONEY);
  mergedText(sheet, `A${thresholdRow+n+3}:I${thresholdRow+n+3}`, 'IRR kosong berarti arus kas tidak memiliki satu IRR yang valid. Gunakan NPV untuk keputusan. Ambang diuji ulang pada kedua sisi perubahan tanda, dengan ketelitian pengali tarif 0,001x.');
  sheet.getRange(`A${thresholdRow+n+3}`).format.rowHeight = 29;
  return sheet;
}

function riskChart(sheet, bins, address, target, title, moneyScale) {
  if (!bins.length) return;
  const [first, last] = target;
  const [r,c] = address;
  const width=(bins[0].high-bins[0].low)/moneyScale;
  const precision=width>0 ? Math.max(0,Math.min(5,Math.ceil(-Math.log10(width))+1)) : 1;
  const label = (value) => (value/moneyScale).toFixed(precision);
  const rows = bins.map(bin => [label((bin.low+bin.high)/2),bin.count]);
  const block = [['Pusat rentang', 'Jumlah percobaan'], ...rows];
  put(sheet, r, c, block);
  shade(sheet, `${col(c)}${r}:${col(c+1)}${r}`);
  const chart = sheet.charts.add('bar', sheet.getRangeByIndexes(r-1,c-1,block.length,2));
  chart.title = title;
  chart.titleTextStyle.typeface = FONT;
  chart.titleTextStyle.fontSize = 13;
  chart.hasLegend = false;
  chart.series.items[0].fill = PALETTE.green;
  chart.xAxis = { axisType: 'textAxis', textStyle: {typeface:FONT,fontSize:8}, tickLabelInterval: 2 };
  chart.yAxis = { numberFormatCode: '#,##0', numberFormatSourceLinked: false, textStyle: {typeface:FONT,fontSize:9} };
  chart.setPosition(first, last);
}

function writeMonteCarlo(wb, analysis, {moneyScale, moneyUnit, refreshText}) {
  const sheet = makeSheet(wb, 'Monte Carlo');
  const keys = Object.keys(analysis.drivers);
  const first = 55;
  const last = first + analysis.rows.length;
  const quarter = 40;
  const cashflowColumn = 20;
  const labels = ['Percobaan', 'Akuisisi penjual', 'Permintaan', 'Tarif', 'Nilai barang', 'Biaya operasi',
    'Penyelesaian', 'Belanja modal', `NPV (${moneyUnit})`, 'IRR', 'Status IRR', 'Tahun melampaui CAPM', 'CAPM',
    `Pendanaan (${moneyUnit})`, `Kas min. terjadwal (${moneyUnit})`, `Kas min. tanpa dana (${moneyUnit})`,
    `Kesenjangan dana (${moneyUnit})`, 'Dana berisiko', `Pesanan ${analysis.assessmentYear}`,
    ...analysis.years.map(year=>`FCFF ${year}`), `Kebutuhan dana min. (${moneyUnit})`];
  if (keys.join(',') !== 'seller,demand,fee,aov,cost,completion,capex') throw new Error('Unexpected Monte Carlo driver columns');
  sheet.getRange('A:A').format.columnWidth = 27;
  sheet.getRange('B:H').format.columnWidth = 13;
  sheet.getRange('I:S').format.columnWidth = 17;
  sheet.getRange(`T:${col(labels.length)}`).format.columnWidth = 13;
  mergedText(sheet, 'A1:H1', 'Monte Carlo | Nilai proyek dan risiko pendanaan', true);
  sheet.getRange('A1').format.rowHeight = 27;
  mergedText(sheet, 'A2:Q2', `${analysis.selector} · ${analysis.n} percobaan · seed ${analysis.seed} · ${analysis.years[0]}–${analysis.assessmentYear} · ${moneyUnit}`);
  mergedText(sheet, 'A3:Q3', analysis.method);
  mergedText(sheet, 'A4:Q4', refreshText);
  sheet.getRange('A2:A4').format.rowHeight = 23;

  put(sheet, first, 1, [labels]);
  const data = analysis.rows.map(row=>[
    row.id, ...keys.map(key=>row.multipliers[key]), safeMoney(row.npv,moneyScale), row.irr,
    row.irrStatus, row.crossing, row.capm, ...[row.funding,row.cashMin,row.cashMinUnfunded,row.fundingGap].map(value=>safeMoney(value,moneyScale)),
    row.fundingAtRisk === null ? null : +row.fundingAtRisk, row.endingOrders,
    ...row.cashflows.map(value=>safeMoney(value,moneyScale)), safeMoney(row.fundingNeeded,moneyScale),
  ]);
  for(let offset=0;offset<data.length;offset+=1000) put(sheet,first+1+offset,1,data.slice(offset,offset+1000));
  shade(sheet, `A${first}:${col(labels.length)}${first}`, true);
  sheet.getRange(`A${first}`).format.rowHeight = 30;
  sheet.getRange(`B${first+1}:H${last}`).setNumberFormat(MULTIPLE);
  for(const column of ['I','N','O','P','Q']) sheet.getRange(`${column}${first+1}:${column}${last}`).setNumberFormat(MONEY);
  for(const column of ['J','M']) sheet.getRange(`${column}${first+1}:${column}${last}`).setNumberFormat(PERCENT);
  sheet.getRange(`T${first+1}:${col(labels.length)}${last}`).setNumberFormat(MONEY);
  sheet.getRange(`S${first+1}:S${last}`).setNumberFormat(INTEGER);

  const range = (column) => `$${column}$${first+1}:$${column}$${last}`;
  put(sheet, 6, 1, [['Distribusi', 'P5', 'P50', 'P95', 'n']]);
  shade(sheet,'A6:E6',true);
  const measures = [
    [`NPV (${moneyUnit})`, 'I'], ['IRR valid','J'], [`Dana disetor (${moneyUnit})`, 'N'],
    [`Kas minimum terjadwal (${moneyUnit})`,'O'], [`Kas minimum tanpa dana (${moneyUnit})`,'P'],
    [`Kesenjangan dana (${moneyUnit})`,'Q'], [`Dana min. tanpa cadangan (${moneyUnit})`,col(labels.length)],
  ];
  for(const [i,[label,c]] of measures.entries()){
    const row=7+i, cells=range(c);
    put(sheet,row,1,[[label]]);
    put(sheet,row,2,[[...['0.05','0.50','0.95'].map(p=>`=IF(COUNT(${cells})>0,PERCENTILE(${cells},${p}),"")`),`=COUNT(${cells})`]],'formulas');
    sheet.getRange(`B${row}:D${row}`).setNumberFormat(c==='J'?PERCENT:MONEY);
  }
  put(sheet, 6, 7, [['Ukuran probabilitas','Jumlah','Penyebut','Proporsi']]);
  shade(sheet,'G6:J6',true);
  sheet.getRange('G:G').format.columnWidth = 24;
  const probability = [
    ['NPV positif',`=COUNTIF(${range('I')},">0")`,`=COUNT(${range('I')})`],
    ['IRR valid di atas CAPM',`=COUNTIF(${range('J')},">"&M${first+1})`,`=COUNT(${range('J')})`],
    ['Pendanaan berisiko',`=COUNTIF(${range('R')},"=1")`,`=COUNT(${range('R')})`],
    ['IRR tanpa akar',`=COUNTIF(${range('K')},"tidak_tersedia")`,`=COUNT(${range('I')})`],
    ['IRR tidak unik',`=COUNTIF(${range('K')},"lebih_dari_satu")`,`=COUNT(${range('I')})`],
    ['IRR tidak terdefinisi',`=COUNTIF(${range('K')},"tidak_terdefinisi")`,`=COUNT(${range('I')})`],
  ];
  probability.forEach(([name,num,den],i)=>{
    const row=7+i;
    put(sheet,row,7,[[name]]);
    put(sheet,row,8,[[num,den,`=IF(I${row}>0,H${row}/I${row},"")`]],'formulas');
  });
  sheet.getRange('J7:J12').setNumberFormat(PERCENT);
  put(sheet, 6, 12, [['IRR pertama melampaui CAPM', 'Jumlah']]);
  shade(sheet, 'L6:M6',true);
  sheet.getRange('L:L').format.columnWidth=25;
  Object.keys(analysis.summary.crossingDistribution).forEach((year,i)=>{
    const row=7+i;
    put(sheet,row,12,[[Number(year)]]);
    put(sheet,row,13,[[`=COUNTIF(${range('L')},L${row})`]],'formulas');
  });
  const finalCrossingRow=7+Object.keys(analysis.summary.crossingDistribution).length;
  put(sheet,finalCrossingRow,12,[['Tidak tercapai']]);
  put(sheet,finalCrossingRow,13,[[`=COUNT(${range('I')})-SUM(M7:M${finalCrossingRow-1})`]],'formulas');

  put(sheet, 15, 1, [['Driver', 'Rendah', 'Modus', 'Tinggi', 'Adopsi', 'Tekanan biaya', 'Korelasi NPV', 'Korelasi gap']]);
  shade(sheet,'A15:H15',true);
  const assoc = Object.fromEntries(analysis.riskDrivers.map(r=>[r.key,r]));
  put(sheet,16,1,keys.map(key=>[analysis.drivers[key].label,...analysis.drivers[key].bounds,
    ...analysis.drivers[key].loadings,assoc[key].npvCorrelation,assoc[key].fundingGapCorrelation]));
  sheet.getRange('B16:D22').setNumberFormat(MULTIPLE);
  sheet.getRange('E16:H22').setNumberFormat('0.00');
  sheet.getRange('A16:A22').format.wrapText = true;
  sheet.getRange('A16:A22').format.rowHeight = 24;
  mergedText(sheet, 'A23:H23', 'Rentang dan bobot korelasi adalah asumsi. Korelasi hasil bersifat deskriptif dalam model.');
  sheet.getRange('A23').format.rowHeight=22;

  put(sheet,19,12,[['Stabilitas NPV', `P50 (${moneyUnit})`, '% NPV positif']]);
  shade(sheet,'L19:N19',true);
  if (analysis.stability) {
    put(sheet,20,12,[['Paruh pertama',safeMoney(analysis.stability.firstHalf.npv.p50,moneyScale),analysis.stability.firstHalf.positiveNpv.probability],
      ['Paruh kedua',safeMoney(analysis.stability.secondHalf.npv.p50,moneyScale),analysis.stability.secondHalf.positiveNpv.probability]]);
    sheet.getRange('M20:M21').setNumberFormat(MONEY);
    sheet.getRange('N20:N21').setNumberFormat(PERCENT);
  }
  riskChart(sheet,analysis.npvHistogram,[quarter,1],['A26','H38'],`Distribusi NPV (${moneyUnit})`,moneyScale);
  riskChart(sheet,analysis.gapHistogram,[quarter,10],['J26','Q38'],`Kesenjangan pendanaan (${moneyUnit})`,moneyScale);
  return {sheet, firstTrialRow:first+1, finalTrialRow:last, cashflowColumn};
}

export function addRiskSheets(wb, {
  simulation, sensitivity, moneyScale=1, moneyUnit='Rp juta',
  refreshText='Hasil memakai input dan seed pada proses pembaruan model. Jalankan ulang pembangun model setelah perubahan input.',
  baseMeasureRef=null,
}) {
  const opts = {moneyScale,moneyUnit,refreshText,baseMeasureRef};
  return {sensitivity:writeSensitivity(wb,sensitivity,opts),monteCarlo:writeMonteCarlo(wb,simulation,opts)};
}
