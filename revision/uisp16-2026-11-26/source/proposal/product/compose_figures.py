from base64 import b64encode
from html import escape
from pathlib import Path
import json
from subprocess import run

OUT = Path(__file__).resolve().parent
SOURCE = OUT / 'local-manifest.json'
INK = '#20342d'
GREEN = '#256a63'
PALE = '#e6efea'
BORDER = '#b9ccc1'
WHITE = '#ffffff'


def canvas(height, title, description):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="170mm" height="{height * 170/1200:.3f}mm" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        f'<rect width="1200" height="{height}" fill="{WHITE}"/>',
    ]


def box(x, y, w, h, fill=PALE, stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def label(x, y, value, size=27, color=INK, bold=False, step=33):
    spans = ''.join(
        f'<tspan x="{x}" dy="{step if i else 0}">{escape(line)}</tspan>'
        for i, line in enumerate(value.split('\n'))
    )
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="Liberation Sans, sans-serif" '
        f'font-size="{size}" font-weight="{700 if bold else 400}">{spans}</text>'
    )


def image(name, at, measure):
    mime = 'image/jpeg' if name.endswith('.jpg') else 'image/png'
    data = b64encode((OUT / name).read_bytes()).decode()
    x, y = at
    w, h = measure
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="data:{mime};base64,{data}"/>'


def save(name, parts):
    svg = OUT / f'{name}.svg'
    png = svg.with_suffix('.png')
    svg.write_text('\n'.join([*parts, '</svg>']), encoding='utf-8')
    run(['inkscape', str(svg), '--export-dpi=300', f'--export-filename={png}'], capture_output=True, check=True)


journey = canvas(
    548, 'Alur prototipe penjual dan pembeli',
    'Cuplikan panduan foto bagi penjual, penanda kondisi dan pratinjau ruang bagi pembeli. Serah terima digambarkan terpisah sebagai rancangan operasi.',
)
journey += [
    box(1, 1, 386, 56, GREEN),
    box(401, 1, 798, 56, GREEN),
    label(17, 39, 'Penjual', 30, WHITE, True),
    label(418, 39, 'Pembeli', 30, WHITE, True),
    box(1, 57, 386, 398, WHITE, BORDER),
    box(401, 57, 798, 398, WHITE, BORDER),
    box(801, 69, 2, 370, BORDER),
    image('ui-penjual.png', (16, 79), (356, 285)),
    image('ui-kondisi.png', (418, 79), (365, 285)),
    image('ui-ruang.png', (819, 79), (365, 285)),
    label(17, 401, 'Dokumentasikan unit', 28, GREEN, True),
    label(17, 435, 'Ikuti panduan mengambil foto.', 24),
    label(417, 401, 'Periksa kondisi', 28, GREEN, True),
    label(417, 435, 'Buka penanda bagian barang.', 24),
    label(818, 401, 'Coba posisi barang', 28, GREEN, True),
    label(818, 435, 'Bandingkan dengan ruang.', 24),
    box(1, 476, 1198, 70, PALE, BORDER),
    label(19, 519, 'Rancangan serah terima', 26, GREEN, True),
    label(347, 519, 'Pilih cara menerima, sepakati jadwal, lalu catat kondisi unit.', 25),
]
save('produk-alur-penjual-pembeli', journey)


lab = canvas(
    570, 'Masukan dan keluaran pemrosesan lokal',
    'Bingkai video dan tangkapan penampil dari rekaman Golden pada kursi yang sama. Keluaran SPZ masih mengandung kabut dan bagian kursi sulit dikenali.',
)
lab += [
    box(1, 1, 284, 55, GREEN),
    box(297, 1, 584, 55, GREEN),
    box(893, 1, 306, 55, GREEN),
    label(16, 38, 'Bingkai sumber', 28, WHITE, True),
    label(314, 38, 'Keluaran SPZ dalam penampil', 28, WHITE, True),
    label(910, 38, 'Satu rekaman uji', 28, WHITE, True),
    box(1, 57, 284, 427, WHITE, BORDER),
    box(297, 57, 584, 427, WHITE, BORDER),
    box(893, 57, 306, 427, PALE, BORDER),
    image('spz-bingkai-golden.jpg', (20, 70), (245, 401)),
    image('spz-penampil-golden.png', (316, 70), (546, 401)),
    label(910, 130, '76 dari 76', 42, GREEN, True),
    label(910, 169, 'bingkai terdaftar', 27),
    label(910, 240, '291,28 detik', 39, GREEN, True),
    label(910, 279, 'waktu pemrosesan', 27),
    label(910, 350, '0,52 MiB', 42, GREEN, True),
    label(910, 389, 'ukuran berkas SPZ', 27),
    label(910, 447, 'Uji 22 November 2026', 22),
    box(1, 503, 1198, 66, PALE, BORDER),
    label(17, 545, 'Model dapat dibuka. Kabut pada hasil mempersulit pemeriksaan kondisi.', 27),
]
save('bukti-pemrosesan-lokal', lab)


manifest = json.loads(SOURCE.read_text())
durations = [25.35, 20.13, 10.03, 10.21, 14.59, 15.0, 14.62]
rows = []
for i, (take, clip_seconds) in enumerate(zip(manifest['takes'], durations, strict=True)):
    run_data = take['run']
    rows.append({
        'id': take['clip'].split('_')[-1].split('.')[0][-5:],
        'seconds_clip': clip_seconds,
        'frames_registered': run_data['registered'],
        'frames_extracted': run_data['extracted'],
        'seconds_processing': round(run_data['totalMs'] / 1000, 3),
        'spz_bytes': run_data['artifactBytes'],
        'spz_mib': round(run_data['artifactBytes'] / 1024**2, 2),
        'note': 'Ekstraksi ulang pada 5 fps setelah lintasan pertama menghasilkan 59 bingkai.' if i == 5 else 'Sumber 4K, bingkai diperkecil menjadi 1.280 piksel di sisi terpanjang.' if i == 6 else '',
    })
data = {
    'title': 'Uji pemrosesan lokal pada tujuh rekaman satu kursi',
    'technical_source_commit': 'c4b3192',
    'artifact_commit': 'cbf69f09fbb41eacaa8ea40e6e6cb55ceec61e4c',
    'technical_source': 'docs/handoff/scan-toolchain.md',
    'artifact_manifest': 'docs/handoff/scan-evidence-manifest.json',
    'recording_date_wib': '2026-11-21',
    'processing_date_wib': '2026-11-22',
    'hardware': 'Acer Predator Helios Neo 16, Windows 11, RTX 4060 Laptop',
    'pipeline': ['FFmpeg 8.1.2', 'COLMAP 4.2.1 (CUDA)', 'Brush 0.3.0', 'splat-transform 3.12.0', 'SPZ'],
    'tables': rows,
    'paired_golden_assets': ['spz-bingkai-golden.jpg', 'spz-penampil-golden.png'],
    'golden_job_id': manifest['takes'][0]['jobId'],
    'limitations': [
        'Tujuh rekaman berasal dari satu objek fisik.',
        'Registrasi bingkai mengukur keterbacaan posisi kamera. Mutu bentuk diperiksa dari artefak visual.',
        'Keluaran dapat dibuka dan masih memperlihatkan kabut atau fragmen.',
        'Durasi berasal dari pemroses lokal pada perangkat yang tercatat.',
        'Bukti belum mencakup uji pemindaian dari kamera ponsel langsung ke penampil di lokasi pilot.',
    ],
}
(OUT / 'bukti-pemrosesan-lokal.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
