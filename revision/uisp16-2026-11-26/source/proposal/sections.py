"""Page modules for the LihatDulu proposal. Values in braces come from the finance workbook."""

def item(title, paras, fig=None, table=None, after=None, note=None, label=None):
    return dict(title=title, paragraphs=paras, figure=fig, table=table, after=after or [], note=note, label=label)

pages = {
11: item('4.1 Segmen awal dan posisi pasar',[
    'Pilih satu pasar yang bisa dilayani sebelum memperluas jangkauan. Penghuni kos di sekitar UI Depok menjadi segmen pembeli awal karena batas ruang, tanggal pindah, serta cara angkut memengaruhi pilihan barang. Namun, survei belum membandingkan tingkat permintaan antarwilayah. Pemilihan klaster awal merupakan keputusan operasional yang harus diuji.',
    'Pedagang furnitur bekas menjadi calon pemasok berulang. Penghuni yang pindah menyediakan tambahan unit dengan waktu penjualan yang lebih sempit. Oleh karena itu, tim mengukur ketersediaan stok dari pedagang secara terpisah dari listing musiman.',
], 'stp', ('Tanda kesiapan tiap segmen', ['Segmen','Keputusan saat pertama bergabung','Tanda kesiapan'],[
    ['Pembeli kos','Memilih barang yang sesuai ruang dan anggaran','Ukuran, lokasi, dan cara terima dapat diperiksa'],
    ['Reseller lokal','Menentukan unit yang siap ditawarkan ulang','Stok terkonfirmasi dan penjual dapat dihubungi'],
    ['Penghuni pindah','Menetapkan batas waktu pengambilan','Jadwal dan foto barang tersedia'],
]), [
    'Posisi LihatDulu bertumpu pada satu iklan yang menyatukan kondisi, ukuran, dan serah terima. Pembeli menilai biaya hingga barang tiba, sementara penjual mengetahui penerimaan bersih sebelum menyetujui transaksi. Profil pembeli dan hipotesis profil penjual dirinci dalam Lampiran B.'
], label='Target awal dalam wilayah layanan'),
12: item('4.2 Ukuran pasar berdasarkan pendapatan',[
    'TAM memperkirakan peluang pendapatan per tahun dari transaksi furnitur rumah tangga bekas di Indonesia. SAM menyaring peluang itu ke area Jabodetabek yang mampu dijangkau. Sementara itu, SOM mengikuti pesanan yang benar-benar dapat dipenuhi pada tahun ketiga dalam model.',
    'Belanja mebel nasional dalam data BPS setara Rp11,635 triliun per tahun. Model memakai porsi furnitur bekas 2,6% dan nilai per unit Rp440.212,50. Pada SAM, faktor keterlayanan 10,5% mengacu pada proksi 11,38% penduduk di Jabodetabek daratan. Porsi bekas dan keterlayanan adalah asumsi skenario.',
], 'market', ('Jembatan perhitungan pasar', ['Lapisan','Perhitungan','Basis tahun'],[
    ['TAM','Belanja kategori × 2,6% × (Rp18.000 ÷ Rp440.212,50 + 6,5%)','Proksi tahunan'],
    ['SAM','TAM × faktor keterlayanan 10,5%','Proksi tahunan'],
    ['SOM','Biaya pembeli Rp89,928 juta + 6,5% × GMV Rp2.177,309 juta','Tahun 3'],
]), [
    'Hasil skenario dasar adalah {{TAM}} untuk TAM, {{SAM}} untuk SAM, dan {{SOM}} untuk SOM. SOM berasal dari 4.746 pesanan selesai pada delapan klaster model. Nilainya sama dengan pendapatan marketplace tahun ketiga dalam workbook. Langganan B2B dan ongkir dicatat terpisah.'
], label='TAM, SAM, dan SOM sebagai pendapatan marketplace'),
13: item('4.3 Persaingan pada tingkat keputusan pembeli',[
    'OLX membantu pembeli menemukan penawaran dengan lokasi dan harga. Grup komunitas mempermudah pencarian di area sempit serta percakapan dengan penjual. Sementara itu, toko furnitur bekas menyediakan akses langsung ke stok. Pilihan tersebut dapat tetap unggul ketika pembeli sudah mengenal penjual atau membutuhkan inspeksi langsung.',
    'LihatDulu mengambil posisi pada pekerjaan sebelum kunjungan. Bukti kondisi, dimensi, serta opsi penerimaan tercatat pada unit yang sama. Namun, model ini menambah biaya pemeriksaan dan dukungan. Tim perlu menguji apakah pembeli mau menyelesaikan transaksi melalui platform setelah memakai informasi itu.',
], 'pesaing', ('Implikasi pembandingan', ['Alternatif','Kekuatan yang dipertahankan','Respons LihatDulu'],[
    ['Iklan lokal','Katalog luas dan lokasi terlihat','Fokus pada kelengkapan per unit dan keterlayanan klaster'],
    ['Komunitas','Pertanyaan cepat dan relasi lokal','Teruskan bukti kondisi hingga serah terima'],
    ['Toko bekas','Inspeksi dan ketersediaan bisa dicek langsung','Jadikan reseller sebagai kanal pasokan yang diuji'],
]), [
    'Contoh iklan Depok menunjukkan variasi kategori dan harga penawaran. Perbandingan fitur dibatasi pada yang terlihat di kanal publik. Catat kategori, lokasi, harga, dan tanggal pengamatan yang sama agar pembanding dapat diaudit. Contoh itu tidak memberikan tingkat penjualan, pangsa pasar, atau mutu setiap penjual.'
], label='Perbandingan alternatif pencarian dan pemeriksaan'),
14: item('4.4 Penawaran, harga, dan distribusi',[
    'Mulai dari meja, kursi, rak, serta lemari yang dapat difoto, diukur, dan dipindahkan dengan rute yang tersedia. Karena itu, kategori katalog mengikuti wilayah yang mampu dilayani. Penawaran yang belum memiliki waktu pengambilan atau opsi angkut siap tidak dipromosikan sebagai barang siap diterima.',
    'Harga dipertimbangkan dari dua sisi. Pembeli melihat biaya sampai barang diterima, sedangkan penjual melihat hasil bersih setelah komisi. Tarif awal {{BUYER_FEE}} per pesanan selesai dan komisi {{SELLER_FEE}} adalah asumsi skenario. Tim menguji keberatan kedua pihak dan kontribusi per pesanan pada pilot.',
], 'marketing-mix', ('Uji harga dan distribusi pada pilot', ['Keputusan','Bukti yang dicatat'],[
    ['Harga pembeli','Bandingkan harga, biaya layanan, serta ongkir pada barang yang sepadan'],
    ['Hasil bersih penjual','Tanyakan biaya dan waktu menjual lewat kanal lain'],
    ['Ketersediaan barang','Konfirmasi stok dan akses pemindahan per unit'],
    ['Pembayaran','Catat peralihan dari rincian biaya ke pesanan yang tuntas'],
]), [
    'Pembayaran ongkos angkut mengikuti tarif aktual mitra pada rute yang dipilih. Sampel 24 iklan OLX Depok menunjukkan median Rp362.500. Pilot mencatat harga penutupan, waktu penjualan, serta margin pesanan. Tim menguji biaya layanan setelah pembeli memperoleh informasi pengiriman, agar keberatan terhadap tarif dapat dibedakan dari hambatan rute. Untuk barang yang perlu diangkat melalui tangga, tim memastikan biaya dan jadwal sebelum menawarkan opsi kirim.'
], label='Bauran pemasaran untuk peluncuran di sekitar kampus'),
15: item('4.5 Fase 1 Kurasi katalog dan rekrutmen lokal',[
    'Pada enam bulan pertama, tim mengajak pedagang lokal mencatat stok dan membantu penghuni yang akan pindah membuat penawaran. Sementara itu, pembeli menerima tautan ke koleksi yang sudah disaring menurut ukuran dan lokasi. Materi promosi menonjolkan informasi yang bisa diperiksa saat itu juga.',
    'Ajak penjual mengirim foto kondisi, ukuran, dan perkiraan tanggal ambil. Tim memeriksa kelengkapan sebelum listing muncul. Karena itu, keberhasilan tidak diukur dari banyaknya formulir masuk. Stok yang terkonfirmasi, listing lengkap, dan pesanan tuntas menjadi syarat untuk menambah promosi.',
], 'mock-material', ('Pelaksanaan awal', ['Saluran','Materi atau ajakan','Sinyal yang dicatat'],[
    ['Pedagang lokal','Bawa satu unit pertama untuk dibantu listing','Unit tersedia dan pembaruan stok'],
    ['Pengelola kos dan komunitas','Bagikan daftar barang sesuai ruang dan area','Kunjungan berkualitas dan pesanan selesai'],
    ['Meja bantuan','Bawa foto, ukuran, lokasi dan jadwal','Rasio pengajuan yang menjadi listing lengkap'],
]), [
    'Kartu kondisi, label unit dan materi meja bantuan menggunakan sistem visual yang sama. Setiap kartu memuat atribut yang dibutuhkan untuk mengambil keputusan, dengan contoh materi konsep pada gambar. Angka harga unit tetap mengikuti barang yang diverifikasi.'
], label='Konsep material kurasi dan meja bantuan'),
16: item('4.6 Fase 2 Konten Muat Nggak',[
    'Kreator lokal memulai dari satu batas yang mudah dipahami. Misalnya, tersisa ruang sempit di antara kasur dan dinding, sehingga pembeli perlu memeriksa lebar meja sebelum menanyakan ongkos. Namun, video hanya diluncurkan jika barang yang ditampilkan masih tersedia atau ada koleksi pengganti yang bisa dilayani.',
    'Tiga adegan bergerak dari mengukur ruang, membuka foto kondisi dan ukuran, lalu melihat cara menerima. Arahkan pembaca ke koleksi klaster setempat. Setelah itu, tanda tautan memisahkan kunjungan, konfirmasi stok, dan pesanan selesai untuk evaluasi biaya kreator.',
], 'mock-creator', ('Naskah kampanye dan pelacakan', ['Adegan','Isi materi','Tindakan yang diukur'],[
    ['Ukur ruang','“Ruangnya segini. Mejanya muat?”','Klik dari tautan kreator'],
    ['Cek bukti','Buka ukuran dan foto aus pada listing','Pembukaan rincian dan konfirmasi stok'],
    ['Rencanakan terima','Bandingkan ambil sendiri dan pengiriman','Pesanan selesai per kanal'],
]), [
    'Jika kunjungan naik dan pesanan tertahan, tim memeriksa stok, kecocokan, biaya angkut, serta jadwal sebelum menambah anggaran. Pembandingnya adalah biaya per pesanan selesai, dengan satu sumber atribusi utama per pesanan. Gunakan penawaran yang sama ketika membandingkan respons antarformat, lalu pisahkan hasil menurut stok yang benar-benar bisa dikonfirmasi.'
], label='Mockup konsep konten Muat Nggak'),
17: item('4.7 Fase 3 Bursa Pindahan',[
    'Bursa Pindahan dirancang untuk klaster yang sudah memiliki stok dan jadwal ambil. Garis di lantai menunjukkan ukuran kamar kos. Sementara itu, pengunjung dapat mencoba penempatan furnitur bekas, melihat kondisi barang, dan membuka penawaran melalui penanda unit.',
    'Pembeli memilih jadwal setelah penjual mengonfirmasi stok. Penjual yang akan pindah membawa foto serta ukuran ke meja bantuan. Karena itu, agenda acara memerlukan petugas katalog, petugas serah terima, dan jalur pengambilan yang tidak mengganggu pergerakan pengunjung.',
], 'mock-bursa', ('Tiga titik keputusan di lokasi', ['Titik','Keputusan pengunjung','Catatan operasi'],[
    ['Ruang kos bergaris','Barang muat dan kondisi bisa diterima','Periksa unit serta catat pertanyaan'],
    ['Penanda unit','Buka penawaran dan pilih cara terima','Konfirmasi stok dan slot'],
    ['Meja penjual','Ajukan barang yang akan ditinggal','Periksa foto sebelum menerbitkan'],
]), [
    'Ukur listing yang terbit, jumlah pesanan selesai yang dapat ditelusuri ke acara dalam 30 hari, dan biaya per pesanan tersebut. Materi ini adalah mockup konsep. Kalender, tempat, dan penyedia angkut disepakati kemudian setelah klaster lulus uji kesiapan.'
], label='Mockup konsep Bursa Pindahan di area kampus'),
18: item('4.8 Dari jangkauan hingga pemakaian kembali',[
    'LihatDulu mengukur keberhasilan pemasaran ketika barang diterima. Awalnya, kunjungan dari komunitas dan kreator memberi gambaran apakah penawaran relevan. Namun, sesi yang berhenti sebelum konfirmasi stok harus ditelusuri ke hambatan yang spesifik. Tim membedakan klik, pemesanan, dan serah terima.',
    'Pembeli yang belum selesai menata kamar dapat menyimpan pencarian. Pedagang lokal dapat memperbarui listing setelah stok berganti. Karena itu, dua bentuk retensi diukur terpisah melalui kohor pembeli dan pemasok. Pembelian ulang mengikuti jumlah pesanan selesai, sedangkan retensi penjual mengikuti publikasi berkualitas dan stok yang tetap aktif.',
], 'aida', ('Aturan evaluasi pemasaran', ['Ukuran','Denominator','Kegunaan'],[
    ['Rasio selesai','Pesanan selesai ÷ pesanan terkonfirmasi','Mendeteksi hambatan pemenuhan'],
    ['Biaya akuisisi','Biaya kanal ÷ pelanggan pertama dengan pesanan selesai','Membandingkan efisiensi kanal'],
    ['Biaya acara per order','Biaya acara ÷ pesanan teratribusi yang selesai dalam 30 hari','Menilai kelayakan pengulangan'],
    ['Penjual aktif kembali','Penjual menerbitkan ulang ÷ kohor penjual yang pernah menyelesaikan pesanan','Mengamati kesinambungan pasokan'],
]), [
    'Dengan ukuran ini, pemasaran menaikkan anggaran hanya ketika operasi mampu menyerap permintaan yang datang. Jika pertanyaan kondisi berulang atau lokasi pengambilan berubah, pembenahan listing dan jadwal ditempatkan sebelum perluasan kanal. Biaya yang terlanjur dikeluarkan untuk pesanan batal tetap dicatat pada kanalnya agar evaluasi menangkap pemborosan.'
], label='Perjalanan pemasaran dan peristiwa yang diukur'),
19: item('5.1 Dasar proyeksi dan penggerak volume',[
    'Proyeksi menggunakan Tahun 0 sebagai masa persiapan, diikuti operasi 2027–2036. Dua puluh empat bulan pertama diperiksa secara bulanan karena penerimaan biaya, pembaruan stok, dukungan, dan pembukaan klaster dapat berbeda waktunya. Setelah itu, model memakai langkah tahunan untuk menampilkan perubahan skala dan biaya.',
    'Pesanan selesai dibatasi oleh nilai terendah dari permintaan yang terkonversi, unit yang mampu terjual, serta kapasitas serah terima dan dukungan. Karena itu, permintaan yang tinggi tidak otomatis menjadi pendapatan. Tolok ukur survei memandu apa yang perlu dibuktikan dalam listing. Survei tidak menjadi input tingkat konversi atau kesediaan membayar.',
], None, ('Rantai volume sampai pendapatan', ['Tahap','Penggerak','Implikasi model'],[
    ['Pasokan','Penjual aktif × unit per penjual × kelengkapan × kesiapan stok','Membatasi unit yang dapat dijual'],
    ['Permintaan','Jangkauan relevan × pesanan masuk; koreksi batal atau refund','Menentukan peluang pesanan yang layak dipenuhi'],
    ['Pemenuhan','Dukungan × produktivitas dan slot serah terima','Cap pesanan selesai per klaster'],
    ['Pendapatan','Pesanan selesai × biaya tetap + GMV selesai × komisi','Harga barang dan ongkos tidak menjadi pendapatan'],
    ['B2B','Pelanggan aktif × tarif periode layanan','Jadwal pendapatan dan biaya terpisah'],
]), [
    'Pesanan tahun pertama sekitar {{ORDERS_Y1}} dan tahun ketiga {{ORDERS_Y3}} pada skenario dasar. Kapasitas harus tersedia di klaster yang sama dengan permintaan. Jadwal teknis media mengikuti jumlah listing yang diperiksa dan dicoba, termasuk pekerjaan yang tidak menghasilkan penjualan.'
]),
20: item('5.2 Ekonomi satu pesanan dan titik impas',[
    'Satu pesanan memuat satu unit furnitur. Pembeli mengetahui harga barang, biaya layanan, serta biaya pengiriman aktual jika memilih kirim. Namun, harga barang bruto dan ongkir merupakan aliran dana terpisah. Komisi dipotong dari hasil bersih penjual setelah pesanan selesai.',
    'Kelengkapan listing dan kesiapan jadwal dapat menambah biaya sebelum ada pesanan. Karena itu, kontribusi dihitung setelah biaya pembayaran, penanganan listing, foto atau media, dukungan, serta pengaduan yang relevan. Biaya tetap menutup fungsi yang tetap berjalan saat volume turun.',
], None, ('Contoh pesanan dalam skenario dasar', ['Arus','Perhitungan','Rupiah'],[
    ['Harga furnitur','Nilai barang model tahun pertama','{{AOV}}'],
    ['Biaya layanan','Tarif per pesanan selesai','{{BUYER_FEE}}'],
    ['Ongkir contoh','Diteruskan kepada penyedia angkut','{{DELIVERY_EXAMPLE}}'],
    ['Total pembeli','Harga + biaya layanan + ongkir','{{BUYER_TOTAL}}'],
    ['Komisi penjual','{{SELLER_FEE}} × harga barang','{{SELLER_COMMISSION}}'],
    ['Bersih penjual','Harga barang dikurangi komisi','{{SELLER_NET}}'],
    ['Pendapatan platform','Biaya layanan ditambah komisi','{{PLATFORM_FEE}}'],
]), [
    'Hasil uji titik impas operasional pada skenario dasar adalah {{OPERATING_BEP}}. Pembacaan ini bergantung pada komposisi pesanan dan kontribusi yang berlaku pada periodenya. Pesanan yang dibatalkan atau dikembalikan penuh tidak menambah pendapatan jasa. Pilot menguji beban dukungan dan biaya yang tidak pulih pada pesanan gagal.'
]),
21: item('5.3 Pendapatan, laba dan arus kas',[
    'Laporan laba rugi memisahkan pendapatan transaksi dan B2B, biaya variabel, biaya tetap, penyusutan, dan pajak. Sementara itu, arus kas memasukkan waktu tagih, pembayaran, dan belanja modal. Perbedaan waktu ini menjelaskan mengapa kenaikan pendapatan belum tentu memperbaiki kas di bulan yang sama.',
    'Neraca mengikat posisi kas, aset operasi, utang usaha, dan ekuitas. Karena sumber pembiayaan yang dimodelkan adalah ekuitas, kas dari penerbitan saham menutup kebutuhan dana dan tidak memperbesar IRR proyek. Dana yang diteruskan ke penjual dan pengangkut tidak tersedia untuk operasi.',
], None, ('Ringkasan skenario dasar per periode', ['Ukuran','2027','2029','2036'],[
    ['Pesanan selesai','{{ORDERS_Y1}}','{{ORDERS_Y3}}','{{ORDERS_Y10}}'],
    ['GMV barang selesai','{{GMV_Y1}}','{{GMV_Y3}}','{{GMV_Y10}}'],
    ['Pendapatan marketplace','{{REV_Y1}}','{{SOM}}','{{REV_Y10}}'],
    ['Pendapatan B2B','{{B2B_Y1}}','{{B2B_Y3}}','{{B2B_Y10}}'],
    ['Laba bersih','{{NET_Y1}}','{{NET_Y3}}','{{NET_Y10}}'],
    ['Arus kas proyek','{{FCF_Y1}}','{{FCF_Y3}}','{{FCF_Y10}}'],
]), [
    'Tabel memakai rupiah nominal dan menunjukkan estimasi per tahun. Rincian biaya media mengikuti listing dan percobaan pemrosesan. Biaya tenaga kerja naik saat kapasitas perlu ditambah. Workbook memuat rekonsiliasi laba, penyusutan, modal kerja, belanja modal, dan kas.'
]),
22: item('5.4 Kebutuhan dana serta syarat pencairan',[
    'Modal pendiri dan pendanaan nondilutif menjadi opsi tahap persiapan. Pasokan terkonfirmasi, serah terima pertama, serta kemampuan mengatasi keluhan menentukan kesiapan pembiayaan berikutnya. Namun, hibah dan hadiah belum dianggap pasti dalam skenario dasar.',
    'Dana ditentukan dari saldo kas sebelum pendanaan, kebutuhan operasi sampai tahap berikutnya, dan cadangan. Sementara itu, pre-seed dan seed bergantung pada kapasitas dan bukti ekonomi pesanan. Ketika dana terlambat, tim menunda pembukaan klaster dan penambahan biaya yang belum perlu.',
], None, ('Jadwal pendanaan indikatif dari model', ['Tahap','Besaran skenario dasar','Penggunaan dan syarat'],[
    ['Persiapan','{{FUND_FOUNDER}}','Penyelesaian prototipe, verifikasi pemasok, uji pemenuhan'],
    ['Pre-seed','{{FUND_PRESEED}}','Dukungan, akuisisi, serta klaster berikut setelah uji'],
    ['Seed','{{FUND_SEED}}','Ekspansi bersyarat dengan biaya dan kapasitas teruji'],
    ['Akumulasi dana','{{FUND_TOTAL}}','Rp2,2924 miliar bersih setelah biaya pendanaan'],
]), [
    'Putaran merupakan kebutuhan indikatif, tanpa mengasumsikan investor sudah berkomitmen. Dilusi mengikuti harga masuk dan saham primer tiap tahap. Masukan valuasi tersaji terpisah dari kinerja operasi. Pada skenario pendanaan terbatas, keputusan yang dinilai adalah jeda ekspansi dan jarak menuju kekurangan kas.'
]),
23: item('5.5 Biaya ekuitas dan kelayakan proyek',[
    'Tingkat pengembalian minimum menggunakan CAPM rupiah nominal. Yield SBN menjadi titik awal, kemudian model mengoreksi risiko gagal bayar negara dan menambahkan premi pasar serta risiko negara secara terpisah. Karena utang pendanaan bernilai nol, WACC dalam struktur yang dimodelkan sama dengan biaya ekuitas.',
    'NPV dan IRR menggunakan arus kas setelah pajak sebelum pembiayaan. Tahun persiapan masuk sebagai arus kas awal dan horizon utama tidak memakai nilai terminal. Oleh karena itu, pencairan modal, dana milik penjual, dan estimasi valuasi putaran tidak menjadi manfaat proyek.',
], 'keuangan', ('Indikator kelayakan dasar', ['Ukuran','Hasil','Definisi operasional'],[
    ['WACC','{{WACC}}','Biaya ekuitas rupiah nominal'],
    ['NPV','{{NPV}}','Arus kas proyek terdiskonto sampai 2036'],
    ['IRR','{{IRR}}','Pengembalian proyek sebelum pembiayaan'],
    ['Balik modal','{{PAYBACK}}','Akumulasi arus kas nominal pertama kali menutup investasi'],
    ['IRR melebihi WACC','{{CROSSING}}','Akhir tahun pertama yang memenuhi kriteria'],
]), [
    'Proyeksi perlu dibaca bersama kebutuhan dana, kapasitas serah terima, dan kondisi skenario rendah. Faktor CAPM, vintage data, metode, serta sumber ditunjukkan dalam workbook. Lampiran E menghubungkan angka ini dengan area model yang dapat dihitung ulang.'
], label='Kelayakan proyek dalam skenario dasar'),
24: item('5.6 Skenario dan risiko pendanaan',[
    'Sensitivitas menggerakkan volume transaksi dan hasil per pesanan, dengan batas pasokan dan pemenuhan yang sama. Sementara itu, simulasi mengubah penggerak operasi sebelum membentuk arus kas. Skenario tidak diperoleh dengan memperbesar atau memperkecil NPV secara langsung.',
    'Pada skenario konservatif, pesanan dan kontribusi melemah sementara sebagian biaya tetap berjalan. Karena itu, penundaan pembukaan klaster dapat melindungi kas, walaupun pertumbuhan pendapatan ikut melambat. Uji keterlambatan pendanaan melihat apakah waktu rekrutmen dan perluasan perlu ditahan.',
], 'risk-chart', ('Kisaran hasil dan cara membaca', ['Ukuran','Hasil model','Keputusan'],[
    ['NPV konservatif','{{NPV_DOWNSIDE}}','Tinjau pengurangan biaya dan laju pembukaan klaster'],
    ['NPV dasar','{{NPV}}','Bandingkan dengan hasil pilot sebelum ekspansi'],
    ['NPV optimistis','{{NPV_UPSIDE}}','Pertahankan disiplin kapasitas dan pengendalian biaya'],
    ['Peluang NPV di atas nol','{{MC_PROB}}','Proporsi percobaan dalam asumsi model'],
    ['P5 / P50 / P95 NPV','{{MC_RANGE}}','Rentang model pada horizon evaluasi yang sama'],
]), [
    'Sebanyak 10.000 lintasan menguji variasi di sekitar skenario dasar. Skenario optimistis memadukan perubahan yang lebih luas daripada sebaran tersebut. Hasil simulasi berlaku untuk asumsi yang diuji. Ukuran ini belum dapat digunakan untuk memperkirakan frekuensi kejadian dari transaksi aktual.'
], label='Distribusi hasil proyeksi pada horizon 2036'),
25: item('5.7 Keputusan peluncuran dan kriteria perluasan',[
    'Mulai dengan katalog yang bisa diperiksa dan satu wilayah yang bisa dilayani. Penghuni kos harus tahu kondisi, ukuran, serta cara menerima barang dari satu penawaran. Sementara itu, reseller perlu melihat bahwa upaya menyiapkan bukti dapat memberi jalan ke serah terima yang lebih pasti.',
    'Pilot menguji kelengkapan penawaran, ketersediaan stok, transaksi selesai, biaya dan pengaduan. Karena itu, tim menunda ekspansi ketika kontribusi tertekan atau ketika tindak lanjut pengaduan melebihi kapasitas. Konten kreator dan Bursa Pindahan mengikuti kesiapan tersebut.',
    'Model menempatkan modal awal {{FUND_FOUNDER}}. Pada skenario dasar, persiapan dan enam bulan pilot menggunakan kas proyek Rp253,28 juta. Dengan cadangan Rp75 juta, kebutuhan indikatif fase uji sekitar Rp328,28 juta. Besaran aktual ditetapkan setelah biaya lokal diverifikasi. Prioritasnya katalog, dukungan transaksi, dan uji jalur angkut. Foto asli tetap tersedia saat 3D belum lolos penilaian mutu.',
], None, ('Keputusan yang diuji sebelum fase berikutnya', ['Keputusan','Bukti yang diminta','Jika hasil di bawah sasaran'],[
    ['Pertahankan katalog awal','Stok aktif, foto cacat, ukuran dan opsi penerimaan tersedia','Perbaiki data produk dan fokus kategori'],
    ['Naikkan pemasaran','Pesanan selesai dan biaya per pesanan dipantau','Periksa biaya angkut, kualitas, dan ketersediaan'],
    ['Buka klaster berikut','Staf, rute, pemasok, dan kas memenuhi syarat','Tunda promosi dan perekrutan tambahan'],
    ['Perluas B2B','Dokumentasi pemrosesan dan kapasitas dukungan memadai','Pertahankan pengujian internal dengan batas volume'],
]), [
    'Survei sisi pembeli sudah selesai. Penilaian pasokan, biaya aktual, dan kesediaan penjual masih memerlukan bukti lapangan. Langkah pertama yang dapat dievaluasi adalah menuntaskan pesanan di klaster kecil sambil mencatat kejadian dari pengajuan listing sampai penyelesaian dana.'
]),
}
