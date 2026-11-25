"""Build the editable SVG figures in this directory. Export to PDF and PNG with Inkscape."""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
WIDTH = 820
MM = 160
INK = "#142b24"
MUTED = "#425950"
GREEN = "#14624c"
DEEP = "#103e32"
MINT = "#e7f2ec"
PALE = "#f1f7f3"
BORDER = "#bfd3c8"
LINE = "#527d6c"
WHITE = "#ffffff"
SAND = "#f5eee0"
COPPER = "#694620"


class Figure:
    def __init__(self, height):
        self.height = height
        self.layers = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{MM}mm" '
            f'height="{height * MM / WIDTH:.4f}mm" viewBox="0 0 {WIDTH} {height}">',
            '<defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="5.8" '
            'refY="3" orient="auto" markerUnits="strokeWidth">'
            f'<path d="M0 0 L6 3 L0 6 Z" fill="{LINE}"/></marker></defs>',
        ]
        self.rect(0, 0, WIDTH, height, WHITE)

    def rect(self, x, y, w, h, fill, stroke="none", radius=0):
        self.layers.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
        )

    def line(self, *points, arrow=False, stroke=LINE, width=2):
        path = " ".join(f"{x},{y}" for x, y in points)
        end = ' marker-end="url(#arrow)"' if arrow else ""
        self.layers.append(
            f'<polyline points="{path}" fill="none" stroke="{stroke}" stroke-width="{width}"'
            f' stroke-linejoin="round" stroke-linecap="round"{end}/>'
        )

    def text(self, x, y, label, size=18, weight=400, color=INK, anchor="start"):
        self.layers.append(
            f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{escape(label)}</text>'
        )

    def lines(self, x, y, labels, size=17, step=23, weight=400, color=MUTED, anchor="start"):
        for i, label in enumerate(labels):
            self.text(x, y + step * i, label, size, weight, color, anchor)

    def card(self, x, y, w, h, title, body=(), *, fill=PALE, edge=BORDER, strong=False, body_size=17, title_size=18):
        self.rect(x, y, w, h, fill, edge, 8)
        self.text(x + 13, y + 26, title, title_size, 700, WHITE if strong else DEEP)
        self.lines(x + 13, y + 51, body, size=body_size, color=WHITE if strong else MUTED)

    def save(self, stem):
        (ROOT / (stem + ".svg")).write_text("\n".join([*self.layers, "</svg>", ""]), encoding="utf-8")


def revenue():
    fig = Figure(237)
    fig.card(1, 57, 250, 127, "Pembeli membayar",
             ("Harga barang", "+ Biaya layanan", "+ Ongkos kirim jika dipilih"),
             fill=DEEP, edge=DEEP, strong=True, title_size=20)
    fig.line((253, 120), (276, 120), (276, 38), (308, 38), arrow=True)
    fig.line((276, 120), (308, 120), arrow=True)
    fig.line((276, 120), (276, 202), (308, 202), arrow=True)
    for y, name, formula, bg in [
        (3, "Penjual", "Harga barang − komisi penjual", PALE),
        (85, "Pendapatan LihatDulu", "Biaya layanan pembeli + komisi penjual", MINT),
        (167, "Penyedia angkutan jika dipilih", "Ongkos kirim sesuai rute", PALE),
    ]:
        fig.card(311, y, 507, 67, name, (formula,), fill=bg, title_size=19)
    fig.save("revenue")


def operations():
    fig = Figure(321)
    fig.text(363, 20, "PILIH CARA SERAH TERIMA", 16, 700, GREEN)
    # The primary path drops straight down through the buyer/stock column, then forks horizontally.
    fig.line((159, 91), (179, 91), arrow=True)
    fig.line((337, 91), (356, 91), arrow=True)
    fig.line((590, 91), (605, 91), (605, 64), (619, 64), arrow=True)
    fig.line((605, 91), (605, 125), (619, 125), arrow=True)
    fig.line((720, 155), (720, 180), (473, 180), (473, 196), arrow=True)
    fig.line((804, 64), (814, 64), (814, 180), (720, 180), width=1.8)
    fig.card(1, 38, 155, 112, "Penjual", ("Siapkan foto,", "ukuran, harga,", "dan jadwal."))
    fig.card(181, 38, 153, 112, "Operasi katalog", ("Cek bukti.", "Terbitkan", "listing."), title_size=15.2)
    fig.card(359, 38, 230, 112, "Pembeli dan penjual", ("Pilih barang.", "Penjual cek stok", "dan ketersediaan jadwal."))
    fig.card(622, 34, 180, 59, "Ambil sendiri", ("Sepakati jadwal.",), body_size=16)
    fig.card(622, 96, 180, 59, "Pengiriman", ("Mitra cek rute & slot.",), body_size=15)
    fig.card(1, 199, 328, 81, "Jika ada selisih kondisi", ("Dukungan cek bukti dan catat koreksi.",), fill=SAND, edge="#dbc8a8", body_size=16)
    fig.card(358, 199, 230, 81, "Pembayaran", ("Pembeli konfirmasi total.",))
    fig.card(621, 199, 197, 81, "Serah terima", ("Catat penerimaan.",))
    fig.line((590, 239), (618, 239), arrow=True)
    fig.line((720, 283), (720, 299), (164, 299), (164, 283), arrow=True, width=1.8)
    fig.rect(404, 289, 164, 24, WHITE)
    fig.text(486, 305, "Jika ada pengaduan", 14, 400, MUTED, "middle")
    fig.save("operations")


def supply():
    fig = Figure(248)
    fig.text(1, 19, "SUMBER STOK", 16, 700, GREEN)
    fig.text(291, 19, "PENERBITAN LISTING", 16, 700, GREEN)
    fig.text(574, 19, "PEMENUHAN PESANAN", 16, 700, GREEN)

    fig.card(1, 35, 242, 64, "Pedagang berulang", ("Perbarui stok berkala.",))
    fig.card(1, 108, 242, 64, "Penyewa yang pindah", ("Jual barang saat pindah.",))
    fig.card(290, 35, 241, 137, "Katalog dan teknis",
             ("Periksa foto dan ukuran.", "Simpan media, kelola", "antrean model 3D."), fill=MINT)
    fig.card(573, 35, 245, 137, "Dukungan pesanan",
             ("Cek stok dan jadwal.", "Kelola pembayaran", "serta catat serah terima."))

    fig.line((246, 68), (264, 68), (264, 103), (286, 103), arrow=True)
    fig.line((246, 140), (264, 140), (264, 103))
    fig.line((535, 103), (569, 103), arrow=True)
    fig.rect(1, 191, 817, 49, DEEP, DEEP, 8)
    fig.text(16, 222, "Barang tetap di penjual sampai diambil pembeli atau dijemput mitra angkut.", 17, 600, WHITE)
    fig.save("supply")


def risks():
    fig = Figure(268)
    x1, y1, w, h = 124, 37, 95, 58
    cell_colors = [
        ["#f5e6c9", "#ecd0bb", "#e9b9aa"],
        ["#e9f0e7", "#f5e6c9", "#ecd0bb"],
        ["#e2efe7", "#e9f0e7", "#f5e6c9"],
    ]
    positions = {
        (0, 0): "R5",
        (0, 1): "R3",
        (1, 1): "R4",
        (1, 2): "R1",
        (2, 2): "R2",
    }
    fig.text(1, 20, "DAMPAK", 16, 700, GREEN)
    for row, label in enumerate(("Tinggi", "Sedang", "Rendah")):
        y = y1 + row * h
        fig.text(4, y + 35, label, 17, 600, INK)
        for col in range(3):
            x = x1 + col * w
            fig.rect(x, y, w - 4, h - 4, cell_colors[row][col], WHITE, 4)
            if (row, col) in positions:
                fig.rect(x + (w - 48) / 2, y + 12, 44, 31, DEEP, DEEP, 10)
                fig.text(x + (w - 4) / 2, y + 34, positions[row, col], 17, 700, WHITE, "middle")
    for col, label in enumerate(("Rendah", "Sedang", "Tinggi")):
        fig.text(x1 + col * w + (w - 4) / 2, 234, label, 16, 600, INK, "middle")
    fig.text(263, 260, "KEMUNGKINAN", 16, 700, GREEN, "middle")
    fig.line((427, 36), (427, 210), stroke=BORDER)
    for i, (code, label) in enumerate((
        ("R1", "Bukti tidak lengkap"),
        ("R2", "Model sulit dipakai"),
        ("R3", "Stok atau angkut bermasalah"),
        ("R4", "Biaya menghambat checkout"),
        ("R5", "Kondisi barang berbeda"),
    )):
        y = 48 + i * 40
        fig.text(449, y, code, 17, 700, GREEN)
        fig.text(492, y, label, 18, 600, INK)
    fig.text(449, 260, "Penilaian awal secara kualitatif", 16, 400, MUTED)
    fig.save("risks")


def roadmap():
    fig = Figure(300)
    labels = (
        ("MULAI DI SEKITAR UI", "Bulan 0–6", "Pendiri / non-dilutif"),
        ("PERLUAS KLASTER", "Bulan 6–12", "Pre-seed"),
        ("PERLUAS WILAYAH", "Mulai tahun 2", "Seed"),
    )
    for i, (stage, timing, funding) in enumerate(labels):
        x = 278 + 180 * i
        fig.rect(x, 2, 174, 76, DEEP if i == 0 else GREEN, radius=7)
        fig.text(x + 87, 24, stage, 14, 700, WHITE, "middle")
        fig.text(x + 87, 46, timing, 15.5, 700, WHITE, "middle")
        fig.text(x + 87, 65, funding, 14, 400, WHITE, "middle")
    tracks = (
        ("Kurasi stok dan alur pesanan", 0, 2),
        ("Kampanye “Muat Nggak?”", 1, 2),
        ("Otomasi media dan katalog B2B", 1, 2),
        ("Bursa Pindahan LihatDulu", 2, 2),
        ("Pengembangan API", 2, 2),
    )
    for row, (label, starts, ends) in enumerate(tracks):
        y = 84 + row * 36
        fig.rect(1, y, 815, 34, PALE if row % 2 == 0 else WHITE, radius=4)
        fig.text(8, y + 22, label, 16, 600, INK)
        for phase in range(3):
            x = 278 + 180 * phase
            if starts <= phase <= ends:
                fig.rect(x + 11, y + 10, 152, 14, GREEN if phase == starts else BORDER, radius=6)
    fig.rect(281, 278, 40, 12, GREEN, radius=5)
    fig.text(330, 289, "Mulai", 16, 400, MUTED)
    fig.rect(417, 278, 40, 12, BORDER, radius=5)
    fig.text(466, 289, "Berlanjut", 16, 400, MUTED)
    fig.save("roadmap")


if __name__ == "__main__":
    for build in (revenue, operations, supply, risks, roadmap):
        build()
