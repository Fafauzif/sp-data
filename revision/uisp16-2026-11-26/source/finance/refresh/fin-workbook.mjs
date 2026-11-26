import fs from "node:fs/promises";
import {Workbook,SpreadsheetFile} from "@oai/artifact-tool";
import {defaults,fields,inputRows,rollups,periodMeta,clusterPlan,evaluate,years} from "./fin-model.mjs";
import {addRiskSheets} from "./risk-sheets.mjs";

const adjustedInput = process.env.LIHATDULU_INPUTS;
if (adjustedInput) Object.assign(defaults,JSON.parse(await fs.readFile(adjustedInput,"utf8")));
const wb=Workbook.create();
const tabs={};
for(const name of ["Ringkasan","Laporan","Operasi Bulanan","Pendanaan","CAPM","Ukuran Pasar","Asumsi","Kasus","Bukti Harga","Rujukan","QA Model","Metode"])tabs[name]=wb.worksheets.add(name);
const ink="#243D35",dark="#15382C",green="#185544",soft="#EEF5F0",line="#DFE9E3",blue="#155782",paleblue="#ECF5FA";
const fmtCash='#,##0.00;[Red](#,##0.00);"-"';
const fmtPrecise='#,##0.000000;[Red](#,##0.000000);"-"';
const fmtInt='#,##0;[Red](#,##0);"-"';
const pct='0.00%;[Red](0.00%);"-"';
function col(i){let name="";for(i++;i>0;i=Math.floor((i-1)/26))name=String.fromCharCode(65+(i-1)%26)+name;return name;}
const cell=(s,addr,v)=>{const rg=s.getRange(addr);if(typeof v==="string"&&v.startsWith("="))rg.formulas=[[v]];else rg.values=[[v]];};
const rg=(s,address)=>s.getRange(address);
const style=(s,address,properties)=>{const f=rg(s,address).format;for(const [k,v] of Object.entries(properties))f[k]=v;};
const setFmt=(s,address,f)=>rg(s,address).setNumberFormat(f);
function widths(s, entries){for(const [address,width] of Object.entries(entries))style(s,address,{columnWidth:width});}
function header(s,address){style(s,address,{fill:green,font:{bold:true,color:"#FFFFFF"},verticalAlignment:"center",rowHeight:24,wrapText:true});}
function merge(s,address,txt){rg(s,address).merge();cell(s,address.split(":")[0],txt);}
function start(s,title,subtitle,end="H",body="K48"){
  s.showGridLines=false;s.tabColor=green;
  style(s,`A1:${body}`,{font:{name:"Aptos",color:ink,size:10},verticalAlignment:"center"});
  merge(s,`A1:${end}2`,title);
  style(s,`A1:${end}2`,{fill:dark,font:{name:"Aptos",bold:true,size:19,color:"#FFFFFF"},rowHeight:18});
  merge(s,`A3:${end}3`,subtitle);
  style(s,`A3:${end}3`,{fill:soft,font:{name:"Aptos",color:green,size:10},rowHeight:22,wrapText:true});
}
function rows(s,at,data){const [r,c]=at;const n=data[0].length;s.getRangeByIndexes(r-1,c-1,data.length,n).values=data;}
function formulaRows(s,r,c,matrix){s.getRangeByIndexes(r-1,c-1,matrix.length,matrix[0].length).formulas=matrix;}
function compactRisk(wb,risk){
 const sens=wb.worksheets.add("Sensitivity");
 const mc=wb.worksheets.add("Monte Carlo");
 const {simulation:s,sensitivity:x}=risk;
 start(sens,"LihatDulu  /  Sensitivitas dua penggerak","Permintaan × monetisasi · Base, 2036 · nilai uang dalam Rp juta.","G","G33");
 widths(sens,{"A:A":28,"B:G":17});
 rows(sens,[6,1],[["Permintaan / tarif",...x.levels]]);header(sens,"A6:F6");
 rows(sens,[7,1],x.cells.map((line,i)=>[x.levels[i],...line.map(v=>v.npv)]));
 setFmt(sens,"B7:F11",fmtCash);style(sens,"D9",{fill:soft,font:{bold:true}});
 rows(sens,[14,1],[["IRR / tarif",...x.levels]]);header(sens,"A14:F14");
 rows(sens,[15,1],x.cells.map((line,i)=>[x.levels[i],...line.map(v=>v.irr??"Tidak ada")]));
 setFmt(sens,"B15:F19",pct);style(sens,"D17",{fill:soft,font:{bold:true}});
 setFmt(sens,"A7:A11",'0.00"x"');setFmt(sens,"A15:A19",'0.00"x"');
 cell(sens,"A23","Selisih pusat vs Base aktif");
 cell(sens,"B23",'=IF(AND(Ringkasan!C6="Base",Ringkasan!C7="Standar"),D9-Ringkasan!C12,"")');
 setFmt(sens,"B23",fmtPrecise);
 merge(sens,"A25:G26","Tidak ada batas NPV nol yang lolos dalam rentang. Tekan biaya operasi dan verifikasi penerimaan tarif sebelum menambah klaster.");
 style(sens,"A25:G26",{wrapText:true,rowHeight:18});
 start(mc,"LihatDulu  /  Monte Carlo","10.000 replikasi di kondisi Base · seed 12026 · proyeksi sampai 2036 · Rp juta","L","L58");
 widths(mc,{"A:A":38,"B:D":19,"E:E":23,"F:F":20,"G:L":17});
 rows(mc,[6,1],[["Ukuran","n","P5","P50","P95"]]);header(mc,"A6:E6");
 const q=s.summary;
 rows(mc,[7,1],[["NPV",q.npv.n,q.npv.p05,q.npv.p50,q.npv.p95],
  ["IRR bila unik",q.irr.n,q.irr.p05,q.irr.p50,q.irr.p95],
  ["Kas setelah pendanaan",q.fundedCash.n,q.fundedCash.p05,q.fundedCash.p50,q.fundedCash.p95],
  ["Kas tanpa pendanaan",q.unfundedCash.n,q.unfundedCash.p05,q.unfundedCash.p50,q.unfundedCash.p95],
  ["Gap likuiditas terhadap buffer",q.fundingGap.n,q.fundingGap.p05,q.fundingGap.p50,q.fundingGap.p95]]);
 setFmt(mc,"C7:E11",fmtCash);setFmt(mc,"C8:E8",pct);
 rows(mc,[14,1],[["Ambang","Kasus","Penyebut","Bagian"]]);header(mc,"A14:D14");
 rows(mc,[15,1],[["NPV > 0",q.positiveNpv.numerator,q.trials,q.positiveNpv.probability],
  ["IRR > CAPM, IRR diketahui",q.overHurdle.numerator,q.irr.n,q.overHurdle.probability??0],
  ["Belum melewati CAPM",q.neverCrosses,q.trials,q.neverCrosses/q.trials],
  ["Tidak ada IRR tersedia",q.irrUnavailable,q.trials,q.irrUnavailable/q.trials],
  ["Saldo kas di bawah buffer",q.fundingRisk.numerator,q.trials,q.fundingRisk.probability]]);
 setFmt(mc,"D15:D19",pct);
 rows(mc,[22,1],[["Penggerak","Minimum","Modus","Maksimum"]]);header(mc,"A22:D22");
 rows(mc,[23,1],Object.values(s.drivers).map(d=>[d.label,...d.bounds]));
 setFmt(mc,"B23:D29",'0.00"x"');
 const hist=(c,label,a,startAt,endAt)=>{
  rows(mc,[31,c],[[label,"Kasus"],...a.map(b=>[`${b.low.toFixed(0)} s.d. ${b.high.toFixed(0)}`,b.count])]);
  const chart=mc.charts.add("column",mc.getRange(`${col(c-1)}31:${col(c)}${31+a.length}`));
  chart.title=label;chart.hasLegend=false;chart.setPosition(startAt,endAt);
 };
 hist(1,"Distribusi NPV (Rp jt)",s.npvHistogram,"G6","M18");
 hist(4,"Distribusi gap kas (Rp jt)",s.gapHistogram,"G21","M33");
 merge(mc,"G35:L39","Tidak semua replikasi memiliki IRR. Persentil IRR memakai hanya replikasi yang mempunyai satu nilai valid. Angka ini merupakan frekuensi skenario, dengan parameter dan korelasi yang diasumsikan.");
 style(mc,"G35:L39",{wrapText:true});
 merge(mc,"A49:L50","Untuk seluruh penggerak, arus kas, dan pembaruan 10.000 replikasi setelah input diedit, jalankan refresh-risk.mjs dari paket sumber. Lembar ini menyimpan hasil per replikasi.");
 style(mc,"A49:L50",{wrapText:true,rowHeight:18});
 rows(mc,[55,1],[["Uji ke","NPV","IRR","Tahun melewati","Kas minimum","Funding gap"]]);header(mc,"A55:F55");
 rows(mc,[56,1],s.rows.map(r=>[r.id,r.npv,r.irr,r.crossing,r.cashMin,r.fundingGap]));
 setFmt(mc,"B56:B10055",fmtCash);setFmt(mc,"C56:C10055",pct);setFmt(mc,"E56:F10055",fmtCash);
 mc.freezePanes.freezeRows(6);
}
const quoted=(s,ref)=>`'${s}'!${ref}`;
const assum=Object.fromEntries(inputRows.map(([k],i)=>[k,7+i]));
const ia=k=>quoted("Asumsi",`$F$${assum[k]}`);
const planHeader=7+inputRows.length+4;
const planValue=planHeader+1;
const periodsBegin=7;
const firstColumn=9;
const fieldCols=Object.fromEntries(fields.map(([k],i)=>[k,col(firstColumn+i)]));
const monthLast=periodsBegin+120;
const monthRange=k=>quoted("Operasi Bulanan",`$${fieldCols[k]}$${periodsBegin}:$${fieldCols[k]}$${monthLast}`);
const refM=(k,m)=>quoted("Operasi Bulanan",`${fieldCols[k]}${periodsBegin+m}`);
const monthRangeIndex=quoted("Operasi Bulanan",`$A$${periodsBegin}:$A$${monthLast}`);
const monthRangeYear=quoted("Operasi Bulanan",`$B$${periodsBegin}:$B$${monthLast}`);

{
 const s=tabs.Asumsi;
 start(s,"LihatDulu  /  Asumsi","Sel biru dapat diedit. Tiga kasus memakai data acuan yang sama dan keputusan perencanaan berbeda.","H","H125");
 widths(s,{"A:A":25,"B:B":49,"C:F":15,"G:G":13,"H:H":60});
 rows(s,[6,1],[["Kode","Driver","Downside","Base","Upside","Pemilihan aktif","Satuan","Asal dan penyesuaian"]]);header(s,"A6:H6");
 rows(s,[7,1],inputRows.map(([k,label,down,base,up,unit,source])=>[k,label,defaults[k].Downside,defaults[k].Base,defaults[k].Upside,null,unit,source]));
 formulaRows(s,7,6,inputRows.map(([k])=>{const r=assum[k];return [`=INDEX(C${r}:E${r},1,MATCH('Ringkasan'!$C$6,$C$6:$E$6,0))`];}));
 style(s,`C7:E${6+inputRows.length}`,{fill:paleblue,font:{color:blue}});
 style(s,`H7:H${6+inputRows.length}`,{wrapText:true});
 for(const [k,,,,,unit] of inputRows)setFmt(s,`C${assum[k]}:F${assum[k]}`,unit==="%"?pct:unit==="Rp jt"?fmtPrecise:unit==="orang"?fmtInt:fmtCash);
 rows(s,[planHeader,1],[["Tahun operasi","2027","2028","2029","2030","2031","2032","2033","2034","2035","2036"],
                ["Maksimum klaster",...(defaults.clusterPlan??clusterPlan)]]);
 header(s,`A${planHeader}:K${planHeader}`);style(s,`B${planValue}:K${planValue}`,{fill:paleblue,font:{color:blue}});
 merge(s,`A${planValue+2}:H${planValue+2}`,"Enam bulan pertama satu klaster. Pada dua tahun awal, batas naik maksimal tiap enam bulan sesuai kesiapan.");
 merge(s,`A${planValue+3}:H${planValue+3}`,"Batas lokasi rencana tidak sama dengan klaster aktif. Perluasan menunggu pesanan dan buffer kas.");
 s.freezePanes.freezeRows(6);
}
{
 const s=tabs.CAPM;
 start(s,"LihatDulu  /  Tingkat diskonto","IDR nominal · acuan 26 November 2026 · hutang pembiayaan = 0","E","E31");
 widths(s,{"A:A":43,"B:B":18,"C:C":18,"D:D":53,"E:E":43});
 rows(s,[6,1],[["Komponen","Nilai","Satuan","Basis","Perlakuan"]]);header(s,"A6:E6");
 const spec=[
  ["Yield SBN benchmark 10 tahun",`=${ia("sbnYield")}`,"%","Indonesia 10Y, 25 Nov 2026","Penutupan sesi"],
  ["Sovereign default spread",`=${ia("defaultSpread")}`,"%","Damodaran Juli 2026, Indonesia Baa2","Input dibulatkan, USD rating proxy"],
  ["Risk-free rupiah disesuaikan","=B7-B8","%","Yield SBN dikurangi default spread","Proksi risiko bebas dalam IDR"],
  ["Equity risk premium pasar matang",`=${ia("matureErp")}`,"%","Damodaran Juli 2026","Premi pasar matang, sebelum CRP"],
  ["Premi risiko negara",`=${ia("countryRisk")}`,"%","Damodaran Juli 2026, Indonesia Baa2","CRP tambahan, input dibulatkan"],
  ["Lambda Indonesia",`=${ia("lambda")}`,"x","Kegiatan dan pelanggan di Indonesia","Asumsi 1, bukan estimasi empiris"],
  ["Beta levered industri",`=${ia("marketBeta")}`,"x","Software (Internet), Global Jan 2026","150 perusahaan; banding proksi asset-light"],
  ["D/E industri",`=${ia("marketDebt")}`,"%","Software (Internet), Global Jan 2026","Rasio pasar yang dipublikasikan"],
  ["Pajak marjinal dataset beta",`=${ia("marketTax")}`,"%","Basis metode industri Damodaran","Bukan tarif PPh LihatDulu"],
  ["Beta unlevered","=B13/(1+(1-B15)*B14)","x","Leverage dihapus dari beta industri","Beta tidak disesuaikan kas"],
  ["D/E target","=0","%","Struktur pendanaan tanpa utang","Kebijakan model"],
  ["Beta target","=B16*(1+(1-Asumsi!F"+assum.taxRate+")*B17)","x","Relever dengan D/E target","Dengan D/E nol, beta tetap"],
  ["Cost of equity","=B9+B18*B10+B12*B11","%","Rf + beta × ERP mature + lambda × CRP","Tidak menambah ERP Indonesia lagi"],
  ["Bobot ekuitas","=1/(1+B17)","%","D/E target","Ekuitas 100%"],
  ["Bobot utang","=1-B20","%","D/E target","Utang 0%"],
  ["WACC","=B19*B20","%","Tanpa utang, sama dengan Ke","Ambang proyek, bukan target VC"],
 ];
 for(let i=0;i<spec.length;i++){
   const [label,form,unit,source,remark]=spec[i];const r=7+i;
   rows(s,[r,1],[[label,null,unit,source,remark]]);cell(s,`B${r}`,form);setFmt(s,`B${r}`,unit==="%"?pct:fmtCash);
 }
 style(s,"A19:E19",{fill:soft,font:{bold:true}});style(s,"A22:E22",{fill:soft,font:{bold:true}});
 merge(s,"A25:E25","Gunakan industri global sebagai proksi beta karena sampel emiten Indonesia yang sepadan tidak memadai.");
 merge(s,"A26:E26","Country risk memakai data Juli 2026 dan tidak mengulang spread dalam premi pasar matang.");
}
{
 const s=tabs["Operasi Bulanan"];
 const last=col(firstColumn+fields.length-1);
 start(s,"LihatDulu  /  Operasi bulanan","Tahun 0 dan 120 bulan kalender. Kolom Rp juta nominal; seluruh angka merupakan hasil skenario.","J",`${last}${monthLast}`);
 widths(s,{"A:F":12,"G:I":15,[`J:${last}`]:17});
 const headings=["Bulan model","Tahun","Bulan kal.","Tahun model","Tutup tahun","Bursa rencana","Batas klaster","Musim","Cair lanjutan",...fields.map(([,t,u])=>t+" · "+u)];
 rows(s,[6,1],[headings]);header(s,`A6:${last}6`);style(s,`A6:${last}6`,{rowHeight:58});
 const formulaMap={"Iff":"IF",iff:"IF",min:"MIN",max:"MAX",power:"POWER",mod:"MOD",and:"AND",or:"OR",floor:"INT",round:"ROUND",roundUp:"ROUNDUP",abs:"ABS"};
 const override={m:"A",year:"B",mo:"C",y:"D",close:"E",bursa:"F",plan:"G",season:"H",allowFunding:"I"};
 const matrix=[];
 const baseValues=[];
 for(let m=0;m<=120;m++){
  const r=periodsBegin+m, p=periodMeta(m);
  baseValues.push([m,p.year,p.mo,p.y,p.close,p.bursa,null,p.season,null]);
  matrix.push(fields.map(([_k,,,expression])=>{
   const term=expression.replace(/\b([apzc])\.(\w+)\b/g,(_full,obj,key)=>{
     if(obj==="a")return ia(key);
     if(obj==="p")return m>0?`${fieldCols[key]}${r-1}`:"0";
     if(obj==="z")return `${fieldCols[key]}${r}`;
     if(key==="capexPast")return m>36?`${fieldCols.assetSum}${r-37}`:"0";
     return override[key]?`${override[key]}${r}`:"1";
   }).replace(/\b(iff|min|max|power|mod|and|or|floor|round|roundUp|abs)\(/g,(_tok,n)=>formulaMap[n]+"(").replaceAll("==","=");
   return "="+term;
  }));
 }
 rows(s,[periodsBegin,1],baseValues);
 formulaRows(s,periodsBegin,7,baseValues.map((_,m)=>{const r=periodsBegin+m;
  return [`=IF(A${r}=0,0,MAX(1,INT(IF(D${r}<3,ROUNDUP(A${r}/6,0),INDEX(Asumsi!$B$${planValue}:$K$${planValue},1,D${r}))*IF(Ringkasan!$C$6="Downside",0.8,IF(Ringkasan!$C$6="Upside",1.15,1)))))`];}));
 formulaRows(s,periodsBegin,9,baseValues.map(()=>[`=IF(Ringkasan!$C$7="Terbatas",0,1)`]));
 formulaRows(s,periodsBegin,firstColumn+1,matrix);
 for(const [k,,unit] of fields)setFmt(s,`${fieldCols[k]}${periodsBegin}:${fieldCols[k]}${monthLast}`,unit==="Rp jt"||unit==="FTE"?fmtCash:fmtInt);
 for (const k of ["orders","marketplaceRevenue","fcff","cash","checkBS","checkStock"]){
   style(s,`${fieldCols[k]}${periodsBegin}:${fieldCols[k]}${monthLast}`,{fill:soft,font:{bold:true,color:green}});
 }
 s.freezePanes.freezeRows(6);
}
const reportRows=[
 ["orders","Pesanan selesai","pesanan"],["clusters","Klaster aktif akhir tahun","klaster"],["dealer","Penjual rutin aktif akhir tahun","penjual"],
 ["listingPassed","Listing terbit","unit"],["gmv","GMV barang","Rp jt"],["buyerRevenue","Biaya layanan pembeli","Rp jt"],
 ["sellerRevenue","Komisi penjual","Rp jt"],["marketplaceRevenue","Pendapatan marketplace","Rp jt"],["b2bRevenue","Pendapatan katalog B2B","Rp jt"],["revenue","Total pendapatan","Rp jt"],
 ["payCost","Biaya pembayaran dan payout","Rp jt"],["media","Biaya media dan pemrosesan","Rp jt"],["salariesDirect","Tenaga langsung katalog/dukungan","Rp jt"],["b2bCost","Biaya layanan B2B","Rp jt"],
 ["grossProfit","Pendapatan dikurangi biaya layanan","Rp jt"],["marketing","Pemasaran dan akuisisi","Rp jt"],["fixed","Operasional tetap dan administrasi","Rp jt"],["ebitda","EBITDA","Rp jt"],
 ["da","Penyusutan","Rp jt"],["ebit","Laba operasi","Rp jt"],["tax","Pajak kas","Rp jt"],["earnings","Laba bersih","Rp jt"],
 ["deltaNwc","Perubahan modal kerja nonkas","Rp jt"],["opCash","Arus kas operasi","Rp jt"],["capex","Belanja aset","Rp jt"],["fcff","Arus kas proyek sebelum pendanaan","Rp jt"],
 ["funding","Pendanaan bersih","Rp jt"],["cash","Kas bebas akhir periode","Rp jt"],["fundingGap","Defisit terhadap buffer akhir tahun","Rp jt"],
 ["ar","Piutang","Rp jt"],["prepaid","Pembayaran di muka","Rp jt"],["ppene","Aset tetap bersih","Rp jt"],["suspense","Dana titipan pada penyedia","Rp jt"],["assets","Total aset model","Rp jt"],
 ["ap","Utang usaha","Rp jt"],["deferred","Pendapatan diterima di muka","Rp jt"],["custLiab","Kewajiban dana titipan","Rp jt"],["equity","Modal yang disetor dan bantuan modal","Rp jt"],["retained","Saldo laba ditahan","Rp jt"],["liabEquity","Total liabilitas dan ekuitas","Rp jt"],
 ["balanceCheck","Cek persamaan neraca","Rp jt"],["cashCheck","Cek mutasi kas","Rp jt"],["contribution","Kontribusi marketplace pra-akuisisi","Rp jt"],["contributionAfter","Kontribusi setelah akuisisi","Rp jt"],
 ["unitContribution","Kontribusi pra-akuisisi per pesanan","Rp"],["unitAfter","Kontribusi pasca-akuisisi per pesanan","Rp"],["cac","Akuisisi per pesanan selesai","Rp"],["event","Bursa Pindahan","acara"],["eventSales","Pesanan selesai asal Bursa","pesanan"],["eventCostOnly","Biaya Bursa nominal","Rp jt"],["eventCac","Biaya Bursa per pesanan atribusi","Rp"],
 ["beAnnual","Volume impas tahunan indikatif","pesanan"],["cumCash","FCFF kumulatif","Rp jt"],["cumDiscounted","FCFF terdiskonto kumulatif","Rp jt"],["sc","Perubahan tanda arus kas","n"],["ls","Tanda terakhir nonnol","flag"],
 ["irr","IRR kumulatif","%"],["cross","Tahun melewati hurdle","tahun"],["pb","Payback nominal bila tercapai","tahun"],["pbDiscount","Payback terdiskonto bila tercapai","tahun"]
];
const rr=Object.fromEntries(reportRows.map(([k],i)=>[k,7+i]));
const lastAnnual="M";
const ann=(k,c=lastAnnual)=>quoted("Laporan",`${c}${rr[k]}`);
{
 const s=tabs.Laporan;
 start(s,"LihatDulu  /  Laporan tahunan","Tahun 0 persiapan 2026. Proyeksi 2027–2036 mengikuti skenario aktif. Tidak ada terminal value.","M","M78");
 widths(s,{"A:A":46,"B:B":12,"C:M":15});
 rows(s,[6,1],[["Pos laporan","Satuan",...years]]);header(s,"A6:M6");
 rows(s,[7,1],reportRows.map(([,label,unit])=>[label,unit]));
 for(const [i,[id,,unit]] of reportRows.entries()){
  const r=7+i;const formulas=[];
  for(const [p,year] of years.entries()){
   const l=col(2+p),prev=col(1+p), ref=k=>l+rr[k], prior=k=>p?prev+rr[k]:"0";
   let f;
   if(fieldCols[id]&&rollups.has(id))f=`SUMIF(${monthRangeYear},${l}$6,${monthRange(id)})`;
   else if(fieldCols[id]&&id!=="irr")f=refM(id,p*12);
   else f=({
    grossProfit:`${ref("revenue")}-${ref("payCost")}-${ref("media")}-${ref("salariesDirect")}-${ref("b2bCost")}`,
    custLiab:ref("suspense"),
    balanceCheck:`${ref("assets")}-${ref("liabEquity")}`,
    cashCheck:`${ref("cash")}-${prior("cash")}-${ref("fcff")}-${ref("funding")}`,
    unitContribution:`IF(${ref("orders")}>0,1000000*${ref("contribution")}/${ref("orders")},"")`,
    unitAfter:`IF(${ref("orders")}>0,1000000*${ref("contributionAfter")}/${ref("orders")},"")`,
    cac:`IF(${ref("orders")}>0,1000000*${ref("marketing")}/${ref("orders")},"")`,
    eventCostOnly:`${ref("event")}*${ia("eventCost")}*(1+${ia("costInflation")})^${Math.max(0,p-1)}`,
    eventCac:`IF(${ref("eventSales")}>0,1000000*${ref("eventCostOnly")}/${ref("eventSales")},"")`,
    beAnnual:`IF(AND(ISNUMBER(${ref("unitAfter")}),${ref("unitAfter")}>0),ROUNDUP(${ref("fixed")}*1000000/MAX(0.01,${ref("unitAfter")}),0),"")`,
    cumCash:`SUM($C${rr.fcff}:${ref("fcff")})`,
    cumDiscounted:p?`$C${rr.fcff}+NPV(CAPM!$B$22,$D${rr.fcff}:${ref("fcff")})`:`$C${rr.fcff}`,
    sc:p?`${prior("sc")}+IF(AND(${prior("ls")}<>0,SIGN(${ref("fcff")})<>0,${prior("ls")}<>SIGN(${ref("fcff")})),1,0)`:"0",
    ls:`IF(${ref("fcff")}=0,${prior("ls")},SIGN(${ref("fcff")}))`,
    irr:p?`IF(${ref("sc")}=1,IFERROR(IRR($C${rr.fcff}:${ref("fcff")}),""),"")`:'""',
    cross:`IF(AND(ISNUMBER(${ref("irr")}),${ref("irr")}>CAPM!$B$22),${l}$6,"")`,
    pb:p?`IF(AND(${prior("cumCash")}<0,${ref("cumCash")}>=0,${ref("fcff")}>0),${p-1}-${prior("cumCash")}/${ref("fcff")},"")`:'""',
    pbDiscount:p?`IF(AND(${prior("cumDiscounted")}<0,${ref("cumDiscounted")}>=0,${ref("fcff")}>0),${p-1}-${prior("cumDiscounted")}/(${ref("fcff")}/(1+CAPM!$B$22)^${p}),"")`:'""'
   })[id];
   formulas.push("="+f);
  }
  formulaRows(s,r,3,[formulas]);
  setFmt(s,`C${r}:M${r}`,unit==="%"?pct:unit==="Rp jt"||id==="pb"||id==="pbDiscount"?fmtCash:fmtInt);
  if(["marketplaceRevenue","revenue","grossProfit","ebitda","earnings","fcff","cash","assets","liabEquity","irr"].includes(id))
    style(s,`A${r}:M${r}`,{fill:soft,font:{bold:true,color:green}});
 }
 s.freezePanes.freezeRows(6);
}
{
 const s=tabs["Ukuran Pasar"];
 start(s,"LihatDulu  /  TAM, SAM dan SOM","Pendapatan marketplace per tahun. Skenario; tidak termasuk langganan B2B atau ongkos angkut.","D","D25");
 widths(s,{"A:A":43,"B:B":20,"C:C":17,"D:D":72});
 rows(s,[6,1],[["Komponen","Skenario aktif","Satuan","Basis"]]);header(s,"A6:D6");
 const rt=[
  ["Belanja mebel Susenas",`=${ia("furnitureSpend")}*1000000`,"Rp/orang/bln","Susenas Maret 2026, Tabel 3.4"],
  ["Jumlah penduduk",`=${ia("population")}`,"orang","Proyeksi BPS pertengahan 2026"],
  ["Benchmark belanja kategori","=B7*B8*12/1000000","Rp jt/thn","Pengeluaran kategori yang dianualkan, mencakup mebel umum"],
  ["Porsi belanja digunakan untuk barang bekas",`=${ia("useShare")}`,"%","Asumsi model. Data pangsa bekas sepadan belum tersedia."],
  ["Estimasi GMV nasional unit bekas","=B9*B10","Rp jt/thn","Asumsi satu unit per transaksi"],
  ["Nilai unit setelah negosiasi",`=${ia("tablePrice")}*${ia("tableMix")}+${ia("chairPrice")}*${ia("chairMix")}+${ia("rackPrice")}*${ia("rackMix")}+${ia("cabinetPrice")}*(1-${ia("tableMix")}-${ia("chairMix")}-${ia("rackMix")})`,"Rp jt/order","OLX 24 tawaran Depok + asumsi bauran dan negosiasi"],
  ["TAM, pendapatan platform nasional",`=B11/B12*${ia("buyerFee")}+B11*${ia("commission")}`,"Rp jt/thn","Jumlah pesanan setara × biaya pembeli + GMV × komisi"],
  ["Porsi pasar Jabodetabek yang dapat dilayani",`=${ia("serviceShare")}`,"%","Asumsi geografi dan densitas permintaan. Porsi penduduk 2025 sekitar 11,38% sebagai patokan."],
  ["SAM, pendapatan platform terlayani","=B13*B14","Rp jt/thn","TAM × asumsi pangsa cakupan layanan"],
  ["SOM tahun ketiga, 2029",`=${ann("marketplaceRevenue","F")}`,"Rp jt/thn","Sama persis dengan pendapatan marketplace pada Laporan 2029"],
  ["Pesanan selesai tahun ketiga",`=${ann("orders","F")}`,"pesanan","Batas permintaan, barang, dukungan dan slot di Operasi Bulanan"],
  ["Klaster aktif akhir tahun ketiga",`=${ann("clusters","F")}`,"klaster","Buka klaster sesuai pesanan dan buffer kas pada skenario"],
  ["Rasio SOM / SAM","=B16/B15","%","Membandingkan hasil dengan potensi; tidak menentukan SOM"],
 ];
 for(let i=0;i<rt.length;i++){const [a,b,c,d]=rt[i];rows(s,[7+i,1],[[a,null,c,d]]);cell(s,`B${7+i}`,b);setFmt(s,`B${7+i}`,c==="%"?pct:c==="Rp jt/order"?fmtPrecise:c==="orang"||c==="pesanan"||c==="klaster"?fmtInt:fmtCash);}
 for(const r of [13,15,16])style(s,`A${r}:D${r}`,{fill:soft,font:{bold:true}});
}
{
 const s=tabs.Pendanaan;
 start(s,"LihatDulu  /  Pendanaan dan runway","Pencairan merupakan skenario bersyarat. Hibah dasar nol; tidak ada bunga, utang atau konversi.","I","I41");
 widths(s,{"A:A":24,"B:E":18,"F:F":32,"G:I":18});
 rows(s,[6,1],[["Tahap","Bulan model","Bruto","Biaya","Neto","Penggunaan utama","Kas sebelum cair","Kas setelah cair","Runway indikatif"]]);header(s,"A6:I6");
 const stages=[
  ["Pendiri/non-dilutif","founderGross","Persiapan dan pengujian UI Depok"],
  ["Pre-seed","preGross","Akuisisi lokal dan dukungan tahap kedua"],
  ["Seed","seedGross","Replikasi klaster setelah milestone"],
 ];
 for(let i=0;i<stages.length;i++){
  const [label,key,use]=stages[i], r=i+7;
  rows(s,[r,1],[[label,null,null,null,null,use]]);
  formulaRows(s,r,2,[[`=IF(SUM(${monthRange(key)})>0,SUMIF(${monthRange(key)},">0",${monthRangeIndex}),"")`,`=SUM(${monthRange(key)})`,i?`=C${r}*${ia("fundFee")}`:"=0",`=C${r}-D${r}`]]);
  formulaRows(s,r,7,[[`=IF(C${r}>0,INDEX(${monthRange("cash")},B${r}+1)-INDEX(${monthRange("funding")},B${r}+1),"")`,
    `=IF(C${r}>0,INDEX(${monthRange("cash")},B${r}+1),"")`,
    `=IF(AND(C${r}>0,AVERAGE(INDEX(${monthRange("fcff")},MIN(B${r}+2,121)):INDEX(${monthRange("fcff")},MIN(B${r}+4,121)))<0),H${r}/-AVERAGE(INDEX(${monthRange("fcff")},MIN(B${r}+2,121)):INDEX(${monthRange("fcff")},MIN(B${r}+4,121))),"")`]]);
 }
 rows(s,[12,1],[["Putaran","Pre-money","Ekuitas baru","Post-money","Pemodal baru","Pendiri terdilusi","Pre-seed terdilusi","Seed terdilusi","Cek kepemilikan"]]);header(s,"A12:I12");
 rows(s,[13,1],[["Setelah pre-seed",null,null,null,null,null,null,null,null],["Setelah seed",null,null,null,null,null,null,null,null]]);
 formulaRows(s,13,2,[
  [`=${ia("preSeedVal")}`,"=C8","=B13+C13","=IF(D13>0,C13/D13,0)","=1-E13","=E13","=0","=SUM(F13:H13)"],
  [`=${ia("seedVal")}`,"=C9","=B14+C14","=IF(D14>0,C14/D14,0)","=F13*(1-E14)","=G13*(1-E14)","=E14","=SUM(F14:H14)"]
 ]);
 setFmt(s,"C7:I9",fmtCash);setFmt(s,"B13:D14",fmtCash);setFmt(s,"E13:I14",pct);
 rows(s,[18,1],[["Ukuran risiko likuiditas","Aktif","Makna"]]);header(s,"A18:I18");
 const risks=[
  ["Kas minimum",`=MIN(${monthRange("cash")})`,"Kas setelah pencairan bersyarat pada model."],
  ["Defisit maksimum atas buffer",`=MAX(${monthRange("fundingGap")})`,"Puncak jarak saldo kas terhadap buffer pembukaan."],
  ["Kebutuhan modal tanpa pendanaan",`=MAX(0,-MIN(${monthRange("freeCash")}))+${ia("triggerCash")}`,"Defisit proyek kumulatif ditambah buffer; bukan komitmen dana."],
  ["Kas bebas akhir horizon",`=${ann("cash")}`,"Simulasi dapat tetap menghitung kegiatan dalam defisit untuk melihat gap."],
 ];
 risks.forEach(([label,val,meaning],i)=>{const r=19+i;rows(s,[r,1],[[label,null,meaning]]);cell(s,`B${r}`,val);});
 setFmt(s,"B19:B22",fmtCash);widths(s,{"A:A":36,"C:C":25});
 merge(s,"A25:I25","Runway indikatif memakai rata-rata burn tiga bulan setelah setiap pencairan; kondisi kas diperiksa lagi pada pengambilan keputusan.");
 merge(s,"A26:I26","Valuasi merupakan posisi negosiasi ilustratif. Nilai saham, fasilitas registrasi dan komitmen investor belum diukur.");
 merge(s,"A27:I27","Gunakan Terbatas pada ringkasan untuk menahan seluruh putaran lanjutan. Ubah fundingDelay untuk menguji keterlambatan.");
}
{
 const s=tabs.Ringkasan;
 start(s,"LihatDulu  /  Proyeksi Keuangan","Rencana usaha UISP16 · UI Depok · horizon 2026–2036 · basis nominal rupiah","J","J41");
 widths(s,{"A:A":28,"B:B":14,"C:C":19,"D:D":9,"E:E":27,"F:F":17,"G:J":15});
 rows(s,[5,1],[["Kontrol model",null,"Edit"]]);header(s,"A5:C5");
 rows(s,[6,1],[["Pilih skenario",null,defaults.activeCase??"Base"],["Pencairan lanjutan",null,defaults.activeFunding??"Standar"]]);
 rg(s,"C6").dataValidation={rule:{type:"list",values:["Downside","Base","Upside"]}};
 rg(s,"C7").dataValidation={rule:{type:"list",values:["Standar","Terbatas"]}};
 style(s,"C6:C7",{fill:paleblue,font:{color:blue,bold:true}});
 rows(s,[10,1],[["Kelayakan setelah pajak","Satuan","Skenario aktif"]]);header(s,"A10:C10");
 const outputs=[
  ["CAPM / WACC","%",`=CAPM!B22`],["NPV proyek","Rp jt",`=${ann("cumDiscounted")}`],
  ["IRR proyek","%",`=IF(ISNUMBER(${ann("irr")}),${ann("irr")},"Tidak terdefinisi")`],
  ["Tahun melewati hurdle","tahun",`=IF(COUNT(Laporan!D${rr.cross}:M${rr.cross})>0,MIN(Laporan!D${rr.cross}:M${rr.cross}),"Belum tercapai")`],
  ["Payback nominal","tahun",`=IF(COUNT(Laporan!D${rr.pb}:M${rr.pb})>0,MIN(Laporan!D${rr.pb}:M${rr.pb}),"Belum tercapai")`],
  ["Payback terdiskonto","tahun",`=IF(COUNT(Laporan!D${rr.pbDiscount}:M${rr.pbDiscount})>0,MIN(Laporan!D${rr.pbDiscount}:M${rr.pbDiscount}),"Belum tercapai")`],
  ["Kas minimum","Rp jt","=Pendanaan!B19"],["Puncak gap vs buffer","Rp jt","=Pendanaan!B20"],
  ["Netto pendanaan skenario","Rp jt",`=SUM(${monthRange("funding")})`],
 ];
 for(const [i,[label,unit,formula]] of outputs.entries()){const r=11+i;rows(s,[r,1],[[label,unit]]);cell(s,`C${r}`,formula);setFmt(s,`C${r}`,unit==="%"?pct:label.startsWith("Payback")?fmtCash:unit==="tahun"?fmtInt:fmtCash);}
 style(s,"A12:C13",{fill:soft,font:{bold:true}});
 rows(s,[10,5],[["Ukuran operasi","Satuan","2027","2028","2029"]]);header(s,"E10:I10");
 for(const [i,[key,label,unit]] of [
  ["orders","Pesanan selesai","pesanan"],["gmv","GMV barang","Rp jt"],["marketplaceRevenue","Pendapatan marketplace","Rp jt"],
  ["b2bRevenue","Pendapatan B2B","Rp jt"],["ebitda","EBITDA","Rp jt"],["fcff","Arus kas proyek","Rp jt"],
  ["unitAfter","Kontribusi setelah akuisisi","Rp/order"],["clusters","Klaster aktif","klaster"],
 ].entries()){
  const r=11+i;rows(s,[r,5],[[label,unit]]);
  formulaRows(s,r,7,[["D","E","F"].map(c=>"="+ann(key,c))]);setFmt(s,`G${r}:I${r}`,unit==="Rp jt"?fmtCash:fmtInt);
 }
 merge(s,"A22:I22","Keputusan pada asumsi aktif");
 header(s,"A22:I22");
 merge(s,"A23:I24",`=IF(AND(C12>0,C17>=0),"Pertimbangkan ekspansi hanya jika hasil pilot memenuhi kontribusi dan buffer kas.","Batasi pada uji lokal. Periksa penggerak margin dan kebutuhan kas sebelum ekspansi.")`);
 style(s,"A23:I24",{fill:soft,font:{bold:true,color:green},wrapText:true,rowHeight:19});
 merge(s,"A26:I26","Skenario menggunakan biaya dan target yang belum menjadi hasil, kontrak atau komitmen pendanaan.");
 merge(s,"A27:I27","Untuk penggantian tarif atau masukan ekonomi, buka Asumsi. Kasus, Sensitivity, dan Monte Carlo menggunakan snapshot edisi 26 Nov.");
 style(s,"A26:I27",{wrapText:true,rowHeight:26});
}
const publishedCases=["Downside","Base","Upside"].map(k=>[k,evaluate(defaults,{caseName:k})]);
const stress1=evaluate(defaults,{allowFunding:false});
const stress2=evaluate({...defaults,fundingDelay:{...defaults.fundingDelay,Base:6}});
{
 const s=tabs.Kasus;
 start(s,"LihatDulu  /  Kasus pembanding","Hasil dihitung ulang dengan mesin yang sama pada 26 Nov 2026. Snapshot tidak mengikuti perubahan input.","J","J25");
 widths(s,{"A:A":30,"B:J":17});
 rows(s,[6,1],[["Kasus","Pesanan th 3","NPV Rp jt","IRR","Crossing","Kas min Rp jt","Gap Rp jt","Ekuitas net Rp jt","SOM Rp jt","Kas akhir Rp jt"]]);header(s,"A6:J6");
 rows(s,[7,1],[...publishedCases,["Base tanpa dana lanjutan",stress1],["Base dengan tunda enam bulan",stress2]].map(([name,q])=>[name,q.annual[3].orders,q.npv,q.irr??"Tidak terdefinisi",q.crossing??"Belum tercapai",q.cashMin,q.fundingGap,q.funding,q.annual[3].marketplaceRevenue,q.annual.at(-1).cash]));
 setFmt(s,"B7:B11",fmtInt);setFmt(s,"C7:C11",fmtCash);setFmt(s,"D7:D11",pct);setFmt(s,"F7:J11",fmtCash);
 style(s,"A8:J8",{fill:soft,font:{bold:true}});
 merge(s,"A15:J15","Perubahan likuiditas dapat menunda pembukaan klaster dan mengurangi volume, sehingga arus kas proyek yang direalisasikan juga berubah.");
 merge(s,"A16:J16","Skenario risiko dan kondisi awal model dapat diperbarui dengan paket penghitungan ulang yang disertakan.");
}
{
 const s=tabs["Bukti Harga"];
 start(s,"LihatDulu  /  Bukti harga penawaran","Sampel kenyamanan OLX Depok, diamati 26 Nov 2026. Harga penawaran berbeda dari harga transaksi.","F","F35");
 widths(s,{"A:A":20,"B:B":55,"C:C":19,"D:D":27,"E:E":24,"F:F":73});
 let raw=await fs.readFile(new URL("./harga.csv",import.meta.url),"utf8").catch(()=>fs.readFile("/tmp/sp-history-reset/finance/olx-depok-sample-2026-11-26.csv","utf8"));
 const parseLine=str=>Array.from(str.matchAll(/(?:^|,)(?:"((?:[^"]|"")*)"|([^,]*))/g),x=>x[1]!==undefined?x[1].replaceAll('""','"'):x[2]);
 const items=raw.trim().split(/\r?\n/).map(parseLine);
 const cols=items.shift();const id=(names)=>names.map(x=>cols.indexOf(x)).find(x=>x>=0);
 rows(s,[6,1],[["Kategori","Judul listing","Tawaran Rp","Wilayah","Tanggal data","Bukti URL"]]);header(s,"A6:F6");
 rows(s,[7,1],items.map(a=>[a[id(["kategori"])],a[id(["judul_ringkas_sumber"])],Number(a[id(["harga_penawaran_idr"])]),
   a[id(["kecamatan_ditampilkan"])],a[id(["tanggal_metadata_listing"])],a[id(["url_listing"])]]));
 setFmt(s,"C7:C30",fmtInt);
}
{
 const s=tabs.Rujukan;
 start(s,"LihatDulu  /  Rujukan input","Tanggal acuan 26 Nov 2026. Informasi terukur dan usulan model tercatat terpisah.","E","E28");
 widths(s,{"A:A":32,"B:B":30,"C:C":50,"D:D":73,"E:E":53});
 rows(s,[6,1],[["Rujukan","Vintage","Input","Tautan","Batas penggunaan"]]);header(s,"A6:E6");
 const refs=[
  ["BPS Susenas","Maret 2026; p.40","Rp3.376 per kapita per bulan, mebel","https://barat.jakarta.go.id/kelurahan/storage/files/images/foto/publikasi-statistik-file/5fd80ff6c397aacb66f4e2235bf5fe96.pdf","Belanja kategori termasuk mebel umum."],
  ["BPS Proyeksi Penduduk","2026","287.198.400 jiwa","https://www.bps.go.id/id/statistics-table/3/WVc0MGEyMXBkVFUxY25KeE9HdDZkbTQzWkVkb1p6MDkjMw%3D%3D/jumlah-penduduk-menurut-kelompok-umur-dan-jenis-kelamin.html","Perlu asumsi pasar bekas dan cakupan."],
  ["BPS daerah Jabodetabek","2025","Terestrial sekitar 32,38 juta dari nasional 284,44 juta atau 11,38%","https://depokkota.bps.go.id/id/statistics-table/2/MzMzIzI%3D/jumlah-penduduk-menurut-kecamatan-di-kota-depok.html","Populasi ini patokan wilayah, bukan pangsa pasar."],
  ["Indonesia Government Bond Yield","25 Nov 2026","Yield 10 tahun penutupan 7,696%","https://id.investing.com/rates-bonds/indonesia-10-year-bond-yield-historical-data","Bukan risk-free sebelum penyesuaian."],
  ["Damodaran Country Risk","Juli 2026","Mature ERP 4,20%, spread 1,52%, CRP 2,36%","https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctrypremJuly26.xlsx","Input spread dan CRP dibulatkan."],
  ["Damodaran Betas by Sector","Jan 2026","Software (Internet): beta 1,39, D/E 10,01%, pajak 25,37%","https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/BetasGlobal.html","Proksi global industri digital asset-light."],
  ["Midtrans publik","26 Nov 2026","VA Rp4.000, QRIS 0,7%, kartu 2,9% + Rp2.000, payout Rp5.000","https://midtrans.com/id/biaya","Metode dan kontrak akhir belum dipilih."],
  ["DJP / PP 20 Tahun 2026","2026","PT biasa lintas pemegang saham; PPh Badan umum 22% dan Pasal 31E bila memenuhi","https://pajak.go.id/index.php/id/artikel/badan-usaha-justru-tidak-terbebani-dengan-pp-202026-ini-penjelasannya","Estimasi, pada B2B/PPN pencatatan netto; verifikasi perjanjian."],
  ["Pemprov Jabar, UMK Depok","2026","UMK Rp5.522.662 per bulan","https://jdih.jabarprov.go.id/page/eksekusi_download/32/2025kg00320862.pdf","Lantai acuan, bukan penawaran gaji."],
  ["Cloudflare R2","26 Nov 2026","Standard $0,015/GB-bulan","https://developers.cloudflare.com/r2/pricing/","Pembulatan anggaran; komputasi dan traffic terpisah."],
  ["Bank Indonesia JISDOR","26 Nov 2026","Rp18.390 per USD","https://www.bi.go.id/id/statistik/informasi-kurs/jisdor/default.aspx","Acuan anggaran vendor, belum hedging."],
  ["Lalamove harga pickup historis","Publik, sebelum acuan","Sekitar Rp80.800 hingga 5 km Depok","https://www.lalamove.com/id/blog/harga-sewa-mobil-pick-up/","Harga aktual perlu quote di aplikasi dan lewat sebagai titipan."],
  ["OLX Depok","26 Nov 2026","24 harga penawaran terpilih; median meja 325k, kursi 375k, rak 325k, lemari 900k","Lihat Bukti Harga","Potongan 9% median untuk Base adalah asumsi."],
  ["Survei dan prototipe LihatDulu","26 Nov 2026","60 respons; 17 pengalaman iklan; 7 rekaman satu kursi lokal","Data agregat dan bukti dalam proposal","Tidak mengukur tingkat konversi, tarif atau SLA."]
 ];
 rows(s,[7,1],refs);style(s,"A7:E20",{wrapText:true,rowHeight:39});
}
{
 const s=tabs["QA Model"];
 start(s,"LihatDulu  /  Pemeriksaan model","Nilai selisih di bawah Rp0,001 juta dianggap nol. Pemeriksaan diperbarui saat input diubah.","D","D25");
 widths(s,{"A:A":41,"B:B":18,"C:C":18,"D:D":75});
 rows(s,[6,1],[["Pemeriksaan","Selisih","Status","Basis"]]);header(s,"A6:D6");
 const mrc=(id)=>monthRange(id);
 const checks=[
  ["Persamaan neraca bulanan",`=MAX(MAX(${mrc("checkBS")}),-MIN(${mrc("checkBS")}))`,"Aset dikurangi liabilitas dan ekuitas."],
  ["Stok listing",`=MAX(MAX(${mrc("checkStock")}),-MIN(${mrc("checkStock")}))`,"Saldo awal + terbit − terjual − ditarik."],
  ["Kapasitas dukungan",`=SUMPRODUCT(--(${mrc("booking")}>${mrc("supportCap")}))`,"Booking tidak melampaui dukungan."],
  ["Unit layak",`=SUMPRODUCT(--(${mrc("booking")}>${mrc("supply")}))`,"Booking tidak melampaui pasokan."],
  ["Aktivitas permintaan",`=SUMPRODUCT(--(${mrc("booking")}>${mrc("demand")}))`,"Booking tidak melampaui permintaan."],
  ["Mutasi kas tahunan",`=MAX(MAX(Laporan!C${rr.cashCheck}:M${rr.cashCheck}),-MIN(Laporan!C${rr.cashCheck}:M${rr.cashCheck}))`,"Kas akhir sama dengan arus proyek + pembiayaan + kas awal."],
  ["Pendapatan tidak mencakup titipan",`=ABS(SUM(${mrc("revenue")})-SUM(${mrc("marketplaceRevenue")})-SUM(${mrc("b2bRevenue")}))`,"Total marketplace dan B2B tanpa ongkos angkut."],
  ["Rekonsiliasi SOM tahun ketiga",`=ABS('Ukuran Pasar'!B16-${ann("marketplaceRevenue","F")})`,"Pendapatan tahun 3 di Laporan dan Ukuran Pasar sama."],
  ["Alokasi kepemilikan",`=MAX(ABS(Pendanaan!I13-1),ABS(Pendanaan!I14-1))`,"Kepemilikan ekuitas kembali ke 100%."],
  ["Utang pembiayaan","=CAPM!B21","Bobot utang adalah nol sesuai rancangan."],
  ["Batas diskonto",`=IF(AND(CAPM!B22>0,CAPM!B22<1),0,1)`,"Model membutuhkan tingkat diskonto nominal positif dan di bawah 100%."],
 ];
 for(let i=0;i<checks.length;i++){const [title,f,note]=checks[i],r=7+i;rows(s,[r,1],[[title,null,null,note]]);cell(s,`B${r}`,f);cell(s,`C${r}`,`=IF(ABS(B${r})<0.001,"LULUS","PERIKSA")`);}
 setFmt(s,"B7:B17",fmtPrecise);
}
{
 const s=tabs.Metode;
 start(s,"LihatDulu  /  Batas model dan penyegaran","Asumsi 2026 · Sumber sp-data 1b5814d · Struktur terinspirasi workbook Auto2000","F","F38");
 widths(s,{"A:A":37,"B:B":66,"C:F":25});
 rows(s,[6,1],[["Bagian","Aturan pengukuran","Pemeriksaan"]]);header(s,"A6:F6");
 rows(s,[7,1],[
  ["Tahun 0","Persiapan sebelum operasi; belanja aset dan biaya langsung dibayarkan dalam 2026.","Diskonto tahunan dari Tahun 0."],
  ["Pendapatan marketplace","Tarif pembeli × pesanan yang selesai + komisi × GMV setelah refund parsial; biaya pembeli tetap pada refund parsial sebagai asumsi.","Pembatalan dan refund penuh dikeluarkan."],
  ["Arus kas proyek","Laba operasi setelah pajak + penyusutan − belanja aset − perubahan modal kerja; tidak memakai nilai terminal.","Pendanaan bukan arus proyek."],
  ["Kas dalam defisit","Model mempertahankan kewajiban operasi dalam defisit agar kebutuhan dana terlihat. Ekspansi baru tertahan bila kas atau milestone gagal.","Operasi nyata akan menunda atau menghentikan belanja."],
  ["Pajak","Asumsi PT biasa, cash tax akhir tahun dan pengimbangan rugi bergulir sampai lima tahun. Tarif layanan ditampilkan sebelum PPN, titipan pajak dimaksudkan selesai pada periode terkait.","Periksa entitas, PKP, kontrak dan ketentuan aktual."],
  ["Sel input","Biru = dapat diedit. Gunakan kontrol Kasus Ringkasan untuk skenario aktif dan asumsi jadwal pendanaan.","Dampak kolom aktif dihitung ulang di Excel."],
  ["Harga referensi","Sampel kenyamanan 24 penawaran OLX Depok; harga realisasi dibolehkan berbeda karena kondisi, negosiasi dan mix.","Tidak mengukur proporsi bekas atau daya bayar."],
  ["Monte Carlo","10.000 simulasi, seed 12026, batas 2026–2036. Trial memakai rumus operasi bulanan yang sama, dengan penarikan parameter dari rentang ilustratif.","Hasil publikasi merupakan snapshot yang dihitung, bukan probabilitas empiris."],
  ["Simulasi jika input berubah","Simpan workbook yang diedit, jalankan refresh-risk.mjs dengan versi sumber yang disertakan. Hasil XLSX baru menggabungkan snapshot baru dan kontrol yang valid.","Tag versi dan seed sebelum membandingkan."],
  ["Uji putaran modal","Pendanaan modal pendiri, pre-seed dan seed hanya berasal dari skenario atau asumsi yang disetujui, tanpa pinjaman atau hibah terkonfirmasi.","Cadangan kas dan arus defisit dipantau terpisah."],
  ["Kebijakan IRR","IRR dihitung bila terjadi satu perubahan tanda; beberapa perubahan memerlukan uji akar tambahan. Tinjau NPV bila IRR tidak tersedia.","Biaya ekuitas bukan return VC yang dijamin."],
 ]);
 style(s,"A7:C17",{wrapText:true,rowHeight:60});widths(s,{"C:C":51});
}

console.log("MODEL_READY");
if(process.env.LIHATDULU_NO_RISK!=="1"){
 const risk=JSON.parse(await fs.readFile(process.env.LIHATDULU_RISK??"/tmp/ldfin/risk.json","utf8"));
 if(process.env.LIHATDULU_RISK_COMPACT==="1")compactRisk(wb,risk);
 else addRiskSheets(wb,{...risk,moneyScale:1,moneyUnit:"Rp juta",baseMeasureRef:`IF(Ringkasan!$C$6="Base",Ringkasan!$C$12,${publishedCases[1][1].npv})`,
  refreshText:"Ubah input pada Asumsi. Untuk sinkronisasi simulasi, jalankan paket refresh-risk.mjs pada workbook yang telah disimpan. Saat pilihan Base aktif, cocokkan NPV tengah dengan Ringkasan."});
 console.log("RISK_READY");
}
await fs.mkdir("/mnt/data",{recursive:true});
const target=process.env.LIHATDULU_TARGET??"/mnt/data/LihatDulu_Financial_Projection.xlsx";
await (await SpreadsheetFile.exportXlsx(wb)).save(target);
console.log("SAVED",target);
if(process.env.LIHATDULU_PREVIEW==="1"){
 for(const [sheetName,range] of [["Ringkasan","A1:J30"],["CAPM","A1:E26"],["Ukuran Pasar","A1:D19"],["Pendanaan","A1:I27"]]){
  const blob=await wb.render({sheetName,range,scale:1.2});
  await fs.writeFile(`/tmp/ldfin/preview-${sheetName}.png`,new Uint8Array(await blob.arrayBuffer()));
 }
}
