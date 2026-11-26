# Figure provenance audit — LihatDulu UISP16 revised proposal

**Verdict.** 28 placed figures, 18 of them (64%) invented vector geometry built by three separate headless toolchains. **Zero** figures are captures of the supplied BCC deck: I hashed all 40 DOCX media against the deck's 173 media and got an empty set. The deck has a template for seven of them — VPC 110, BMC 111, STP 96, Personas 97–98, TAM/SAM/SOM with `Rp` fields 91, AIDA 99–100, Competitor Benchmarking 89–90 — and every one was rebuilt by hand in a different shape. Fauzi's comment 19 said the *arrows* were the problem; the revision answered it with a figure carrying 8 connectors.

## 1. The package is a dumping ground

40 media, 28 placed. **12 orphans (30%)**, all identified by hash:

| orphan | what it is | note |
|---|---|---|
| image1, 2, 3, 4, 5, 10, 14 | outputs of `pipeline.tex`, `issue.tex`, `swimlane.tex`, `market.tex`, `gantt.tex`, `journey.tex`, `chair.tex` | superseded by PIL/SVG versions |
| image6, image9 | duplicate `quality.tex` / `fragment.tex` | the placed copies are image39 / image37 |
| image8.jpg | **real product page capture, 1387×672, fully legible** | 7 figures reuse a worse copy of this screen |
| image11.jpg | inherited A4 page background from the draft | |
| image13.jpg | inherited on-brand cabinet+AR concept render | the best image in the pack, unused |

Of nine TikZ sources, **seven never reach the document**.

## 2. The 28 figures, by source

| # | Source | Reference does instead |
|---|---|---|
| G1 Informasi sulit dipastikan… | PIL bar chart | Thrifty p5: real BPS/Forms charts with source lines |
| G2 Halaman barang, bukti kondisi, ruang | PIL composite | EverWear p10: 3 real app screenshots |
| G3 Value Proposition Canvas | PIL box table | **deck 110**: circle+square canvas |
| G4 Alur dokumentasi penjual | PIL 3 panels + 2 arrows | EverWear p8 (deck slide export) |
| G5 Arsitektur mesin rekonstruksi | PIL 8 boxes + 6 arrows | EverWear p12: one flow + legend |
| G6 Bingkai kursi, GLB, foto asli | PIL 4 panels | captioned photo plates |
| G7 Aliran dana | SVG | Thrifty p10: real Thredup/Jagofon screenshots |
| G8 Alur pesanan | SVG 10 boxes + 8 connectors | Thrifty p14: **one** lane diagram + legend |
| G9 Sumber pasokan | SVG 3 equal columns | a table |
| G10 Jadwal indikatif | SVG pseudo-Gantt | Thrifty p16; needs a real time axis |
| G11 Peta risiko | SVG 3×3 heatmap | EverWear p11 real matrix. Correct answer to comment 22 |
| G12 Segmentasi, target, posisi | SVG card table | **deck 96** STP matrix |
| G13 Profil kerja pembeli/penjual | SVG 2 cards + glyphs | Thrifty p13: **real portrait photos** |
| G14 TAM, SAM, SOM | SVG 3 circles | Thrifty p11 / EverWear p9: donut **with Rp** |
| G15 Materi akuisisi | SVG mock ad | — |
| G16 Kreator "Muat Nggak?" | SVG mock, screenshot twice | — |
| G17 Perjalanan dari melihat konten | SVG 4 chevrons | **deck 99–100** AIDA |
| G18 Bursa Pindahan | SVG + AI photo | real event photos |
| A.1 BMC | PIL 5+4 cards | **deck 111**: 9-block canvas |
| B.1 Tindakan setelah iklan | PIL bar chart | fine |
| B.2 Perubahan keyakinan | PIL paired bars | fine |
| C.1 Halaman barang | real UI capture | correct |
| C.2 Empat sudut GLB | real render grid | correct, unlabelled |
| C.3 Foto sumber dan model | real photos + renders | correct — strongest item |
| C.4 Segitiga fragmen | **TikZ/PGFPlots** | a sentence; one bar, other value 0 |
| C.5 Foto bingkai, SPZ | PIL composite | correct |
| F.1 Jalur publikasi foto | **TikZ** | EverWear p12-style flow with legend |
| G.1 Tag kondisi, meja bantuan | SVG 3 cards, fake QR | — |

Counts: TikZ **2**, Python→SVG→Inkscape **13**, PIL **11**, real photograph **2**. Straight real product-UI or photo plates: **3 of 28 (11%)**; anything containing a real capture, 7 of 28 (25%). Density 0.90 figures/page vs EverWear's ~9 numbered *Gambar* in 37 pages (0.24).

## 3. What the TikZ actually cost

241 lines across 9 files; **lines 1–16 are byte-identical in all nine** (144 duplicated lines, 60%), the drawing is 6–17 lines. Changing one label means XeLaTeX → PDF → `pdftoppm -r 300` → re-insert in Word, per `assets/README.md`, for 2 of 28 figures. `chair.tex` and `journey.tex` use LaTeX to lay out four and three JPEGs. `fragment.tex` spends 13 lines plotting the pair (354, 0). All nine ship in `upload/LihatDulu_UISP16_Figure_Sources.zip`; seven produce nothing.

## 4. Arrows

Seven figures, **31 arrowheads across 33 connectors**:

| figure | arrows |
|---|---|
| G3 VPC (PIL) | 6 |
| G5 pipeline (PIL) | 6 |
| F.1 quality (TikZ) | 5 + edge labels "Ya"/"Belum" |
| G8 operations (SVG) | 7 arrows + 1 arrowless connector at x=804→814 |
| G7 revenue (SVG) | 3 |
| G9 supply (SVG) | 2 arrows + 1 arrowless line |
| G4 journey (PIL) | 2 |

Plus G14's 3 leader lines, G17's 4 chevrons, G11's one stray rule at `fig.line((427,36),(427,210))` — which sits **inside** the 124–409 grid and reads as an orphan divider.

Three arrowhead implementations — TikZ `Latex[length=2.4mm]`, SVG `<marker> M0 0 L6 3 L0 6 Z`, PIL `draw.polygon(tip=12/14)` — visible across facing pages G5 and G7 (p8, p9).

Reference behaviour: Thrifty p14 is **one** diagram — 2 lanes, ~14 nodes, green decision diamonds, colour-coded classes, a legend. EverWear p12 Gambar 9 is one flow with a 2-item key. The revision splits that content over G5, G8, G9 and F.1: four diagrams, 24 boxes, no legend, one diamond.

It also breaks: `operations.svg` routes an anonymous line (804,64)→(814,180)→(720,180) with no arrowhead, ending in whitespace; "Jika ada selisih kondisi" has no incoming connector; "Pembayaran → Serah terima" is drawn as a step.

## 5. Generated-figure tells — present unless noted

1. **Uniform hairline stroke, same box, centred label** — every SVG rect `stroke-width="1.2"`, every PIL box `width=2`, every TikZ flow `.65pt`; `box` / `stage()` / `card()` are one primitive written three times.
2. **Equal columns** — G4 (3), G5 (4+4), G6 (4), G8 (3+3), G9 (3), G.1 (3), G18 (3). G5's rows are 371×176 and 371×175.
3. **Gradients / drop shadows** — absent. Credit where due.
4. **Always rounded** — TikZ 2pt, PIL 13/14/18, SVG 4/5/6/7/8/10, against a deck whose template frames are square (slides 91, 96, 110, 111). No figure has a square corner.
5. **One asset as an icon** — the Lemari Sora screen appears six times (G2, G4 ×2, G16 ×2, C.1, G.1). G13's two glyphs (a bag, a parcel) denote nothing. G.1's "QR code" is three rects and four squares; it cannot scan.
6. **Text under 7 pt** — 6 figures; 12 under 8.5 pt, computed as `font_units × placed_mm ÷ artboard_units`:

Under 7 pt (illegible): **G1 survey-barriers 5.9**, B.2 survey-demo 6.1, A.1 BMC 6.4, B.1 survey-actions 6.4, G4 journey 6.4. Under 8 pt: G2, G3, G5, G10, G11 (7.5 each), G8 (7.5 min / 8.6 body). C.4 and F.1 sit at 10.0/10.5 pt.

Only the two TikZ diagrams and the marketing panels hit a readable size. The five worst are all PIL/SVG.

7. **Repeats a table or paragraph already in the document** — 8: G10 ↔ Tabel F.3 + Tabel G.1 (same three phases, same names); G11 ↔ Tabel F.4 (identical R1–R5 labels, 18 pages apart); G12 + G13 ↔ §4.1 prose and each other; G7 ↔ §2.5; G9 ↔ §3.2; G17 ↔ Tabel G.2; C.4 ↔ Tabel C.1; A.1 ↔ §2.1.

8. **Broken on the page** — A.1 (p20) clips and overlaps: "Segmen pelangg" cut at the right edge, "Proposisi nilai" body running under the card row below. G13's "Rumah tangga muda…" touches its cell floor. G6's "Tab Foto asli diprioritaskan" wraps out of its panel.

## 6. Where the figures are *missing*

BAB V Financial Strategy (pp.18–19) has **zero charts** — only Tabel 4 and 5 with `[Rp per tahun]` placeholders. Lampiran D, the competitor appendix, has **zero figures** (only Tabel D.1–D.3) while the deck offers Competitor Benchmarking (89) and SWOT (87). §4.3 SWOT has no figure. So the count is 28 figures in the fiction chapters and none where a figure would carry data.

## 7. Delete / replace / keep

All 28 accounted for, no overlaps.

**DELETE (8) — restatements with no evidence.** G5 (pipeline: 8 boxes for what Tabel C.2 already tabulates), G9 (supply: 3 equal columns of §3.2 prose), G10 (roadmap: no time axis; Tabel F.3 and G.1 already carry the three phases), G15 and G16 (mock ad and creator collateral for campaigns that do not exist), C.4 (TikZ plotting the pair 354/0, already in Tabel C.1 and the prose), F.1 (quality: duplicates one sentence, and its return arrow `(e.west)-|(a.south)` lands in whitespace), G.1 (3 cards incl. a QR that cannot scan).

**REPLACE WITH A DECK SLIDE (6).** G3 → slide 110. A.1 → slide 111 (this one must be replaced, not deleted: the current 5+4 card wrap is clipping text). G12 → slide 96. G13 → slides 97–98. G14 → slide 91 with `Rp x TAM` filled from §4.2 (`Rp11,63 triliun`; `Rp3.376/orang/bulan`). G17 → slides 99–100. Then **add** slide 89 (Competitor Benchmarking) and 87 (SWOT) into §4.3 and Lampiran D, which have no figures at all.

**REPLACE WITH A REAL CAPTURE OR PHOTO (3).** G2 → the orphaned `image8.jpg`, which is already in the package and legible. G7 → a screenshot of the real checkout, as Thrifty p10 does with Thredup/Jagofon. G18 → real photos of the first event, or cut the AI scene entirely.

**MERGE (1).** G4 folds into G2: both show the same Lemari Sora screens, one at 4× the size.

**REBUILD (1).** G8, as a single two-lane diagram with a legend, square template frames, decision diamonds, and one arrowhead style — i.e. what Thrifty p14 and EverWear p12 Gambar 9 already are.

**KEEP (9).** G1, B.1, B.2 (real survey data), G11 (the only correct response to a comment: fix the stray rule at x=427, drop the "penilaian awal secara kualitatif" hedge), G6 (real chair frames and GLB output — label the four panels and stop letting the caption wrap out of panel 4), C.1, C.2, C.3, C.5 (real proof of concept; C.3 is the strongest plate in the document).
