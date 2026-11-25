from pathlib import Path
import json,re
from copy import deepcopy
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_TAB_ALIGNMENT,WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT

root=Path('revision'); src=next(Path('upload').glob('*Proposal (3)*'))
d=Document(src)
els=list(d._element.body); end=els[-1]
cover=els[4]; cover_p=Paragraph(cover,d); cover_p.clear()
for ref in cover.xpath('.//w:headerReference|.//w:footerReference'):
 ref.getparent().remove(ref)
for i,e in enumerate(els[:-1]):
 if i not in [4,5,8,9,10,11,13,20,22,29,42,44,46,53,60,68,82,90,92,99,103,108,116,121,124,126,134,141,148,153,157,162,164,166,167,175,181,193,211,252,274,277,302]:
  e.getparent().remove(e)
for rel in list(d.part.rels.values()):
 if '/comments' in rel.reltype:
  d.part.drop_rel(rel.rId)
  if rel.rId in d.part.rels: del d.part.rels[rel.rId]

def add_book(p,name):
 if not name:return
 add_book.i+=1
 a=OxmlElement('w:bookmarkStart');a.set(qn('w:id'),str(add_book.i));a.set(qn('w:name'),name)
 b=OxmlElement('w:bookmarkEnd');b.set(qn('w:id'),str(add_book.i))
 p._p.insert(1 if p._p.pPr is not None else 0,a);p._p.append(b)
add_book.i=100
heading_ids={13:'Summary',20:'Bab1',22:'Sec11',29:'Sec12',42:'Sec13',44:'Bab2',46:'Sec21',53:'Sec22',60:'Sec23',68:'Sec24',82:'Sec25',90:'Bab3',92:'Sec31',99:'Sec32',103:'Sec33',108:'Sec34',116:'Sec35',121:'Sec36',124:'Bab4',126:'Sec41',134:'Sec42',141:'Sec43',148:'Sec44',153:'Sec45',157:'Sec46',162:'Bab5',164:'Sec51',166:'Sec52',167:'References',175:'AppendixIndex',181:'AppendixA',193:'AppendixB',211:'AppendixC',252:'AppendixD',274:'AppendixE',277:'AppendixF',302:'AppendixG',8:'Authorship'}
linkcolor='176250'
for i,anchor in heading_ids.items():
 p=Paragraph(els[i],d)
 p.paragraph_format.page_break_before=i in [8,13,153,175]
 p.paragraph_format.space_before=Pt(9 if p.style.name=='Heading 1' else 7)
 p.paragraph_format.space_after=Pt(4)
 p.paragraph_format.keep_with_next=True
 p.paragraph_format.keep_together=True
 p.paragraph_format.line_spacing=1.12
 if p.style.name=='Heading 2':p.paragraph_format.left_indent=Pt(0)
 add_book(p,anchor)
 if i==193:
  for r in p.runs:r.text=''
  p.add_run('Lampiran B. Survei dan Wawancara')
for i in [5,8,13,20,44,90,124,162,167,175]:
 p=Paragraph(els[i],d)
 for r in p.runs:
  r.font.name='Times New Roman';r.font.size=Pt(14);r.bold=True;r.font.color.rgb=RGBColor(0,0,0)
for name in ['LD Body','LD Caption','LD Exhibit','LD Navigation','LD Reference','LD Table Text']:
 s=d.styles[name]
 s.font.name='Times New Roman';s.font.color.rgb=RGBColor(0,0,0)
s=d.styles['LD Body'];s.font.size=Pt(12);s.paragraph_format.line_spacing=1.5
s.paragraph_format.space_after=Pt(5);s.paragraph_format.first_line_indent=Cm(.65)
s.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
s.paragraph_format.keep_with_next=False;s.paragraph_format.keep_together=False
s.paragraph_format.widow_control=True
d.styles['LD Caption'].paragraph_format.line_spacing=1.12
d.styles['LD Caption'].paragraph_format.space_after=Pt(7)
d.styles['LD Exhibit'].paragraph_format.space_before=Pt(8)
d.styles['LD Exhibit'].paragraph_format.keep_with_next=True

def link(p,label,target):
 h=OxmlElement('w:hyperlink')
 if target.startswith('https:'):
  h.set(qn('r:id'),p.part.relate_to(target,RT.HYPERLINK,is_external=True))
 else: h.set(qn('w:anchor'),target)
 r=OxmlElement('w:r'); pr=OxmlElement('w:rPr')
 col=OxmlElement('w:color');col.set(qn('w:val'),linkcolor)
 u=OxmlElement('w:u');u.set(qn('w:val'),'single')
 pr.extend([col,u]);r.append(pr)
 t=OxmlElement('w:t');t.set(qn('xml:space'),'preserve');t.text=label
 r.append(t);h.append(r);p._p.append(h)

anchors=sorted(heading_ids)
active=13
def section(i):
 global active
 active=i
def move(e):
 dest=next((els[k] for k in anchors if k>active),end)
 dest.addprevious(e)
def para(text='',refs=(),kind='LD Body',anchor=None):
 p=d.add_paragraph(style=kind);move(p._p)
 p.add_run(text)
 for label,target in refs:
  p.add_run('  ' if not text else ' ');link(p,label,target)
 add_book(p,anchor)
 return p
def exhibit(text,anchor=None):
 p=para(text,kind='LD Exhibit',anchor=anchor)
 p.runs[0].bold=True
 p.paragraph_format.first_line_indent=Pt(0)
 return p
def navigation(target):
 p=para('',[('Kembali ke bagian utama',target),('Daftar lampiran','AppendixIndex')],kind='LD Navigation')
 p.paragraph_format.keep_with_next=True
def pic(path,caption,anchor=None,width=15.6):
 pth=root/path
 if not pth.exists():
  return False
 p=para('',kind='LD Caption')
 p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 p.paragraph_format.space_before=Pt(4);p.paragraph_format.space_after=Pt(2)
 p.paragraph_format.first_line_indent=Pt(0);p.paragraph_format.keep_with_next=True
 s=p.add_run().add_picture(str(pth),width=Cm(width));s._inline.docPr.set('descr',caption)
 q=para(caption,kind='LD Caption',anchor=anchor)
 q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.paragraph_format.first_line_indent=Pt(0)
 q.paragraph_format.keep_with_next=False;q.paragraph_format.keep_together=True
 return True
def table(caption,rows,ratios=None,anchor=None):
 c=para(caption,kind='LD Caption',anchor=anchor)
 c.paragraph_format.keep_with_next=True;c.paragraph_format.first_line_indent=Pt(0)
 c.paragraph_format.space_before=Pt(6);c.paragraph_format.space_after=Pt(3)
 t=d.add_table(rows=0,cols=len(rows[0]))
 move(t._tbl);t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
 width=15.85
 ratios=ratios or [1/len(rows[0])]*len(rows[0])
 for col,r in zip(t.columns,ratios):col.width=Cm(width*r)
 pr=t._tbl.tblPr
 borders=OxmlElement('w:tblBorders')
 for side in ['top','left','bottom','right','insideH','insideV']:
  e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'CBD9D1');borders.append(e)
 pr.append(borders)
 margins=OxmlElement('w:tblCellMar')
 for side,v in [('top','52'),('bottom','52'),('left','98'),('right','98')]:
  e=OxmlElement('w:'+side);e.set(qn('w:type'),'dxa');e.set(qn('w:w'),v);margins.append(e)
 pr.append(margins)
 for i,row in enumerate(rows):
  r=t.add_row();r._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  if i==0:r._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
  for j,(cell,content) in enumerate(zip(r.cells,row)):
   cell.width=Cm(width*ratios[j]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   p=cell.paragraphs[0];p.style='LD Table Text';f=p.paragraph_format
   f.line_spacing=1.12;f.space_after=Pt(0);f.first_line_indent=Pt(0)
   f.keep_with_next=i==0;f.alignment=WD_ALIGN_PARAGRAPH.LEFT
   e=OxmlElement('w:shd');e.set(qn('w:fill'),'154938' if i==0 else ('EFF5F1' if i%2==0 else 'FFFFFF'));cell._tc.get_or_add_tcPr().append(e)
   if isinstance(content,tuple):
    link(p,*content)
   else:
    rn=p.add_run(str(content));rn.font.size=Pt(10.5)
    if i==0:rn.bold=True;rn.font.color.rgb=RGBColor.from_string('FFFFFF')
 return t

def old_table(i,caption,ratios=None,anchor=None,rows=None):
 a=[[c.text for c in r.cells] for r in Table(els[i],d).rows]
 return table(caption, rows if rows is not None else a,ratios,anchor)
def old_graph(i,caption,anchor=None,width=15.6):
 b=els[i].xpath('.//a:blip')
 if not b:return
 rid=b[0].get(qn('r:embed')); part=d.part.related_parts[rid]
 p=root/'assets'/f'master-{i}.{part.partname.ext}';p.write_bytes(part.blob)
 return pic(p.relative_to(root),caption,anchor,width)

section(13)
para('Seminggu sebelum pindah kos, seorang mahasiswa menemukan lemari bekas yang sesuai anggaran. Sebelum mengatur penjemputan, ia masih harus tahu apakah engselnya berfungsi dan apakah lemari itu bisa melewati pintu kamar. Dalam survei awal kami, 13 dari 15 responden yang pernah mempertimbangkan iklan furnitur bekas kesulitan memastikan kondisi barang. Sebelas meminta informasi lagi kepada penjual.',[('Hasil survei','B2')])
para('LihatDulu adalah marketplace furnitur bekas yang membawa foto kondisi, ukuran, dan pilihan pengambilan ke halaman barang yang sama. Penjual mengikuti panduan di ponsel untuk mendokumentasikan satu unit. Pembeli menelusuri foto bekas pakai, menilai ukuran, dan mencoba pratinjau penempatan pada barang yang mendukung. Saat memesan, pembeli memilih pengambilan sendiri atau pengiriman pada rute yang tersedia. Penjual menyimpan barang sampai jadwal serah terima, sedangkan tim LihatDulu menggunakan catatan pesanan untuk menangani selisih kondisi.')
para('Penjualan dimulai di kawasan kos sekitar Universitas Indonesia, Depok. Pedagang furnitur bekas menjaga ketersediaan katalog, sementara penghuni yang akan pindah mendapat bantuan menerbitkan barang. Konten “Muat Nggak?” membawa pencari barang ke penawaran yang sesuai ruangnya. Ketika pasokan dan pemenuhan siap di kawasan berikutnya, Bursa Pindahan memberi pembeli kesempatan melihat dan mereservasi barang langsung serta memberi penjual tempat mendaftarkan furnitur.')
para('LihatDulu memperoleh biaya layanan pembeli dan komisi penjual ketika pesanan selesai. Karena pendapatan mengikuti serah terima yang berhasil, perluasan bergantung pada ketersediaan barang dan biaya memperoleh serta melayani setiap pesanan. Langganan katalog 3D untuk bisnis menjadi sumber pendapatan lanjutan setelah pemrosesan media dan dukungannya dapat dijalankan berulang.',[('Proyeksi dan kebutuhan modal','Bab5')])

section(22)
para('Furnitur dapat berganti pemilik selama masih layak pakai, tetapi jalur guna ulang belum berkembang sebanding dengan volume barang yang dibuang. Joint Research Centre memperkirakan sekitar 10 juta ton limbah furnitur per tahun di Uni Eropa dan mencatat terbatasnya investasi untuk guna ulang dan perbaikan (Faraca et al., 2024, hlm. 200–201). Pada sisi permintaan, survei 864 responden Eropa Barat menemukan furnitur bekas mendapat persepsi paling positif dari tiga kategori barang bekas yang dibandingkan (Frahm et al., 2025).')
para('Di Indonesia, penjual dapat menjangkau calon pembeli lewat beberapa kanal. Pada 2024, 94,76% usaha e-commerce menggunakan pesan instan, 29,66% menggunakan media sosial, dan 17,23% menggunakan marketplace. Satu usaha dapat memakai lebih dari satu kanal (BPS, 2025, hlm. 17). Untuk furnitur besar, jarak tetap memengaruhi apakah penawaran yang ditemukan dapat dibeli dan diangkut. Di sekitar Kampus UI Depok, pilihan kos di Kukusan, Pondok Cina, dan Margonda mencakup kamar dengan maupun tanpa perabot. Bagi penyewa yang harus mengisi kamar menjelang pindah, harga meja atau lemari perlu dinilai bersama ukurannya dan cara membawanya (Departemen Kesejahteraan Sosial FISIP UI, t.t.).')

section(29)
para('Ketidakpastian bermula dari barang itu sendiri. Foto keseluruhan bisa menunjukkan bentuk lemari, tetapi bekas air di bawah laci atau fungsi engsel memerlukan informasi yang lebih dekat. Riset tentang pasar barang bekas daring menempatkan kondisi, riwayat penggunaan, dan informasi dari penjual sebagai sumber ketidakpastian sebelum membeli (Ovaz & Hasiloglu, 2026). Pada furnitur, pembeli juga harus mencocokkan dimensi dengan ruang dan memastikan barang bisa melewati pintu atau tangga. Ukuran yang besar dapat menambah pekerjaan dan biaya pemindahan (Hagejärd et al., 2025).')
para('Situs iklan sudah memudahkan pencarian berdasarkan jenis barang dan lokasi. OLX menganjurkan foto yang sesuai, keterangan yang jelas, dan informasi lokasi pertemuan. Panduan bagi pembeli juga menyarankan menghubungi penjual untuk mengetahui spesifikasi lebih lanjut (OLX Indonesia, t.t.-a, t.t.-b). Percakapan dan kunjungan langsung membantu memastikan kondisi. Celahnya muncul ketika pembeli harus merangkai sendiri bukti kondisi, ukuran, dan ongkos angkut dari beberapa percakapan, terutama ketika waktu pindah sudah dekat.')

section(42)
para('Survei awal per 25 November 2026 mencatat 50 respons, terdiri atas 46 mahasiswa dan empat responden lain. Dari 15 responden yang mempertimbangkan satu iklan furnitur bekas dalam 12 bulan terakhir, 13 sulit memastikan kondisi barang, sembilan ragu barang akan muat di ruangan, dan delapan menghadapi ketidakjelasan biaya atau cara mengangkut. Sebelas meminta informasi tambahan kepada penjual dan tujuh melihat barang langsung. Semua 15 responden pada bagian pengalaman iklan adalah mahasiswa, sehingga angka ini menggambarkan pengalaman kelompok tersebut.',[('Lampiran B.2','B2')])
pic('assets/survey-barriers.png','Gambar 1. Informasi yang sulit dipastikan saat mempertimbangkan iklan furnitur bekas',width=14.5)

section(46)
para('LihatDulu adalah marketplace furnitur bekas yang membantu pembeli menilai kondisi dan ukuran barang sebelum mengatur pengambilan atau pengiriman. Di kawasan awal sekitar UI Depok, penghuni kos dapat mencari meja, kursi, rak, atau lemari dari pedagang furnitur bekas dan sesama penghuni yang akan pindah. Setiap penawaran menyertakan foto unit, dimensi yang dicatat penjual, serta kondisi dan lokasi barang. Pembeli dapat membuka pratinjau ruang pada barang yang mendukung, lalu melihat pilihan serah terima pada pesanan yang sama.',[('Model bisnis','A1')])
if not pic('product/hero.png','Gambar 2. Halaman barang, bukti kondisi, dan pratinjau ruang pada prototipe LihatDulu', 'FigHero'):
 old_graph(220,'Gambar 2. Halaman barang pada prototipe LihatDulu','FigHero')

section(53)
para('Bagi pembeli, foto dekat dan catatan kondisi menunjukkan bagian mana yang perlu diperiksa. Penjual mengukur barang dan mencatat fungsi komponen seperti laci atau engsel sekali untuk setiap unit. Pembeli kemudian dapat merujuk pada bukti yang sama ketika bertanya atau memesan. Jika hasil pemindaian layak ditampilkan, model membantu melihat bentuk dari sudut lain. Barang tetap dapat ditawarkan dengan foto asli, ukuran, dan deskripsi kondisi yang lengkap.',[('Kendali mutu listing','F2')])
if not pic('product/vpc.png','Gambar 3. Value Proposition Canvas penjual dan pembeli', 'FigVPC'):
 table('Tabel. Pekerjaan, kendala, dan manfaat pada kedua sisi pasar',[
 ('Sisi pasar','Pekerjaan dan kendala','Manfaat dan cara layanan bekerja'),
 ('Pembeli','Memilih barang yang berfungsi dan muat. Bukti kondisi dan total biaya tersebar.','Saring dari dimensi dan lokasi, cek foto dekat serta lihat opsi terima.'),
 ('Penjual','Mengalihkan stok atau barang pindahan. Menjawab pertanyaan unit berulang.','Dokumentasikan sekali dengan panduan ponsel dan bagikan satu halaman barang.')])

section(60)
para('Penjual lemari contoh mengikuti panduan foto, meninjau gambar, dan mengisi ukuran luar sebelum menerbitkan penawaran. Saat membuka halaman yang sama, pembeli melihat harga dan dimensi, memeriksa titik aus dari foto detail, lalu menggunakan simulasi untuk membayangkan posisi lemari di ruang. Ukuran pintu, tangga, dan jalur masuk diperiksa langsung sebelum barang diangkut.')
if not pic('product/journey.png','Gambar 4. Alur dokumentasi penjual dan pemeriksaan barang oleh pembeli','FigJourney'):
 pic('assets/figures/journey.png','Gambar 4. Alur dokumentasi penjual dan pemeriksaan barang oleh pembeli','FigJourney')
para('Setelah memilih barang, pembeli melihat total biaya dan menentukan ambil sendiri atau meminta pengiriman. Penjual mengonfirmasi stok serta waktu. Catatan pesanan menyimpan versi bukti yang dipakai pembeli sehingga tim dukungan dapat memeriksa perbedaan kondisi saat barang diterima. Tangkapan layar memperlihatkan perjalanan di prototipe. Pembayaran, pengiriman, dan pengaduan mengikuti rancangan operasi marketplace.',[('Rangkaian tangkapan layar','C2'),('Alur operasi','F1')])

section(68)
para('Mesin rekonstruksi LihatDulu dikembangkan dari percobaan yang memproses rekaman tanpa mengirimnya ke layanan rekonstruksi eksternal. FFmpeg menyiapkan bingkai dari video ponsel. COLMAP mendaftarkan bingkai dan memperkirakan posisi kamera, lalu Brush mengoptimalkan representasi Gaussian splat untuk diekspor sebagai SPZ. Penampil memuat hasil bersama foto asli. Pada rancangan produksi, aplikasi memeriksa cakupan sudut dan menilai kelayakan hasil sebelum menentukan media yang ditampilkan pertama.',[('Seri pemrosesan lokal','C7')])
if not pic('product/pipeline.png','Gambar 5. Arsitektur mesin rekonstruksi LihatDulu dan keputusan penayangan', 'FigPipeline'):
 table('Gambar 5. Arsitektur rekonstruksi lokal dan penayangan',[
 ('Rekaman','Rekonstruksi','Publikasi'),('FFmpeg mengekstrak bingkai','COLMAP memperkirakan pose. Brush mengoptimalkan splat dan mengekspor SPZ.','Cek liputan dan artefak. Foto tampil lebih dulu bila model lemah.')])
para('Seri lokal menghasilkan berkas SPZ dari tujuh rekaman kursi yang sama. Berkas yang dapat dibuka menunjukkan bahwa alur dapat dijalankan, sementara sebagian hasil memperlihatkan fragmen atau bentuk yang kurang utuh. Pada demonstrasi terpisah yang mengintegrasikan keluaran rekonstruksi GLB pihak ketiga, 101 bingkai menghasilkan berkas olahan sekitar 1,95 MB dalam sekitar 1 menit 45 detik. Model dapat diputar, tetapi sebagian sandaran, dudukan, dan sambungan bawah tidak terbentuk dengan baik. Karena itu, foto asli langsung ditampilkan agar kondisi unit tetap dapat diperiksa.',[('Hasil dan asal pemrosesan','C3')])
if not pic('product/chair.png','Gambar 6. Bingkai kursi, hasil rekonstruksi GLB, dan tampilan foto asli','FigChair'):
 pic('assets/figures/chair.png','Gambar 6. Bingkai kursi, hasil rekonstruksi GLB, dan tampilan foto asli','FigChair')
para('Nilai penyajian bukti diuji melalui contoh iklan lemari. Sesudah membaca catatan kondisi dan melihat foto dekat, 29 dari 50 responden melaporkan keyakinan yang lebih tinggi untuk menilai kondisi, 14 tetap, dan tujuh turun. Dari 24 orang yang semula ingin bertanya, 13 memilih mengatur kunjungan dan enam ingin menghubungi penjual untuk membeli atau mengatur pengambilan. Hasil ini mencatat pilihan pada demo berurutan dengan beberapa informasi tambahan, sehingga perubahan tersebut belum bisa dikaitkan pada satu fitur atau digunakan sebagai konversi penjualan.',[('Perbandingan respons demo','B3')])

section(82)
para('Penjual menerbitkan listing standar secara gratis. Pembeli membayar biaya layanan tetap per pesanan, sedangkan komisi penjual dihitung dari harga barang dan dipotong dari hasil penjualan. Kedua biaya menjadi pendapatan ketika pesanan selesai. Pembeli melihat total sebelum membayar dan penjual melihat hasil bersih sebelum menyepakati pesanan. Pada pesanan yang batal atau dikembalikan penuh, kedua biaya dikeluarkan dari pendapatan. Ongkos angkut dicatat sebagai pembayaran untuk layanan pengiriman.',[('Rincian penyelesaian dana','A2')])
pic('exhibits/revenue.png','Gambar 7. Aliran dana pada pesanan selesai','FigRevenue')
para('Setelah pemrosesan media stabil, pedagang furnitur dapat berlangganan penampil 3D yang ditanam di katalog mereka. Paket mencakup penyimpanan dan kuota pemrosesan. Pendapatan langganan mengikuti periode layanan dan dihitung terpisah dari transaksi marketplace.')

section(92)
para('Penjual menyiapkan bukti dan menyimpan barang hingga jadwal pengambilan. Tim katalog memeriksa kelengkapan sebelum listing terbit. Pembeli memilih metode penerimaan, lalu penjual mengonfirmasi stok dan waktu. Jika pembeli memilih pengiriman, dukungan pesanan memeriksa rute serta slot dengan penyedia angkut sebelum pembeli berkomitmen. Saat ada selisih kondisi, dukungan membandingkan barang dengan bukti pesanan sebelum dana diselesaikan.',[('Pemilik proses dan jalur pengecualian','F1')])
pic('exhibits/operations.png','Gambar 8. Alur pesanan dari dokumentasi barang hingga serah terima','FigOperations')
section(99)
para('Pedagang furnitur bekas memberi pasokan berulang, sedangkan penghuni yang pindah menambah pilihan pada periode pergantian kos. Barang tetap berada pada penjual, sehingga perluasan katalog bergantung pada kemampuan tim memeriksa listing dan memastikan stok, serta pada kapasitas serah terima di tiap area. Penyimpanan media dan antrean rekonstruksi ditangani tim teknis. Operasi katalog memeriksa bukti dan dukungan pesanan mengurus jadwal serta keluhan.')
pic('exhibits/supply.png','Gambar 9. Sumber pasokan dan sumber daya pemenuhan','FigSupply')
section(103)
para('Foto unit, dimensi dengan satuan yang jelas, dan uraian kondisi menjadi syarat minimum publikasi. Tim katalog mengembalikan listing dengan instruksi spesifik bila foto atau ukuran belum memadai. Bila model 3D memiliki celah besar, halaman membuka foto asli. Pada saat volume naik, listing yang sudah lengkap tetap dapat terbit sementara antrean model ditangani terpisah, sehingga kapasitas pemrosesan 3D tidak menentukan seluruh kapasitas katalog.',[('Alur pemeriksaan bukti','F2'),('Model kapasitas','F3')])
section(108)
para('Enam bulan pertama dipakai untuk menjalankan alur jual beli di klaster UI Depok. Fase berikutnya mengulang akuisisi di klaster berdekatan sekaligus memperbaiki pemrosesan media dan dukungan. Sejak tahun kedua, Bursa Pindahan membuka area baru setelah stok, pengambilan, dan penanganan masalah siap. Pengembangan katalog B2B dan API mengikuti mutu pemrosesan dan kapasitas dukungan. Perkiraan pendanaan mengikuti kebutuhan masing-masing tahap.',[('Prasyarat perluasan','F4')])
pic('exhibits/roadmap.png','Gambar 10. Jadwal indikatif peluncuran dan ekspansi','FigRoadmap')
section(116)
para('Ukuran utama operasi adalah pesanan yang benar-benar selesai. Tim membaca angka itu bersama ketersediaan listing dan waktu terbit agar tahu apakah kemacetan terjadi saat penjual memasukkan barang, pembeli memilih, atau kedua pihak mengatur serah terima.')
old_table(119,'Tabel 1. Indikator untuk mengarahkan perbaikan operasi',[.26,.42,.32])
section(121)
para('Stok yang sudah terjual atau angkutan tanpa slot dapat menggagalkan pesanan di akhir. Tim mengonfirmasi keduanya sebelum pembayaran. Peta berikut memakai penilaian awal untuk menentukan urutan pengendalian. Tim memperbaruinya dari kejadian pesanan setelah layanan berjalan.',[('Indikator dan penanggung jawab risiko','F5')])
pic('exhibits/risks.png','Gambar 11. Peta risiko operasi berdasarkan kemungkinan dan dampak','FigRisk')

section(126)
para('Pasar awal dipilih berdasarkan momen pindah. Mahasiswa kos dan penyewa muda di sekitar UI Depok membutuhkan barang yang bisa dibandingkan dengan ukuran kamar dan diambil sebelum waktu pindah. Pedagang furnitur bekas menjaga stok, sedangkan penghuni yang akan pindah memasok unit tambahan. Dengan satu wilayah yang rapat, tiap barang yang masuk katalog dapat dipromosikan kepada pembeli yang bisa mengambilnya.',[('Dasar profil pembeli','B2')])
pic('marketing/stp.png','Gambar 12. Segmentasi, target, dan posisi LihatDulu di wilayah awal','FigSTP')
pic('marketing/personas.png','Gambar 13. Profil kerja pembeli kos dan pedagang furnitur bekas','FigPersona')
para('Profil pembeli merujuk pada pengalaman responden mahasiswa. Profil pedagang dan pola pasokannya menjadi hipotesis kerja untuk wawancara penjual.',[('Panduan wawancara','B4')])

section(134)
para('Peluang LihatDulu diukur sebagai pendapatan tahunan dari biaya layanan pembeli dan komisi penjual atas pesanan furnitur bekas yang selesai. TAM mencakup Indonesia, SAM menyaring area Jabodetabek yang dapat dilayani, dan SOM tahun ketiga didasarkan pada jumlah pesanan yang dapat dipenuhi di klaster aktif.',[('Definisi dan masukan','D1')])
pic('marketing/market.png','Gambar 14. TAM, SAM, dan SOM dari pendapatan transaksi marketplace','FigMarket')
para('Susenas Maret 2026 mencatat rata-rata belanja mebel Rp3.376 per orang per bulan. Jika diterapkan pada proyeksi penduduk pertengahan 2026, belanja mebel nasional setara sekitar Rp11,63 triliun per tahun (BPS, 2026a, 2026b). Angka ini mencakup kategori mebel secara umum. Untuk memperoleh GMV furnitur bekas dan mengubahnya menjadi pendapatan platform, diperlukan porsi belanja bekas, cakupan layanan, nilai pesanan rata-rata, dan tarif. Khusus SOM, pesanan selesai dibatasi oleh permintaan yang dapat dijangkau, unit tersedia yang terjual, serta slot pemenuhan.',[('Rumus dan batas kapasitas','D3')])

section(141)
para('Alternatif terdekat pembeli adalah mencari di situs iklan, bertanya lewat chat, atau melihat barang langsung. Masing-masing berguna pada tahap berbeda. LihatDulu bersaing pada keputusan sebelum kunjungan dan menjaga bukti yang sama sampai serah terima.',[('Contoh listing dan panduan OLX','D4')])
old_table(144,'Tabel 2. Alternatif pembeli menurut kegunaannya',[.27,.35,.38])
para('Bukti per unit memudahkan penyaringan sekaligus menambah pekerjaan pemeriksaan. Musim pindah mempertemukan pasokan dan permintaan setempat. Untuk mengurangi transaksi yang beralih ke chat, biaya ditampilkan sejak awal dan catatan kondisi tetap dapat dibuka sampai serah terima.',[('Kendali mutu','F2')])

section(148)
para('LihatDulu mempromosikan barang yang tersedia dan bisa diambil atau dikirim di area sasaran. Setiap fase memperluas jangkauan sesudah tim siap memenuhi pesanan di klaster berikutnya.')
table('Tabel 3. Marketing mix di klaster peluncuran',[
 ('Unsur','Keputusan peluncuran'),
 ('Product','Meja, kursi, rak, dan lemari dengan foto kondisi, dimensi, ketersediaan, dan pilihan penerimaan.'),
 ('Price','Listing standar gratis. Biaya layanan pembeli dan komisi penjual berlaku pada pesanan selesai.'),
 ('Place','Katalog web untuk klaster kos sekitar UI Depok. Ambil sendiri atau pengiriman sesuai rute barang.'),
 ('Promotion','Katalog terkurasi melalui pengelola kos dan komunitas pindahan, lalu konten “Muat Nggak?” serta Bursa Pindahan.')],[.19,.81])
exhibit('Fase 1 · Bulan 0–6 · Isi katalog di sekitar UI Depok','Phase1')
para('Tim mendatangi pedagang furnitur bekas dan menawarkan bantuan membuat listing pertama. Pengelola kos dan komunitas pindahan menjadi jalur untuk mengajak penghuni yang akan keluar memasukkan barang. Pembeli menerima tautan koleksi menurut ukuran dan lokasi. Tim memperluas promosi setelah listing lengkap tersedia dan pesanan mulai dapat diselesaikan dalam klaster.',[('Pelaksanaan per fase','G1')])
pic('marketing/phase-1.png','Gambar 15. Contoh materi akuisisi pembeli dan pemasok di klaster UI Depok',width=14.95)

section(153)
exhibit('Fase 2 · Bulan 6–12 · Ulangi “Muat Nggak?” di klaster berdekatan','Phase2')
para('Kreator lokal membuka konten dengan masalah nyata, misalnya meja yang harus masuk di antara dinding dan kasur. Mereka menunjukkan pengukuran, kondisi barang, dan cara mengecek pengambilan. Tautan membawa penonton ke barang yang masih tersedia atau koleksi setempat. Tim melacak jumlah pesanan selesai dan biaya per pesanan per kanal. Jika kunjungan tinggi tetapi checkout tertahan, tim memeriksa stok, kelengkapan informasi, atau biaya angkut sebelum menaikkan belanja promosi.')
pic('marketing/phase-2.png','Gambar 16. Contoh materi kreator “Muat Nggak?” dan tujuan klik')
pic('marketing/funnel.png','Gambar 17. Perjalanan dari melihat konten hingga pesanan selesai','FigFunnel')
p=exhibit('Fase 3 · Tahun kedua dan seterusnya · Bursa Pindahan LihatDulu','Phase3')
p.paragraph_format.page_break_before=True
para('Bursa Pindahan membuka klaster berikutnya saat stok dan penjemputan sudah siap. Garis di lantai menggambarkan denah kamar kos. Pengunjung dapat memeriksa furnitur asli, mencocokkan ukuran, lalu memindai tag kondisi untuk membuka listing. Pembeli mereservasi barang dengan jadwal pengambilan. Penghuni yang akan pindah membawa foto dan ukuran ke meja bantuan untuk mendaftarkan penawaran.')
pic('marketing/phase-3.png','Gambar 18. Ilustrasi rencana Bursa Pindahan LihatDulu','FigBursa')
para('Petugas mencocokkan reservasi dengan ketersediaan unit dan waktu penjual. Tautan acara menandai asal listing dan pesanan agar tim dapat mengukur listing yang terbit, pesanan yang selesai dalam 30 hari, dan biaya acara per pesanan selesai. Anggaran acara mencakup ruang, materi, petugas, dan angkutan contoh.',[('Contoh materi di lokasi','G4'),('Definisi konversi','G2')])

section(157)
para('Pembeli yang belum selesai mengisi kamar dapat menyimpan pencarian dan memilih pengingat barang baru sesuai rentang ukuran, harga, dan lokasi. Bagi pedagang, panduan yang sama mempersingkat persiapan penawaran berikutnya. Tim membandingkan pembukaan ulang pencarian dengan pembelian ulang, serta listing baru pedagang dengan penjualan yang selesai. Pola ini membantu menentukan klaster yang layak menerima lebih banyak pasokan dan promosi.',[('Ukuran retensi','G3')])

section(164)
para('Proyeksi marketplace mengikuti pesanan yang berhasil dipenuhi per klaster. Pendapatan berasal dari biaya pembeli per pesanan dan komisi dari nilai barang yang selesai terjual. Setelah dikurangi biaya pembayaran, penyimpanan dan pemrosesan media, serta dukungan variabel, kontribusi per pesanan menutup biaya tim, teknologi, dan pemasaran. Pendapatan katalog B2B mengikuti jumlah pelanggan aktif dan periode layanan.')
table('Tabel 4. Hasil utama proyeksi usaha',[
 ('Ukuran','Dasar perhitungan','Hasil proyeksi'),
 ('Pesanan selesai','Permintaan, penjualan unit, dan kapasitas','[Pesanan tahun 1 dan tahun 3]'),
 ('Pendapatan marketplace','Biaya pembeli × pesanan + komisi × nilai barang','[Rp per tahun]'),
 ('Pendapatan katalog B2B','Pelanggan aktif × tarif periode layanan','[Rp per tahun]'),
 ('Kontribusi dan laba operasi','Pendapatan dikurangi biaya variabel, lalu biaya tetap','[Rp per tahun]'),
 ('Volume impas','Biaya tetap ÷ kontribusi per pesanan pada fase awal','[Pesanan per bulan]'),
 ],[.26,.46,.28],'FinancialResults')
para('Batas harga, skenario pesanan, dan rincian biaya diturunkan ke model bulanan.',[('Lampiran E','E1')])

section(166)
para('Modal awal membiayai kesiapan katalog dan serah terima di sekitar UI. Kebutuhan berikutnya mengikuti kapasitas pemrosesan dan biaya membuka klaster baru. Arus kas diproyeksikan berdasarkan waktu penerimaan biaya dan pengeluaran operasional. Nilai barang dan ongkos pengiriman pada dana pesanan dipisahkan dari kas yang menjadi milik platform.')
table('Tabel 5. Arus kas dan kebutuhan pendanaan',[
 ('Ukuran','Dasar pengisian','Hasil proyeksi'),
 ('Kebutuhan dana awal','Defisit kas puncak sebelum pendanaan dan cadangan operasi','[Rp dan sumber pendanaan]'),
 ('Kas minimum','Saldo bulanan terendah serta waktu terjadinya','[Rp dan bulan]'),
 ('Pencairan per tahap','Kebutuhan peluncuran UI, penguatan operasi, dan ekspansi','[Rp dan waktu]'),
 ('Kelayakan investasi','Arus kas proyek, horizon, dan asumsi diskonto','[NPV, IRR, payback]'),
 ],[.26,.46,.28],'FinancialCash')

references=[
 ('Badan Pusat Statistik. (2025). Statistik E-Commerce 2024.','Publikasi BPS','https://www.bps.go.id/id/publication/2025/11/28/647323224ecc656c2933571b/statistik-e-commerce-2024.html'),
 ('Badan Pusat Statistik. (2026a). Pengeluaran untuk konsumsi penduduk Indonesia Maret 2026. Tabel 3.4, hlm. 40.','Publikasi BPS','https://www.bps.go.id/id/publication/2026/10/05/4e167126f0dc9e67c8e602b2/pengeluaran-untuk-konsumsi-penduduk-indonesia-maret-2026.html'),
 ('Badan Pusat Statistik. (2026b). Jumlah penduduk menurut kelompok umur dan jenis kelamin, Indonesia, 2026.','Tabel BPS','https://www.bps.go.id/id/statistics-table/3/WVc0MGEyMXBkVFUxY25KeE9HdDZkbTQzWkVkb1p6MDkjMw%3D%3D/jumlah-penduduk-menurut-kelompok-umur-dan-jenis-kelamin.html'),
 ('Departemen Kesejahteraan Sosial FISIP Universitas Indonesia. (t.t.). Layanan mahasiswa.','Universitas Indonesia','https://socialwelfare.fisip.ui.ac.id/layanan-mahasiswa/'),
 ('Faraca, G., Ranea Palma, A., Spiliotopoulos, C., Rodríguez Manotas, J., Sanyé Mengual, E., Amadei, A. M., Maury, T., Pasqualino, R., Wierzgala, P., Perez Camacho, M. N., Alfieri, F., Bernad Beltran, D., Lag Brotons, A., Delre, A., Perez Arribas, Z., Arcipowska, A., La Placa, M. G., Ardente, F., Mathieux, F., & Wolf, O. (2024). Ecodesign for Sustainable Products Regulation: Study on new product priorities. Publications Office of the European Union.','DOI 10.2760/7400680','https://doi.org/10.2760/7400680'),
 ('Frahm, L. B., Mugge, R., & Laursen, L. N. (2025). Walk a mile in someone’s sweaty second-hand shoes: Differences in motivations and barriers for second-hand products. Resources, Conservation & Recycling, 219, 108307.','DOI 10.1016/j.resconrec.2025.108307','https://doi.org/10.1016/j.resconrec.2025.108307'),
 ('Hagejärd, S., Femenías, P., & Pettersen, I. N. (2025). User perspectives on circular value propositions for kitchen furniture and appliances. Circular Economy and Sustainability, 5, 4389–4420.','DOI 10.1007/s43615-025-00560-0','https://doi.org/10.1007/s43615-025-00560-0'),
 ('KIRI Engine. (t.t.). Image upload.','Dokumentasi Photo Scan','https://docs.kiriengine.app/photo-scan/image-upload/'),
 ('LihatDulu. (2026a). Bukti prototipe dan rekonstruksi kursi [Repositori, revisi 29961f0].','Repositori','https://github.com/Fafauzif/Lihatdulu/tree/29961f0'),
 ('LihatDulu. (2026b). Survei furnitur bekas LihatDulu v3 [Data primer sementara, 25 November 2026].','Ringkasan dan metode','B1'),
 ('OLX Indonesia. (t.t.-a). Tips pasang iklan yang baik dan benar.','Pusat Bantuan OLX','https://www.olx.co.id/help/pasang-iklan/cara-pasang-dan-kelola-iklan/panduan-pasang-iklan/tips-pasang-iklan-yang-baik-dan-benar'),
 ('OLX Indonesia. (t.t.-b). Tips jual beli.','Pusat Bantuan OLX','https://www.olx.co.id/help/kebijakan-dan-privasi/panduan-keamanan/tips-bertransaksi-aman/tips-jual-beli'),
 ('Schönberger, J. L., & Frahm, J.-M. (2016). Structure-from-motion revisited. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 4104–4113.','CVF Open Access','https://openaccess.thecvf.com/content_cvpr_2016/html/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.html'),
 ('Ovaz, F., & Hasiloglu, S. B. (2026). Perceived effectiveness of risk-reduction strategies in online second-hand marketplaces: The pre-purchase decision process. Journal of Theoretical and Applied Electronic Commerce Research, 21(11), 389.','DOI 10.3390/jtaer21110389','https://doi.org/10.3390/jtaer21110389'),
]
section(167)
for text,label,uri in sorted(references):
 p=para(text,[(label,uri)],kind='LD Reference')
 p.paragraph_format.line_spacing=1.1;p.paragraph_format.space_after=Pt(6);p.paragraph_format.keep_together=True

section(175)
table('Daftar bukti pendukung',[
 ('Lampiran','Bukti yang dapat diperiksa','Bagian utama'),
 (('A · Model bisnis','AppendixA'),'Business Model Canvas dan aliran transaksi',('§2.5','Sec25')),
 (('B · Survei dan wawancara','AppendixB'),'Metode, temuan pengalaman belanja dan demo, panduan wawancara',('§1.3','Sec13')),
 (('C · Bukti prototipe','AppendixC'),'Tangkapan layar, hasil GLB, seri lokal SPZ, dan batas hasil',('§2.4','Sec24')),
 (('D · Pasar dan pesaing','AppendixD'),'Dasar penghitungan pendapatan pasar dan pembanding',('§4.2','Sec42')),
 (('E · Keuangan','AppendixE'),'Masukan proyeksi, kontribusi, kas, dan pendanaan',('Bab V','Bab5')),
 (('F · Operasi','AppendixF'),'Titik serah kerja, kapasitas, jadwal, dan penanganan risiko',('Bab III','Bab3')),
 (('G · Pemasaran','AppendixG'),'Contoh kampanye, penelusuran pesanan, dan retensi',('§4.4','Sec44')),
 ],[.29,.53,.18])

section(181)
navigation('Sec25')
exhibit('A.1 Business Model Canvas LihatDulu','A1')
pic('assets/bmc.png','Gambar A.1. Hubungan pelanggan, kegiatan, sumber daya, biaya, dan pendapatan')
exhibit('A.2 Aliran barang, bukti, dan dana','A2')
old_table(190,'Tabel A.1. Jejak pesanan sampai penyelesaian dana',[.16,.45,.39])

section(193)
navigation('Sec13')
exhibit('B.1 Cakupan survei dan aturan pembacaan','B1')
para('Data sementara per 25 November 2026 terdiri atas 50 jawaban, 46 mahasiswa dan empat responden lain. Sebanyak 24 belum mencari furnitur bekas daring dalam 12 bulan terakhir, 11 sempat mencari tanpa menimbang satu iklan, dan 15 menimbang sedikitnya satu iklan. Penyebut hambatan, tindakan, dan hasil pembelian adalah 15. Penyebut evaluasi demo adalah 50 pasangan lengkap. Sampel ini didominasi mahasiswa dan berdasar jawaban responden yang terkumpul.')
exhibit('B.2 Tindakan pada iklan terakhir','B2')
pic('assets/survey-actions.png','Gambar B.1. Tindakan setelah melihat iklan terakhir')
para('Pertanyaan hambatan dan tindakan mengizinkan beberapa jawaban. Seorang responden memilih “tidak melakukan tindakan lanjutan” sekaligus mencari pilihan lain. Enam orang membeli barang pada iklan, dua membeli barang bekas lain, satu membeli barang baru, tiga masih mempertimbangkan, dan tiga membatalkan pembelian furnitur yang dicari.')
exhibit('B.3 Respons saat bukti kondisi ditambahkan','B3')
pic('assets/survey-demo.png','Gambar B.2. Perubahan keyakinan dan rencana tindakan pada contoh iklan')
para('Tahap awal memperlihatkan kabinet contoh tertutup dan terbuka. Tahap kedua menambahkan contoh cacat tercatat dan foto dekat. Urutan tetap dan beberapa detail ditambahkan bersamaan. Karena itu pola respons bersifat deskriptif. Dari 28 jawaban terbuka yang substantif, tema yang muncul antara lain foto menyeluruh, kejelasan cacat, fungsi engsel atau pintu, bahan, dan lokasi. Nilai digunakan untuk menajamkan atribut yang diuji, dengan penilaian akhir mengikuti data lengkap.')
exhibit('B.4 Panduan wawancara penjual dan pembeli','B4')
old_table(201,'Tabel B.1. Pengalaman pembeli',[.15,.85])
old_table(205,'Tabel B.2. Pengalaman penjual',[.15,.85])
para('Setiap wawancara mengikuti satu pengalaman nyata. Catatan anonim memuat konteks barang, kanal, informasi yang hilang, tindakan, dan hasil. Temuan wawancara penjual ditambahkan setelah pengumpulan.',kind='LD Caption')

section(211)
navigation('Sec24')
exhibit('C.1 Artefak prototipe yang dapat diperiksa','C1')
para('Tangkapan Sora berasal dari rilis 29961f0 dan menggunakan kabinet contoh. Galeri kursi berasal dari uji atas objek fisik. Penampil mandiri menyimpan keluaran agar evaluasi bentuk dan pilihan bukti dapat diulangi.',[
 ('Repositori rilis 29961f0','https://github.com/Fafauzif/Lihatdulu/tree/29961f0'),
 ('Penampil kursi','https://github.com/Fafauzif/Lihatdulu/blob/29961f0/docs/handoff/explore/chair-explore.html')])
exhibit('C.2 Halaman barang dan rincian harga','C2')
if not pic('product/appendix_sora.png','Gambar C.1. Halaman barang, galeri kondisi, dan rincian harga prototipe'):
 old_graph(220,'Gambar C.1. Halaman barang dan rincian harga prototipe')
para('Harga dan ongkos di layar merupakan isian demonstrasi. Penilaian keuangan memakai asumsi harga pesanan sendiri.',kind='LD Caption')
exhibit('C.3 Dua pengujian GLB pada satu kursi','C3')
para('Dua hasil GLB menggunakan KIRI Engine Photo Scan dengan masking. LihatDulu mengolah hasil untuk penampil dan memilih media antara foto dan model. Waktu berikut mencakup tahapan sesuai catatan masing-masing dan berasal dari satu barang.',[
 ('Catatan pemrosesan','https://github.com/Fafauzif/Lihatdulu/blob/29961f0/docs/handoff/refinement.md'),
 ('Metadata hasil demo','https://github.com/Fafauzif/Lihatdulu/blob/29961f0/public/demo/kursi/job.json')])
old_table(226,'Tabel C.1. Masukan dan keluaran dua proses GLB',[.24,.38,.38])
exhibit('C.4 Bentuk kursi dan celah yang terlihat','C4')
old_graph(232,'Gambar C.2. Empat sudut GLB mentah dan olahan')
old_graph(234,'Gambar C.3. Foto sumber dan model dari sudut yang mendekati arah serupa')
exhibit('C.5 Hasil pembersihan dan percobaan penutupan celah','C5')
pic('assets/figures/fragment.png','Gambar C.4. Segitiga fragmen yang dihapus pada dua percobaan',width=14.8)
para('Penghapusan 354 segitiga pada uji terdahulu menunjukkan tindakan pembersihan. Pada hasil demo, jumlah segitiga tetap. Percobaan penutupan celah berbasis siluet menghasilkan permukaan yang menutup bagian terbuka. Irisan relatif siluet (IoU) dalam uji itu turun dari 0,144 pada hasil tanpa pengisian ke 0,026 setelah pengisian. Percobaan tersebut dihentikan.')
exhibit('C.6 Aturan penayangan foto dan model','C6')
para('Proporsi area kosong proyeksi pada sudut terburuk sekitar 18,8% pada hasil demo. Ukuran ini mencakup kemungkinan celah fisik dan kegagalan rekonstruksi. Aturan penayangan mengutamakan foto ketika bentuk tidak meyakinkan. Data dimensi tetap berasal dari pengukuran penjual.')
exhibit('C.7 Pemrosesan lokal dari tujuh rekaman kursi','C7')
pic('product/appendix_local.png','Gambar C.5. Foto bingkai sumber dan keluaran SPZ percobaan lokal')
old_table(248,'Tabel C.2. Seri FFmpeg, COLMAP, dan Brush pada kursi fisik yang sama',[.18,.20,.21,.23,.18])
para('Pendaftaran bingkai dan keluaran yang bisa dibuka mengukur keberhasilan proses. Pada seri ini keluaran masih dapat mengandung fragmen dan kabut. Pemrosesan lokal menerbitkan SPZ, sedangkan dua pengujian pada Tabel C.1 menggunakan GLB dari jalur terpisah.',[
 ('Manifest tujuh rekaman','https://github.com/Fafauzif/Lihatdulu/blob/cbf69f0/docs/handoff/scan-evidence-manifest.json')])

section(252)
navigation('Sec42')
exhibit('D.1 Dasar pengeluaran dan konversi ke pendapatan','D1')
table('Tabel D.1. Input pasar dan status pengukuran',[
 ('Komponen','Nilai atau definisi','Peran dalam perhitungan'),
 ('Belanja mebel nasional','Rp3.376 per kapita per bulan','BPS, Susenas Maret 2026, Tabel 3.4'),
 ('Penduduk Indonesia','287.198.400 jiwa','BPS, proyeksi pertengahan 2026'),
 ('Patokan nasional belanja mebel','Rp11.634.981.580.800 per tahun','Perkalian dua input × 12; kategori mebel umum'),
 ('GMV furnitur bekas','Belanja mebel × proporsi pengeluaran untuk unit bekas','[Porsi terukur per area]'),
 ('Pesanan setara','GMV furnitur bekas ÷ nilai barang rata-rata per pesanan','[Harga barang rata-rata per area]'),
 ('Biaya pembeli dan komisi','Biaya tetap per pesanan dan persentase nilai barang','[Tarif Bab V]')
 ],[.28,.38,.34])
exhibit('D.2 Penyaringan menurut area layanan','D2')
para('TAM menggunakan transaksi furnitur bekas rumah tangga di Indonesia. SAM membatasi kategori yang dapat didokumentasikan serta area Jabodetabek yang memiliki penjual, pembeli, dan salah satu opsi serah terima. Porsi wilayah dihitung dari pengeluaran kategori yang sepadan atau dari penjumlahan klaster tanpa tumpang tindih. Satu unit yang muncul di beberapa kanal tetap dihitung sekali.')
exhibit('D.3 Pesanan dan kapasitas pada tahun ketiga','D3')
table('Tabel D.2. Rekonsiliasi SOM dengan pesanan selesai',[
 ('Batas','Penggerak per klaster','Pengukuran'),
 ('Permintaan','Calon pembeli yang memenuhi kriteria × tingkat penyelesaian','Pesanan per tahun'),
 ('Pasokan','Unit layak jual tersedia selama tahun berjalan × tingkat unit terjual lewat platform','Pesanan per tahun'),
 ('Pemenuhan','Slot serah terima layak, setelah memperhitungkan pembatalan','Pesanan per tahun'),
 ('SOM','Jumlah batas terendah setiap klaster × biaya pembeli + komisi × GMV pesanan tersebut','Pendapatan platform per tahun')
 ],[.18,.60,.22])
para('Perhitungan memakai satu unit furnitur per pesanan sebagai basis dan diselaraskan dengan definisi pesanan pada Bab V. Komisi dan biaya pembeli dihitung dari pesanan yang memenuhi syarat pengakuan. Langganan B2B menggunakan model pelanggan dan tarif tersendiri.')
exhibit('D.4 Contoh penyajian pada situs iklan','D4')
old_table(269,'Tabel D.3. Informasi awal dalam dua hasil penelusuran OLX',[.34,.25,.41])
para('',[('Penelusuran lemari bekas','https://www.olx.co.id/items/q-lemari-bekas-bekas'),('Penelusuran lemari tiga pintu','https://www.olx.co.id/mebel_c4835/q-lemari-3-pintu-bekas')],kind='LD Caption')
para('Judul pada hasil penelusuran menunjukkan informasi yang tersedia sebelum halaman detail dibuka. Harga yang terlihat adalah harga penawaran. Gunakan judul sebagai contoh penyajian, karena kelengkapan perlu diperiksa pada halaman masing-masing.')

section(274)
navigation('Bab5')
exhibit('E.1 Masukan untuk model bulanan','E1')
table('Tabel E.1. Penggerak volume, biaya, dan kas',[
 ('Kelompok','Masukan per fase'),
 ('Volume dan harga','Listing aktif, unit terjual, pesanan selesai, nilai barang rata-rata, tarif biaya pembeli, komisi penjual, pelanggan B2B dan tarif langganan.'),
 ('Biaya per pesanan','Pembayaran, dukungan dan pengaduan, pemrosesan, penyimpanan, dan subsidi apabila tersedia.'),
 ('Biaya tetap dan investasi','Tim, sistem, infrastruktur, pemasaran lokal, pengembangan teknologi, dan belanja awal.'),
 ('Bursa Pindahan','Tempat, petugas, material, angkutan barang contoh, jumlah listing, dan pesanan selesai.'),
 ('Kas dan pendanaan','Waktu pencairan, modal kerja, cadangan, sumber dan biaya modal, serta skenario penjualan rendah.')
 ],[.29,.71])
exhibit('E.2 Pemeriksaan antarbagian','E2')
para('Volume tahunan mengikuti batas pasar, pasokan, dan pemenuhan. Arus kas memakai tanggal penerimaan dan pembayaran yang terkait. Dana harga barang dan ongkos pengiriman dipisahkan dari pendapatan platform. Pada skenario rendah, pesanan berkurang dan biaya tetap tetap berjalan. Perluasan dievaluasi berdasarkan kemampuan kas menutup operasi dan biaya klaster selanjutnya.')

section(277)
navigation('Sec31')
exhibit('F.1 Titik serah terima pekerjaan','F1')
old_table(282,'Tabel F.1. Pemilik pekerjaan, keluaran, dan jalur pengecualian',[.22,.21,.28,.29])
exhibit('F.2 Pemeriksaan bukti listing','F2')
pic('assets/figures/quality.png','Gambar F.1. Jalur publikasi foto dan penambahan model')
exhibit('F.3 Batas kapasitas','F3')
old_table(291,'Tabel F.2. Pengukuran kapasitas berdasarkan sumber daya',[.25,.52,.23])
exhibit('F.4 Keluaran dan prasyarat perpindahan fase','F4')
table('Tabel F.3. Ukuran kesiapan untuk ekspansi',[
 ('Tahap','Penanggung jawab','Keluaran dan kondisi'),
 ('0–6 bulan · Klaster UI','Produk, operasi, akuisisi','Kerja sama pemasok dijajaki, barang tersedia, dan pesanan selesai dapat dicatat.'),
 ('6–12 bulan · Klaster berdekatan','Pemasaran, teknis, operasi','Konten penjualan dapat ditelusuri ke pesanan selesai. Media dan dukungan dapat mengikuti volume.'),
 ('Tahun kedua dan seterusnya','Operasi, pemasaran, pengembangan bisnis','Jalankan Bursa Pindahan setelah stok dan serah terima siap. Perluas langganan dan API ketika kemampuan layanan serta pendanaan mendukung.')
 ],[.25,.25,.50])
exhibit('F.5 Risiko dan respons operasi','F5')
risk=[[c.text for c in r.cells] for r in Table(els[300],d).rows]
for i,row in enumerate(risk[1:],1):row[0]=f'R{i} · {row[0]}'
table('Tabel F.4. Pemicu risiko dan pemilik respons',risk,[.25,.36,.39])

section(302)
navigation('Sec44')
exhibit('G.1 Akuisisi pembeli dan pasokan','G1')
table('Tabel G.1. Pelaksanaan pemasaran per fase',[
 ('Fase','Jalur dan tindakan','Keputusan dari pengukuran'),
 ('Katalog sekitar UI','Pedagang, pengelola kos, dan komunitas pindahan. Bantu listing pertama, kirim tautan koleksi.','Perluas setelah listing lengkap dan pesanan selesai cukup untuk menopang klaster.'),
 ('Muat Nggak?','Kreator lokal berangkat dari kondisi ruang, lalu mengarahkan penonton ke unit tersedia atau koleksi.','Pelajari biaya per pesanan selesai dan pertahankan kanal yang menghasilkan pembelian dalam area layanan.'),
 ('Bursa Pindahan','Petugas membantu pemeriksaan, pemindaian tag, reservasi dan listing. Gunakan tautan khusus acara.','Bandingkan listing terbit, pesanan selesai dalam 30 hari, dan biaya per pesanan selesai.')
 ],[.23,.42,.35])
exhibit('G.2 Perjalanan dan pengukuran pesanan','G2')
old_table(311,'Tabel G.2. Tahap perjalanan dan ukuran',[.20,.44,.36])
para('Biaya per pesanan selesai dihitung dari biaya yang dapat dikaitkan dengan program dibagi pesanan teratribusikan yang selesai pada jendela pengukuran. Satu pesanan dihitung sekali. Reservasi, kunjungan, pemindaian QR, dan pembukaan listing membantu menjelaskan letak hambatan.',kind='LD Caption')
exhibit('G.3 Penggunaan kembali','G3')
old_table(315,'Tabel G.3. Ukuran retensi pembeli dan penjual',[.22,.39,.39])
exhibit('G.4 Materi di lokasi Bursa Pindahan','G4')
pic('marketing/bursa-touchpoints.png','Gambar G.1. Contoh tag kondisi, reservasi, dan meja bantuan listing')
para('Tag membawa pengunjung ke listing item. Petugas memastikan barang masih tersedia sebelum mengunci jam. Pada meja bantuan, penjual mengirim foto barang, ukuran, lokasi, dan jadwal. Persetujuan penerbitan mengikuti pemeriksaan bukti.',kind='LD Caption')

# Compact clickable front matter with field-backed page labels.
source_pages=root/'page-map.json'
page_map=json.loads(source_pages.read_text()) if source_pages.exists() else {}
for i in anchors:
 if i in (5,):continue
 p=d.add_paragraph()
 els[8].addprevious(p._p)
 f=p.paragraph_format;f.space_after=Pt(0);f.space_before=Pt(0);f.line_spacing=1.06
 f.first_line_indent=Pt(0);f.keep_with_next=False
 src_p=Paragraph(els[i],d); is_sub=src_p.style.name=='Heading 2' and i<175
 f.left_indent=Cm(.35 if is_sub else 0)
 f.tab_stops.add_tab_stop(Cm(15.75),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
 label=src_p.text.strip()
 link(p,label,heading_ids[i])
 for h in p._p.xpath('.//w:hyperlink/w:r/w:rPr'):
  size=OxmlElement('w:sz');size.set(qn('w:val'),'20');h.append(size)
 p.add_run('\t').font.size=Pt(10)
 r=p.add_run(str(page_map.get(heading_ids[i],'')));r.font.size=Pt(10)
 pagefield=OxmlElement('w:fldSimple');pagefield.set(qn('w:instr'),f' PAGEREF {heading_ids[i]} ')
 p._p.remove(r._r);pagefield.append(r._r);p._p.append(pagefield)

# Drop the reviewer markup from the clean revision and refresh front-matter fields.
for e in d._element.xpath('.//w:commentRangeStart|.//w:commentRangeEnd|.//w:commentReference'):
 e.getparent().remove(e)
settings=d.settings.element
update=settings.find(qn('w:updateFields'))
if update is None:
 update=OxmlElement('w:updateFields');settings.append(update)
update.set(qn('w:val'),'true')
d.core_properties.title='LihatDulu – Proposal Rencana Bisnis UISP16'
d.core_properties.subject='Proposal bisnis marketplace furnitur bekas'
d.save(root/'output/LihatDulu_UISP16_Proposal_Revised.docx')
