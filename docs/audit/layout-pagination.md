# LihatDulu UISP16 — layout & pagination audit

Sources: `revision/finalqa/…Revised.pdf` (31 pp, A4 595×842), `p01–p31.png`, DOCX XML, `pptx_dump.txt`, refs Thrifty (29 pp) / EverWear (37 pp).

**Measured frame.** Text x 72.1–526.5 (454 pt), y 72.5–769.9 (697 pt). Body 12 pt, pitch 20.7 pt (1.5 lines), justified, no hyphenation. Captions 9 pt centred. Folio 779–792, right-aligned.

## 1. Blank space (Comment 7)

Empty = 769.9 − bottom of last ink (text, figure or rule), % of the 697 pt frame.

| p | § | empty | p | § | empty |
|---|---|---|---|---|---|
| 1 | cover | **100 %** | 17 | 4.5–4.6 | 2.9 % |
| 2 | Daftar Isi | 17.2 % | 18 | 5.1–5.2 | 4.2 % |
| 3 | Statement | **89.0 %** | 19 | Referensi | 3.3 % |
| 4 | ExecSum/BAB I | 2.0 % | 20 | Lampiran/A | 0.1 % |
| 5 | 1.1–1.3 | 6.7 % | 21 | A.1/B | 18.4 % |
| 6 | 2.1–2.2 | 0.0 % | 22 | B.2–B.3 | 1.4 % |
| 7 | 2.2–2.3 | 2.8 % | 23 | C | 2.3 % |
| 8 | 2.3–2.4 | 16.7 % | 24 | C.3–C.6 | **27.7 %** |
| 9 | 2.4–2.5 | 6.7 % | 25 | C.6 | 9.9 % |
| 10 | BAB III/3.1–3.2 | 16.8 % | 26 | C.7/D | 1.8 % |
| 11 | 3.3–3.4 | 8.6 % | 27 | D.1–D.3 | 6.6 % |
| 12 | 3.5–4.1 | 1.5 % | 28 | E/F | 4.9 % |
| 13 | 4.1–4.2 | 12.4 % | 29 | F.3–F.4 | 8.5 % |
| 14 | 4.2–4.3 | 2.6 % | 30 | F.5/G | 1.0 % |
| 15 | 4.3–4.4 | 8.6 % | 31 | G.4 (end) | **25.1 %** |
| 16 | 4.5 | 18.6 % | | | |

Average 10.9 % (8.3 % excluding p1, p3). **Over 30 %: p1, p3 only.** Over 15 %: p2, p8, p10, p16, p21, p24, p31.

The blanket "huge gaps" charge is largely fixed — 20 of 31 pages finish within 8 % of the frame. What survives is mechanical: **six holes (p8, p10, p13, p16, p21, p24) are each one unbreakable figure block pushed forward** — 770 pt, 1.1 pages of white, proven by what opens the next page (p9: the *Gambar 6* caption; p11: *Gambar 9*; p14: *Gambar 14*; p25: *Gambar C.3*). Nothing was rebalanced. Thrifty fills to the bottom rule (p24); where EverWear stops short (p5, ~35 %) its bands box the page.

## 2. Page breaks

Five forced breaks (every other heading carries `pageBreakBefore w:val="0"`):

1. before **Statement of Authorship** → p3
2. before **Executive Summary** → p4
3. before **4.5 Awareness, Consideration & Conversion** → p16
4. before the **"Fase 3 – Tahun kedua…"** exhibit → p17
5. before **Lampiran** → p20

Chapters do **not** start on fresh pages: BAB I opens p4 at y 594.7 (78 % down), II p6 at 225, III p10 at 143, IV p12 at 660, V p18 at 123 — Comment 7 compliance, and it should be credited. But 4.5 is the only section that jumps a page, splitting 4.4→4.5 for no structural reason. Breaks 1–2 also yield the blank p1 and the 89 %-blank p3.

## 3. Widows and orphans

- Six pages open with a 2–3 line carry-over (p7, p8, p10, p13, p15, p18); no 1-line orphan.
- All 28 captions sit 5.9 pt under their image — **no caption/figure separation**. Pass.
- Five pages end on a caption (p9, p11, p15, p16, p24).
- Real widow: **p18** — "Lampiran E" breaks so a lone **"E"** sits at the left margin.
- **p26** stacks captions: "Gambar C.5…" y 292.6, "Tabel C.2…" y 313.1 — 8 pt apart, under the figure's own in-image caption line.

## 4. Cover and Statement of Authorship

- **p1 is 100 % white**, zero ink. Literally as asked, but there is now nowhere for team name, members or institution — the old `Nama tim ____` block was deleted, not replaced. Both references open with designed covers.
- **p3 (folio 2)** spends a page on two lines — "Tempat dan tanggal ____" / "Nama dan tanda tangan ____" — then 89 % white. No statement text, no originality declaration.

## 5. Front matter — Daftar Isi (p2)

- **38 entries; 38/38 page numbers match the printed folio.** Real dot leaders, no dead link.
- But it is **not a TOC field**: each line is `<w:hyperlink w:anchor>` around a run with `<w:color 176250/><w:u single/>`, a dot-leader tab, then `<w:fldSimple PAGEREF>` holding a hard-typed number. **All 38 lines print as teal underlined text** — a web index, not a contents page. Thrifty p3: seven numbered blocks "01."…"07.", no leaders, no underline.
- No **Daftar Gambar**, no **Daftar Tabel**, with 28 figures and 21 tables; A.1/B.1/C.1 unlisted.

## 6. Figure sizes

28 placements. 25 are exactly 442 pt wide (97 % of measure) — **9 pt inside the text's left edge (81.1 vs 72.1), 3 pt inside its right (523.3 vs 526.5)**; none aligns to a margin. Outliers p6 (411), p15 (424), p25 (420). Heights 11–49 % of frame, median 26 %; only **p17 Gambar 18 at 49 %** distorts flow. Nothing is too narrow — the failure is the inverse: no figure sets internal text at body size (body = 9.6 pt ink; caption 9.6 for 9 pt). Measured internal type: Gambar 1 footnote (p6) ≈5 pt = 42 % of body; Gambar 3 VPC body (p7) ≈6.5–7 pt; Gambar 6 phone panel (p9) ≈2.5 pt = 21 %; Gambar C.1 "Rp2.199.000" (p23) **≈2–3.5 pt = 25 %**; Gambar A.1 BMC cells (p20) ≈7.5 pt. A VPC in 32 % of page height and a phone UI in a quarter of a figure cannot survive that.

## 7. Footer / header

No header text. `header1.xml`/`header2.xml` hold **only a 595.3 × 841.9 pt full-bleed image at 0,0 behind the text** — pale-green leaf art on p2–p31, appendix included. No running title, no team name. Footer `w:jc="right"` with one `PAGE` field; footer1 has none, so p1 is unnumbered; printed = physical − 1. EverWear runs a header ("EverWear : *Style with care, for Earth we share*") and a footer band ("— Kucing Cimit"); Thrifty is numeral-only, like the revision, which keeps Thrifty's minimum and adds decoration where information should be.

## 8. Appendices (p20–p31)

12 pages, 2,443 words, 10 figures, 19 tables. **Three pages carry no figure**: p27 (D.1–D.3), p28 (E.1–F.1 — "Perhitungan Keuangan" with **no calculation and no number**), p30 (F.4–G.2). Comment 26 unmet; Thrifty p24 answers it — two full-page graphics, one sentence.

## 9. Machine-assembled tells

1. **Dangling cross-reference stubs at paragraph ends** — link fragments after a full stop, no lead-in. Ten sites, p4–p27: "Hasil survei" (p4), "Model bisnis" (p6), "Rangkaian tangkapan layar Alur operasi" (p8, two links concatenated), "Alur pemeriksaan bukti Model kapasitas" (p11), "Penelusuran lemari bekas Penelusuran lemari tiga pintu" (p27). Same mechanism as the "Tabel C.1" mid-paragraph artefact of Comment 1.
2. **Space above headings varies 2.8×**: 9.0 (2.2 p6; Lampiran C p23) → 25.6 (3.6 p12); BAB II sits 11 pt under a figure caption. **Flat scale**: H1 14 pt bold, H2 12 pt bold — H2 is body size.
3. **Five visual dialects**: TikZ greyscale small caps (5, 8, 9, 10, 11, 14, 17, C.4, F.1 — nine `assets/figures/*.tex`), Inkscape mockups on white plates (2, C.1, G.1), flat card grids (3, 4, 12, 13, A.1), data-viz with in-figure footnotes (1, B.1, B.2), AI photography (18). **Tables differ page to page**: dark header + white rows (p12, 14, 15, 18, 24) vs dark header + pale zebra (p22, 26, 29, 31) vs picture-tables (Gambar 12, p13). Gambar 3 (p7) even disagrees with itself: dark seller header, pale buyer header.
4. **5 tables split, each leaving an orphan header row**: Tabel 5 p18→19, A.1 p20→21, B.2 p22→23, D.1 p26→27, F.1 p28→29; Tabel 5 and F.1 also split inside a row (no `cantSplit`).
5. On-page failures: Chapter V (p18) all placeholders — "[Rp per tahun]", "[Pesanan tahun 1 dan tahun 3]"; BMC Gambar A.1 (p20) **clipped and overlapping** — fifth column off the page edge, "Segmen pelangg…" cut; C.2 (p24) an unlabelled 4×2 grid; leaked filename "chair001001242…07_368.jpg" at ≈3 pt in C.3 (p25); "Lemari Sora", rejected in Comment 2, survives in Gambar 2 (p6), 16 (p16), C.1 (p23), G.1 (p31).
6. **No deck template used.** BCC slide 91 "TAM SAM SOM Analysis", 96 "STP Analysis", 97 "Customer Personas", 110 "Value Proposition Canvas" (Products & Services / Gain Creators / Pain Relievers vs Gains / Pains / Customer Jobs), plus SWOT-TOWS, 4Ps, BMC, JOURNEY MAP, risk matrices. Used: none. Gambar 3 (p7) is a 2×2 box matrix with no Products/Gains/Pains/Customer-Job cells — not a VPC.

## 10. Density target

| | pages | words/page | figures/page |
|---|---|---|---|
| Thrifty | 29 | ≈150–500 (2-col ~10 pt; p4 ≈390) | ≈1.4 |
| EverWear | 37 | ≈200–290 (1-col ~11 pt, 2.0 spacing) | ≈0.8 |
| **Revision** | **31** | **192** (body 207, appendix 204; 5,950 total) | **0.9** |

Word count is not the problem — 192 sits between the references. Spending 31 pages on 5 chapters where Thrifty spends 24 on 7 is what 12 pt / 1.5-spaced single-column prose with no secondary structure, and figures bolted on instead of pages composed, does.

## Verdict

Chapters flow; Comment 7's literal instruction was fixed. Nothing else on layout was: blank p1, 89 %-blank p3, 5 forced breaks (one pointless, at 4.5), 6 unabsorbed figure holes, 5 split tables, a fake TOC of 38 underlined hyperlinks with no figure or table lists, 28 figures whose type runs 2–7.5 pt across five systems, no deck template, prose appendices where graphics were demanded.
