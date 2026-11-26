# Did the revision use the BCC framework deck?

Deck: `02-FRAMEWORK-BCC.pptx`, 111 slides, 20 × 11.25 in. Revision: 31 pp.
Page numbers = PDF pages of the revision; slide numbers = the deck.

## Verdict: not used — not partially, not once

1. **Colour.** The deck's palette is hard-coded per shape: `256A63`, `3C8C5F`, `6BAF89`,
   `179386`, `6D6A49`, `FCD12A` (`C59600`/`E4C02F`). A grep of every figure source the
   document ships (`marketing/*.svg`, `exhibits/*.svg`, `assets/figures/*.tex`) returns
   **zero occurrences of any of the eight hexes.** The document runs `#172C23`,
   `#124934`, `#103E32`, `#425950`.
2. **Geometry.** 15 of the 40 embedded images are generated diagrams — flat PNGs from three
   bespoke pipelines (TikZ, `exhibits/build_exhibits.py`, `marketing/build.py`): 2 + 13.
   Not one is a native shape. Every deck template is 100 % native.
3. **Provenance.** Nine TikZ sources exist; two shipped. `market.tex` still prints
   **"Nilai menunggu data"** inside its SAM box. That is an iterated drawing pipeline,
   not a ported template.
4. **The comments named the deck and were ignored.** C12 *"use a value proposition canvas
   (the two sided on in the template pptX)"* → p07. C23 *"Insert the template STP and User
   persona … DRIVEN BY VISUALS!"* → p13. C24 *"use the template pptx instead for this"* → p14.

Two figures echo a deck device — Gambar 14 (p14) reproduces slide 91's ring-and-leader
idiom, Gambar 17 (p16) slide 99's chevrons — and both lose every distinguishing feature:
the gold, the numbers, the layers. A copy with nothing left is a reinvention with extra steps.

## What the deck holds

Diagnosis 87–95, 106–109 · 91 TAM/SAM/SOM (variants 12, 23, 54–56) · 96 STP (22, 31,
71–77) · 97–98 personas (13–15, 24, 30), 49 journey · 89 benchmarking, 90 matrix, 99–100
AIDA, 101 4Ps, 105 five forces · 8 and 110 VPC, 111 BMC · 9 roadmap, 3/6/29/60/61/70 risk
matrix, 103 KPI, 102 BSC, 20 financial cards · dividers 82–85.

Measured type on 9/89/90/101/103: title 40 pt, labels 21–30 pt, **body 15.3–19 pt**.

## The eight templates that were owed

| Slide | Construction | Why it works |
|---|---|---|
| **110** VPC | Square + circle Ø6.57 in, joined by a connector, both X-divided into 3 zones, 0.35 in icons | The fit between offer and need is the whole argument; the connector carries it |
| **8** VPC variant | Hourglass map + 3 annuli split GAINS / JOBS / PAINS, 15 pills on leaders | 3 segments against one offer |
| **91** TAM/SAM/SOM | Discs Ø7.61/5.78/4.27 in nested from one origin, band ≈0.9 in, value inside the band, 3.65 in leaders to a right column | Size as area; the leader forces you to name each number |
| **96** STP | 4 dimension pills, 10 dashed criteria chips, 6-column matrix where **pill length = segment size, fill = primary/secondary**, 2-dot legend | Segments and targets resolved in one graphic, no prose |
| **97** Personas | Ø2.41 in avatar + dashed speech bubble, notch at the face, first person | Forces voice, not a profile table |
| **98** Card | Name bar, descriptor bar, 3 label pills → value chips, 3 icon bullets | The 8 fields a judge checks |
| **99–100** AIDA | 4 chevrons (gold/olive) → title pill → picture → Objectives → grey Impact strip | A funnel becomes a plan: title, objective, channel, outcome |
| **111** BMC | 9 panels, 18.09 × 8.74 in, 5 × 3.38 in columns, Activities over Resources, CR over Channels | The canvas every judge knows; deviating reads as not knowing it |

## Where a template existed and the revision drew its own

| Rev. | Figure | Deck | Drawn instead | The difference |
|---|---|---|---|---|
| p07 | Gambar 3 VPC | 110 / 8 | Two 3×2 tables of pale cards (*Pekerjaan/Hambatan/Hasil* → *Layanan/Pengurang/Pencipta*), once per actor | No square, no circle, no icons, no connector. The halves never touch, so the figure proves nothing about fit. C12 asked for "two sided"; this is two tables. |
| p13 | Gambar 12 STP | 96 | 3×3 table: rows *Wilayah/Pembeli/Penjual*, columns *Segmentasi/Fokus awal/Perluasan*, + a "Positioning" band | Wrong taxonomy — the deck's axis is Geographic/Demographic/Psychographic/Behavioral. No criteria, no size encoding, no legend. "Pembeli/Penjual" are channel sides, not segments. The Positioning line is clipped at the source PNG's bottom edge. |
| p13 | Gambar 13 personas | 97 + 98 | Two 8.5 cm cards: icon circle, "Pembeli / Penghuni kos baru", Kebutuhan / Hambatan / Pemicu | No name, age, income, avatar, quote or goals — 3 of the deck's 8 fields, third person. |
| p14 | Gambar 14 TAM/SAM/SOM | 91 | 3 nested discs + 3 leaders + 3 **prose** cards | **No number in any ring, none on any card.** Deck 91 puts "Rp x TAM" in the band; Thrifty p12 and EverWear p10 both put the figure in the ring. The section's only number ("Rp11,63 triliun") sits in body prose, and `market.tex` says Rp8,71 triliun. The figure is decoration. |
| p16 | Gambar 17 journey | 99–100 | 4 chevrons in one flat green, 4 tactic cards, 1 mint strip | No title/objective/channel/metric layer, no icons, no Impact strip. Heading says "Awareness, Consideration & Conversion"; the figure says AIDA — two models, one section. 4th column runs to 1.3 mm of the image edge. |
| p20 | Gambar A.1 BMC | 111 | 5 top cards + 2 bottom | **Sumber daya is in the bottom row**, killing Activities-over-Resources; **Saluran** sits bottom-middle, so CR-over-Channels is gone. 9 blocks → 7. Headers truncated by the card edge ("Hubungan pelang", "Segmen pelangg"); body text occluded ("setiap pesa…", "…pada fase berikutnya" vanish behind neighbours); two orphan glyphs ("g", "an") float in the gap. Worst artefact in the document. |

## Also reinvented, unwatched

- **KPI 103 → Tabel 1, p12.** Deck column 3 is "KPI (x-year target)". The revision's is
  *Tindakan*, and every row is a ratio ("Listing lolos bukti minimum ÷ listing yang
  diajukan per minggu"). No target, baseline or date anywhere.
- **Competitor 89/90 → Tabel 2, p14.** Deck asks "Min. 3 competitors & 5 aspects". The
  table compares 4 channels, names no competitor, and no 2×2 map exists. EverWear p10
  does it properly with logos.
- **4Ps 101 → Tabel 3, p15.** 2×2 quadrant with aspect prompts became a 4-row list.
- **Risk 3/6 → Gambar 11, p12.** Grid survives; the deck's *Risk | Cause | Mitigation |
  Strategy* register is replaced by a 5-line legend, so no risk has an owner.
- **Roadmap 9 → Gambar 10, p11.** 4 year columns became 3 phases; legend detached.
- **Financial 20 → Tabel 4/5, p18.** Deck slide 20 is three number cards (`+IDR 661
  Million/NPV`, `2 Years/Payback`, `37.9%/ROI`). The revision ships ten bracketed
  placeholders in that slot: `[NPV, IRR, payback]`, `[Rp per tahun]`, `[Rp dan waktu]`.
- **Dividers 82–85 unused.** BAB II starts at the foot of p06.

Defects that stand on their own, deck or no deck:

- **p01 is blank**; p02 is a bare Contents that places 4.1 at page 11 when Gambar 12/13 are
  on p13 — headings never renumbered after figures moved.
- **Leading.** 11 pt body on a measured 23.3 pt baseline (34 px of 1228 = 8.2 mm): double
  spacing is why 5 600 words fill 31 pages.
- **Link tokens in print.** "Hasil survei", "Rumus dan batas kapasitas", "Lampiran E"
  (split as "Lampiran / E") — teal underlined fragments at paragraph ends.
- **Dead space.** p10 loses 20 % of the page, p16 22 %; p11 opens with a figure orphaned
  from its paragraph on p10.
- **p17** spends 100 mm on a synthetic photograph of a "Bursa Pindahan" event with
  generated students, disclaimed at 8 pt grey — the biggest image in the document,
  depicting something that did not happen.

---

# Porting spec: deck template → A4 portrait

**Arithmetic.** A4 at 20 mm margins = 170 mm. Slide = 508 mm. Scale 0.335, so the deck's
15.3–19 pt body lands at **5.1–6.4 pt** — below any print floor. To hold 8 pt the type
must be 1.3–1.6× larger relative to its box, cutting words per box to **40–60 % of the
slide's**. No template drops in. Re-set every one at 3 bullets × ≤6 words per zone,
8 pt floor, 9.5 pt headers.

**Mechanics.** Duplicate the slide → Design ▸ Slide Size ▸ Custom 21 × 29.7 cm ▸ "Scale to
Fit": all shapes stay editable at A4 size. Delete the deck's title bar and grey instruction
text ("Aspects include:", "How big is the largest possible market?", "Min. 3 competitors"),
retype at 8 pt. Never paste a PNG of a framework; rasterise only photographs and screenshots.

| Template | A4 box | Grid | Budget | Cut |
|---|---|---|---|---|
| **Cover** | full 210 × 297, bleed | — | title ≤9 words | everything but logo, one photo, year |
| **BMC** | **full page** 170 × 120 | 5 cols × 34, top 84, bottom 28 | 3 bullets × ≤6 words; headers ≤22 chars, wrapped | all prose → Tabel A.1 |
| **VPC** | **full page** 170 × 120 | square 78 + gap 14 + circle Ø78 | 3 bullets × ≤5 words × 6 zones | second actor → own page |
| **TAM/SAM/SOM** | **half page** 170 × 95 | rings Ø95/75/55 one origin, band 10; list 62 | figure per band at 14 pt + 3 × ≤12-word definitions | deck's question prompts |
| **STP** | **full page** 170 × 105 | labels 30, 8 criteria, 4 target cols × 26 | ≤3 words/cell, 7.5 pt floor | 6 targets → 4; italic helpers |
| **Personas** | **half page each** 170 × 62 | avatar Ø26 + text 140 | name/age, ≤12-word descriptor, 3 chips ≤8, 3 goals ≤9 | third-person summaries |
| **AIDA** | **full width** 170 × 95 | 4 chevrons × 42 × 15, 4 layers × 18 | title ≤4, objective ≤10, channel+tactic ≤12, metric ≤8 | "Objectives" label; fix `Awarenes`/`Desir` |
| **KPI** | **half page** table 170 × 90 | Area / Now / Target (x-yr) / Owner | 6–8 rows, every target numeric | open-ended ratios |
| **4Ps** | **half page** 170 × 100 | 2×2 × 80 × 45 | ≤35 words/quadrant | deck's example lists |
| **Competitor** | **one page, 2 blocks** 170 × 95 | 5 cols × 5 aspects; 2×2 with logos Ø22 | 4–6 words/cell | — |
| **Risk** | **full page** 70 × 70 + 100 | 3×3 cells 23; 4-col register | risk id in cell; register ≤12 words/col | 5-line legend |
| **Roadmap** | **half page** 170 × 70 | 4 phase cols × 4 rows | ≤8 words/bar, 8.5 pt | detached legend |
| **Financial** | **strip** 170 × 30 | 3 cards 55 | figures 26 pt bold + 8 pt label | must carry real numbers |

**Allocation.** Full page: cover, VPC (p07), STP (p13), BMC (p20), risk (p12). Half page:
TAM/SAM/SOM, personas ×2, AIDA, 4Ps, competitor + matrix, roadmap, KPI, financial strip.
Twelve figure-led pages replacing 31 pages of prose, 15 raster diagrams and 10 placeholders.
