from base64 import b64encode
from html import escape
from pathlib import Path

from subprocess import run

root = Path(__file__).parent
assets = root / 'resources'
green = '#124934'
dark = '#172C23'
mint = '#E8F2E8'
lime = '#CBE6AE'
grass = '#27644C'
paper = '#FAFBF6'
muted = '#435B4D'
stroke = '#CDDCD0'
white = '#FFFFFF'


class Graphic:
    def __init__(self, height, bg=white):
        self.h = height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="{height}" viewBox="0 0 1200 {height}">']
        self.rect(0, 0, 1200, height, bg)

    def put(self, value):
        self.parts.append(value)

    def rect(self, x, y, w, h, fill, r=0, edge=None):
        css = f' stroke="{edge}" stroke-width="2"' if edge else ''
        self.put(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{css}/>')

    def circ(self, x, y, r, fill, edge=None):
        css = f' stroke="{edge}" stroke-width="2"' if edge else ''
        self.put(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{css}/>')

    def path(self, d, fill, edge=None, width=2):
        css = f' stroke="{edge}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"' if edge else ''
        self.put(f'<path d="{d}" fill="{fill}"{css}/>')

    def text(self, x, y, value, size=32, color=dark, bold=False, align='start', gap=None):
        gap = gap or round(size * 1.2)
        for i, line in enumerate(value.split('\n')):
            self.put(f'<text x="{x}" y="{y+i*gap}" text-anchor="{align}" fill="{color}" font-family="Liberation Sans" font-size="{size}" font-weight="{700 if bold else 400}">{escape(line)}</text>')

    def photo(self, p, x,y,w,h, r=16, cover=True):
        mime = 'image/png' if p.suffix == '.png' else 'image/jpeg'
        key = f'clip-{len(self.parts)}'
        self.put(f'<defs><clipPath id="{key}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath></defs>')
        self.put(f'<image x="{x}" y="{y}" width="{w}" height="{h}" clip-path="url(#{key})" preserveAspectRatio="xMidYMid {"slice" if cover else "meet"}" xlink:href="data:{mime};base64,{b64encode(p.read_bytes()).decode()}"/>')

    def save(self, name):
        xml = (''.join(self.parts) + '</svg>').encode()
        (root/f'{name}.svg').write_bytes(xml)
        for suffix in ("png", "pdf"):
            run(["inkscape", str(root/f"{name}.svg"), "--export-width=1920", f"--export-filename={root}/{name}.{suffix}"], check=True)


def matrix():
    g=Graphic(520)
    g.rect(0,0,1200,76,green,14)
    g.text(24,48,'Segmentasi',33,white,True)
    g.text(422,48,'Fokus awal',33,white,True)
    g.text(820,48,'Perluasan',33,white,True)
    rows=[
      ('Wilayah','Klaster kos sekitar UI','Klaster hunian terdekat'),
      ('Pembeli','Mahasiswa kos dan\npenyewa baru','Rumah tangga muda\nyang melengkapi hunian'),
      ('Penjual','Reseller lokal dan\npenghuni yang akan pindah','Penjual perorangan\ndi klaster perluasan'),
    ]
    for i,(label,primary,secondary) in enumerate(rows):
        y=88+i*102
        g.rect(0,y,370,92,paper,12,stroke)
        g.rect(380,y,394,92,lime,12)
        g.rect(784,y,416,92,mint,12)
        g.text(25,y+55,label,32,dark,True)
        g.text(401,y+(38 if '\n' in primary else 55),primary,29)
        g.text(808,y+(38 if '\n' in secondary else 55),secondary,29)
    g.rect(0,402,1200,118,green,14)
    g.text(24,441,'Positioning',29,lime,True)
    g.text(24,479,'Furnitur bekas dengan kondisi, dimensi, dan pilihan serah terima',33,white,True)
    g.text(24,507,'yang dapat diperiksa sebelum memesan.',29,white)
    g.save('stp')


def person_icon(g,x,y,kind):
    g.circ(x,y,46,lime)
    if kind=='buy':
        g.path(f'M{x-25} {y+15}V{y-5}Q{x-25} {y-17} {x-13} {y-17}H{x+13}Q{x+25} {y-17} {x+25} {y-5}V{y+15}Z',green)
        g.path(f'M{x-9} {y-15}V{y-26}H{x+9}V{y-15}','none',green,5)
        g.path(f'M{x-25} {y}H{x+25}','none',lime,4)
    else:
        g.path(f'M{x-26} {y-6}L{x} {y-22}L{x+26} {y-6}V{y+22}L{x} {y+35}L{x-26} {y+22}Z',green)
        g.path(f'M{x-26} {y-6}L{x} {y+8}L{x+26} {y-6}M{x} {y+8}V{y+35}','none',lime,3)


def personas():
    g=Graphic(426)
    for i,(role,focus,need,friction,trigger,kind) in enumerate([
        ('Pembeli','Penghuni kos baru','Mencari meja atau lemari\nyang muat dan siap diambil.','Sulit membandingkan kondisi,\nukuran, dan total biaya angkut.','Pindah atau mulai semester.','buy'),
        ('Penjual','Reseller lokal','Memperbarui stok dan menjual\nbarang tanpa banyak tanya ulang.','Foto dan ukuran perlu disiapkan\nuntuk setiap unit yang berbeda.','Stok baru masuk atau lama tersimpan.','sell'),
    ]):
        x=i*612
        g.rect(x,0,588,426,paper,16,stroke)
        g.rect(x,0,588,113,green,16)
        person_icon(g,x+60,56,kind)
        g.text(x+119,44,role,26,lime,True)
        g.text(x+119,88,focus,38,white,True)
        for y,l,d in [(153,'Kebutuhan',need),(260,'Hambatan',friction),(365,'Pemicu',trigger)]:
            g.text(x+23,y,l,25,grass,True)
            g.text(x+23,y+35,d,30, gap=31)
    g.save('personas')


def market():
    g=Graphic(410)
    for x,y,r,c in [(194,207,188,green),(194,238,151,grass),(194,274,112,lime)]:
        g.circ(x,y,r,c)
    for y,label,color,target in [(83,'TAM',white,327),(143,'SAM',white,330),(264,'SOM',green,300)]:
        g.text(194,y+13,label,39,color,True,'middle')
        g.path(f'M{target} {y}H421','none',grass,3)
        g.circ(421,y,7,grass)
    for y,title,txt in [
        (44,'Potensi pendapatan marketplace nasional','Pesanan furnitur bekas yang layak dilayani\nsecara digital × pendapatan per pesanan.'),
        (160,'Potensi pendapatan di area layanan','Pesanan yang memenuhi cakupan Jabodetabek\n× pendapatan per pesanan.'),
        (276,'Pendapatan marketplace tahun ketiga','Pesanan selesai sesuai proyeksi dan kapasitas\n× pendapatan per pesanan.'),
    ]:
        g.rect(444,y-10,756,105,paper,13,stroke)
        g.text(465,y+25,title,32,green,True)
        g.text(465,y+57,txt,27,gap=29)
    g.save('market')


def funnel():
    g=Graphic(336)
    for i,(label,title,lines) in enumerate([
      ('Awareness','Temukan barang','Koleksi dekat kos\natau video kreator'),
      ('Interest','Buka listing','Lihat harga, lokasi,\nukuran, dan foto'),
      ('Desire','Periksa kecocokan','Bandingkan kondisi\ndan cara angkut'),
      ('Action','Selesaikan pesanan','Pilih serah terima,\nlalu lanjutkan pesanan'),
    ]):
        x=i*300
        end=0 if i==3 else 22
        tip=x+298
        notch=f'L{x+19} 36L{x+1} 72' if i else f'L{x+1} 72'
        g.path(f'M{x+1} 1H{tip-end}L{tip} 36L{tip-end} 72H{x+1}' + (f'L{x+19} 36Z' if i else 'Z'),[green,grass,'#3C7656','#4B7D55'][i])
        g.text(x+148,47,label,32,white,True,'middle')
        g.rect(x+1,83,297,156,paper,12,stroke)
        g.text(x+15,126,title,29,dark,True)
        g.text(x+15,166,lines,28,gap=33)
    g.rect(0,252,1200,76,mint,12)
    g.text(20,298,'Setelah transaksi',31,green,True)
    g.text(283,298,'Simpan pencarian pembeli dan bantu penjual memasang stok berikutnya.',27)
    g.save('funnel')


def phase_one():
    g=Graphic(524)
    g.rect(0,0,1200,524,green,18)
    room=assets/'images/journey-room.jpg'
    g.rect(806,0,394,524,white,18)
    g.photo(room, 824, 16, 358, 492,12,False)
    g.text(36,62,'KOLEKSI DEKAT UI',29,lime,True)
    g.text(36,152,'Baru pindah?',69,white,True)
    g.text(36,224,'Isi kos satu per satu.',54,white,True)
    g.text(38,282,'Cari furnitur bekas yang bisa kamu',35,white)
    g.text(38,327,'cek ukuran, kondisi, dan lokasinya.',35,white)
    g.rect(38,369,393,67,lime,10)
    g.text(58,413,'Lihat koleksi sekitar UI',32,green,True)
    g.text(38,491,'Contoh materi komunitas kos · layar demo.',29,lime)
    g.save('phase-1')


def phase_two():
    g=Graphic(630)
    g.rect(0,0,1200,630,mint,18)
    g.rect(0,0,402,630,green,18)
    g.text(25,62,'VIDEO KREATOR LOKAL',25,lime,True)
    g.text(25,160,'Muat',68,white,True)
    g.text(25,234,'Nggak?',68,white,True)
    g.text(25,316,'Tunjukkan ruang.\nCek listing.\nPilih ambil.',34,white)
    g.text(25,555,'Ajakan ke pengguna',26,lime,True)
    g.text(25,598,'Buka listing barangnya',31,white,True)
    for x,img,key,line in [
        (423,'journey-product.jpg','01   Periksa detail','Tunjukkan ukuran dan kondisi.'),
        (813,'journey-room.jpg','02   Coba di ruang','Bandingkan dengan ruang kos.'),
    ]:
        g.rect(x,18,366,588,white,16)
        g.photo(assets/'images'/img,x+25,33,316,460,12,False)
        g.text(x+18,536,key,30,green,True)
        g.text(x+18,575,line,23,muted)
    g.save('phase-2')


def phase_three():
    g=Graphic(928)
    g.photo(assets/'bursa-hero.png',0,0,1200,690,16)
    for i,(title,desc) in enumerate([
        ('Coba di ruang kos','Lihat barang pada denah\nkos berukuran nyata.'),
        ('Pindai penanda','Cek kondisi dan ukuran.\nReservasi jadwal ambil.'),
        ('Daftarkan barang','Bawa foto serta ukuran,\npetugas bantu buat listing.'),
    ]):
        x=i*403
        g.rect(x,713,394,162,mint,14)
        g.text(x+20,760,title,35,green,True)
        g.text(x+20,806,desc,29,gap=34)
    g.text(0,916,'Ilustrasi aktivasi yang diusulkan. Penanda pada gambar merupakan contoh visual.',25,muted)
    g.save('phase-3')



def bursa_touchpoints():
    g=Graphic(625)
    g.rect(0,0,1200,625,paper,18,stroke)
    g.rect(25,25,310,496,white,14,stroke)
    g.rect(38,36,284,122,green,12)
    g.text(180,85,'LIHATDULU',29,lime,True,'middle')
    g.text(180,127,'Bursa Pindahan',30,white,True,'middle')
    g.text(51,202,'Lemari kayu',39,green,True)
    g.text(51,242,'Contoh penanda barang',25,muted)
    g.rect(52,270,109,109,mint,7,stroke)
    for a,b in [(62,280),(115,280),(62,333)]:
        g.rect(a,b,36,36,green,3)
        g.rect(a+7,b+7,22,22,white,2)
        g.rect(a+13,b+13,10,10,green)
    g.rect(112,327,8,8,green)
    g.rect(126,343,8,8,green)
    g.rect(139,327,10,12,green)
    g.rect(139,354,10,14,green)
    g.text(177,300,'Kode unik',27,dark,True)
    g.text(177,333,'per listing',27,dark)
    g.text(52,425,'Cek kondisi dan ukuran.',24,green,True)
    g.text(52,463,'Reservasi jadwal ambil.',24,green,True)
    g.text(25,570,'Penanda kondisi',30,green,True)

    g.rect(360,25,435,496,green,15)
    g.rect(376,39,401,112,lime,13)
    g.text(577,89,'BANTU PASANG',37,green,True,'middle')
    g.text(577,129,'LISTING',37,green,True,'middle')
    g.text(395,212,'1   Bawa foto asli',34,white,True)
    g.text(395,255,'Tampak depan dan sisi.',27,white)
    g.text(395,317,'2   Catat ukuran',34,white,True)
    g.text(395,360,'Panjang, lebar, dan tinggi.',27,white)
    g.text(395,422,'3   Ceritakan kondisi',34,white,True)
    g.text(395,465,'Sebutkan aus atau rusak.',27,white)
    g.text(360,570,'Papan meja bantuan',30,green,True)

    g.rect(819,25,355,496,white,14,stroke)
    g.photo(assets/'images/journey-product.jpg',835,39,323,463,12,False)
    g.text(819,570,'Layar demo listing',30,green,True)
    g.text(25,609,'Konsep materi acara. Penanda kode berfungsi sebagai ilustrasi tata letak.',23,muted)
    g.save('bursa-touchpoints')

for build in (matrix,personas,market,funnel,phase_one,phase_two,phase_three,bursa_touchpoints):
    build()
