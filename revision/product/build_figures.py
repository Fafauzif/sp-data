from functools import lru_cache
from pathlib import Path
from math import atan2, cos, sin
from PIL import Image, ImageDraw, ImageFont, ImageOps

folder = Path(__file__).resolve().parent
images = folder.parent / "assets/images"
published = folder / "checkout/public/images"
raw = folder / "raw"
width = 1600
ink = "#172B24"
green = "#185842"
green_dark = "#124333"
sage = "#EBF4EE"
sage_border = "#CDDCD2"
stone = "#F4F2EC"
stone_border = "#DDD9C9"
grey = "#465C52"
white = "#FFFFFF"
amber = "#966831"
font_folder = Path("/usr/share/fonts/truetype/open-sans")

@lru_cache
def face(size, bold=False):
    return ImageFont.truetype(str(font_folder / ("OpenSans-Bold.ttf" if bold else "OpenSans-Regular.ttf")), size)

class Figure:
    def __init__(self, height):
        self.image = Image.new("RGB", (width, height), white)
        self.draw = ImageDraw.Draw(self.image)

    def label(self, x, y, value, size=32, color=ink, bold=False, anchor="lt"):
        self.draw.text((x, y), value, font=face(size, bold), fill=color, anchor=anchor)

    def block(self, x, y, value, max_width, size=30, color=grey, bold=False, step=None):
        font = face(size, bold)
        step = step or round(size * 1.35)
        for paragraph in value.split("\n"):
            line = ""
            for word in paragraph.split():
                test = f"{line} {word}".strip()
                if line and self.draw.textlength(test, font=font) > max_width:
                    self.label(x, y, line, size, color, bold)
                    line = word
                    y += step
                else:
                    line = test
            if line:
                self.label(x, y, line, size, color, bold)
                y += step
        return y

    def box(self, box, fill=sage, line=sage_border, radius=18, stroke=2):
        self.draw.rounded_rectangle(box, radius=radius, fill=fill, outline=line, width=stroke)

    def rule(self, x0, y, x1, color=sage_border):
        self.draw.line((x0, y, x1, y), fill=color, width=2)

    def arrow(self, start, end, color=green, stroke=4, tip=14):
        self.draw.line((start, end), fill=color, width=stroke)
        angle = atan2(end[1] - start[1], end[0] - start[0])
        points = [end, (end[0] - tip*cos(angle-.55), end[1] - tip*sin(angle-.55)),
                  (end[0] - tip*cos(angle+.55), end[1] - tip*sin(angle+.55))]
        self.draw.polygon(points, fill=color)

    def picture(self, path, box, crop=None, fit="contain", align=(0.5, 0.5), fill=white, radius=18, border=sage_border):
        im = Image.open(path).convert("RGB")
        if crop:
            im = im.crop(crop)
        x, y, right, bottom = box
        size = (right-x, bottom-y)
        if fit == "cover":
            fitted = ImageOps.fit(im, size, Image.Resampling.LANCZOS, centering=align)
        else:
            fitted = Image.new("RGB", size, fill)
            im.thumbnail(size, Image.Resampling.LANCZOS)
            if im.width < size[0] and im.height < size[1]:
                im = ImageOps.contain(im, size, Image.Resampling.LANCZOS)
            fitted.paste(im, (round((size[0]-im.width)*align[0]), round((size[1]-im.height)*align[1])))
        mask = Image.new("L", size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0]-1, size[1]-1), radius=radius, fill=255)
        self.image.paste(fitted, (x,y), mask)
        if border:
            self.draw.rounded_rectangle((x,y,right-1,bottom-1), radius=radius, outline=border, width=2)

    def stage(self, x, y, w, h, heading, copy, variant="local"):
        self.box((x,y,x+w,y+h), fill=sage if variant=="local" else stone,
                 line=sage_border if variant=="local" else stone_border, radius=14)
        self.label(x+18, y+15, heading, 30, green_dark, True)
        self.block(x+18, y+58, copy, w-36, 27)

    def save(self, name):
        self.image.save(folder / (name + ".png"), dpi=(300,300), optimize=True)

def hero():
    f = Figure(830)
    f.picture(images/"journey-product.jpg", (0,0,520,830), align=(0.5,0))
    f.label(565, 28, "Yang bisa diperiksa pembeli", 43, green_dark, True)
    f.picture(published/"wear-scratch.webp", (565,104,977,342), fit="cover")
    f.label(1009, 143, "Kondisi unit", 35, ink, True)
    f.block(1009, 200, "Lihat foto detail dan posisi goresan pada lemari contoh.", 563, 31)
    f.label(1009, 298, "Contoh: goresan pintu kiri", 27, green, True)
    f.rule(565, 367, 1599)
    f.picture(images/"journey-room.jpg", (565,398,977,830), (19,553,790,1207), fit="cover", align=(.5,.5))
    f.label(1009, 478, "Ukuran dan ruang", 35, ink, True)
    f.block(1009, 535, "Bandingkan dimensi 90 × 47,5 × 120 cm dengan ruang yang disiapkan.", 563, 31)
    f.block(1009, 675, "Simulasi penempatan Lemari Sora", 540, 27, green, True)
    f.save("hero")

def journey():
    f = Figure(635)
    panels = (
        ("Penjual merekam bukti", "Mulai dari tampak depan.", images/"journey-seller.jpg", (0, 0, 768, 790), (0.5,0.2)),
        ("Pembeli periksa kondisi", "Kenali bentuk dan letak cacat.", images/"journey-product.jpg", (20,430,804,1210), (0.5,0.5)),
        ("Pembeli coba penempatan", "Bandingkan barang dengan ruang.", images/"journey-room.jpg", (20,430,804,1210), (0.5,0.5)),
    )
    for i, (title, subtitle, path, crop, align) in enumerate(panels):
        x = i*551
        f.label(x+8, 2, ("PENJUAL", "PEMBELI", "PEMBELI")[i], 23, green, True)
        f.label(x+8, 40, title, 32, ink, True)
        f.picture(path, (x,106,x+498,551), crop, fit="cover", align=align)
        f.block(x+8, 569, subtitle, 488, 27)
        if i < 2:
            f.arrow((x+510,330),(x+541,330))
    f.save("journey")

def vpc():
    f = Figure(802)
    sides = [
        ("PENJUAL FURNITUR BEKAS", [
            ("Pekerjaan", "Mencatat kondisi, memasang barang, dan mengatur waktu pengambilan.",
             "Layanan", "Panduan rekam dan formulir ukuran untuk satu unit."),
            ("Hambatan", "Pertanyaan yang sama muncul di setiap percakapan.",
             "Pengurang hambatan", "Tautan listing dengan foto dekat, catatan fungsi, dan jadwal."),
            ("Hasil yang dicari", "Stok cepat terlihat dan dana bersih mudah diperkirakan.",
             "Pencipta manfaat", "Listing standar gratis. Estimasi dana bersih sebelum terbit."),
        ]),
        ("PEMBELI FURNITUR BEKAS", [
            ("Pekerjaan", "Menilai unit yang sesuai kebutuhan, ruang, dan biaya pindahan.",
             "Layanan", "Katalog berdasarkan barang, harga, ukuran, dan lokasi."),
            ("Hambatan", "Cacat kecil, dimensi, dan ongkos angkut sulit dipastikan.",
             "Pengurang hambatan", "Foto dekat, ukuran terukur, dan pilihan serah terima."),
            ("Hasil yang dicari", "Dapat memilih sebelum menyiapkan kendaraan atau jadwal.",
             "Pencipta manfaat", "Simulasi ruang pada barang yang didukung dan catatan pesanan."),
        ]),
    ]
    for i,(title,rows) in enumerate(sides):
        x=i*814
        f.box((x,0,x+786,65), green_dark, green_dark, 14)
        f.label(x+20,19,title,27,white,True)
        f.label(x+18,82,"Kebutuhan pengguna",27,ink,True)
        f.label(x+424,82,"Penawaran LihatDulu",27,green_dark,True)
        for j,(need,need_copy,offer,offer_copy) in enumerate(rows):
            y=130+j*222
            f.box((x,y,x+367,y+198), white, sage_border, 13)
            f.box((x+407,y,x+785,y+198), sage, sage_border, 13)
            f.arrow((x+374,y+99),(x+400,y+99),tip=12)
            f.label(x+17,y+22,need,28,green_dark,True)
            f.label(x+423,y+22,offer,28,green_dark,True)
            f.block(x+17,y+68,need_copy,335,28)
            f.block(x+423,y+68,offer_copy,342,28)
    f.save("vpc")

def pipeline():
    f = Figure(648)
    f.label(0,4,"DIUJI PADA PEMROSES LOKAL",28,green,True)
    local = [
        ("Rekam & ekstrak", "FFmpeg memilih bingkai dari video orbit."),
        ("Selaraskan", "COLMAP mencocokkan fitur dan posisi kamera."),
        ("Rekonstruksi", "Brush membentuk representasi Gaussian splat."),
        ("Siapkan aset", "Splat-transform mengemas SPZ untuk penampil."),
    ]
    for i,(title, content) in enumerate(local):
        x=i*409
        f.stage(x,52,371,176,title,content)
        if i<3: f.arrow((x+377,140),(x+402,140),tip=12)
    f.label(0,283,"RANCANGAN MESIN PRODUK",28,amber,True)
    planned = [
        ("Panduan adaptif", "Minta ulang sudut yang belum tercakup."),
        ("Bukti terpisah", "Simpan foto cacat dan dimensi dari penjual."),
        ("Kendali mutu", "Cek bentuk, artefak, dan cakupan."),
        ("Tampilan listing", "Utamakan foto. Buka 3D jika layak."),
    ]
    for i,(title, content) in enumerate(planned):
        x=i*409
        f.stage(x,332,371,175,title,content,"plan")
        if i<3: f.arrow((x+377,419),(x+402,419),tip=12)
    f.rule(0,553,1600)
    f.block(0,574,"Foto asli dan ukuran tetap tersedia pada barang yang modelnya belum memenuhi kriteria tampilan.",1590,30)
    f.save("pipeline")

def chair():
    f = Figure(575)
    positions=[(0,373),(409,782),(818,1191),(1227,1600)]
    paths=[
        ("Bingkai sumber","Kursi fisik",images/"chair-source.jpg",(0,18,392,697)),
        ("GLB mentah","Hasil rekonstruksi",images/"chair-raw.jpg",None),
        ("GLB olahan","Celah besar masih terlihat",images/"chair-refined.jpg",None),
        ("Tampilan pembeli","Tab Foto asli diprioritaskan",images/"chair-fallback.jpg",None),
    ]
    for (l,r),(title,sub,p,crop) in zip(positions,paths):
        f.label(l+6, 2, title, 33, ink, True)
        f.picture(p,(l,59,r,492),crop,fill="#F3F2EF")
        f.block(l+6,511,sub,r-l-18,29,grey)
    # Two small contours annotate missing mesh on the actual refined model crop.
    offset = 818 + round((373 - 373)/2)
    sy = 59 + round((433 - 365)/2)
    # Final derived positions follow the source crop, with no alteration of pixels.
    f.draw.rounded_rectangle((offset+133,sy+28,offset+268,sy+122),radius=11,outline=amber,width=5)
    f.draw.rounded_rectangle((offset+104,sy+147,offset+261,sy+228),radius=11,outline=amber,width=5)
    f.save("chair")

def appendix_sora():
    f = Figure(700)
    f.picture(images/"sora-gallery.jpg",(0,0,1600,700),fit="contain")
    f.save("appendix_sora")

def appendix_local():
    f = Figure(705)
    f.label(0,5,"Bingkai dari rekaman",36,ink,True)
    f.label(523,5,"SPZ dalam penampil",36,ink,True)
    f.picture(raw/"local-still.jpg",(0,62,485,608),fit="cover",align=(0.5,0.44))
    f.picture(raw/"local-viewer.png",(523,62,1063,608),fill="#202520")
    f.box((1100,62,1599,608),sage,sage_border)
    x=1132
    f.label(x,96,"Rekaman 27976",34,green_dark,True)
    f.rule(x,157,1568)
    f.label(x,190,"76 dari 76",52,green_dark,True)
    f.label(x,256,"bingkai terdaftar",27,grey)
    f.label(x,320,"291,28 detik",44,green_dark,True)
    f.label(x,381,"waktu proses lokal",27,grey)
    f.label(x,459,"0,52 MiB",44,green_dark,True)
    f.label(x,520,"ukuran berkas SPZ",27,grey)
    f.block(0,639,"Berkas siap dimuat. Kabut dan bentuk yang tidak utuh masih terlihat pada hasil.",1580,30)
    f.save("appendix_local")

for build in (hero, journey, vpc, pipeline, chair, appendix_sora, appendix_local):
    build()
