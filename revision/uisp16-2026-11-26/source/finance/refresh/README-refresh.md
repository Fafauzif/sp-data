# Menghitung ulang skenario LihatDulu

Excel menghitung ulang skenario aktif, laporan, CAPM, ukuran pasar, kas, dan cek integritas ketika Anda mengubah sel biru. Lembar Kasus, Sensitivity, dan Monte Carlo berisi hasil evaluasi tanggal acuan. Lembar tersebut perlu pembaruan terpisah setelah perubahan input karena 10.000 replikasi dihitung melalui mesin periode bulanan yang sama.

1. Simpan workbook yang telah Anda ubah.
2. Siapkan Node.js 20 atau lebih baru, Python 3, dan paket Python `openpyxl`. Jalankan dari folder paket ini.
3. Jalankan `node refresh-risk.mjs LihatDulu_Financial_Projection.xlsx hasil-risiko`. Hasilnya berupa 10.000 jalur, ringkasan risiko/sensitivitas, serta salinan asumsi yang dipakai.

Pengujian memakai seed 12026. NPV, IRR, dan tahun penilaian dihitung kembali dari arus kas masing-masing jalur. Pengujian risiko berpusat pada asumsi di kolom Base. Untuk menerbitkan workbook baru dengan hasil terpasang, gunakan argumen opsional ketiga untuk nama XLSX baru di lingkungan yang memiliki `@oai/artifact-tool`, misalnya lingkungan Codex yang membuat workbook ini.

Kasus aktif pada Ringkasan menggerakkan perhitungan utama Excel. Skenario Monte Carlo dan sensitivitas mengukur sekitar Base. Model menggunakan asumsi yang bertanggal 26 November 2026. Tidak ada pendanaan atau transaksi yang diklaim telah berlangsung.
