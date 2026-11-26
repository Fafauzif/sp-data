# Prompt Financial Projection LihatDulu

Susun dan selesaikan financial projection LihatDulu untuk proposal kompetisi UISP16. Gunakan operational plan dan draft proposal dalam repositori sebagai dasar bisnis, serta workbook AUTO2000 yang saya lampirkan sebagai template struktur, keterhubungan rumus, dan kualitas penyajian. Hasilnya harus berupa model keuangan LihatDulu yang dapat ditelusuri, diedit, dihitung ulang, dan dipertanggungjawabkan, beserta integrasinya ke proposal.

Kerjakan implementasinya sampai selesai. Jangan berhenti pada kerangka, contoh tabel kosong, rekomendasi, atau kode pembuat file. Gunakan bahasa Indonesia profesional dan jelas. Asumsi utama boleh rasional cenderung optimistis untuk proposal lomba, dengan sumber, benchmark nyata, batas kapasitas, dan kebutuhan modal yang mendukungnya. Perlakukan hasil proyeksi sebagai estimasi, bukan pencapaian usaha.

## 1. Bahan kerja dan urutan sumber

Repositori: [Fafauzif/sp-data](https://github.com/Fafauzif/sp-data).

Gunakan checkout yang tersedia atau clone repositori tersebut. Catat commit yang dipakai. Baseline yang sebelumnya diperiksa adalah `4ad34f8`; periksa perubahan jika checkout berbeda. Baca:

- `README.md` dan `docs/CURRENT-CONTEXT.md`.
- `revision/output/LihatDulu_UISP16_Proposal_Revised.docx` sebagai draft kerja utama.
- `revision/finalqa/LihatDulu_UISP16_Proposal_Revised.pdf` sebagai acuan susunan dan tampilan.
- `docs/CHAT-FEEDBACK.md`, `docs/WORD-REVIEW-COMMENTS.md`, dan `docs/AUDIT-HANDOFF-2026-11-26.md` untuk batas revisi dan catatan mutu yang belum selesai.
- `survey-analysis/analysis.md` dan CSV survei dalam `upload/`.
- Bab II, Bab III, Bab IV, Bab V, serta Lampiran A, C, D, E, F, dan G dalam proposal.
- `upload/LihatDulu_MASTER_AI_CONTEXT_2026-11-25_Updated.md` dan `docs/SOURCES-AND-REPOS.md` hanya untuk detail atau asal bukti yang belum tercakup di sumber terbaru.

Attachment terpisah: `Auto2000_Digiroom_KEY_FinPro_FIX.xlsx`. Workbook ini tidak otomatis berada di dalam repo. Cari attachment dengan nama tersebut. Jika benar-benar tidak tersedia, minta attachment itu sebelum mengaku menggunakan templatenya. Screenshot WACC/CAPM yang dilampirkan hanya menjelaskan tingkat detail yang ingin diperbaiki; angkanya bukan input LihatDulu yang sudah disetujui.

Utamakan keputusan dalam permintaan ini, kemudian draft revisi dan current context, baru arsip historis. Instruksi lama yang menyisakan keuangan kosong sudah digantikan oleh tugas ini. Jangan menjalankan `revision/build.py` tanpa memahami bahwa script itu dapat membangun ulang dari dokumen baseline lama. Kerjakan pada salinan hasil dan pertahankan dokumen sumber.

Tanggal acuan model adalah 26 November 2026. Tahun 0 adalah persiapan sebelum operasi 2027. Gunakan informasi yang sudah tersedia pada tanggal acuan dan cantumkan tanggal data serta tanggal akses. Jangan menggunakan hasil aktual masa depan sebagai informasi yang seolah sudah diketahui. Jika sumber terbaru tidak tersedia, jelaskan vintage data yang benar.

## 2. Keputusan bisnis yang harus dipertahankan

LihatDulu adalah marketplace furnitur rumah tangga bekas. Penjual menyimpan barang sampai serah terima. Standar listing mencakup foto asli, ukuran, kondisi, harga, lokasi, ketersediaan, dan cara penerimaan. Model 3D merupakan pelengkap ketika hasilnya memadai; listing yang lengkap tetap dapat terbit menggunakan foto.

Peluncuran berfokus di klaster kos sekitar UI Depok. Pedagang furnitur bekas memasok berulang dan penghuni yang pindah menambah pasokan. Enam bulan pertama berfokus pada klaster awal; bulan 7–12 pada klaster berdekatan sesuai kesiapan. Tahun kedua dan seterusnya mencakup Bursa Pindahan setelah stok dan serah terima siap. Kampanye kreator “Muat Nggak?” mengikuti tahapan Bab IV. Langganan katalog tertanam B2B dikembangkan setelah pemrosesan dan dukungan memadai. API hanya dimonetisasi jika fase, pelanggan, biaya, dan layanan pendukungnya dapat dijelaskan.

Pendapatan marketplace berasal dari biaya layanan pembeli per pesanan selesai dan komisi penjual atas nilai barang yang selesai terjual. Listing standar gratis. Pesanan yang batal atau dikembalikan penuh tidak menghasilkan kedua pendapatan tersebut. Pengiriman merupakan pass-through sesuai desain proposal. Langganan B2B dihitung terpisah.

Gunakan basis satu unit furnitur per pesanan sebagaimana Lampiran D. Jika ada alasan kuat mengubahnya, jelaskan dan selaraskan definisi seluruh model dan proposal. Jangan menambah gudang, pembelian stok, armada milik sendiri, pinjaman, atau lini bisnis baru demi membuat proyeksi terlihat menarik.

Tidak ada debt financing: tidak ada pinjaman bank, venture debt, convertible debt, bunga pinjaman, atau pelunasan pokok. Utang usaha dari waktu pembayaran biaya operasional tetap boleh dimodelkan secara wajar dan harus dibedakan dari utang pendanaan.

## 3. Batas bukti dan asumsi

Belum ada angka harga, modal pendiri, hibah, valuasi, atau tarif final yang dikunci tim. Susun estimasi yang dapat dipertanggungjawabkan, bukan angka yang diklaim sudah disepakati atau terealisasi.

Survei sementara mencakup 50 responden, 46 di antaranya mahasiswa. Modul pengalaman mempertimbangkan listing spesifik memiliki 15 responden. Demo berpasangan menghasilkan 29 responden dengan keyakinan meningkat, 14 tetap, dan tujuh turun. Baca data dan denominator aslinya sebelum menggunakannya. Hasil demo bukan penjualan, conversion rate marketplace, willingness to pay, atau bukti sebab-akibat suatu fitur. Wawancara penjual masih belum tersedia pada baseline; jangan menciptakan temuannya.

Uji lokal FFmpeg–COLMAP–Brush–SPZ menggunakan tujuh rekaman atas satu kursi. Demonstrasi GLB pihak ketiga merupakan bukti terpisah. Jangan menganggap waktu, ukuran file, dan mutu hasil vendor sebagai performa pipeline lokal atau SLA produksi. Gunakan bukti itu untuk membatasi asumsi dan merancang biaya percobaan, bukan untuk mengklaim kapasitas produksi terukur.

Setiap input material harus diberi status: data primer, data sekunder, benchmark, atau asumsi model. Untuk benchmark, tunjukkan angka sumber, satuan, periode, konteks, dan penyesuaian menjadi asumsi LihatDulu. Untuk asumsi tanpa bukti langsung, beri alasan dan rentang pengujian. Jangan melabeli estimasi internal sebagai hasil riset.

## 4. Audit dan adaptasi template AUTO2000

Periksa seluruh sheet, rumus, format, grafik, scenario selector, horizon, dan hubungan antarsheet dalam template. Struktur awalnya mencakup `Cover`, `Assumption`, `Budgeting`, `Volume Projection`, `Revenue & Cost Projection`, `Financial Projection`, `Sensitivity`, dan `Monte Carlo`.

Pertahankan alur logis yang berguna. Ganti mekanisme incremental program otomotif dengan model keseluruhan usaha LihatDulu. Hapus asumsi otomotif, batas investasi casebook, discount rate tetap AUTO2000, margin proxy otomotif, identitas tim lama, dan istilah yang tidak relevan. Jangan sekadar mengganti nama perusahaan.

Tambahkan perhitungan CAPM, funding, laporan keuangan, dan jadwal biaya/aset sesuai kebutuhan. Jangan membuat banyak sheet yang hanya menyalin hasil. Gunakan satu sumber asumsi dan selector skenario yang jelas. Seluruh pendapatan, biaya, kapasitas, dan kebutuhan kas harus mengikuti skenario terpilih.

Template menampilkan proyeksi utama sampai tahun pertama IRR melampaui hurdle, sementara perhitungan lanjutannya tetap tersedia. Untuk LihatDulu, tampilkan horizon dasar penuh dan tandai tahun pertama melewati CAPM; jangan menghapus tahun setelahnya atau menyembunyikan kebutuhan investasi lanjutan.

## 5. Horizon, waktu, dan skenario

Gunakan Tahun 0, lalu 10 tahun operasi awal 2027–2036. Sediakan detail bulanan 24 bulan pertama untuk peluncuran, burn, kas, dan funding. Tahun berikutnya boleh tahunan; gunakan detail tambahan di sekitar putaran pendanaan jika dibutuhkan agar timing dan saldo kas dapat diuji. Rekonsiliasikan agregasi bulanan ke tahunan tanpa menghitung dua kali periode yang sama.

Hitung IRR kumulatif proyek pada setiap akhir tahun dan identifikasi tahun pertama IRR > cost of equity berbasis CAPM. Jika belum tercapai dalam 10 tahun, evaluasi perpanjangan berdasarkan rencana operasi yang masih masuk akal, penurunan pertumbuhan saat bisnis matang, investasi tambahan, dan kapasitas pasar. Jelaskan alasan dan hasil perpanjangan. Jangan memaksakan pertumbuhan, menurunkan diskonto, atau memperpanjang tanpa dasar untuk memperoleh kelulusan.

Buat Base yang rasional cenderung optimistis, Downside yang material, dan Upside yang masih masuk akal. Perbedaan kasus harus berada pada driver operasional, misalnya kecepatan akuisisi penjual, pasokan, penyelesaian transaksi, biaya akuisisi, dan kesiapan ekspansi. Jangan mengganti hasil akhir secara manual. Sajikan perbandingan skenario dengan metode refresh yang jelas dan hasil yang benar-benar dihitung untuk setiap kasus.

## 6. Penelitian benchmark nyata

Gunakan sumber primer semaksimal mungkin: data pemerintah, laporan perusahaan, dokumentasi dan tarif resmi penyedia, serta publikasi akademik untuk metode. Buka sumber aslinya; search snippet tidak cukup. Jangan memindahkan angka kompetitor tanpa memperhatikan model bisnis, ukuran, negara, satuan, dan periode.

Cari benchmark yang benar-benar dipakai untuk:

- Harga penawaran furnitur bekas relevan di Depok/Jabodetabek, menurut kategori dan kondisi. Gunakan sampel lintas listing, jelaskan jumlah sampel dan median/rentangnya. Harga penawaran tidak sama dengan harga transaksi; asumsi negosiasi dan mix kategori harus terpisah.
- Biaya atau komisi platform dengan mekanisme layanan yang sebanding, serta tarif katalog/penampil B2B jika tersedia. Benchmark harga tidak otomatis membuktikan willingness to pay pelanggan LihatDulu.
- Payment gateway, payout, refund, pajak biaya layanan, dan biaya platform pembayaran jika diperlukan. Cocokkan tarif dengan negara, metode, merchant tier, dan tanggalnya.
- Hosting, database, penyimpanan, requests, traffic, serta CPU/GPU untuk pemrosesan. Bedakan free tier, biaya setelah free tier, kurs valuta asing, dan batas layanan.
- Gaji/freelance untuk fungsi teknis, katalog/QC, dukungan, dan akuisisi. Gunakan benchmark lokal yang relevan, ketentuan ketenagakerjaan, THR serta iuran yang berlaku. Jika upah 2027 belum tersedia pada tanggal acuan, gunakan data yang tersedia dan nyatakan eskalasinya sebagai asumsi.
- Tempat, petugas, materi, kreator, dan angkutan contoh untuk Bursa Pindahan. Jangan menyebut quotation yang tidak pernah diperoleh.
- Demografi dan kebutuhan pasar sekitar klaster, serta data pasar yang mendukung rekonsiliasi Bab IV.

Titik awal riset yang boleh digunakan setelah memeriksa data dan tanggalnya:

- [Damodaran Current Data](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html).
- [Damodaran Country Default Spreads and Risk Premiums](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html).
- [Damodaran Country Risk Methodology](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valquestions/CountryRisk.htm).
- [DJPPR Kementerian Keuangan](https://www.djppr.kemenkeu.go.id/) dan [ADB AsianBondsOnline Indonesia](https://asianbondsonline.adb.org/indonesia/) untuk yield SBN yang tanggalnya jelas.
- [Bank Indonesia](https://www.bi.go.id/) untuk kurs atau data relevan; jangan otomatis memakai BI Rate sebagai risk-free jangka panjang.
- [Midtrans Biaya](https://midtrans.com/id/biaya) dan [Xendit Biaya](https://www.xendit.co/id/biaya).
- [Cloudflare R2 Pricing](https://developers.cloudflare.com/r2/pricing/) serta harga resmi penyedia komputasi yang benar-benar dipilih.
- [BPS](https://www.bps.go.id/), [DJP](https://www.pajak.go.id/), dan publikasi resmi pemerintah daerah untuk data dan aturan yang relevan.

Daftar ini adalah titik pencarian, bukan angka yang sudah disetujui, pilihan vendor final, atau bukti kemitraan. Jika halaman resmi dan halaman legacy berbeda, selesaikan perbedaannya dan dokumentasikan pilihan yang dipakai.

## 7. Proyeksi volume dari operational plan

Bangun model per klaster dan fase: klaster aktif, penjual baru, penjual aktif berulang, penghuni pindahan, listing baru, listing lolos bukti, stok listing aktif, barang terjual, pembatalan, refund, dan pesanan selesai. Stok listing harus memiliki roll-forward: awal + tambahan − terjual − ditarik/kedaluwarsa. Satu furnitur unik tidak boleh dihitung terjual berkali-kali.

Turunkan permintaan dari jangkauan yang memenuhi kriteria dan funnel yang dapat dijelaskan. Pertimbangkan musim pindah dan sifat pembelian furnitur yang tidak sesering barang konsumsi. Jangan memperlakukan semua mahasiswa, pengunjung, atau listing sebagai pelanggan berbayar. Pastikan kohor penjual dan pembeli tidak menggandakan orang yang sama.

Pesanan selesai harus dibatasi oleh permintaan yang relevan, unit tersedia yang dapat terjual lewat platform, kapasitas dukungan, dan kapasitas serah terima. Perhitungkan ambil sendiri serta pengiriman sesuai mix yang dipilih, bukan seolah semua pesanan memerlukan slot angkutan. Penambahan klaster harus menaikkan kebutuhan staf, akuisisi, dukungan, dan kesiapan pemenuhan.

Untuk katalog/QC, bangun kapasitas dari FTE, waktu kerja efektif, waktu per pemeriksaan, pengecualian, dan pekerjaan ulang. Modelkan antrean 3D terpisah karena foto memungkinkan publikasi. Jika permintaan melampaui kapasitas, tampilkan backlog, waktu tunggu, pembatasan volume, atau tambahan sumber daya beserta biayanya.

Gunakan definisi KPI Bab III: kelengkapan bukti, waktu publikasi, pesanan selesai, pengaduan kondisi, dan penjual aktif kembali. Bedakan target model dari hasil pengukuran nyata.

## 8. Pendapatan, unit economics, dan biaya

Tampilkan nilai barang rata-rata per kategori dan mix. Hitung:

- GMV selesai = pesanan selesai × nilai barang rata-rata yang konsisten dengan mix.
- Pendapatan biaya pembeli = pesanan yang memenuhi syarat × biaya per pesanan.
- Pendapatan komisi penjual = GMV yang memenuhi syarat × komisi.
- Pendapatan marketplace = kedua pendapatan tersebut, setelah koreksi terkait.
- Pendapatan B2B = pelanggan aktif × tarif periode layanan, disertai penambahan pelanggan, churn, kuota, dan biaya dukungannya.

Jelaskan transaksi multi-periode, pengembalian sebagian, diskon, dan siapa yang menanggung subsidi. Jangan menyamakan GMV, total pembayaran pelanggan, dan pendapatan platform. Ongkos angkut pass-through tidak menambah laba platform. Jika ada perubahan mekanisme yang diperlukan, jelaskan sebelum menerapkannya di seluruh model.

Biaya pembayaran harus memakai dasar yang benar: gateway dapat menagih atas nilai yang diproses, bukan hanya komisi platform. Perhitungkan mix metode, biaya tetap, persentase, payout, refund, dan siapa yang menanggungnya. Uji pembayaran terpusat versus alternatif yang masuk akal tanpa mengubah desain transaksi secara diam-diam.

Biaya media mengikuti listing atau pekerjaan yang diproses, termasuk yang tidak terjual. Hitung unggahan foto/video, jumlah scan, tingkat percobaan ulang, waktu CPU/GPU, utilisasi, concurrency, penyimpanan kumulatif dan retensi, requests, serta traffic sesuai kontrak penyedia. Gunakan biaya terpisah untuk pekerjaan B2B dan alokasikan infrastruktur bersama tanpa menghitung dua kali. Jangan menyebut compute atau transfer data gratis secara umum hanya karena salah satu komponen memiliki free tier.

Susun biaya variabel, semi-variabel, dan tetap: QC, dukungan, pengaduan, tenaga kerja, teknologi, pemasaran, legal/administrasi, dan pembukaan klaster. Modelkan gaji founder dengan kebijakan yang jelas; kontribusi sukarela pada awal usaha tidak boleh membuat pekerjaan penting gratis selamanya. Kaitkan penambahan staf dengan utilisasi dan service level yang diasumsikan.

Bursa Pindahan harus memiliki jadwal dan anggaran tersendiri: tempat, petugas, materi, angkutan contoh, listing terbit, pesanan selesai dalam jendela atribusi 30 hari, dan biaya per pesanan selesai. Cegah double counting dengan funnel pemasaran reguler.

Tampilkan contribution margin per pesanan, margin setelah biaya akuisisi yang relevan, CAC dengan denominator pelanggan/pesanan yang jelas, break-even volume, dan kebutuhan utilisasi. Jangan menggunakan EBITDA sebagai pengganti arus kas. Hitung payback akuisisi atau LTV hanya jika pola pembelian ulang dan biaya dukungannya memiliki dasar yang layak.

## 9. Laporan keuangan, pajak, dan modal kerja

Buat laba rugi, arus kas, dan neraca yang saling merekonsiliasi. Sediakan jadwal capex, depresiasi/amortisasi, belanja pengembangan, dan penggantian aset. Jangan mengapitalisasi semua pengeluaran teknis demi mempercantik laba; jelaskan kebijakan dan dampaknya.

Tentukan bentuk entitas dan perlakuan pajak sebagai asumsi legal yang diverifikasi melalui sumber resmi pada tanggal acuan. Periksa kelayakan, batas waktu, dan transisi pajak UMKM jika digunakan; jangan memakai pajak omzet kecil selamanya atau menghitungnya atas GMV tanpa dasar. Perhitungkan PPN dan pajak biaya penyedia sesuai ketentuan relevan. Jelaskan kerugian fiskal dan cash tax; jangan membuat tax refund otomatis pada periode rugi.

Modelkan piutang biaya platform, utang biaya operasi, pembayaran di muka, pendapatan diterima di muka B2B, dan settlement sesuai mekanisme yang dipilih. Hindari proxy modal kerja persentase GMV jika tidak mencerminkan hak dan kewajiban platform.

Pisahkan dana pelanggan/penjual yang dititipkan atau diselesaikan melalui penyedia pembayaran dari kas bebas LihatDulu. Jika masuk neraca, rekonsiliasikan aset terkait dan kewajibannya. Dana tersebut tidak boleh dipakai sebagai runway, laba, atau modal ekspansi. Akun payable operasional bukan debt financing.

## 10. CAPM terperinci dan dapat ditelusuri

Hitung cost of equity dari data, bukan memasukkan persentase final dari screenshot atau mempertahankan hurdle AUTO2000. Input pasar mentah boleh berupa angka bersumber; transformasi, pemilihan beta, pembobotan, dan hasil diskonto harus dihitung dengan rumus. Jangan menciptakan komponen perhitungan yang tidak tersedia dalam sumber.

Gunakan mata uang IDR nominal yang konsisten dengan arus kas. Tampilkan tabel: komponen, data mentah, satuan, tanggal, sumber, penyesuaian, rumus, dan hasil.

a. Risk-free rate: identifikasi yield SBN jangka panjang yang relevan pada atau sebelum tanggal acuan. Bedakan yield obligasi negara dengan risk-free yang disesuaikan atas sovereign default risk. Bila memakai pendekatan Damodaran, tunjukkan sumber yield dan default spread serta perhitungan `Rf_IDR = yield SBN_IDR − sovereign default spread`. Jelaskan kesepadanan tenor, mata uang, dan keterbatasan proksi spread. Jangan otomatis memakai angka pada gambar, BI Rate, atau yield USD tanpa penyesuaian.

b. Equity risk premium dan country risk: ambil vintage data mature-market ERP, Indonesia default spread, dan country risk premium yang konsisten. Periksa file unduhan dan tanggal aktual; label “2026” tidak cukup. Bedakan default spread, CRP, dan total Indonesia ERP. Jika sumber menyediakan komponen pembentukan CRP, tampilkan perhitungannya; jika hanya angka estimasi final tersedia, kutip dengan jujur.

c. Bottom-up beta: pilih pembanding marketplace/listing/platform asset-light yang relevan. Cari sekurang-kurangnya beberapa peer yang datanya dapat diverifikasi jika tersedia. Tampilkan alasan pemilihan, beta beserta metode/periode estimasinya, nilai pasar ekuitas, debt-to-equity, pajak, dan perlakuan kas. Jangan menyamakan produsen atau retailer pemilik inventori dengan marketplace tanpa penyesuaian. Jangan memakai beta fintech hanya karena ditampilkan pada contoh. Jika peer tidak memadai, gunakan industry unlevered beta dari sumber tepercaya dengan alasan dan sensitivity; jangan mengarang peer data.

d. Tampilkan unlevering, misalnya `Beta_U = Beta_L / [1 + (1 − T) × D/E]`, dan penyesuaian kas jika digunakan. Gunakan perlakuan debt/lease dan tax rate yang konsisten. Agregasikan beta dengan median atau bobot yang beralasan. Jika B2B material, jelaskan pengaruh mix bisnis tanpa menciptakan pembobotan yang berputar dengan valuasi hasil model. Dengan target debt nol, tampilkan relevering sehingga `Beta_L_target = Beta_U` pada asumsi formula tersebut.

e. Pilih satu spesifikasi utama cost of equity yang konsisten. Pendekatan yang dapat dipakai adalah CAPM dengan penyesuaian country risk: `Ke_IDR = Rf_IDR + Beta_L_target × ERP_mature + lambda × CRP_Indonesia`. Nyatakan bahwa komponen CRP merupakan penyesuaian tambahan terhadap CAPM dasar dan jelaskan lambda. Lambda = 1 boleh sebagai asumsi eksposur Indonesia yang dijelaskan, bukan estimasi empiris fiktif. Jika memilih alternatif berbasis total Indonesia ERP, jelaskan penempatan beta dan jangan menambahkan CRP lagi. Hindari double counting country risk.

f. Karena debt financing nol, tunjukkan `E/(D+E)=100%`, `D/(D+E)=0%`, dan `WACC=Ke` dalam struktur yang dimodelkan. Dana hibah bukan alasan menganggap biaya ekuitas nol. Gunakan Ke yang dihitung sebagai hurdle utama dan uji input diskontonya. Jangan menyisipkan premi startup atau illiquidity ke CAPM tanpa label; jika diuji, pisahkan sebagai analisis tambahan. Cost of equity CAPM juga tidak boleh diklaim sebagai target return aktual investor VC.

## 11. Funding stage, runway, dan dilusi

Bangun pendanaan berdasarkan kebutuhan kas dan milestone, mengikuti urutan modal pendiri/non-dilutif, pre-seed, lalu seed. Jangan membuat semua putaran cair otomatis pada tanggal yang nyaman untuk model.

Untuk setiap tahap, tampilkan waktu indikatif, milestone masuk, kebutuhan penggunaan dana, saldo kas sebelum funding, burn, runway, buffer kas, nilai dana yang dibutuhkan, biaya penghimpunan dana, dan saldo setelah funding. Gunakan runway target yang dijelaskan sebagai asumsi perencanaan dan uji sensitivitasnya. Tentukan modal pendiri sebagai kebutuhan/rekomendasi, bukan uang yang telah dijanjikan pengguna.

Hitung funding gap dari kas sebelum financing dan kebutuhan sampai milestone/putaran berikutnya. Hindari rumus circular antara funding, kas, staf, dan ekspansi. Bedakan initial investment proyek, capex, kumulatif burn, total dana yang dihimpun, dan nilai putaran; kelimanya bukan ukuran yang dapat dipertukarkan.

Hibah atau hadiah kompetisi yang belum diperoleh harus dilabeli belum committed dan diuji pada kasus tanpa hibah. Tampilkan kelayakan operasi sebelum dukungan hibah serta efek hibah pada kebutuhan pendanaan secara terpisah. Perlakuan laporan keuangan hibah mengikuti syarat dan standar yang relevan; hibah tidak boleh disamarkan sebagai pendapatan pelanggan.

Berikan cap table indikatif untuk founder, pre-seed, dan seed. Gunakan `post-money = pre-money + new primary equity` serta persentase investor dan dilusi kumulatif yang benar. Jelaskan basis valuasi, jangan menghitung valuasi hanya dari nominal pendanaan yang diinginkan. Jika memasukkan option pool, nyatakan ukuran, timing, dan siapa yang terdilusi. Skenario ini bukan termsheet atau komitmen investor.

Uji funding terlambat dan funding tidak tersedia, termasuk kas minimum, penundaan klaster/rekrutmen, dan milestone yang berubah. Jangan menutup kekurangan kas dengan pinjaman tersembunyi atau suntikan ekuitas tanpa batas. Jika seed tidak diperlukan karena bisnis sudah mendanai dirinya sendiri, jelaskan opsi ekspansinya dan jangan memaksa round yang tidak dibutuhkan.

## 12. Kelayakan proyek dan return investor

Gunakan arus kas proyek setelah pajak sebelum financing. Tampilkan investasi Tahun 0 dan seluruh investasi, biaya, cash tax, serta perubahan modal kerja berikutnya. Bentuk dasarnya: `FCFF = EBIT + D&A − cash operating taxes − capex − perubahan operating non-cash working capital`, dengan penyesuaian jelas untuk kas lain yang relevan. Rekonsiliasikan ke laporan arus kas. Setoran modal, hasil fundraising, dana titipan, dan pendapatan pendanaan tidak boleh menaikkan project IRR.

Hitung NPV pada Ke/WACC yang konsisten, IRR/XIRR sesuai tanggal, payback nominal, discounted payback, operating break-even, cash break-even, dan tahun pertama IRR kumulatif > Ke. Penjumlahan bulanan, tanggal XIRR, dan diskonto tahunan harus konsisten. Investasi Tahun 0 tidak boleh didiskontokan dua kali atau dimasukkan lagi ke biaya periode berikutnya.

Jadikan kelayakan dari arus kas operasi selama horizon eksplisit, tanpa exit/terminal value, sebagai hasil utama. Jika menampilkan terminal value atau exit valuation, pisahkan sebagai analisis tambahan dan ungkapkan kontribusinya terhadap nilai. Pertumbuhan terminal harus konsisten dengan reinvestasi dan discount rate. Jangan memasukkan pelepasan modal kerja likuidasi bersamaan dengan going-concern terminal value yang mengasumsikan operasi tetap berjalan.

Jika arus kas memiliki beberapa pergantian tanda, periksa kemungkinan IRR tidak unik. Jangan menyembunyikan kegagalan IRR menjadi nol atau memaksa satu angka. Gunakan NPV dan bila relevan MIRR/NPV profile sebagai pendamping, dengan asumsi yang jelas.

Return investor per putaran boleh diberikan sebagai tambahan indikatif hanya jika investasi, kepemilikan terdilusi, dividen/distribusi, asumsi exit, dan waktu exit dijelaskan. Pisahkan founder return, project IRR, dan investor IRR. Nilai putaran pendanaan bukan pendapatan atau cash exit bagi semua investor.

## 13. Sensitivity analysis

Pertahankan dan adaptasi sheet Sensitivity. Gunakan driver LihatDulu, bukan reach/lift otomotif. Pilih sekurang-kurangnya satu matriks dua variabel yang material, tampilkan NPV dan IRR pada kombinasi yang sama, serta tambahan analisis satu variabel/tornado untuk risiko utama jika berguna.

Contoh driver yang layak: permintaan/pasokan yang dapat menjadi pesanan selesai dan monetisasi net per order; biaya pemrosesan, CAC, biaya staf, pembatalan, serta komponen Ke. Pilih berdasarkan materialitas hasil dan alasan bisnis, bukan daftar formalitas. Nyatakan apakah biaya kapasitas disesuaikan atau dianggap tetap dalam masing-masing pengujian.

Semua kombinasi harus menghitung ulang cash flow dan menghormati batas kapasitas. Pusat matriks harus sama dengan hasil Base pada periode dan definisi yang sama. Tampilkan rentang dengan sumber atau alasan, ambang NPV nol, serta interpretasi keputusan operasi yang dapat diambil. Jika memakai Ke versus variabel lain, perubahan Ke mengubah NPV/hurdle, bukan IRR arus kas secara langsung.

Gunakan tahun penilaian yang sama untuk sensitivity dan Monte Carlo. Default-nya akhir horizon dasar penuh; tahun pertama crossing Base boleh menjadi analisis tambahan. Jangan menyesuaikan tahun akhir setiap kombinasi agar masing-masing tampak lolos.

## 14. Monte Carlo analysis

Pertahankan dan bangun ulang sheet Monte Carlo menggunakan model LihatDulu yang sama. Targetkan 10.000 simulasi jika performa memungkinkan; gunakan minimal 5.000 dengan alasan dan pemeriksaan stabilitas jika ukuran workbook menjadi masalah. Catat jumlah percobaan, seed, metode, distribusi, parameter, korelasi, dan tahun penilaian.

Pilih driver ketidakpastian yang material: misalnya akuisisi dan pasokan penjual, konversi/penyelesaian, nilai barang, monetisasi, biaya akuisisi, biaya media/retry, dan biaya operasional. Hindari terlalu banyak variabel yang tidak berpengaruh atau menggandakan ketidakpastian yang sama. Harga/biaya bersumber tetap tidak otomatis berarti volatilitasnya terukur.

Gunakan distribusi bounded untuk probabilitas dan kapasitas, nilai nonnegatif untuk volume/biaya, serta distribusi lain dengan alasan yang sesuai. Jika memakai triangular atau PERT, jelaskan low/mode/high sebagai asumsi terstruktur bila belum ada data empiris. Bedakan ketidakpastian jangka panjang per trial dan variasi antarperiode. Jangan mengacak tingkat pertumbuhan secara independen tanpa batas sehingga volume meledak.

Pertahankan hubungan logis antara volume, kebutuhan staf, compute, refund, kapasitas, dan ekspansi. Jelaskan korelasi atau common factor yang digunakan; jangan mengklaim matriks korelasi asumsi sebagai hasil estimasi. Funding delay dapat diuji sebagai skenario diskret atau stress test terpisah agar dampaknya terhadap operasi dan likuiditas tetap jelas.

Setiap trial harus membentuk arus kas dari driver dan struktur model, bukan menambahkan noise langsung pada IRR/NPV final. Gunakan seed yang dapat direproduksi. Sediakan mekanisme refresh yang benar-benar bekerja serta jelaskan apakah hasil berubah melalui formula workbook atau proses simulasi yang disertakan; jangan menyerahkan snapshot yang diklaim dinamis.

Laporkan P5/P50/P95 NPV, IRR untuk trial yang valid, peluang NPV > 0, peluang IRR > Ke, jumlah trial IRR tidak tersedia/tidak unik, distribusi tahun pertama crossing beserta trial yang tidak pernah crossing, dan distribusi kebutuhan dana/kas minimum. Nyatakan denominator setiap probabilitas dan jangan menghapus trial gagal. Ukur funding gap/negative cash dalam kasus financing terbatas atau pendanaan terjadwal, bukan setelah unlimited equity plug.

Tampilkan histogram NPV dan grafik risiko pendanaan yang berguna, dengan interpretasi sumber risiko terbesar. Gunakan common assessment horizon untuk semua trial utama. Jika diskonto ikut disimulasikan, jelaskan parameter dan bandingkan setiap IRR dengan Ke trial yang konsisten; jangan mencampur metrik tersebut dengan hasil Ke tetap tanpa label.

## 15. Integrasi ke draft proposal

Lengkapi Bab V §5.1 dan §5.2 serta Lampiran E dengan hasil model yang benar-benar dihitung. Ganti placeholder, bukan menambahkan paragraf keuangan yang terpisah dari cerita bisnis.

Bab V harus mencakup penggerak pendapatan, unit economics, struktur biaya, profitabilitas, break-even, arus kas, kebutuhan dana per fase, CAPM, dan hasil kelayakan. Sajikan angka utama dan interpretasi yang dapat dijelaskan saat presentasi. Detail asumsi, sumber, beta/CAPM, jadwal pendanaan, sensitivity, dan Monte Carlo ditempatkan di Lampiran E secara ringkas dan terbaca.

Sinkronkan Executive Summary, Bab II §2.5, kapasitas/staf/milestone Bab III, biaya dan hasil kampanye Bab IV, serta Lampiran D/F/G ketika angka model memerlukannya. Jangan mengubah temuan survei atau mengarang bukti produk untuk menyesuaikan angka keuangan. Jika terjadi konflik mendasar dengan desain usaha, nyatakan dan selesaikan dengan perubahan paling terbatas yang dapat dijelaskan.

TAM/SAM/SOM harus berupa pendapatan tahunan marketplace dari transaksi furnitur bekas yang selesai, sesuai draft. Bedakan dari GMV dan belanja mebel umum. Angka BPS dalam repo merupakan konteks kategori luas dan harus diverifikasi sebelum dipakai; porsi barang bekas tidak boleh diasumsikan sebagai fakta. Jika data porsi tidak tersedia, nyatakan rentang/skenario secara jujur. Jangan memakai shortcut pangsa pasar tanpa dasar. SOM tahun ketiga harus sama dengan output marketplace tahun ketiga pada cakupan dan harga yang sama; pendapatan B2B ditampilkan terpisah.

Sertakan tabel rekonsiliasi angka proposal ke sheet/range workbook: volume, GMV, pendapatan, biaya, EBITDA/laba, cash flow, kapasitas, dana per fase, CAPM, NPV, IRR, dan payback. Bedakan target periode tertentu dari hasil sepanjang horizon.

## 16. Penyajian dan verifikasi

Gunakan tampilan profesional yang mengikuti keteraturan template AUTO2000 dengan identitas LihatDulu. Acuan warna dalam repo: hijau `#185544`, hijau gelap `#15382C`, teks `#243D35`, latar lembut `#EEF5F0`, dan abu `#DFE9E3`. Gunakan aksen secukupnya, penanda input/formula yang konsisten, satuan Rp yang jelas, serta angka dalam Rp juta bila sesuai skalanya. Jangan mempertahankan unit Rp miliar hanya karena dipakai AUTO2000.

Hindari ruang kosong berlebihan, dekorasi, label rumit, tabel yang terpotong, font terlalu kecil, atau grafik yang hanya mengulang angka. Sediakan freeze panes, format angka, print area, dan grafik yang berguna. Formula utama tidak boleh diganti dengan angka hasil tempelan atau bergantung pada external workbook link yang hilang.

Catat sumber pada area input yang relevan: judul, penerbit, URL langsung, tanggal data/akses, angka sumber, penyesuaian, dan input yang dipengaruhi. Sumber raw data perlu jelas, sedangkan asumsi tetap diberi label asumsi. Gunakan sitasi nama penulis/lembaga dan tahun dalam proposal, beserta daftar referensi yang benar-benar dapat dibuka.

Pertahankan struktur, heading, header/footer, dan format proposal: A4, margin 2,54 cm, Times New Roman 12, serta pengaturan spasi dan gaya yang terdapat pada draft revisi. Edit isi yang perlu diintegrasikan, bukan merombak desain keseluruhan. Perbarui daftar isi, caption, nomor halaman, dan rujukan lampiran setelah perubahan.

Validasi model dan file final, setidaknya:

- Neraca seimbang, perubahan kas merekonsiliasi arus kas, dan retained earnings mengikuti laba serta distribusi.
- Agregasi bulanan/tahunan, Tahun 0, tanggal diskonto, cash tax, capex, D&A, dan modal kerja benar; GMV, dana titipan, dan dana fundraising tidak menjadi pendapatan proyek.
- Volume tidak melebihi pasokan/permintaan/kapasitas, biaya media mengikuti seluruh pekerjaan, dan pembukaan klaster mengikuti kas serta milestone.
- Funding dan cap table merekonsiliasi, tidak ada debt financing, dan funding gap terlihat pada stress test yang relevan.
- Pusat sensitivity sama dengan Base; Monte Carlo menghitung cash flow yang sama, memakai denominator jelas, dan tidak menyembunyikan trial gagal.
- Perubahan selector dan input material benar-benar mengubah hasil, grafik, horizon/crossing, serta funding secara tepat; hasil perbandingan kasus memiliki metode refresh yang valid.
- Tidak ada `#NAME?`, `#REF!`, `#VALUE!`, error tidak disengaja, circular reference, external link hilang, atau hasil cache yang diklaim sebagai bukti recalculation. Laporkan keterbatasan pengujian engine Excel secara jujur.
- Seluruh angka proposal cocok dengan workbook dan seluruh halaman DOCX/PDF diperiksa secara visual setelah render.

## 17. Deliverable dan pelaksanaan

Serahkan:

1. `LihatDulu_Financial_Projection.xlsx`: model lengkap yang dapat diedit, mencakup CAPM, funding/cap table, sensitivity, Monte Carlo, dan seluruh jadwal pendukung yang diperlukan.
2. `LihatDulu_Proposal_Integrated_Finance.docx`: salinan draft revisi dengan Bab V, Lampiran E, dan perubahan sinkronisasi yang diperlukan.
3. `LihatDulu_Proposal_Integrated_Finance.pdf`: versi proposal yang sudah dirender dan diperiksa.
4. Ringkasan singkat dalam chat: asumsi paling menentukan, sumber benchmark utama, CAPM, tahun pertama IRR > CAPM jika tercapai, NPV/IRR pada horizon penuh, kebutuhan dana per tahap, serta temuan sensitivity/Monte Carlo. Tunjukkan perubahan material pada proposal dan batas bukti yang masih relevan.

Sertakan kode simulasi atau instruksi refresh hanya jika diperlukan untuk memakai hasil dengan benar; jangan menggantikan workbook dan proposal dengan kode. Jangan mengirim varian file berulang yang membingungkan.

Mulai dari audit bahan, pengumpulan input, dan pemetaan operasi ke volume/biaya/kas. Ambil keputusan implementasi rutin secara mandiri dalam batas desain yang telah disepakati. Tanyakan hanya jika sumber wajib benar-benar hilang atau pilihan akan mengubah bisnis secara material. Ketika data empiris tidak cukup untuk suatu asumsi, gunakan estimasi berlabel dengan benchmark/rentang dan uji risikonya. Selesaikan model, integrasi, recalculation, dan pemeriksaan visual sebelum menyerahkan hasil.
