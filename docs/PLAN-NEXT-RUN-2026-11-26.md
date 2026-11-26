# LihatDulu UISP16, second revision: implementation plan

> For the next agent: read "Why the first revision failed" before Task 1, and answer the four blocking decisions before touching the document. Steps are checkboxed.

**Goal.** Turn the 31-page revised proposal from a Word report with generated figures into a document a competition judge reads as designed, with the framework deck doing the visual work and the prose carrying an argument.

**Architecture.** EverWear supplies the page skeleton (single column, serif, running header band, frameworks quarantined to the appendix). Thrifty supplies the instinct (one exhibit owns a page, real artefacts instead of drawn ones). The BCC deck supplies every framework shape. No bespoke figure pipeline survives.

**Tech stack.** Word DOCX assembled by `revision/build.py`, PowerPoint 21 x 29.7 cm pages ported from the deck, 300 dpi PNG or EMF exports, Word fields for the TOC.

**Spec.** The audit that produced this plan is in `docs/AUDIT-HANDOFF-2026-11-26.md`, the seven reports in `C:/Users/fauzi/AppData/Local/Temp/audit/findings/`, and the 27 reviewer comments in `docs/WORD-REVIEW-COMMENTS.md`.

---

## Why the first revision failed

Five causes. Every reviewer complaint traces to one of them.

**1. The comments were executed as text, not as intent.** "Empty the cover" produced a page with zero ink and no placeholders, so there is nowhere to write the team name. "A chapter doesn't need to start on a new page" produced chapters at 78 percent down the page, but the six figure blocks that no longer fit were never rebalanced, so p8, p10, p13, p16, p21 and p24 each lose 12 to 28 percent of the page to one unbreakable image pushed forward. "Have figures" produced 28 of them.

**2. The figure pipeline was invented instead of the deck being ported.** Zero of the 40 images in the DOCX come from the deck: the media hashes and the deck's 173 images share nothing, and none of the deck's eight hard-coded colours (`256A63`, `3C8C5F`, `6BAF89`, `179386`, `6D6A49`, `FCD12A`) appears in any figure source. 18 of 28 placed figures are invented box, arrow or card geometry built by three separate pipelines: nine TikZ files (241 lines, of which 144 are a byte-identical preamble, and seven never reach the document), `exhibits/build_exhibits.py` and `marketing/build.py` (13 figures), and PIL compositing (11). Seven figures carry 31 arrowheads drawn three different ways, so facing pages show three arrow styles.

**3. The prose lost weight without gaining voice.** Body text runs about 127 words per page over 16 pages against roughly 300 in the references, yet only one sentence in 2,964 words opens with a conjunction, "Pada" is the commonest first word, and 24 of 39 body paragraphs end on a bare cross-reference fragment ("kendali mutu listing", "alur operasi", "model bisnis") with no full stop before it. BAB I is now 397 words, has no closing hinge, and repeats 1.1's example in 1.2. The chapter was cut, not rewritten.

**4. The bookkeeping is machine-assembled.** The contents page is 38 paragraph hyperlinks with a dot-leader tab, so every line prints teal and underlined, and there is no Daftar Gambar or Daftar Tabel for 28 figures and 21 tables. Five tables split across pages and leave their header row alone. Heading space above varies 2.8 times. Two caption tiers collide on p26. Figure text runs from 2 pt to 7.5 pt.

**5. The numbers were deferred.** BAB V is ten bracketed placeholders, including `[NPV, IRR, payback]`. The finance workbook was never supplied, so some of this is a real dependency, but the deck's three-card financial strip (slide 20) could have carried the shape.

## What the references actually demand

Three things, none of them a citation.

1. **One exhibit owns a page.** Thrifty p12 puts the TAM/SAM/SOM rings across half a page with the values inside the rings and the arithmetic in the bullets. EverWear p12 gives its operating figure a bordered container, a rotated lane label and a legend. The revision's median figure occupies 26 percent of the page height and 97 percent of the width, which is neither.
2. **A real artefact beats a drawing of one.** Thrifty's product pages are phone frames holding real screenshots; its marketing pages are real Instagram captures; p20 is a photograph of a hand holding the phone. The revision has three figures built on real evidence and 18 drawn.
3. **A reader exists.** Thrifty writes "Berapa banyak baju baru yang Anda beli setiap tahun?", uses Anda and kita, and joins clauses with Namun, Tapi, Untuk itu. EverWear names the team in the footer. The revision addresses nobody, and its commonest word after the first "Pada" is "Pembeli".

## Global constraints

Facts any task must preserve. Each was measured, not estimated.

| Fact | Value | Why it constrains |
|---|---|---|
| Text measure | 454 pt wide, body 12 pt on a 20.7 pt baseline | 5,950 words spread over 31 pages |
| Figure width | 25 of 28 sit at 442 pt | No figure aligns to either text edge (81.1 vs 72.1 left, 523.3 vs 526.5 right) |
| Deck body type | 15.3 to 19 pt on a 508 mm slide | At A4 it lands at 5.1 to 6.4 pt. No template drops in |
| Deck colour | 8 fixed hexes, none present in the document | Proof of non-use, and the palette to inherit |
| Chapter position | BAB I at 78 % down p4, II p6, III p10, IV p12, V p18 | Comment 7 compliance already exists. Do not regress it |
| Sora | 1 body sentence plus 6 figures | Comment 2 still open |
| KIRI | References line, plus body "Dua hasil GLB menggunakan KIRI Engine Photo Scan" | Comment 15 still open |
| Market size | Text says Rp11,63 triliun per tahun; the figure shows no number | Comment 25 |
| Blank space | Mean 10.9 % per page; p3 is 89 % blank | The blanket "gaps" charge is largely fixed |
| TOC | 38 of 38 page numbers correct, none are fields | Correct numbers, wrong mechanism |

**Do not run `revision/build.py`.** It rebuilds from the commented proposal (3) and will overwrite the clean DOCX with whatever the script encodes. Either edit the DOCX directly or port every change into the script before running it. This is the single fastest way to lose a day's work.

## Blocking decisions

Only the user can settle these. Ask before Task 1; each changes what the tasks do.

**D1. Which reference is the target?** EverWear is a formatted report (single column, serif, olive header band, pastel frameworks, three-level headings). Thrifty is a designed magazine (full-bleed colour, two columns, portraits in circles, screenshots as evidence). The revision tried EverWear's skeleton with TikZ figures. Recommendation: EverWear skeleton, Thrifty's exhibit discipline. Doing full Thrifty means rebuilding the document in a page-layout tool.

**D2. Chapter breaks.** The reviewer wrote "A CHAPTER DOESNT NEED TO START ON A NEW PAGE", but both references do start chapters on a fresh page, and both strand white space doing it (EverWear p4 loses 4.5 in, p20 loses 75 percent). The rule that satisfies both is break for the figure, never for the chapter. Confirm.

**D3. Financials.** Either leave the brackets until the workbook arrives, or build the deck's three-card strip with the formula and one bracket per card. The second is presentable; ten brackets in a table is not.

**D4. Line spacing.** Body is 12 pt at 1.5 lines. If the competition guide requires 1.5, keep it and accept 31 pages. If not, 1.15 reclaims roughly six pages of room for figures. Check the guide before changing anything.

---

## File structure

| Path | Action | Responsibility |
|---|---|---|
| `revision/output/LihatDulu_UISP16_Proposal_Revised.docx` | modify | The deliverable |
| `revision/figures-v2/` | create | One 21 x 29.7 cm PPTX page per ported template, plus its 300 dpi export |
| `revision/figures-v2/README.md` | create | Which deck slide each page came from, the word budget per zone, the export command |
| `revision/assets/figures/*.tex` | freeze | Archive only. `fragment.tex` and `quality.tex` stay because they ship. The other seven are dead |
| `revision/exhibits/`, `revision/marketing/` | freeze | Archive the scripts. Do not extend them |
| `revision/product/build_figures.py` | edit | Keeps the screenshot compositing (real evidence). Drops the invented diagram builders |
| `docs/WORD-REVIEW-COMMENTS.md` | read only | Source of truth for verdicts |

---

## Task 1: port twelve deck templates to A4

**Files.** Create `revision/figures-v2/` with one PPTX per template and a 300 dpi PNG beside it. Source: `upload/02-FRAMEWORK-BCC.pptx`.

**Interfaces.** Each output is a PNG named `fig-<template>-a4.png`, exportable to 170 mm wide at 300 dpi, with all internal type at 8 pt or larger. Later tasks place these by filename.

- [ ] Duplicate the deck slide, then Design, Slide Size, Custom 21 x 29.7 cm, Scale to Fit. Shapes stay editable.
- [ ] Delete the deck's title bar and its grey scaffolding: "Aspects include:", "How big is the largest possible market?", "What proportion of the market fits you?", "Min. 3 competitors". These are presenter prompts.
- [ ] Re-set type to the floor: 9.5 pt headers, 8 pt body. Cut words per zone to 40 to 60 percent of the slide's.
- [ ] Port these twelve, in this order: 111 BMC, 110 VPC, 91 TAM/SAM/SOM, 96 STP, 97 plus 98 personas, 99 plus 100 AIDA, 103 KPI, 89 plus 90 competitor, 101 4Ps, 3 plus 6 risk register, 9 roadmap, 20 financial strip, plus 87 SWOT.
- [ ] Export each at 300 dpi.

**Done when** twelve PNGs exist, each carries a header at 9.5 pt and body at 8 pt or larger, and none contains the deck's instruction text. Open each at 100 percent and read every label out loud; if a label needs guessing, the budget was exceeded.

Template budgets, from the deck porting audit:

| Template | A4 box | Grid | Budget |
|---|---|---|---|
| BMC | full 170 x 120 | 5 cols x 34, top 84, bottom 28 | 3 bullets, 6 words max; headers 22 chars max |
| VPC | full 170 x 120 | square 78 + gap 14 + circle 78 | 3 bullets, 5 words max, 6 zones |
| TAM/SAM/SOM | half 170 x 95 | rings 95/75/55 one origin, band 10, list 62 | figure per band at 14 pt, three definitions of 12 words |
| STP | full 170 x 105 | labels 30, 8 criteria, 4 targets x 26 | 3 words per cell, 7.5 pt floor |
| Personas | half each 170 x 62 | avatar 26 + text 140 | name, age, descriptor 12 words, 3 chips, 3 goals |
| AIDA | full width 170 x 95 | 4 chevrons x 42 x 15, 4 layers x 18 | objective 10 words, channel 12, metric 8 |
| KPI | half 170 x 90 | Area, Now, Target, Owner | 6 to 8 rows, every target numeric |
| 4Ps | half 170 x 100 | 2x2, 80 x 45 | 35 words per quadrant |
| Competitor | one page, two blocks | 5 aspects, then a 2x2 with logos 22 | 4 to 6 words per cell |
| Risk | full 170 x 100 | grid 70 + register 100 | risk id in cell, register 12 words per column |
| Roadmap | half 170 x 70 | 4 phase columns x 4 rows | 8 words per bar |
| Financial | strip 170 x 30 | 3 cards 55 | figure at 26 pt with an 8 pt label |

## Task 2: put the money inside the market figure

**Files.** `revision/figures-v2/fig-tam-sam-som-a4.png`, plus the paragraph under Gambar 14 on p14.

**Interfaces.** Consumes the TAM/SAM/SOM page from Task 1. Produces the only place in the document where the three market numbers are stated.

- [ ] Fill TAM from the text that already exists: Rp11,63 triliun per year, BPS mebel, with the base year.
- [ ] Derive SAM as a stated share of TAM and write the share into the figure. Derive SOM as a stated share of SAM and write the share into the figure. No share may be left implicit, because the reviewer asked for revenue and the current text gives spend.
- [ ] Put each rupiah figure inside its ring at 14 pt, in the deck's `Rp x TAM` slot.
- [ ] Reconcile the arithmetic with the rest of the chapter before placing it. Rp3.376 per person per month times 287 million people times 12 gives household spend. Platform revenue equals spend times listing share times conversion times take rate. The current SOM implies a per-capita figure 60 times smaller than the Rp2,45 juta cabinet listed on p6, so the assumptions need to be written down, not implied.

**Done when** the figure carries three rupiah values and three explicit shares, and a reader can reproduce the SOM from the numbers printed on the page.

## Task 3: rebuild the figure set

**Files.** `revision/output/....docx` figure slots; `revision/figures-v2/`; `revision/product/build_figures.py`.

**Interfaces.** Consumes Task 1's PNGs. Produces 12 figure-led pages.

- [ ] Delete eight figures that restate a table or paragraph: Gambar 5, 9, 10, 15, 16, C.4, F.1, G.1.
- [ ] Replace six with the ported deck pages: Gambar 3 becomes the VPC (110), A.1 becomes the BMC (111), 12 becomes STP (96), 13 becomes personas (97 plus 98), 14 becomes the numbered rings from Task 2, 17 becomes AIDA (99 plus 100).
- [ ] Replace three with real captures: Gambar 2 uses the unused `image8.jpg` product-page capture, which is cleaner than anything currently placed; Gambar 7 becomes a real checkout or order-detail screenshot; Gambar 18 drops the synthetic "Bursa Pindahan" photograph or is cut.
- [ ] Merge Gambar 4 into Gambar 2. Same screens, four pages apart.
- [ ] Rebuild Gambar 8 as one two-lane flow with a legend, or drop it and let the deck roadmap (9) and risk page carry section 3.
- [ ] Keep nine: Gambar 1, B.1, B.2, 11, 6, C.1, C.2, C.3, C.5. Fix Gambar 11's stray rule and delete its "penilaian awal secara kualitatif" note.
- [ ] Add the two deck templates no figure currently answers: competitor benchmarking (89 plus 90) into 4.3, SWOT (87) into 4.3 or Lampiran D.

**Done when** no figure is a box-and-arrow diagram of something a screenshot could show, every placed figure is at least 8 pt internally, and 12 pages carry one full or half-page exhibit.

## Task 4: purge the cross-reference stubs

**Files.** `revision/output/....docx`, body blocks listed below.

**Interfaces.** None. This is a repair.

24 body paragraphs end in a bare hyperlink with no punctuation, which is what the reviewer saw as "Tabel C.1" in the original and reads as a broken sentence now. Block indices from the structure dump: 45, 48, 57, 62, 66, 73, 75, 78, 81, 83, 89, 97, 99, 107, 112, 117, 119, 122, 124, 127, 133, 147, 149, 155. Three carry two concatenated labels ("Alur pemeriksaan bukti Model kapasitas", "Penelusuran lemari bekas Penelusuran lemari tiga pintu", "Catatan pemrosesan Metadata hasil demo").

- [ ] For each, either delete the link, or write a sentence that points somewhere and finishes: "Rincian perhitungan ada di Lampiran E." Not "…Lampiran E" alone.
- [ ] Where the stub points at a table, name the table properly and keep it in the appendix.
- [ ] Remove the teal underline styling from anything that survives.

**Done when** no paragraph before the References section has a hyperlink as its last element, and no paragraph ends without a full stop.

## Task 5: remove Sora

**Files.** `revision/output/....docx`; the screenshots in `revision/product/raw/` and `revision/assets/images/`.

- [ ] Rewrite the body sentence in Lampiran C: "Sora berasal dari rilis 29961f0 dan menggunakan kabinet contoh" becomes a sentence about the example cabinet.
- [ ] Relabel the six figures that print "Lemari Sora": Gambar 2 (twice), 3, 16, C.1, G.1, plus "Foto acuan - Sora" and "Tangkapan Sora" in captions.
- [ ] Either crop the label out of the source screenshots or recapture them.

**Done when** a case-insensitive search of the DOCX text and of every placed image finds no "Sora".

## Task 6: rebuild the executive summary

**Files.** Blocks 44 to 48, p4.

**Interfaces.** Consumes Task 2's three numbers and Task 7's financial shape.

- [ ] Keep the four-beat arc that is already there (what it is, how selling works, how buying works, where growth comes from) and add the missing half: one market number, one operating number, one financial number, and the ask.
- [ ] Remove the dead links at the end of the first and fourth paragraphs.

**Done when** a reader can answer what it is, how big, how it makes money, and what it needs, without turning the page.

## Task 7: give the financial chapter a shape

**Files.** Blocks 155 to 160, p18 to p19, plus `revision/figures-v2/fig-financial-a4.png`.

**Interfaces.** Consumes the three-card strip from Task 1.

- [ ] Build the strip: NPV, payback, and one revenue or margin figure, at 26 pt with 8 pt labels. If the workbook has not arrived, the card carries the formula and one bracket, and the caption says which input is missing.
- [ ] Split the ten-bracket table into assumptions (with the bracket) and results (derived from those assumptions, with one worked order shown).
- [ ] Write one worked order end to end: item price, buyer fee, seller commission, delivery pass-through, net to seller, net to platform. Nine of the reviewer's comments come down to "show the numbers".
- [ ] Keep the revenue rule once. It currently appears in the executive summary, 2.5, 4.2, 5.1 and Tabel A.1.

**Done when** every number in BAB V either has a value or names the input it waits on, and one order can be followed from price to take.

## Task 8: rewrite BAB I

**Files.** Blocks 49 to 57, pp. 4 to 6.

**Interfaces.** Consumes the survey figures in `survey-analysis/analysis.md`.

- [ ] Keep the inverted triangle that now exists: EU or global quantity, then Indonesia, then Jabodetabek, then the kos cluster.
- [ ] Cut the instant-messaging statistic. "94,76% usaha e-commerce menggunakan pesan instan" is about messaging apps, not furniture, and the sentence after it concedes incumbents already work.
- [ ] Add the two sentences from `survey-analysis/analysis.md` that make the counts mean something. The chapter currently reports 13 of 15 could not judge condition and then ends on a caveat.
- [ ] Cut the repeated example. 1.2 restates 1.1's water stain and hinge, about 40 words spent twice.
- [ ] Close the chapter on a hinge: "karena itu" plus the one thing the gap demands. There is currently no closing sentence at all.
- [ ] Swap two of the four European papers for sources a judge expects: an Indonesian ministry or regulator, one Indonesian academic work on secondhand or kos, one market-research figure, and one business-press item. Cite the survey as your own work.
- [ ] Add one concrete scene. The document has one in 31 pages and it sits in the executive summary, not here.

**Done when** the chapter runs 550 to 650 words, carries no mention of LihatDulu or the solution, ends on a sentence that forces chapter 2, and cites two to three sources per page.

## Task 9: fix the page system

**Files.** `revision/output/....docx`: TOC field, headers and footers, table properties.

- [ ] Replace the 38 hyperlink paragraphs with a real TOC field, then add Daftar Gambar and Daftar Tabel, which the document needs at 28 figures and 21 tables.
- [ ] Rebalance the six figure holes at p8, p10, p13, p16, p21 and p24 by moving one figure or allowing it to run to 60 percent of the page. The next page currently opens with a caption, which is the tell.
- [ ] Remove the pointless break before 4.5. It is the only mid-document section break and it splits 4.4 from 4.5 for no reason.
- [ ] Fill p3 with the actual statement text, or move the signature block onto p2. It currently spends a page on two lines and 89 percent white.
- [ ] Return the cover to placeholders for team name, members, and institution. The reviewer will fill it himself, but the fields must exist.
- [ ] Stop five tables splitting their header row: Tabel 5, A.1, B.2, D.1, F.1. Set repeated header rows and keep rows together.
- [ ] Add a running header or footer band with the team name and document title. EverWear carries both; the revision carries a leaf graphic and a page number.
- [ ] Normalise heading space to one value per level. It currently varies 2.8 times.
- [ ] Rebuild Gambar A.1 regardless of Task 3, because the current BMC is clipped: "Hubungan pelang", "Segmen pelangg", body text occluded by neighbours, two orphan glyphs.

**Done when** the TOC and both lists are fields that update, every page number matches, no table has an orphaned header row, and no page before the appendix loses more than 15 percent of its frame.

## Task 10: verification gate

Run before calling the revision done. Each check has a pass condition, not an opinion.

- [ ] Zero paragraphs in the body whose last element is a hyperlink.
- [ ] Case-insensitive search finds no "Sora" in text or images.
- [ ] Case-insensitive search finds no vendor name (KIRI, Luma, Polycam, Photo Scan vendor) anywhere except a references entry that must be removed as well.
- [ ] Every placed figure has internal type at 8 pt or larger, checked at 100 percent on the exported PDF.
- [ ] Every figure is one of: a deck-derived page, a real capture, a real photograph, or a real data chart. Count them; the number that are none of those should be zero.
- [ ] The three market numbers in the figure match the paragraph under it and the appendix.
- [ ] Five tables, zero split header rows.
- [ ] TOC, Daftar Gambar, Daftar Tabel all update from fields and print correct page numbers.
- [ ] Page count is a decision, not an accident. Report it against 31 and say what changed.
- [ ] Read p4 aloud. It must sell problem, solution, operations, marketing, and finance, and reach a number before the page ends.
- [ ] Open the appendix. Four of the last twelve pages are currently text and grid with no figure; comment 26 is still open.
- [ ] Re-read the 27 comments. Every verdict that was PARTLY or NOT MET in the audit needs a page reference that now shows the fix.

## Review focus

Five things most likely to bite, in order.

**The A4 type floor.** The deck's 15.3 to 19 pt type becomes 5.1 to 6.4 pt at A4. This is why the previous run drew its own figures: the templates did not fit the content. Anyone porting a template will be tempted to shrink type to keep the words. Hold 8 pt and cut the words instead.

**The Sora screenshot.** It appears in six figures and in the source captures. Any figure regenerated from those captures reintroduces the name.

**The build script.** `revision/build.py` rebuilds from proposal (3). Running it after editing the DOCX silently reverts everything.

**Figure aspect and alignment.** 25 of 28 figures sit 9 pt inside the left text edge and 3 pt inside the right. A redesign that keeps the old placement keeps the ragged edge, which is half of why the pages look assembled.

**Inheriting the references' own defects.** Thrifty ships "CONVENTION" for Consideration, "Poter's Forces", "7Bulan", a pie label over body text and unfilled TOC placeholders. EverWear still has its own copy in a Thrifty appendix table. Copy the system, not the typos.

## Self-review

Checked against the audit reports before writing.

Coverage: all 27 comments map to a task. The 24 link stubs and the six Sora figures are Task 4 and 5. The twelve deck templates are Task 1. Market size, the revenue basis, and the implausible SOM are Task 2. The figure delete and replace list is Task 3. BAB I length, hinge, and citations are Task 8. Financial placeholders are Task 7. Layout, TOC, and tables are Task 9. The comment 22 heatmap already exists as Gambar 11 and stays.

Proportion: no task transcribes code. Where a value matters (Rp11,63 triliun, 8 pt, 12 pages, the 24 block indices) it is named, not described.

Open items this plan cannot settle: the finance workbook, the competition's line-spacing rule, and the choice between EverWear's format and Thrifty's. Those are the four blocking decisions at the top and they belong to the user.
