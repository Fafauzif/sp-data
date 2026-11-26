import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const out=fileURLToPath(new URL('.', import.meta.url));
const deck=Presentation.create({slideSize:{width:793.7007874,height:1122.519685}});
const colors={forest:'#184833',deep:'#16352A',sage:'#DCE9D8',light:'#F0F5EE',dark:'#202C25',olive:'#6A7E54',grey:'#53645B',edge:'#C8D6C7',soft:'#F7F8F4',white:'#FFFFFF',rose:'#ECD3CA',tan:'#F3E6C7',mint:'#C6DECE'};
const {forest,deep,sage,light,dark,olive,grey,edge,soft,white,rose,tan,mint}=colors;
const L=73,W=648,T=126,Y=174;
const layout=[];
let next=0;

function shape(s,x,y,w,h,fill='none',geometry='rect',source='',stroke='none',weight=0){
  return s.shapes.add({ geometry, name:source ? 'BCC__'+source : `shape-${++next}`,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:weight,style:'solid'} });
}
function txt(s,x,y,w,h,copy,opt={}){
  const a=shape(s,x,y,w,h,'none','textbox');
  a.text=copy;
  a.text.style={typeface:'Liberation Sans',fontSize:`${opt.pt??10}pt`,color:opt.color??dark,bold:opt.bold??false,italic:opt.italic??false,
    alignment:opt.align??'left',verticalAlignment:opt.valign??'middle',insets:0,wrap:'square',autoFit:'none'};
  return a;
}
function rule(s,x,y,w,fill=edge){shape(s,x,y,w,1,fill)}
function heading(s,title){
  shape(s,L,T,W,35,forest);
  txt(s,L+12,T+2,W-24,31,title,{pt:13,bold:true,color:white});
}
function start(id,title,source,height,note=''){
  const s=deck.slides.add();
  s.speakerNotes.text=`Template BCC ${source}. Sumber isi: proposal LihatDulu UISP16 dan audit revisi. ${note}`;
  heading(s,title);
  layout.push({id,title,source,clip:[L-1,T-1,L+W+1,Y+height]});
  return s;
}
function foot(s,y,copy){txt(s,L,y,W,25,copy,{pt:8.5,color:grey,italic:true})}
function port(s,source,name,x,y,w,h,fill){
  return shape(s,x,y,w,h,fill,'rect',`${source}__${name}`);
}
function band(s,x,y,w,h,label,fill=forest,pt=10){
  shape(s,x,y,w,h,fill);
  txt(s,x+8,y,w-16,h,label,{pt,bold:true,color:white});
}
function multi(s,x,y,w,h,label,copy,opt={}){
  const tx=x+(opt.margin??9);
  const tw=w-2*(opt.margin??9);
  txt(s,tx,y+7,tw,opt.head??25,label,{pt:opt.headPt??10,bold:true,color:opt.labelColor??forest,valign:'top'});
  txt(s,tx,y+8+(opt.head??25),tw,h-14-(opt.head??25),copy,{pt:opt.pt??9.5,color:opt.color??dark,valign:'top'});
}
function matrix(s,{head,rows,widths,rowH=48,top=Y,sources=[],source='',firstTint=true}){
  let x=L;
  for(const [i,w] of widths.entries()){
    if(sources[i]) { const [page,name]=Array.isArray(sources[i])?sources[i]:[source,sources[i]]; port(s,page,name,x,top,w-3,34,i===0?olive:forest); }
    else shape(s,x,top,w-3,34,i===0?olive:forest);
    txt(s,x+7,top+1,w-17,32,head[i],{pt:9.5,bold:true,color:white});
    x+=w;
  }
  rows.forEach((row,r)=>{
    let left=L;
    row.forEach((value,c)=>{
      const w=widths[c], yy=top+39+r*rowH;
      shape(s,left,yy,w-3,rowH-3,c===0&&firstTint?sage:r%2===0?light:soft);
      txt(s,left+7,yy+2,w-17,rowH-7,value,{pt:9.2,bold:c===0,color:c===0?deep:dark});
      left+=w;
    });
  });
  return top+39+rows.length*rowH;
}

// BMC: calibrated to the five-column layout and nine cell freeforms of slide 111.
{
 const s=start('bmc','Model bisnis LihatDulu','111',332,'Bab II, Bab III, Bab IV dan Lampiran A.');
 const c=128,g=2;
 const items=[
  [0,0,128,219,'Freeform 6','Mitra utama','Pedagang furnitur lokal\nPengelola kos\nPenyedia pembayaran\ndan angkutan'],
  [130,0,c,108,'Freeform 22','Kegiatan utama','Rekrut penjual\nPeriksa bukti\nDukung pesanan'],
  [130,110,c,109,'Freeform 25','Sumber daya','Katalog digital\nFoto dan model 3D\nTim operasi'],
  [260,0,c,219,'Freeform 16','Proposisi nilai','Pembeli memeriksa kondisi, ukuran, dan cara terima.\n\nPenjual punya satu tautan bukti per barang.'],
  [390,0,c,108,'Freeform 28','Hubungan pelanggan','Panduan listing\nDukungan pesanan'],
  [390,110,c,109,'Freeform 39','Saluran','Komunitas kos\nKreator lokal\nBursa Pindahan'],
  [520,0,c,219,'Freeform 19','Segmen pelanggan','Mahasiswa kos dan penyewa baru.\n\nReseller dan penghuni yang pindah.'],
  [0,221,323,92,'Freeform 10','Struktur biaya','Pengembangan, media, pembayaran, dukungan dan pemasaran.'],
  [325,221,323,92,'Freeform 13','Pendapatan','Biaya pembeli dan komisi penjual pada pesanan selesai. B2B terpisah di fase lanjut.']
 ];
 items.forEach(([x,y,w,h,p,ttl,copy])=>{
   port(s,111,p,L+x,Y+y,w,h,light);
   multi(s,L+x,Y+y,w,h,ttl,copy,{head:ttl.includes('pelanggan')?38:22,headPt:9.8,pt:9.1,margin:8});
 });
}

{
 const s=start('vpc','Kecocokan penawaran dengan kebutuhan pengguna','110',351,'Kebutuhan pembeli ditopang survei final. Profil penjual merupakan hipotesis kerja.');
 const fit=[
  ['Pembeli','Foto dekat, kondisi dan ukuran.','Pilihan ambil sendiri atau angkut.','Referensi yang tetap bisa dibuka.','Mencari barang yang muat.','Sulit menilai kondisi dan cara terima.','Yakin sebelum mengatur serah terima.'],
  ['Penjual','Formulir foto, dimensi dan jadwal.','Satu tautan bukti untuk setiap unit.','Estimasi hasil bersih dan status.','Menawarkan stok dan mengatur pengambilan.','Mengulang jawaban tentang barang.','Stok terlihat dan dana dapat diperkirakan.']
 ];
 for(const [i,r] of fit.entries()){
   const y=Y+i*159;
   band(s,L,y,W,24,r[0],olive,9.4);
   port(s,110,'Freeform 6',L,y+30,285,116,light);
   port(s,110,'Freeform 9',L+357,y+30,291,116,sage);
   shape(s,L+296,y+79,50,18,olive,'rightArrow');
   txt(s,L+12,y+36,265,20,'Penawaran LihatDulu',{bold:true,pt:9.4,color:forest});
   // The oval is shallow inside the landscape exhibit; the text rests in its central band.
   txt(s,L+389,y+41,221,19,'Profil pengguna',{bold:true,pt:9.4,align:'center',color:forest});
   for(let j=0;j<3;j++){
      txt(s,L+12,y+58+j*22,265,22,r[1+j],{pt:9});
      txt(s,L+373,y+61+j*19,258,19,r[4+j],{pt:8.7,align:'center'});
   }
 }
 foot(s,Y+319,'Profil pembeli bersumber dari survei. Profil penjual perlu validasi wawancara.');
}

{
 let m={marketBands:['TAM','SAM','SOM'],marketValues:['Indonesia','Jabodetabek layak layanan','Klaster aktif pada tahun ketiga'],marketMethod:['Pendapatan tahunan atas pesanan furnitur bekas selesai.','Pendapatan dari wilayah dan kategori yang bisa dilayani.','Pesanan selesai dibatasi permintaan, unit, dan slot pemenuhan.'],marketFoot:'Rp11,63 triliun per tahun merupakan tolok ukur belanja mebel umum (BPS, 2026).'};
 try{m={...m,...JSON.parse(await fs.readFile(out+'/model.json','utf8'))}}catch(err){if(err.code!=='ENOENT')throw err}
 const s=start('market','Ukuran pasar berbasis pendapatan platform','91',304,'BPS Statistik Pengeluaran untuk Konsumsi Penduduk Indonesia Maret 2026 dan Proyeksi Penduduk Indonesia. Bedakan belanja mebel umum dari GMV serta pendapatan LihatDulu.');
 const xs=[L+8,L+35,L+65], ys=[Y+5,Y+60,Y+120], dim=[240,186,126], names=['Freeform 3','Freeform 6','Freeform 9'], fills=[forest,olive,mint];
 for(let i=0;i<3;i++)port(s,91,names[i],xs[i],ys[i],dim[i],dim[i],fills[i]);
 for(let i=0;i<3;i++){
   const cr=i===2?deep:white;
   txt(s,L+44,[Y+14,Y+69,Y+129][i],165,42,m.marketBands[i],{pt:10.5,bold:true,color:cr,align:'center'});
   shape(s,L+248,Y+36+i*70,35,1,olive);
   port(s,91,['Freeform 21','Freeform 24','Freeform 27'][i],L+286,Y+6+i*70,362,65,light);
   multi(s,L+286,Y+6+i*70,362,65,m.marketValues[i],m.marketMethod[i],{head:18,headPt:10.1,pt:8.9});
 }
 txt(s,L,Y+253,W,43,m.marketFoot,{pt:8.5,color:grey,italic:true,valign:'top'});
}

{
 const s=start('stp','Segmen prioritas di sekitar UI Depok','96',277,'Hasil survei final mendukung fokus pembeli. Urutan klaster dan profil penjual adalah keputusan rencana operasi.');
 const rows=[
 ['Geografi','Klaster kos UI Depok','Klaster hunian berdekatan'],
 ['Peran','Mahasiswa kos dan reseller lokal','Penyewa lain dan penghuni pindah'],
 ['Preferensi','Bukti kondisi dan ukuran','Pilihan barang serta serah terima'],
 ['Perilaku','Kebutuhan saat pindah, stok berulang','Pasokan musiman atau sesekali']
 ];
 const y=matrix(s,{head:['Dimensi','Target utama','Target pendukung / ekspansi'],rows,widths:[138,255,255],rowH:41,source:96,sources:['Freeform 6','Freeform 48','Freeform 51']});
 foot(s,y+4,'Posisi LihatDulu ialah furnitur bekas yang dapat diperiksa sebelum dipesan.');
}

{
 const s=start('persona-pembeli','Profil pembeli pertama','97',192,'Survei pengguna versi akhir, n = 60, modul pengguna yang mempertimbangkan iklan n = 17 (semuanya mahasiswa). Ringkasan perilaku, bukan kutipan peserta.');
 port(s,97,'Freeform 6',L+12,Y+19,117,117,sage);
 txt(s,L+26,Y+39,89,68,'PENGHUNI\nKOS',{pt:10.4,bold:true,color:forest,align:'center'});
 port(s,97,'Freeform 8',L+133,Y+5,515,146,light);
 txt(s,L+171,Y+19,462,28,'Mahasiswa yang sedang menyiapkan kamar',{pt:12,bold:true,color:forest});
 txt(s,L+171,Y+57,459,81,'Mencari meja, rak, atau lemari sebelum pindah. Untuk memilih, ia membutuhkan bukti kondisi, ukuran barang, dan opsi serah terima. Ukuran serta jarak menentukan apakah ia perlu menghubungi penjual.',{pt:10,valign:'top'});
 foot(s,Y+157,'Semua 17 responden yang mempertimbangkan satu iklan spesifik adalah mahasiswa.');
}

{
 const s=start('persona-penjual','Profil pemasok awal','98',220,'Profil reseller dipakai sebagai hipotesis operasi. Belum ada wawancara penjual.');
 port(s,98,'Freeform 3',L,Y,W,175,light);
 port(s,98,'Freeform 12',L+14,Y+15,70,70,sage);
 txt(s,L+17,Y+20,64,58,'STOK',{pt:9.3,bold:true,color:forest,align:'center'});
 port(s,98,'Freeform 6',L+94,Y+11,541,34,forest);
 txt(s,L+110,Y+12,502,32,'Reseller furnitur lokal',{pt:11,bold:true,color:white});
 port(s,98,'Freeform 9',L+94,Y+52,541,27,sage);
 txt(s,L+110,Y+53,502,25,'Hipotesis kerja untuk wawancara penjual',{pt:9.3,bold:true,color:forest});
 multi(s,L+14,Y+88,200,78,'Perilaku','Stok berganti dan harus diperbarui.',{head:17,pt:9.5});
 multi(s,L+214,Y+88,208,78,'Hambatan','Setiap unit membutuhkan bukti sendiri.',{head:17,pt:9.5});
 multi(s,L+430,Y+88,202,78,'Kebutuhan','Perjelas hasil bersih dan jadwal ambil.',{head:17,pt:9.5});
 foot(s,Y+178,'Penghuni yang akan pindah menjadi sumber pasokan tambahan.');
}

{
 const s=start('aida','Tindakan pemasaran sampai pesanan selesai','99–100',191,'Bab IV dan Lampiran G. Tahap kampanye berbeda dari horizon ekspansi.');
 const stages=[['Kenal','Kenal katalog kos','Komunitas dan kreator lokal','Kunjungan koleksi'],['Tertarik','Buka barang yang tersedia','Tautan ke listing tertentu','Pembukaan listing'],['Menimbang','Cek ukuran dan kondisi','Demo “Muat Nggak?”','Pengecekan bukti'],['Bertindak','Pilih cara terima','Reservasi atau pemesanan','Pesanan selesai']];
 const a=['Freeform 19','Freeform 22','Freeform 25','Freeform 28'];
 const b=['Freeform 21','Freeform 24','Freeform 27','Freeform 30'];
 for(const [i,[label,goal,tactic,kpi]] of stages.entries()){
  const x=L+i*162;
  port(s,99,a[i],x,Y,157,33,i%2===0?forest:olive);
  txt(s,x+11,Y+1,132,30,label,{pt:10,bold:true,color:white,align:'center'});
  port(s,100,b[i],x,Y+38,157,38,light);
  txt(s,x+6,Y+41,145,32,goal,{pt:9.4,bold:true,align:'center'});
  txt(s,x+7,Y+83,143,38,tactic,{pt:9.1,align:'center'});
  shape(s,x,Y+128,157,40,sage);
  txt(s,x+6,Y+129,145,37,kpi,{pt:8.8,bold:true,color:forest,align:'center'});
 }
}

{
 const s=start('kpi','Indikator untuk mengendalikan operasi awal','103',259,'Rancangan KPI Bab III. Target numerik merupakan ambang uji pilot. Tim masih perlu mengukur nilai awal.');
 const y=matrix(s,{head:['Indikator dan target uji','Definisi terukur','Pemilik / pemicu'],widths:[153,246,249],rowH:47,source:103,
 sources:['Freeform 10','Freeform 7','Freeform 22'],rows:[
  ['Listing lengkap\n≥90%','Listing lolos bukti minimum ÷ listing diajukan','Tim katalog menyederhanakan panduan bila banyak revisi.'],
  ['Kesiapan serah terima\n≥85%','Pesanan dengan unit dan slot pasti ÷ pesanan masuk','Dukungan pesanan memeriksa antrean dan pembatalan.'],
  ['Pesanan selesai\n≥85%','Serah terima tuntas dan dana tercatat ÷ pesanan terkonfirmasi','Operasi merekonsiliasi satu ID per transaksi.'],
  ['Selisih kondisi\n≤5%','Keluhan kondisi ÷ serah terima tercatat','Dukungan memeriksa foto dan versi listing.']
 ]});
 foot(s,y+4,'Angka adalah target uji pilot Depok. Tim mengukur nilai awal selama pilot.');
}

{
 const s=start('pesaing','Alternatif pembeli sebelum menyepakati barang','89–90',268,'Pengamatan listing dan panduan OLX pada Lampiran D. Perbandingan fungsional berdasarkan cara pakai, tanpa skor pangsa atau kinerja.');
 const rows=[
  ['Penemuan','Katalog per klaster','Pencarian iklan','Kiriman anggota','Kunjungan lokasi'],
  ['Kondisi','Foto dekat dan catatan','Menurut isi iklan','Tanya penjual','Cek unit langsung'],
  ['Ukuran','Kolom dimensi','Menurut isi iklan','Tanya atau ukur','Ukur di lokasi'],
  ['Serah terima','Opsi per barang','Atur dengan penjual','Koordinasi dalam chat','Atur angkut sendiri'],
  ['Bukti pesanan','Versi listing terhubung','Simpan iklan sendiri','Riwayat chat','Catatan terpisah'],
 ];
 const y=matrix(s,{head:['Kriteria','LihatDulu¹','Iklan umum (OLX)','Grup/chat kos','Kunjung langsung'],widths:[110,135,131,131,141],
 rowH:40,source:89,sources:[[90,'Freeform 25'],'Freeform 8','Freeform 11','Freeform 14','Freeform 17'],rows});
 foot(s,y+3,'¹ Kolom LihatDulu menyatakan rancangan layanan. Ketersediaan bukti alternatif bervariasi.');
}

{
 const s=start('marketing-mix','Bauran pemasaran klaster UI Depok','101',207,'Bab IV. Biaya layanan pembeli, komisi penjual, dan angkutan terpisah adalah rancangan model.');
 const cards=[
 ['Wilayah','Mulai dari klaster kos yang bisa dilayani lewat pengambilan atau angkutan.', 'Freeform 15'],
 ['Promosi','Koleksi komunitas kos, “Muat Nggak?” dari kreator, dan Bursa Pindahan.','Freeform 6'],
 ['Harga','Pembeli melihat harga dan biaya layanan. Penjual melihat komisi dan hasil bersih.','Freeform 12'],
 ['Produk','Katalog furnitur bekas dengan bukti unit, ukuran, dan pilihan serah terima.','Freeform 9']
 ];
 cards.forEach(([title,copy,p],i)=>{
   const x=L+i%2*326,y=Y+Math.floor(i/2)*96;
   port(s,101,p,x,y,322,91,light);
   multi(s,x,y,322,91,title,copy,{head:20,pt:10,margin:12});
 });
}

{
 const s=start('risiko','Prioritas risiko dan respons operasi','3 dan 6',268,'Risiko dan penilaian awal dari usulan tim. Posisi diperbarui setelah data pilot.');
 const cell=[tan,rose,rose,light,tan,rose,light,light,tan];
 const portNames=['Freeform 21','Freeform 30','Freeform 39','Freeform 24','Freeform 33','Freeform 42','Freeform 27','Freeform 36','Freeform 45'];
 const cellcodes=['R5','R3','','','R4','R1','','','R2'];
 txt(s,L,Y,240,19,'Dampak',{pt:9.3,bold:true,color:forest});
 for(const [i,r] of ['Tinggi','Sedang','Rendah'].entries()){
   txt(s,L,Y+24+i*46,51,40,r,{pt:8.7});
   for(let c=0;c<3;c++){
    let j=i*3+c;
    port(s,3,portNames[j],L+52+c*56,Y+24+i*46,53,43,cell[j]);
    txt(s,L+52+c*56,Y+26+i*46,53,39,cellcodes[j],{pt:10,bold:true,color:forest,align:'center'});
   }
 }
 for(const [i,r] of ['Rendah','Sedang','Tinggi'].entries())txt(s,L+52+i*56,Y+166,53,18,r,{pt:8.5,align:'center'});
 txt(s,L+20,Y+186,232,20,'Kemungkinan',{pt:9.3,bold:true,color:forest,align:'center'});
 const rr=[
  ['R1','Bukti kurang','Katalog minta perbaikan.'],
  ['R2','3D sulit dibaca','Produk dahulukan foto.'],
  ['R3','Stok atau slot hilang','Operasi konfirmasi sebelum bayar.'],
  ['R4','Biaya menghambat','Produk tampilkan total di awal.'],
  ['R5','Kondisi tidak sesuai','Dukungan cek bukti sebelum dana selesai.'],
 ];
 const sx=L+241;
 port(s,6,'Freeform 18',sx,Y,407,25,forest);
 txt(s,sx+7,Y+1,393,22,'Kode, risiko, dan pemilik respons',{pt:9.6,bold:true,color:white});
 rr.forEach(([code,risk,response],i)=>{
   const y=Y+28+i*38;
   shape(s,sx,y,407,35,i%2===0?light:soft);
   txt(s,sx+7,y+1,31,32,code,{pt:9,bold:true,color:forest});
   txt(s,sx+40,y+1,133,32,risk,{pt:9.1,bold:true});
   txt(s,sx+176,y+1,225,32,response,{pt:9.1});
 });
 foot(s,Y+226,'Peta menunjukkan penilaian awal, yang diperbarui setelah pilot.');
}

{
 const s=start('roadmap','Tahap peluncuran dan syarat perluasan','9',202,'Bab III dan IV. Fase mengikuti kesiapan katalog dan pemenuhan.');
 matrix(s,{head:['Fokus','Bulan 0–6','Bulan 7–12','Tahun kedua dan lanjut'],widths:[106,170,170,202],rowH:48,source:9,
 sources:['Freeform 15','Freeform 3','Freeform 6','Freeform 9'],rows:[
 ['Wilayah','UI Depok','Klaster berdekatan','Klaster layanan berikutnya'],
 ['Eksekusi','Kurasi stok dan uji transaksi','Ulangi “Muat Nggak?”','Jalankan Bursa Pindahan'],
 ['Prasyarat','Bukti listing dan stok siap','Pesanan selesai dan biaya terukur','Stok, slot, dan atribusi 30 hari siap'],
 ]});
}

{
 let model={finance:[['Biaya pembeli','Per pesanan selesai'],['Komisi penjual','Persentase harga barang'],['Angkutan','Diteruskan ke penyedia']],financeFoot:'Kelayakan dan kebutuhan dana dihitung dari model arus kas per tahap.'};
 try{model={...model,...JSON.parse(await fs.readFile(out+'/model.json','utf8'))}}catch(err){if(err.code!=='ENOENT')throw err}
 const s=start('keuangan','Kelayakan keuangan skenario dasar','20',138,'Bab V dan Lampiran E. Hasil sensitif terhadap volume, biaya, dan tarif yang dipakai.');
 port(s,20,'Freeform 3',L,Y,W,90,forest);
 for(const [i,[value,label]] of model.finance.entries()){
    const x=L+i*216;
    if(i)shape(s,x,Y+23,1,51,mint);
    txt(s,x+13,Y+13,194,34,value,{pt:12,bold:true,color:white});
    txt(s,x+13,Y+49,194,35,label,{pt:8.8,color:white,valign:'top'});
 }
 foot(s,Y+95,model.financeFoot);
}

{
 const s=start('swot','Prioritas tindak lanjut dari SWOT','87',299,'Sintesis rencana dan risiko internal. Tidak mengasumsikan hasil komersial sudah tercapai.');
 const w=321;
 const items=[
  [0,0,'Kekuatan','Bukti per unit menghubungkan foto, dimensi, kondisi, dan serah terima.','Freeform 3'],
  [327,0,'Kelemahan','Pemeriksaan listing butuh waktu. Model 3D tidak selalu dapat dipakai.','Freeform 15'],
  [0,88,'Peluang','Musim pindah mempertemukan calon pembeli dan pemasok dalam radius yang sama.','Freeform 9'],
  [327,88,'Ancaman','Penjual dan pembeli dapat beralih ke chat, atau gagal menemukan pengangkut.','Freeform 39'],
  [0,176,'Prioritas pertumbuhan','Rekrut pemasok berulang dan kurasi unit yang dapat dibeli serta diambil.','Freeform 45'],
  [327,176,'Prioritas pengendalian','Wajibkan bukti minimum, tampilkan biaya sejak awal, dan periksa stok serta slot.','Freeform 51'],
 ];
 items.forEach(([x,y,title,copy,p])=>{
   port(s,87,p,L+x,Y+y,w,84,y===176?sage:light);
   multi(s,L+x,Y+y,w,84,title,copy,{head:20,headPt:10.4,pt:9.6});
 });
}

await (await PresentationFile.exportPptx(deck)).save(out+'/draft-native.pptx');
await fs.writeFile(out+'/layout.json',JSON.stringify(layout,null,2));
