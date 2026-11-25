# Sumber gambar LihatDulu UISP16

Folder figures berisi sembilan sumber LaTeX dengan TikZ atau PGFPlots, PDF vektor, PNG penempatan 300 dpi, dan data kanonis gambar. Folder images berisi potongan sumber yang dirujuk oleh TeX dan gambar bukti pendukung. Pertahankan kedua folder pada tingkat yang sama.

Kompilasi ulang berkas TeX dari dalam folder figures dengan XeLaTeX, kelas standalone, fontspec, TikZ dan PGFPlots. Contoh perintah:

    xelatex -no-shell-escape -halt-on-error journey.tex
    pdftoppm -r 300 -singlefile -png journey.pdf journey

Gambar memakai Liberation Serif pada kompilasi ini. Teks dokumen Word menggunakan Times New Roman. Data kuantitatif dan asal tangkapan dicatat di data-figures.json. Tangkapan Sora menunjukkan demonstrasi dengan kabinet contoh dari rilis 29961f0. Bingkai sumber serta model kursi berasal dari rangkaian uji satu objek fisik. Diagram operasi dan jadwal adalah rancangan. Batas pasar bersifat skematis.
