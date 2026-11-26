# Audit handoff: LihatDulu UISP16 revision vs its review

Started 26 November 2026, stopped early at the user's request. Nothing in the proposal, the scripts, or the existing docs was modified. This file is the only addition.

Read `docs/WORD-REVIEW-COMMENTS.md`, `docs/CURRENT-CONTEXT.md`, and `docs/CHAT-FEEDBACK.md` first. This file records what the audit already established so a new session does not redo it.

## Verified findings

Each line below was checked directly against the rendered pages or the DOCX XML, not inferred.

1. **Cover (page 1) is completely blank.** Comment 0 asked to empty the cover. It was emptied to nothing: no placeholder lines for team name, members, or institution survive in the DOCX body block 0, so there is nothing to fill in later. Page 1 also carries no header or footer.
2. **Page 2 (Statement of Authorship) is a near-blank page.** Three short lines at the top, roughly 85 percent of the page empty. This is the exact shape comment 7 was written about.
3. **Page budget is inverted.** Body runs pages 3-18, appendix pages 19-29. Financial strategy (BAB V) gets two pages, 17-18, of a 31-page document. Marketing gets six. The appendix is about a third of the document.
4. **"Sora" survives.** Body block 218 in Lampiran C reads "Sora berasal dari rilis 29961f0 dan menggunakan kabinet contoh", and the product mockup placed on page 5 prints "Lemari Sora" twice inside the image. Comment 2 is not met, in text and in artwork.
5. **Build artefact in body prose.** Sixteen dangling cross-references are pasted at the ends of sentences, for example "Bukti tersebut menunjukkan satu alur teknis yang dapat diperiksa sendiri. Tabel C.1". Full list: Tabel A.1, B.1, B.2, C.1 (twice), C.2, D.1, D.2, D.3, E.1, F.1, F.2, F.3, F.4, G.1, G.2, G.3. They read as broken sentences, not citations.
6. **Figure 14 (TAM/SAM/SOM) contains no rupiah figure.** The graphic is three concentric green circles with three label cards reading "Potensi pendapatan marketplace nasional", "Potensi pendapatan di area layanan", "Pendapatan marketplace tahun ketiga", each multiplied by a per-order value. The actual revenue arithmetic is in the paragraph below the figure. Comment 25 ("needs to be revenue based") is half addressed: the labels are revenue-flavoured, the visual is not.
7. **All 28 figures are raster and all sit at the same width.** Every image is placed 5.7-6.14 in wide, 1.1-4.8 in tall (10-45 percent of the text block), at 195-333 dpi. The figure typeface is sans while body text is Times New Roman 12 pt on 1.5 spacing. Nothing in the DOCX is a PowerPoint object or a native shape.
8. **Headings are English, body is Indonesian.** "BAB I. Problem Background & Validation", "BAB II. Business Model", "BAB III. Operation Strategy", "BAB V. Financial Strategy" against Indonesian paragraph text and Indonesian figure captions.
9. **Caption numbering is actually fine.** 18 body figures (Gambar 1-18) and 10 appendix figures (A.1, B.1-B.2, C.1-C.5, F.1, G.1). 28 figure blocks, 28 captions, no orphaned image. Do not "fix" this in the next run.
10. **What the references actually look like, and the size of the gap.** Thrifty is a designed magazine: full-bleed colour fields, brand lockup, a hook headline, a phone mockup showing the real app, emoji storytelling with numbered points (p8), Instagram screenshot collages and an influencer photo card (p18). EverWear sits closer to a Word report but still carries a persistent header banner with tagline and partner logo, a footer with the team name ("Kucing Cimit"), a three-level heading hierarchy (3.1.1), the two-sided Value Proposition Canvas as a pastel coloured canvas with arrows (p5), and persona cards with avatar circles, a job chip, and Behaviour / Motivation columns (p8). The revision has a decorative green corner motif, a page number, justified Times prose, and wide thin band figures dropped between paragraphs.
11. **The supplied deck was not used at all.** `upload/02-FRAMEWORK-BCC.pptx` is 111 slides at 20 x 11.25 in, built from native shapes. Slide 91 is the concentric TAM/SAM/SOM with leader cards and the three questions; slide 96 is the STP grid with a Primary/Secondary target legend; 97-98 are persona cards with an avatar circle and a goals panel; 99-100 are a four-band AIDA ribbon with icons and a numbered step strip; 8 and 110 are the two-sided VPC; 111 is the BMC in the standard nine-block layout. None of that geometry appears anywhere in the document.

## What the reference standard implies

The two exemplars are visual systems, and the reviewer is asking for that system, not for citations to it. A page in those documents is usually one designed object: a headline, a graphic that carries the argument, and prose that explains the graphic. The revision treats the graphic as an interruption of the prose. That is the root difference behind comments 12, 13, 14, 16, 18, 19, 20, 23, 24 and 26, which all say the same thing in different words.

EverWear is the realistic target for a Word-based submission. Thrifty is the upper bound on effort.

## Not analysed yet

- [ ] Full per-page reference spec for all 29 Thrifty pages and all 37 EverWear pages. Only spot checks were done: Thrifty 1, 8, 18; EverWear 6, 9.
- [ ] One row per reviewer comment with a verdict (met / partly / not met) and the evidence. No verdict table exists yet.
- [ ] Deck inventory outside the nine noted slides. What competitor, SWOT, KPI, roadmap or financial templates the 111 slides also hold, and how each ports to A4 portrait at readable body size.
- [ ] TikZ source review. The nine `.tex` files in `revision/assets/figures/` were not read, so figure provenance is only inferred from filenames and rendered output.
- [ ] Delete / replace / keep decision for each of the 28 figures.
- [ ] Indonesian prose audit: word counts per subsection in BAB I, the list of sentences in BAB I that leak the solution, in-text citation count and quality per chapter, and counts of the robotic patterns (repeated sentence openings, missing conjunctions, hedge stacks).
- [ ] Layout sweep of all 31 pages: empty-space percentage per page, every forced page break, orphaned captions, footer and header contents, TOC page numbers against printed folios.
- [ ] Appendix A-G audit against comment 26: words versus figures per appendix. Lampiran D and E appear to have no figure at all; unconfirmed.
- [ ] Comment 15: whether the 3D vendor is named anywhere. A quick grep for "Sora" was run, a grep for KIRI, Luma, Polycam or similar was not.
- [ ] Comment 22: Gambar 11 is captioned "Peta risiko operasi berdasarkan kemungkinan dan dampak" and is probably a heatmap. Its actual visual quality was not inspected.
- [ ] Comment 1: whether the executive summary sells problem, solution, operations, marketing and finance in that order, or still reads as a product description.
- [ ] Survey figures against `survey-analysis/analysis.md`: 50 responses, 46 students, 15 with a specific listing, 13 / 9 / 8 for the three difficulties.
- [ ] Financial plausibility of BAB V and Lampiran E. Two pages of numbers for a competition business plan was not checked for arithmetic or for the revenue-based market link the reviewer demanded.
- [ ] Figure typography and resolution normalisation, and whether the 40 media files contain duplicates or unused images.
- [ ] Whether `SHA256SUMS.txt` still matches the files (it was never verified this session).

## Artifacts that survive on disk

All under `C:/Users/fauzi/AppData/Local/Temp/audit` (Git Bash: `/tmp/audit`). These take real time to rebuild, so check them before regenerating.

| Path | What it is |
|---|---|
| `pages/thrifty/p01-29.png` | Thrifty reference, one PNG per page, 105 dpi |
| `pages/everwear/p01-37.png` | EverWear reference, same |
| `pages/revised/p01-31.png` | The revised proposal, same |
| `revised.txt` | pdftotext of the revised PDF, text layer intact |
| `revised_structure.txt` | The DOCX dumped block by block: `[index] Style |PIC :: text`, 289 blocks |
| `pptx_dump.txt` | All 111 deck slides with per-shape geometry in inches and text |
| `docx/` | The unzipped revised DOCX, media included |
| `docxmedia/` | A copy of the 40 media images, if the figures agent got that far |
| `dump_docx.py`, `dump_pptx.py` | The extraction scripts, rerunnable |

Rebuild commands, if the temp folder is gone:

```sh
python -m pip install python-docx python-pptx pymupdf
cd /tmp/audit
python dump_docx.py && python dump_pptx.py
pdftotext -layout "<repo>/revision/finalqa/LihatDulu_UISP16_Proposal_Revised.pdf" revised.txt
```

Paths inside Python on this machine must be `C:/...`, not `/c/...`. `read_file` on a PNG path returns the image, which is how the pages and figures were inspected.

## Seven audit agents were mid-run

They were spawned at roughly 14:55 and were still running when this session stopped. Any of them that finished wrote its report to `/tmp/audit/findings/<name>.md`. Check that folder before starting any of the work above; the report may already exist.

| Agent | Task | Report path |
|---|---|---|
| `ref-everwear` | Page-by-page spec of the EverWear reference | `findings/ref-everwear.md` |
| `ref-thrifty` | Page-by-page spec of the Thrifty reference | `findings/ref-thrifty.md` |
| `deck-template` | Deck inventory and the A4 porting spec per template | `findings/deck-template.md` |
| `comments-compliance` | Verdict table for all 27 comments | `findings/comments-compliance.md` |
| `figures-provenance` | Figure provenance, delete/replace/keep list | `findings/figures-provenance.md` |
| `prose-voice` | Indonesian prose and BAB I structure audit | `findings/prose-voice.md` |
| `layout-pagination` | 31-page layout, blank space, page breaks, TOC | `findings/layout-pagination.md` |

The `figures-provenance` agent had already written crops and contact sheets into `findings/_crops/` and `findings/sheets/` before stopping.

## Suggested opening message for the next session

> Continue the LihatDulu UISP16 audit. Read docs/AUDIT-HANDOFF-2026-11-26.md, then check /tmp/audit/findings/ for any agent reports that finished after the handoff was written. Finish the items in the "Not analysed yet" checklist, then write the next-run improvement plan. Read only: do not edit the proposal, the scripts, or the existing docs. The plan should focus on why the revision reads as a Word report with generated figures when the reviewer wanted the EverWear and Thrifty treatment, why the framework deck's templates went unused, and what each chapter needs to change.
