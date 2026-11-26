# LihatDulu UISP16 | Handoff 26 November 2026

Extract the ZIP at the root of `Fafauzif/sp-data`. Its only destination is `revision/uisp16-2026-11-26/`. This path was checked against `origin/main` at `fc2e7b57ed61fe8a46a9161fb9b32cacc89b7370`. The bundle is additive. The archived revision, prior survey analysis, project contacts, and Git history remain in the checkout.

## Start here

| Path | Contents |
|---|---|
| [deliverables](deliverables/) | Final proposal in DOCX and PDF, primary financial model, editable figures in PPTX, and ZIP to rerun financial risk. |
| [source/proposal](source/proposal/) | Proposal generator, text and metric bindings, index cache, survey and finance charts, real product captures, editable SVG compositions, and technical evidence. |
| [source/figures](source/figures/) | 14 exported framework figures with build source, slide geometry evidence, and PDF preview. The supplied BCC template stays at [the repository input path](../../upload/02-FRAMEWORK-BCC.pptx). |
| [source/campaign](source/campaign/) | Three original final campaign mockups plus the earlier material concept. |
| [source/finance](source/finance/) | Financial assumptions, benchmark evidence, risk engine and seeded outputs. The optional Full Trials workbook exposes more columns for each simulation and differs from the compact primary deliverable. |
| [source/survey](source/survey/) | Final 60-response CSV with timestamps removed, a standard-library script, and its aggregate output. The earlier 50-response source in the base repository is historical. |
| [source/brief](source/brief/) | Run instructions used for the revision, financial modeling prompt and example, official booklet and authorship template, and a style-reference index. |
| [audit](audit/) | Five-round editorial review, navigation and workbook checks, and independent finance validation. Some audit helpers retain original scratch paths. |

The final proposal has 25 body pages. The initial pages, references, and appendices bring the physical PDF total to 42. Word uses Times New Roman. The PDF preview uses Liberation Serif. Existing `revision/output/LihatDulu_UISP16_Proposal_Revised.docx` is the previous house copy. Use the DOCX in this bundle for the next edit.

## Decisions and remaining inputs

- Keep the EverWear layout, Thrifty-style evidence, BCC template geometry, and LihatDulu palette. The campaign progresses from listing support to creator content and then to Bursa Pindahan. The generated mockups depict campaign concepts.
- Use the final buyer survey as buyer evidence. Of 60 responses, 17 came from people who considered a particular used-furniture listing. The comparison used a fixed viewing order. Treat the results as changes in stated confidence and intent.
- Replace the marked placeholder in Appendix B.2 after one seller interview. Record permission and the discussion date privately. Ask about where listings originate, how inventory and defects are confirmed, what handoff costs the seller, and which proposed services they would pay for. Update the seller persona and the affected discussion only after checking the answers. Leave unverified statements framed as assumptions. The cover and authorship page await the team.
- Keep the product case specific to the observed evidence. The repository prototype captures show the seller and buyer workflows. The local SPZ evaluation tested seven recordings of the same chair. Test a broader set of objects before claiming reconstruction quality across categories.
- Preserve the financing conclusion unless new evidence changes the inputs. The primary Base model yields NPV of negative Rp2.51 billion at a 13.97% WACC. The proposal recommends a one-cluster pilot near UI Depok before expansion. Each round of funding is modeled. It has yet to be raised.

## Reproducing the package

From the repository root, enter `revision/uisp16-2026-11-26`. The proposal build uses Python with `python-docx`, `lxml`, `Pillow`, and `matplotlib`. Verification and figure cropping also use `PyMuPDF`.

```sh
python source/survey/summarize.py
python source/proposal/build_proposal.py
```

The default Word output goes to `build/`. The build refreshes its three survey chart PNGs and the navigation index in `source/proposal/`. It reads the included proposal bindings and figure assets. Editing the CSV also requires updating the proposal narrative and chart values.

To regenerate the metric bindings and finance charts, run `python source/proposal/prepare_metrics.py` and `python source/proposal/charts_finance.py`. Review any later narrative values added directly to the document. Rendering the proposal PDF requires Word or LibreOffice. Recheck the folios with `source/proposal/verified_folios.py` after any page-flow change.

The editable PPTX is ready to use. Rebuilding it from source requires Node.js with `@oai/artifact-tool`, Python, the repository BCC template, and LibreOffice. The order is `node source/figures/build.mjs`, `python source/figures/port_geometry.py`, export the resulting `source/figures/LihatDulu_Figur_UISP16.pptx` to PDF in the same folder, then run `python source/figures/export.py`. The product SVG/PNG composer uses Inkscape and the bundled raw captures.

Begin finance work with the compact published workbook. Recompute the Base-centered simulation and sensitivity after editing assumptions. With Node.js 20+, Python 3, and `openpyxl` installed, run

```sh
node source/finance/refresh/refresh-risk.mjs deliverables/LihatDulu_Financial_Projection.xlsx build/risk
```

This writes the regenerated driver assumptions, 10,000-trial CSV, sensitivity outputs, and risk summary. An optional third output argument emits a new XLSX in an environment with `@oai/artifact-tool`. See [the risk instructions](source/finance/refresh/README-refresh.md).

`SHA256SUMS.txt` lists the SHA-256 digest of each file in this handoff, excluding the manifest itself.
