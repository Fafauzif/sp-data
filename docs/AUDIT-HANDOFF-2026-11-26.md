# Audit handoff: LihatDulu UISP16 revision vs its review

Audit run 26 November 2026. Nothing in the proposal, the scripts, or the existing docs was modified. Two files were added: this one and `docs/PLAN-NEXT-RUN-2026-11-26.md`.

Read `docs/WORD-REVIEW-COMMENTS.md`, `docs/CURRENT-CONTEXT.md`, and `docs/CHAT-FEEDBACK.md` first. This file records what the audit already established so a new session does not redo it.

## Verified findings

Each line below was checked directly against the rendered pages or the DOCX XML, not inferred.

1. **Cover (page 1) is completely blank.** Comment 0 asked to empty the cover. It was emptied to nothing: no placeholder lines for team name, members, or institution survive in the DOCX body block 0, so there is nothing to fill in later. Page 1 also carries no header or footer.
2. **Page 2 (Statement of Authorship) is a near-blank page.** Three short lines at the top, roughly 85 percent of the page empty. This is the exact shape comment 7 was written about.
3. **Page budget is inverted.** Body runs pages 3-18, appendix pages 19-29. Financial strategy (BAB V) gets two pages, 17-18, of a 31-page document. Marketing gets six. The appendix is about a third of the document.
4. **"Sora" survives.** Body block 218 in Lampiran C reads "Sora berasal dari rilis 29961f0 dan menggunakan kabinet contoh", and the product mockup placed on page 5 prints "Lemari Sora" twice inside the image. Comment 2 is not met, in text and in artwork.
5. **Build artefact in body prose.** 24 body paragraphs end on a bare hyperlink label with no full stop before it: "…pada pesanan yang sama. Model bisnis", "…bukti minimum. Kendali mutu listing". Three have two labels jammed together ("Alur pemeriksaan bukti Model kapasitas", "Penelusuran lemari bekas Penelusuran lemari tiga pintu", "Catatan pemrosesan Metadata hasil demo"). Block indices: 45, 48, 57, 62, 66, 73, 75, 78, 81, 83, 89, 97, 99, 107, 112, 117, 119, 122, 124, 127, 133, 147, 149, 155. This is the original's "Tabel C.1" artefact with new wording: the build appends a reference token to the paragraph instead of writing a sentence. A correction to an earlier draft of this note: the 16 literal "Tabel A.1 … G.3" strings are the appendix table captions, and only one appears in running prose ("…dua pengujian pada Tabel C.1 menggunakan GLB dari…"). The defect is the links, not the table references.
6. **Figure 14 (TAM/SAM/SOM) contains no rupiah figure.** The graphic is three concentric green circles with three label cards reading "Potensi pendapatan marketplace nasional", "Potensi pendapatan di area layanan", "Pendapatan marketplace tahun ketiga", each multiplied by a per-order value. The actual revenue arithmetic is in the paragraph below the figure. Comment 25 ("needs to be revenue based") is half addressed: the labels are revenue-flavoured, the visual is not.
7. **All 28 figures are raster and all sit at the same width.** Every image is placed 5.7-6.14 in wide, 1.1-4.8 in tall (10-45 percent of the text block), at 195-333 dpi. The figure typeface is sans while body text is Times New Roman 12 pt on 1.5 spacing. Nothing in the DOCX is a PowerPoint object or a native shape.
8. **Headings are English, body is Indonesian.** "BAB I. Problem Background & Validation", "BAB II. Business Model", "BAB III. Operation Strategy", "BAB V. Financial Strategy" against Indonesian paragraph text and Indonesian figure captions.
9. **Caption numbering is actually fine.** 18 body figures (Gambar 1-18) and 10 appendix figures (A.1, B.1-B.2, C.1-C.5, F.1, G.1). 28 figure blocks, 28 captions, no orphaned image. Do not "fix" this in the next run.
10. **What the references actually look like, and the size of the gap.** Thrifty is a designed magazine: full-bleed colour fields, brand lockup, a hook headline, a phone mockup showing the real app, emoji storytelling with numbered points (p8), Instagram screenshot collages and an influencer photo card (p18). EverWear sits closer to a Word report but still carries a persistent header banner with tagline and partner logo, a footer with the team name ("Kucing Cimit"), a three-level heading hierarchy (3.1.1), the two-sided Value Proposition Canvas as a pastel coloured canvas with arrows (p5), and persona cards with avatar circles, a job chip, and Behaviour / Motivation columns (p8). The revision has a decorative green corner motif, a page number, justified Times prose, and wide thin band figures dropped between paragraphs.
11. **The supplied deck was not used at all.** `upload/02-FRAMEWORK-BCC.pptx` is 111 slides at 20 x 11.25 in, built from native shapes. Slide 91 is the concentric TAM/SAM/SOM with leader cards and the three questions; slide 96 is the STP grid with a Primary/Secondary target legend; 97-98 are persona cards with an avatar circle and a goals panel; 99-100 are a four-band AIDA ribbon with icons and a numbered step strip; 8 and 110 are the two-sided VPC; 111 is the BMC in the standard nine-block layout. None of that geometry appears anywhere in the document.

## What the reference standard implies

The two exemplars are visual systems, and the reviewer is asking for that system, not for citations to it. A page in those documents is usually one designed object: a headline, a graphic that carries the argument, and prose that explains the graphic. The revision treats the graphic as an interruption of the prose. That is the root difference behind comments 12, 13, 14, 16, 18, 19, 20, 23, 24 and 26, which all say the same thing in different words.

EverWear is the realistic target for a Word-based submission. Thrifty is the upper bound on effort.

## Audit status

All seven audit agents finished and wrote to `/tmp/audit/findings/`. The synthesis is in `docs/PLAN-NEXT-RUN-2026-11-26.md`.

| Report | Headline |
|---|---|
| `ref-everwear.md` | 14 of 21 body pages are pure text; frameworks quarantined to the appendix; every flow figure is a lane spine with a real screenshot, never a box diagram |
| `ref-thrifty.md` | Zero text layer, all pixels. One exhibit owns a page, values live inside the rings, marketing rides on real captures, prose is question-led with Anda/kita |
| `deck-template.md` | The deck was not used, not once: no shared colour, no shared shape, 0 of 40 images from its 173. Also the A4 arithmetic that explains why nobody ported it |
| `comments-compliance.md` | 10 MET, 13 PARTLY, 4 NOT MET: comments 2, 17, 25, 26 |
| `figures-provenance.md` | 18 of 28 figures are invented geometry, 3 are real evidence plates, 8 delete, 6 replace with deck pages, 3 replace with captures |
| `prose-voice.md` | 127 words per page of body prose, 1 sentence-initial conjunction in 2,964 words, 24 paragraphs ending on a link, BAB I cut hollow |
| `layout-pagination.md` | Blank space is mostly fixed (mean 10.9 percent); what remains is six unabsorbed figure holes, five split tables, a fake TOC, and figure type from 2 to 7.5 pt |

Still open, in the plan as the four blocking decisions:

- [ ] Which reference is the target, EverWear's format or Thrifty's. Only the user can decide
- [ ] The chapter-break rule, since both references break on chapter and comment 7 forbids it
- [ ] The finance workbook, and whether BAB V keeps its brackets until it arrives
- [ ] Whether 1.5 line spacing is a competition requirement. If not, 1.15 reclaims about six pages

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

## Where the agent reports live

All seven finished. Their reports, and the extraction artifacts they worked from, are under `C:/Users/fauzi/AppData/Local/Temp/audit/findings/`. Copy that folder somewhere durable before clearing temp, because the page renders and dumps took the bulk of the work.

## Suggested opening message for the next session

> Continue LihatDulu UISP16 from the audit. Read docs/PLAN-NEXT-RUN-2026-11-26.md and docs/AUDIT-HANDOFF-2026-11-26.md. The four blocking decisions at the top of the plan need my answers before you touch the document. Once I answer, work through the tasks in order and stop after Task 1 so I can check the ported deck pages before you rebuild the figure set. Do not run revision/build.py.
