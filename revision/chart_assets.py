from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

base=Path('revision/assets')
green='#185544'; deep='#15382C'; ink='#243D35'; gray='#DFE9E3'; soft='#EEF5F0'; amber='#B46B37'
fp=Path('/usr/share/fonts/truetype/dejavu')
def text(draw,x,y,s,n=28,bold=False,color=ink):
 draw.text((x,y),s,font=ImageFont.truetype(str(fp/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),n),fill=color)
def canvas(h):
 i=Image.new('RGB',(1600,h),'white')
 return i,ImageDraw.Draw(i)
def chart(out, title, rows, note, maximum=15):
 i,d=canvas(140+len(rows)*69)
 text(d,18,12,title,37,True,deep)
 for r,(name,num) in enumerate(rows):
  y=76+r*69
  text(d,22,y+7,name,27)
  d.rounded_rectangle((660,y,1450,y+42),radius=8,fill=soft)
  if num:d.rounded_rectangle((660,y,660+round(790*num/maximum),y+42),radius=8,fill=green)
  text(d,1470,y+5,str(num),29,True,green)
 text(d,22,89+len(rows)*69,note,23)
 i.save(base/out)
chart('survey-barriers.png','Hambatan yang muncul pada iklan terakhir',[
 ('Kondisi barang',13),('Kecocokan dengan ruang',9),('Biaya atau cara angkut',8),('Dimensi barang',7),('Keandalan penjual',4)],'15 responden dengan iklan spesifik · jawaban bisa lebih dari satu · data sementara 25 November 2026')
chart('survey-actions.png','Langkah setelah melihat iklan',[
 ('Meminta informasi tambahan',11),('Melihat barang langsung',7),('Menghubungi penjual untuk membeli',5),('Mencari pilihan lain',5),('Menyimpan iklan',5),('Memilih tanpa tindakan lanjutan',1)],'15 responden dengan iklan spesifik · jawaban bisa lebih dari satu · data sementara 25 November 2026')
i,d=canvas(730)
text(d,22,10,'Respons setelah melihat catatan kondisi dan foto dekat',37,True,deep)
x=22
for label,n,c in [('Keyakinan naik',29,green),('Tetap',14,'#547365'),('Turun',7,amber)]:
 w=round(1556*n/50)
 d.rectangle((x,75,x+w,142),fill=c);text(d,x+13,88,f'{n}  {label}',24,True,'white')
 x+=w
text(d,22,168,'Pilihan tindakan berikutnya',32,True,deep)
d.rounded_rectangle((1022,176,1048,195),radius=3,fill='#A9BEB2');text(d,1057,170,'Awal',23)
d.rounded_rectangle((1177,176,1203,195),radius=3,fill=green);text(d,1212,170,'Setelah catatan kondisi',23)
for j,(name,a,b) in enumerate([('Meminta informasi',24,11),('Mengatur kunjungan',7,20),('Menghubungi untuk beli / ambil',3,9),('Menyimpan iklan',13,6),('Melewati iklan',3,3),('Belum tahu',0,1)]):
 y=225+j*71
 text(d,22,y+14,name,26)
 for y2,v,c in [(y,a,'#A9BEB2'),(y+23,b,green)]:
  if v:d.rounded_rectangle((580,y2,580+32*v,y2+19),radius=5,fill=c)
  text(d,589+32*v,y2-4,str(v),22,True)
text(d,22,663,'50 pasangan lengkap · urutan demo tetap · tindakan yang dipilih dalam skenario',23)
i.save(base/'survey-demo.png')
i,d=canvas(950)
blocks=[
 ('Mitra utama','Pedagang furnitur bekas. Pengelola kos dan komunitas pindahan. Penyedia pembayaran dan angkutan.'),
 ('Kegiatan utama','Akuisisi stok, pemeriksaan listing, pemrosesan media, pencatatan pesanan, serah terima dan dukungan.'),
 ('Proposisi nilai','Pembeli memeriksa kondisi, ukuran, dan cara angkut dalam satu halaman. Penjual memakai ulang bukti dalam setiap percakapan tentang unit yang sama.'),
 ('Hubungan pelanggan','Panduan dokumentasi, bantuan listing pertama, pengingat pilihan sendiri, dan dukungan saat ada selisih kondisi.'),
 ('Segmen pelanggan','Penghuni kos dan penyewa muda. Pedagang bekas dan penghuni yang akan pindah. Pelanggan katalog bisnis pada fase berikutnya.'),
 ('Sumber daya','Katalog web, antarmuka ponsel, penyimpanan media, pemroses dan penampil, tim katalog dan dukungan.'),
 ('Saluran','Tautan koleksi lokal, pengelola kos, konten “Muat Nggak?”, Bursa Pindahan, dan tautan yang dibagikan penjual.'),
 ('Struktur biaya','Pembayaran, penyimpanan, pemrosesan, dukungan, akuisisi, dan pengembangan. Stok disimpan penjual sampai serah terima.'),
 ('Arus pendapatan','Biaya layanan pembeli dan komisi penjual atas pesanan selesai. Langganan penampil katalog B2B setelah operasi media stabil.')]
def card(x,y,w,h,label,body):
 d.rounded_rectangle((x,y,x+w,y+h),radius=14,fill=soft,outline=gray,width=2)
 text(d,x+22,y+16,label,31,True,deep)
 font=ImageFont.truetype(str(fp/'DejaVuSans.ttf'),29)
 lines=[]; line=''
 for wd in body.split():
  if d.textlength((line+' '+wd).strip(),font=font)>w-43:lines.append(line);line=wd
  else:line=(line+' '+wd).strip()
 lines.append(line)
 for idx,t in enumerate(lines):
  text(d,x+22,y+63+idx*38,t,29)
for j,k in enumerate([0,1,2,3,4,5,6]):
 if j<5: card(10+j*319,8,301,400,*blocks[k])
 else: card(10+(j-5)*790,428,763,235,*blocks[k])
for j,k in enumerate([7,8]):card(10+j*790,683,763,235,*blocks[k])
i.save(base/'bmc.png')
