// A common expression registry drives the editable workbook and numerical risk engine.
export const notes = {
  assumption: "Asumsi perencanaan 26 Nov 2026. Ganti dengan bukti pilot atau penawaran aktual.",
  dp: "UI Depok; pemasok berulang dan penghuni pindahan. Kapasitas serta tarif belum dikontrak.",
  noSales: "Survei 60 respons dan prototipe mendukung rancangan; keduanya tidak mengukur volume penjualan.",
  funding: "Contoh kebutuhan dan batas pencairan indikatif. Dana ini belum menjadi komitmen.",
  price: "Skenario nilai transaksi furnitur bekas. Sesuaikan dengan kategori, kondisi dan negosiasi pilot.",
  infra: "Anggaran vendor indikatif. Jumlah direktori, retensi, retry, beban dan kurs merupakan asumsi model."
};
export const inputRows = [
  ["useShare", "Porsi belanja kategori untuk unit bekas", .014, .026, .043, "%", "Asumsi tanpa estimasi pasar terukur"],
  ["serviceShare", "Porsi pasar nasional yang memenuhi cakupan SAM", .075, .105, .135, "%", "Asumsi ekonomi dan jangkauan Jabodetabek"],
  ["listingInflation", "Eskalasi harga barang dan biaya platform", .02, .026, .035, "%", "Asumsi nominal tahunan"],
  ["costInflation", "Eskalasi gaji dan biaya non-personalia", .045, .035, .027, "%", "Asumsi nominal tahunan"],
  ["newDealer", "Penjual berulang baru per klaster per bulan", 1.4, 1.9, 2.4, "n", "Asumsi akuisisi pasokan; hubungi pemasok dalam pilot"],
  ["dealerChurn", "Penjual berulang tidak aktif per bulan", .145, .11, .08, "%", "Asumsi kohor penjual"],
  ["dealerListing", "Listing baru per penjual berulang aktif per bulan", 3.5, 4.5, 5.3, "n", "Asumsi produktivitas stok; satu listing per unit"],
  ["moveListing", "Listing pindahan per klaster per bulan", 22, 31, 40, "n", "Asumsi akuisisi penjual perorangan"],
  ["passRate", "Kelengkapan QC setelah satu pemeriksaan ulang", .80, .88, .93, "%", "Asumsi kelengkapan bukti"],
  ["qcRecheck", "Porsi listing yang dirujuk untuk pemeriksaan ulang", .30, .23, .18, "%", "Asumsi rework katalog, satu kali"],
  ["stockExpiry", "Penarikan dan listing kedaluwarsa per bulan", .23, .19, .16, "%", "Asumsi listing tidak laku atau ditarik"],
  ["sellableRate", "Porsi stok yang bisa terjual pada periode", .32, .39, .47, "%", "Asumsi keterjangkauan pasokan dan kecocokan"],
  ["reachPerCluster", "Prospek unik yang memenuhi kriteria per klaster per bulan", 700, 950, 1200, "n", "Asumsi jangkauan deduplikasi; survei bukan sumber volume"],
  ["bookRate", "Permintaan menjadi pesanan yang diajukan", .054, .079, .100, "%", "Asumsi operasional; dari prospek unik"],
  ["cancelRate", "Pembatalan sebelum serah terima", .11, .07, .05, "%", "Asumsi transaksi yang diajukan"],
  ["fullRefund", "Refund penuh dari serah terima", .025, .015, .009, "%", "Asumsi transaksi yang sudah diserahkan"],
  ["partialRefund", "Nilai refund parsial dibanding GMV selesai", .020, .010, .006, "%", "Asumsi koreksi nilai barang"],
  ["supportAlert", "Kasus tambahan pada transaksi yang diajukan", .14, .10, .07, "%", "Asumsi sengketa atau bantuan tambahan"],
  ["deliveryMix", "Porsi permintaan pengiriman", .57, .48, .40, "%", "Asumsi; sisanya jadwal ambil sendiri"],
  ["pickupSlots", "Slot ambil sendiri per klaster per bulan", 65, 81, 95, "n", "Asumsi jadwal yang siap dikonfirmasi"],
  ["deliverySlots", "Slot angkut per klaster per bulan", 38, 52, 64, "n", "Asumsi kapasitas pihak ketiga sebelum konfirmasi"],
  ["deliveryAsk", "Nilai angkut pass-through dalam keranjang saat dikirim", .120, .100, .090, "Rp jt", "Acuan historis pickup Depok dan variasi jarak; tarif aktual harus dikutip"],
  ["buyerFee", "Biaya layanan pembeli per pesanan", .014, .018, .021, "Rp jt", "Usulan tarif, bukan willingness to pay"],
  ["commission", "Komisi penjual atas harga unit setelah pengembalian", .049, .065, .075, "%", "Usulan tarif platform"],
  ["tablePrice", "Nilai transaksi meja", .247, .29575, .324, "Rp jt", "Median 10 tawaran OLX Depok Rp0,325 jt; skenario realisasi"],
  ["chairPrice", "Nilai transaksi kursi", .285, .34125, .374, "Rp jt", "Median 5 tawaran OLX Depok Rp0,375 jt; skenario realisasi"],
  ["rackPrice", "Nilai transaksi rak", .247, .29575, .324, "Rp jt", "Median 4 tawaran OLX Depok Rp0,325 jt; skenario realisasi"],
  ["cabinetPrice", "Nilai transaksi lemari", .684, .819, .899, "Rp jt", "Median 5 tawaran OLX Depok Rp0,9 jt; skenario realisasi"],
  ["tableMix", "Porsi meja", .27, .27, .27, "%", "Komposisi pesanan ilustratif"],
  ["chairMix", "Porsi kursi", .30, .30, .30, "%", "Komposisi pesanan ilustratif"],
  ["rackMix", "Porsi rak", .18, .18, .18, "%", "Komposisi pesanan ilustratif; lemari = sisa"],
  ["gwVa", "Porsi virtual account", .40, .32, .25, "%", "Asumsi pilihan pembayaran; sisanya QRIS"],
  ["gwCard", "Porsi kartu", .095, .07, .04, "%", "Asumsi pilihan pembayaran; sisanya QRIS"],
  ["vaFee", "Biaya gateway VA per transaksi", .004, .004, .004, "Rp jt", "Acuan publik Midtrans; cek kelas merchant"],
  ["cardFixed", "Biaya kartu tetap per transaksi", .002, .002, .002, "Rp jt", "Acuan publik Midtrans"],
  ["cardRate", "Tarif kartu", .029, .029, .029, "%", "Acuan publik Midtrans"],
  ["qrisFee", "Tarif QRIS", .007, .007, .007, "%", "Acuan publik Midtrans"],
  ["payoutFee", "Tarik dana standar ke bank", .005, .005, .005, "Rp jt", "Acuan publik Midtrans; model payout berkelompok"],
  ["payTax", "Faktor biaya pajak penyedia", 1.11, 1.11, 1.11, "x", "Anggaran gross-up indikatif bila belum termasuk pajak"],
  ["batchSize", "Pesanan per payout pada rata-rata bauran penjual", 1.8, 2.8, 4, "n", "Asumsi agregasi payout"],
  ["qcMinutes", "Menit QC per percobaan", 8.0, 6.0, 5.0, "menit", "Asumsi target, perlu ukur pilot"],
  ["supportMinutes", "Menit dukungan inti per pesanan yang diajukan", 14, 11, 9, "menit", "Asumsi target + penanganan tambahan pengecualian"],
  ["effectiveMinutes", "Menit kerja efektif per FTE bulanan", 6700, 7200, 7600, "menit", "Jam kerja produktif setelah jeda dan tugas lain"],
  ["maxQcByCluster", "FTE QC maksimum yang bisa dialokasikan per klaster", .16, .21, .25, "FTE", "Rencana kapasitas personel"],
  ["maxSupportByCluster", "FTE dukungan maksimum per klaster", .19, .25, .30, "FTE", "Rencana kapasitas personel"],
  ["entryPayroll", "Gaji dasar QC dan dukungan per FTE", 5.95, 5.75, 5.60, "Rp jt", "Lantai UMK Depok 2026 Rp5,522662 jt; asumsi penawaran tim"],
  ["techPayroll", "Gaji teknis per FTE", 13.0, 11.5, 10.5, "Rp jt", "Anggaran peran teknis, bukan penawaran kontraktor"],
  ["payBurden", "Cadangan THR dan beban pemberi kerja", .22, .20, .18, "%", "Anggaran gabungan; rincian payroll harus divalidasi"],
  ["founderPay", "Imbalan pendiri awal bulanan", 6.5, 6.0, 5.6, "Rp jt", "Asumsi; bertahap menjadi biaya kerja tetap"],
  ["eventCost", "Paket acara Bursa per pelaksanaan", 19, 15, 12, "Rp jt", "Asumsi sewa, petugas, materi, dan angkut contoh"],
  ["eventOrders", "Pesanan selesai teratribusikan per Bursa", 20, 36, 50, "n", "Batas target 30 hari, sudah termasuk pesanan reguler total"],
  ["acquisition", "Anggaran promosi lokal per klaster per bulan", .75, .65, .55, "Rp jt", "Asumsi distribusi komunitas/kreator; CAC dihitung dari target"],
  ["sellerVisitCost", "Biaya akuisisi satu pemasok berulang baru", .075, .060, .050, "Rp jt", "Asumsi verifikasi dan onboarding"],
  ["infraBase", "Hosting/database dasar bulanan", 2.2, 1.7, 1.35, "Rp jt", "Paket vendor dan observabilitas ilustratif"],
  ["localSpend", "Operasi lokal per klaster per bulan", .72, .58, .49, "Rp jt", "Asumsi administrasi dan kunjungan lapangan"],
  ["adminMonthly", "Legal, penagihan dan administrasi dasar bulanan", 3.5, 2.8, 2.4, "Rp jt", "Asumsi PT noninventori"],
  ["scanMix", "Bagian listing baru yang masuk antrian 3D", .11, .12, .14, "%", "Asumsi pilihan seller; foto cukup untuk publikasi"],
  ["scanRetry", "Percobaan tambahan rata-rata per job", .45, .28, .16, "%", "Asumsi; hasil satu kursi tidak mengukur tingkat retry"],
  ["cloudPerHour", "Anggaran komputasi per jam", .016, .012, .009, "Rp jt", "Estimasi paket komputasi atas dasar kurs dan biaya penyedia"],
  ["gpuMinutes", "Menit per percobaan terlepas dari antrean", 12, 9, 7, "menit", "Asumsi operasi dengan overhead; satu benda diuji"],
  ["gpuUtil", "Fraksi jam komputasi yang efektif", .50, .63, .75, "%", "Asumsi utilisasi/overhead"],
  ["imgGB", "Ukuran foto dan bukti per listing", .025, .020, .016, "GB", "Asumsi file terkompresi"],
  ["scanGB", "Ukuran input video + output per job", .100, .080, .060, "GB", "Asumsi per job; termasuk video sumber"],
  ["keepMedia", "Retensi ekuivalen media per listing", 8, 6, 5, "bulan", "Asumsi penghapusan dan retensi bukti"],
  ["storageFee", "Objek media per GB-bulan", .00030, .00026, .00024, "Rp jt", "R2 Standard US$0,015/GB-bulan, anggaran IDR"],
  ["requestsCost", "Traffic dan permintaan per listing", .00032, .00024, .00017, "Rp jt", "Asumsi pemrosesan CDN/gateway; bukan klaim gratis"],
  ["b2bStart", "Bulan layanan katalog B2B mulai", 46, 32, 28, "bulan", "Asumsi setelah alur media serta dukungan stabil"],
  ["b2bRate", "Langganan katalog per bisnis per bulan", .26, .36, .49, "Rp jt", "Usulan tarif tanpa bukti kemauan bayar; API tidak ditagih"],
  ["b2bAdds", "Pelanggan B2B baru per klaster per bulan", .10, .21, .31, "n", "Asumsi mode katalog berlangganan"],
  ["b2bChurn", "Churn B2B bulanan", .09, .065, .05, "%", "Asumsi dari pelanggan aktif"],
  ["b2bUnitCost", "Biaya kuota media dan dukungan B2B per akun", .15, .12, .10, "Rp jt", "Kuota dan biaya dukungan terpisah"],
  ["settlementDays", "Hari penerimaan biaya platform", 6, 3, 2, "hari", "Asumsi interval settlement"],
  ["payableDays", "Hari termin biaya penyedia", 8, 12, 16, "hari", "Asumsi biaya eksternal; gaji dibayar bulan berjalan"],
  ["shortPrepay", "Setara bulan belanja SaaS dibayar sebelumnya", 1.25, 1, .75, "bulan", "Asumsi saldo prepaid layanan"],
  ["prepExp", "Belanja persiapan yang langsung dibebankan", 58, 49, 43, "Rp jt", "Anggaran riset pilot, pengembangan dan legal"],
  ["prepCapex", "Aset dan perangkat awal", 36, 32, 29, "Rp jt", "Perangkat kerja yang memenuhi pengakuan, bukan seluruh R&D"],
  ["capexCluster", "Perangkat kerja tambahan saat membuka klaster", 3.3, 2.7, 2.2, "Rp jt", "Asumsi biaya setup tanpa pembelian stok"],
  ["capexReplacement", "Perangkat pengganti per klaster per tahun mulai tahun 4", 1.25, 1.05, .95, "Rp jt", "Asumsi pengadaan peralatan tahunan"],
  ["founderEquity", "Setoran pendiri yang direncanakan", 430, 430, 430, "Rp jt", "Asumsi batas pendanaan. Belum didanai."],
  ["preSeedEquity", "Batas dana ekuitas primer pre-seed", 820, 820, 820, "Rp jt", "Asumsi batas tahap. Tidak dijamin."],
  ["seedEquity", "Batas dana ekuitas primer seed", 1100, 1100, 1100, "Rp jt", "Asumsi batas tahap bila kas dibutuhkan."],
  ["grant", "Hibah atau hadiah yang dimasukkan", 0, 0, 0, "Rp jt", "Belum committed; kasus utama tanpa hibah"],
  ["fundingDelay", "Penundaan pertama pencairan lanjutan", 3, 0, 0, "bulan", "Ubah angka; diletakkan sebelum dukungan putaran berikutnya"],
  ["preSeedMonth", "Bulan pertama layak untuk pre-seed", 8, 8, 8, "bulan", "Tergantung volume terukur setelah fase 1"],
  ["seedMonth", "Bulan pertama layak untuk seed", 19, 19, 19, "bulan", "Tergantung pembuktian fase 2"],
  ["minOrdersPre", "Pesanan satu bulan untuk milestone pre-seed", 18, 18, 18, "n", "Sasaran indikator, bukan pencapaian"],
  ["minOrdersSeed", "Pesanan satu bulan untuk milestone seed", 70, 70, 70, "n", "Sasaran yang perlu divalidasi"],
  ["minClusterOrders", "Target satu klaster sebelum membuka berikutnya", 22, 22, 22, "n", "Tentukan ulang dari kohor pilot"],
  ["triggerCash", "Minimum kas untuk izin membuka klaster tambahan", 75, 75, 75, "Rp jt", "Buffer peluncuran"],
  ["preSeedVal", "Valuasi pre-money indikatif pre-seed", 4400, 4400, 4400, "Rp jt", "Hipotesis negosiasi saat pilot terbukti; bukan valuasi yang ditetapkan"],
  ["seedVal", "Valuasi pre-money indikatif seed", 10200, 10200, 10200, "Rp jt", "Hipotesis uplift bersyarat jika replikasi berjalan"],
  ["fundFee", "Biaya penghimpunan ekuitas luar", .035, .03, .025, "%", "Asumsi legal/admin per putaran; tidak dalam FCFF"],
  ["taxRate", "PPh Badan umum sebelum fasilitas", .22, .22, .22, "%", "DJP, tarif normal badan 22%; PT biasa"],
  ["smallTaxCut", "Reduksi tarif Pasal 31E pada bagian yang memenuhi", .50, .50, .50, "%", "DJP, reduksi 50% atas bagian peredaran yang memenuhi"],
  ["smallTaxFloor", "Peredaran bruto untuk bagian tarif tereduksi", 4800, 4800, 4800, "Rp jt", "DJP Pasal 31E"],
  ["smallTaxLimit", "Peredaran bruto ambang fasilitas", 50000, 50000, 50000, "Rp jt", "DJP Pasal 31E"],
  ["sbnYield", "Yield SBN IDR tenor 10 tahun", .07696, .07696, .07696, "%", "Penutupan 25 Nov 2026, seri benchmark Indonesia 10Y"],
  ["defaultSpread", "Sovereign default spread Indonesia", .0152, .0152, .0152, "%", "Damodaran, Jul 2026, Baa2"],
  ["matureErp", "Premi ekuitas pasar matang", .0420, .0420, .0420, "%", "Damodaran, Jul 2026"],
  ["countryRisk", "Premi risiko negara Indonesia", .0236, .0236, .0236, "%", "Damodaran, Jul 2026"],
  ["marketBeta", "Beta levered publik industri Software (Internet)", 1.39, 1.39, 1.39, "x", "Damodaran Global Jan 2026, 150 perusahaan"],
  ["marketDebt", "Rasio utang/ekuitas industri Software (Internet)", .1001, .1001, .1001, "%", "Damodaran Global Jan 2026"],
  ["marketTax", "Tarif marjinal basis unlever beta dataset", .2537, .2537, .2537, "%", "Damodaran Global Jan 2026"],
  ["lambda", "Eksposur risiko negara", 1, 1, 1, "x", "Asumsi fokus Indonesia"],
  ["population", "Proyeksi penduduk nasional pertengahan tahun", 287198400, 287198400, 287198400, "orang", "BPS, 2026"],
  ["furnitureSpend", "Pengeluaran bulanan mebel per kapita", .003376, .003376, .003376, "Rp jt", "BPS, Susenas Maret 2026 Tabel 3.4"],
];

export const defaultInputs = Object.fromEntries(inputRows.map(([key,,down,base,up]) => [key,{Downside:down,Base:base,Upside:up}]));
export const clusterPlan = [2,4,8,13,19,26,34,43,52,60];
export const defaults = {...defaultInputs, clusterPlan, sourceDate:"2026-11-26"};

export const functions = {
  min: Math.min, max:Math.max, power:Math.pow, mod:(x,y)=>x%y,
  and:(...xs)=>xs.every(Boolean), or:(...xs)=>xs.some(Boolean),
  floor:Math.floor, round:(x,y=0)=>Math.round(x*10**y)/10**y,
  roundUp:(x,y=0)=>Math.ceil(x*10**y)/10**y,
  iff:(x,a,b)=>x?a:b, abs:Math.abs, safe:(x,y)=>y?x/y:0
};

// The expressions use a (inputs), p (previous month), z (current month) and c (period or overrides).
export const fields = [
  ["preGross", "Pre-seed bruto", "Rp jt", "iff(and(c.allowFunding==1,c.m>0,c.m>=a.preSeedMonth+a.fundingDelay,p.preTaken==0,p.orders>=a.minOrdersPre,p.cash<a.triggerCash*3),a.preSeedEquity,0)"],
  ["seedGross", "Seed bruto", "Rp jt", "iff(and(c.allowFunding==1,c.m>0,c.m>=a.seedMonth+a.fundingDelay,p.seedTaken==0,p.orders>=a.minOrdersSeed,p.cash<a.triggerCash*6,or(p.preTaken==1,z.preGross>0)),a.seedEquity,0)"],
  ["preTaken", "Pre-seed cair kumulatif", "flag", "min(1,p.preTaken+iff(z.preGross>0,1,0))"],
  ["seedTaken", "Seed cair kumulatif", "flag", "min(1,p.seedTaken+iff(z.seedGross>0,1,0))"],
  ["founderGross", "Modal pendiri bruto", "Rp jt", "iff(c.m==0,a.founderEquity,0)"],
  ["grant", "Hibah skenario", "Rp jt", "iff(c.m==0,a.grant,0)"],
  ["funding", "Pendanaan bersih", "Rp jt", "z.founderGross+z.grant+(z.preGross+z.seedGross)*(1-a.fundFee)"],
  ["clusters", "Klaster layanan aktif", "n", "iff(c.m==0,0,iff(c.m==1,1,iff(and(p.cash+z.funding>=a.triggerCash,p.orders>=max(1,p.clusters)*a.minClusterOrders),min(max(p.clusters,c.plan),p.clusters+1),p.clusters)))"],
  ["stockBegin", "Stok jual awal", "n", "p.stockEnd"],
  ["newDealer", "Pemasok rutin baru", "n", "z.clusters*a.newDealer*c.seller"],
  ["repeatDealer", "Pemasok rutin dari kohor sebelumnya", "n", "p.dealer*(1-a.dealerChurn)"],
  ["dealer", "Pemasok rutin aktif", "n", "z.newDealer+z.repeatDealer"],
  ["event", "Jumlah Bursa Pindahan pada bulan ini", "n", "iff(and(c.m>=19,c.bursa==1,z.clusters>=3,p.cash+z.funding>=a.triggerCash),max(1,floor(z.clusters/14)),0)"],
  ["moveListing", "Listing penghuni pindahan", "n", "z.clusters*a.moveListing*c.season+z.event*22"],
  ["intake", "Listing unit unik masuk", "n", "z.dealer*a.dealerListing+z.moveListing"],
  ["qcFte", "FTE katalog dan pemeriksaan", "FTE", "iff(z.clusters==0,0,min(max(.5,z.clusters*a.maxQcByCluster),max(.5,roundUp(z.intake*a.qcMinutes*(1+a.qcRecheck)/a.effectiveMinutes*4,0)/4)))"],
  ["qcCapacity", "Kapasitas pemeriksaan listing bulanan", "n", "floor(z.qcFte*a.effectiveMinutes/(a.qcMinutes*(1+a.qcRecheck)))"],
  ["qcProcessed", "Listing diperiksa", "n", "floor(min(z.intake+p.qcBacklog,z.qcCapacity))"],
  ["qcBacklog", "Listing belum diperiksa", "n", "max(0,z.intake+p.qcBacklog-z.qcProcessed)"],
  ["listingPassed", "Listing terbit setelah pemeriksaan", "n", "floor(z.qcProcessed*a.passRate)"],
  ["eligible", "Stok tersedia", "n", "z.stockBegin+z.listingPassed"],
  ["supply", "Batas dari unit layak terjual", "n", "floor(z.eligible*a.sellableRate)"],
  ["demand", "Permintaan checkout yang memenuhi", "n", "floor((z.clusters*a.reachPerCluster*c.season*a.bookRate+z.event*a.eventOrders*.75)*c.demand)"],
  ["supportFte", "FTE dukungan pesanan", "FTE", "iff(z.clusters==0,0,min(max(.5,z.clusters*a.maxSupportByCluster),max(.5,roundUp(min(z.demand,z.supply)*a.supportMinutes*(1+a.supportAlert)/a.effectiveMinutes*4,0)/4)))"],
  ["supportCap", "Kapasitas staf pesanan", "n", "floor(z.supportFte*a.effectiveMinutes/(a.supportMinutes*(1+a.supportAlert)))"],
  ["pickupCap", "Slot ambil sendiri", "n", "floor(a.pickupSlots*z.clusters)"],
  ["deliveryCap", "Slot pengiriman kurir", "n", "floor(a.deliverySlots*z.clusters)"],
  ["booking", "Pesanan dibuat, sebelum batal/refund", "n", "floor(min(z.supply,z.demand,z.supportCap,z.pickupCap/max(.001,1-a.deliveryMix),z.deliveryCap/max(.001,a.deliveryMix)))"],
  ["cancels", "Pesanan batal", "n", "z.booking*(1-max(0,min(.99,(1-a.cancelRate)*c.completion)))"],
  ["full", "Refund penuh setelah serah terima", "n", "(z.booking-z.cancels)*a.fullRefund"],
  ["orders", "Pesanan selesai neto", "n", "max(0,floor(z.booking-z.cancels-z.full))"],
  ["expired", "Stok penarikan/kedaluwarsa", "n", "floor((z.eligible-z.orders)*a.stockExpiry)"],
  ["stockEnd", "Stok akhir", "n", "z.eligible-z.orders-z.expired"],
  ["eventSales", "Pesanan Bursa dalam jendela 30 hari", "n", "min(z.orders,z.event*a.eventOrders)"],
  ["aov", "Nilai barang setara sebelum refund sebagian", "Rp jt", "(a.tablePrice*a.tableMix+a.chairPrice*a.chairMix+a.rackPrice*a.rackMix+a.cabinetPrice*(1-a.tableMix-a.chairMix-a.rackMix))*c.aov*power(1+a.listingInflation,max(0,c.y-1))"],
  ["gmv", "GMV neto barang", "Rp jt", "z.orders*z.aov*(1-a.partialRefund)"],
  ["buyerRevenue", "Biaya layanan pembeli", "Rp jt", "z.orders*a.buyerFee*c.fee*power(1+a.listingInflation,max(0,c.y-1))"],
  ["sellerRevenue", "Komisi penjual", "Rp jt", "z.gmv*a.commission*c.fee"],
  ["marketplaceRevenue", "Pendapatan marketplace", "Rp jt", "z.buyerRevenue+z.sellerRevenue"],
  ["delivery", "Pengiriman sebagai dana lewat", "Rp jt", "z.orders*a.deliveryMix*a.deliveryAsk"],
  ["checkout", "Total nilai yang diproses gateway", "Rp jt", "z.booking*(z.aov+a.buyerFee*c.fee*power(1+a.listingInflation,max(0,c.y-1))+a.deliveryMix*a.deliveryAsk)"],
  ["releaseB2B", "Status kelayakan katalog B2B", "flag", "iff(or(p.releaseB2B==1,and(c.m>=a.b2bStart,c.m>0,z.clusters>=4,p.cash+z.funding>=a.triggerCash)),1,0)"],
  ["b2b", "Akun katalog B2B aktif", "n", "iff(z.releaseB2B==1,p.b2b*(1-a.b2bChurn)+z.clusters*a.b2bAdds,0)"],
  ["b2bRevenue", "Pendapatan langganan B2B", "Rp jt", "z.b2b*a.b2bRate*power(1+a.listingInflation,max(0,c.y-1))"],
  ["revenue", "Pendapatan usaha", "Rp jt", "z.marketplaceRevenue+z.b2bRevenue"],
  ["scanN", "Job 3D pada listing terbit", "n", "z.listingPassed*a.scanMix"],
  ["scanTries", "Percobaan termasuk retry", "n", "z.scanN*(1+a.scanRetry)"],
  ["gpuHours", "Jam komputasi tertagih", "jam", "z.scanTries*a.gpuMinutes/60/a.gpuUtil"],
  ["mediaStored", "GB disimpan pada akhir bulan", "GB", "max(0,p.mediaStored*(1-1/max(1,a.keepMedia)))+z.scanN*a.scanGB+z.listingPassed*a.imgGB"],
  ["media", "Biaya konten, simpan dan komputasi", "Rp jt", "(z.listingPassed*a.requestsCost+z.gpuHours*a.cloudPerHour+z.mediaStored*a.storageFee)*c.cost"],
  ["payCost", "Gateway, biaya refund dan payout", "Rp jt", "(z.booking*(a.gwVa*a.vaFee+a.gwCard*a.cardFixed)+z.checkout*(a.gwCard*a.cardRate+(1-a.gwCard-a.gwVa)*a.qrisFee)+roundUp(z.orders/max(1,a.batchSize),0)*a.payoutFee)*a.payTax*c.cost"],
  ["b2bCost", "Kuota dan dukungan B2B", "Rp jt", "z.b2b*a.b2bUnitCost*c.cost"],
  ["salariesDirect", "Tenaga katalog dan dukungan", "Rp jt", "(z.qcFte+z.supportFte)*a.entryPayroll*(1+a.payBurden)*power(1+a.costInflation,max(0,c.y-1))*c.cost"],
  ["contribution", "Kontribusi marketplace sebelum akuisisi", "Rp jt", "z.marketplaceRevenue-z.media-z.payCost-z.salariesDirect"],
  ["marketing", "Kampanye, pemasok dan Bursa", "Rp jt", "((z.clusters*a.acquisition*iff(c.m<7,1,1.2))+z.newDealer*a.sellerVisitCost+z.event*a.eventCost)*power(1+a.costInflation,max(0,c.y-1))*c.cost"],
  ["contributionAfter", "Kontribusi marketplace setelah akuisisi", "Rp jt", "z.contribution-z.marketing"],
  ["techFte", "FTE teknologi dan pemeliharaan", "FTE", "iff(z.clusters==0,0,.75+floor(z.clusters/9)*.5)"],
  ["fixed", "Personalia tetap, hosting dan operasi lokal", "Rp jt", "iff(c.m==0,a.prepExp,(z.techFte*a.techPayroll*(1+a.payBurden)+a.founderPay+a.infraBase+a.adminMonthly+z.clusters*a.localSpend)*power(1+a.costInflation,max(0,c.y-1)))*c.cost"],
  ["ebitda", "EBITDA", "Rp jt", "z.contributionAfter+z.b2bRevenue-z.b2bCost-z.fixed"],
  ["capex", "Belanja aset", "Rp jt", "iff(c.m==0,a.prepCapex,max(0,z.clusters-p.clusters)*a.capexCluster+iff(and(c.y>=4,c.mo==12),a.capexReplacement*z.clusters,0))*power(1+a.costInflation,max(0,c.y-1))*c.capex"],
  ["assetSum", "Belanja aset kumulatif", "Rp jt", "p.assetSum+z.capex"],
  ["da", "Penyusutan perangkat 36 bulan", "Rp jt", "iff(c.m==0,0,(p.assetSum-c.capexPast)/36)"],
  ["ppene", "Aset tetap bersih", "Rp jt", "p.ppene+z.capex-z.da"],
  ["ebit", "Laba operasi", "Rp jt", "z.ebitda-z.da"],
  ["yEbit", "Laba operasi kumulatif tahun berjalan", "Rp jt", "z.ebit+iff(c.mo==1,0,p.yEbit)"],
  ["yRevenue", "Pendapatan kumulatif tahun berjalan", "Rp jt", "z.revenue+iff(c.mo==1,0,p.yRevenue)"],
  ["offsetOldest", "Kompensasi rugi dari tahun tertua", "Rp jt", "iff(c.close==1,min(p.loss5,max(0,z.yEbit)),0)"],
  ["offsetFour", "Kompensasi rugi tahun keempat", "Rp jt", "iff(c.close==1,min(p.loss4,max(0,z.yEbit-z.offsetOldest)),0)"],
  ["offsetThree", "Kompensasi rugi tahun ketiga", "Rp jt", "iff(c.close==1,min(p.loss3,max(0,z.yEbit-z.offsetOldest-z.offsetFour)),0)"],
  ["offsetTwo", "Kompensasi rugi tahun kedua", "Rp jt", "iff(c.close==1,min(p.loss2,max(0,z.yEbit-z.offsetOldest-z.offsetFour-z.offsetThree)),0)"],
  ["offsetOne", "Kompensasi rugi tahun lalu", "Rp jt", "iff(c.close==1,min(p.loss1,max(0,z.yEbit-z.offsetOldest-z.offsetFour-z.offsetThree-z.offsetTwo)),0)"],
  ["loss1", "Rugi fiskal tersedia, umur 1 tahun", "Rp jt", "iff(c.close==1,max(0,-z.yEbit),p.loss1)"],
  ["loss2", "Rugi fiskal tersedia, umur 2 tahun", "Rp jt", "iff(c.close==1,p.loss1-z.offsetOne,p.loss2)"],
  ["loss3", "Rugi fiskal tersedia, umur 3 tahun", "Rp jt", "iff(c.close==1,p.loss2-z.offsetTwo,p.loss3)"],
  ["loss4", "Rugi fiskal tersedia, umur 4 tahun", "Rp jt", "iff(c.close==1,p.loss3-z.offsetThree,p.loss4)"],
  ["loss5", "Rugi fiskal tersedia, umur 5 tahun", "Rp jt", "iff(c.close==1,p.loss4-z.offsetFour,p.loss5)"],
  ["tax", "Pajak dibayar, perkiraan PPh badan", "Rp jt", "iff(c.close==1,a.taxRate*(1-iff(and(z.yRevenue<=a.smallTaxLimit,z.yRevenue>0),a.smallTaxCut*min(1,a.smallTaxFloor/max(.001,z.yRevenue)),0))*max(0,z.yEbit-z.offsetOldest-z.offsetFour-z.offsetThree-z.offsetTwo-z.offsetOne),0)"],
  ["earnings", "Laba bersih", "Rp jt", "z.ebit-z.tax"],
  ["ar", "Piutang biaya marketplace", "Rp jt", "z.marketplaceRevenue*a.settlementDays/30"],
  ["prepaid", "Pembayaran dimuka SaaS", "Rp jt", "iff(z.clusters>0,a.infraBase*a.shortPrepay*power(1+a.costInflation,max(0,c.y-1)),0)"],
  ["ap", "Utang biaya pihak ketiga", "Rp jt", "(z.payCost+z.b2bCost+z.marketing+z.media)*a.payableDays/30"],
  ["deferred", "Pendapatan B2B diterima dimuka", "Rp jt", "z.b2bRevenue*(2-mod(max(1,c.m)-1,3))"],
  ["nwc", "Modal kerja operasi nonkas", "Rp jt", "z.ar+z.prepaid-z.ap-z.deferred"],
  ["deltaNwc", "Perubahan modal kerja", "Rp jt", "z.nwc-p.nwc"],
  ["opCash", "Kas kegiatan operasi", "Rp jt", "z.earnings+z.da-z.deltaNwc"],
  ["fcff", "Arus kas proyek setelah pajak", "Rp jt", "z.opCash-z.capex"],
  ["cash", "Kas bebas setelah pembiayaan", "Rp jt", "p.cash+z.fcff+z.funding"],
  ["freeCash", "Kas kumulatif tanpa pembiayaan", "Rp jt", "p.freeCash+z.fcff"],
  ["fundingGap", "Kekurangan kas terhadap buffer", "Rp jt", "max(0,a.triggerCash-z.cash)"],
  ["equity", "Setoran ekuitas neto kumulatif", "Rp jt", "p.equity+z.funding"],
  ["retained", "Saldo laba ditahan", "Rp jt", "p.retained+z.earnings"],
  ["suspense", "Dana titipan angkutan dan penjual di penyedia", "Rp jt", "(z.gmv-z.sellerRevenue+z.delivery)*a.settlementDays/30"],
  ["assets", "Total aset", "Rp jt", "z.cash+z.ar+z.prepaid+z.ppene+z.suspense"],
  ["liabEquity", "Liabilitas dan ekuitas", "Rp jt", "z.ap+z.deferred+z.suspense+z.equity+z.retained"],
  ["checkBS", "Cek neraca", "Rp jt", "z.assets-z.liabEquity"],
  ["checkStock", "Cek roll-forward stok", "n", "z.stockEnd-z.stockBegin-z.listingPassed+z.orders+z.expired"],
];

const compiled = fields.map(([k,,,s]) => [k,new Function("a","p","z","c",`const {min,max,power,mod,and,or,floor,round,roundUp,iff,abs,safe}=this;return ${s};`).bind(functions)]);
export const emptyPeriod = Object.fromEntries(fields.map(([k]) => [k,0]));
export const years = Array.from({length:11},(_,i)=>2026+i);
export const rollups = new Set("preGross seedGross founderGross grant funding newDealer event moveListing intake qcCapacity qcProcessed listingPassed supply demand supportCap pickupCap deliveryCap booking cancels full orders expired eventSales gmv buyerRevenue sellerRevenue marketplaceRevenue delivery checkout b2bRevenue revenue scanN scanTries gpuHours media payCost b2bCost salariesDirect contribution marketing contributionAfter fixed ebitda capex da ebit tax earnings deltaNwc opCash fcff".split(" "));
export function periodMeta(m, plan=clusterPlan, scale=1) {
  const y = m ? Math.ceil(m/12) : 0;
  const mo = m ? (m-1)%12+1 : 12;
  const p = y<3 ? (m===0?0:Math.ceil(m/6)) : plan[y-1];
  return {m,y,mo,year:2026+y,close:+(mo===12),bursa:+(mo===2||mo===8),
    plan:Math.max(y?1:0,Math.floor(p*scale)),
    season:({1:1.12,2:1.13,6:1.17,7:1.25,8:1.21,12:.94})[mo]??.90};
}
export function discount(inputs,caseName="Base") {
  const get=k=>inputs[k][caseName];
  return get("sbnYield")-get("defaultSpread")+get("marketBeta")/(1+(1-get("marketTax"))*get("marketDebt"))*get("matureErp")+get("lambda")*get("countryRisk");
}
export const npvAt=(cash,rate)=>cash.reduce((v,cf,i)=>v+cf/(1+rate)**i,0);
export function irrAt(cash) {
  let last=0, changes=0;
  for (const x of cash) { const sign=Math.sign(x); if(sign){if(last&&last!==sign)changes++;last=sign;} }
  if(changes!==1)return {irr:null,status:changes>1?"Tanda CF >1":"Tanpa perubahan tanda"};
  let lo=-.95, hi=1;
  let low=npvAt(cash,lo), high=npvAt(cash,hi);
  while(low*high>0&&hi<64){hi*=2;high=npvAt(cash,hi);}
  if(low*high>0)return {irr:null,status:"Akar di luar rentang"};
  for(let j=0;j<36;j++){const mid=(lo+hi)/2;const m=npvAt(cash,mid);if(low*m<=0){hi=mid;high=m;}else{lo=mid;low=m;}}
  return {irr:(lo+hi)/2,status:"Tersedia"};
}
export const paybackAt=(cash,rate=0)=>{
  let cumulative=0;
  for(let i=0;i<cash.length;i++){const period=cash[i]/(1+rate)**i;const previous=cumulative;cumulative+=period;if(i&&previous<0&&cumulative>=0)return i-1-previous/period;}
  return null;
};
export function market(a) {
  const benchmark=a.population*a.furnitureSpend*12;
  const aov=a.tablePrice*a.tableMix+a.chairPrice*a.chairMix+a.rackPrice*a.rackMix+a.cabinetPrice*(1-a.tableMix-a.chairMix-a.rackMix);
  const netGmv=benchmark*a.useShare;
  const revenue=netGmv/aov*a.buyerFee+netGmv*a.commission;
  return {benchmark,aov,gmv:netGmv,tam:revenue,sam:revenue*a.serviceShare};
}
export function evaluate(inputs=defaults, options={}) {
  const k = options.caseName??"Base";
  const multipliers = options.multipliers??{};
  const a = Object.fromEntries(inputRows.map(([key])=>[key,inputs[key][k]]));
  const annual=[];
  const periods=[];
  const weights = {seller:1,demand:1,fee:1,aov:1,cost:1,completion:1,capex:1,...multipliers};
  const clusterScale = k==="Downside"?.8:k==="Upside"?1.15:1;
  let prev=emptyPeriod;
  let aggregate={};
  let cashMin=Infinity, cashMinUnfunded=Infinity, fundingGap=0, verify=0;
  let totalEquity=0;
  const months=Math.min(120, Math.max(0,(options.horizon??2036)-2026)*12);
  for(let m=0;m<=months;m++) {
    const meta=periodMeta(m,inputs.clusterPlan??clusterPlan,clusterScale);
    const c={...meta,allowFunding:options.allowFunding===false?0:1,...weights,
      capex:weights.capex,capexPast:m>36 ? (options.compact?previousAssets[m-37]:periods[m-37].assetSum):0};
    const z={...meta};
    for(const [id,expr] of compiled)z[id]=expr(a,prev,z,c);
    for(const k of rollups)aggregate[k]=(aggregate[k]??0)+z[k];
    if(options.compact)previousAssets[m]=z.assetSum;
    else periods.push(z);
    prev=z;
    cashMin=Math.min(cashMin,z.cash);
    cashMinUnfunded=Math.min(cashMinUnfunded,z.freeCash);
    fundingGap=Math.max(fundingGap,z.fundingGap);
    totalEquity+=z.funding;
    verify=Math.max(verify,Math.abs(z.checkBS),Math.abs(z.checkStock));
    if(meta.close){const record={...z,...aggregate};
      record.unitContribution=record.orders?record.contribution/record.orders:null;
      record.unitAfter=record.orders?record.contributionAfter/record.orders:null;
      record.cac=record.orders?record.marketing/record.orders:null;
      record.beAnnual=record.unitAfter>0?record.fixed/record.unitAfter:null;
      annual.push(record);aggregate={};
    }
  }
  const capm=discount(inputs,k);
  const flows=annual.map(z=>z.fcff);
  let crossing=null;
  for(let i=1;i<flows.length;i++){
    if(npvAt(flows.slice(0,i+1),capm)>0){const root=irrAt(flows.slice(0,i+1));if(root.irr!==null&&root.irr>capm){crossing=years[i];break;}}
  }
  const {irr,status:irrStatus}=irrAt(flows);
  return {annual,periods,npv:npvAt(flows,capm),irr,irrStatus,crossing,capm,
    payback:paybackAt(flows),discountedPayback:paybackAt(flows,capm),
    funding:totalEquity,cashMin,cashMinUnfunded,fundingGap,equity:totalEquity,
    terminal:null,verify,market:market(a)};
}
const previousAssets = new Float64Array(121);
