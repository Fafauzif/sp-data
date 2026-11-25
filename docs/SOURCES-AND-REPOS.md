# Sources and linked repositories

## Clone only as needed

The handoff avoids vendoring the marketplace and other GitHub repositories. These were the links used in the project. Pinned revisions are reproducibility anchors, not statements about current deployment or branch status.

| Repository | URL | Relevant revision |
|---|---|---|
| LihatDulu | [Fafauzif/Lihatdulu](https://github.com/Fafauzif/Lihatdulu) | `29961f0043f0b1f21dde957a9b3ab0b6d0e4396e` for product screenshots and the competition-judge release evidence. Historical `main` observed at `8b404df`. |
| BPC Studio | [Fafauzif/BPC-Studio](https://github.com/Fafauzif/BPC-Studio) | `b0f6a9226b60896dffe3795578a09ffc20299a37` |
| Competition Proposal Skill | [Fafauzif/Competition-Proposal-Skill](https://github.com/Fafauzif/Competition-Proposal-Skill) | `1538659efd5350db87938c6e1746623ea6d6d8d3` |
| Design with Character | [Fafauzif/Design-with-Character](https://github.com/Fafauzif/Design-with-Character) | Historical review at `40ba7e9ef8211fe461579ff7e409cee3598d80a4` |

```sh
git clone https://github.com/Fafauzif/Lihatdulu.git revision/product/checkout
git -C revision/product/checkout checkout --detach 29961f0043f0b1f21dde957a9b3ab0b6d0e4396e

git clone https://github.com/Fafauzif/BPC-Studio.git refs/BPC-Studio
git -C refs/BPC-Studio checkout --detach b0f6a9226b60896dffe3795578a09ffc20299a37

git clone https://github.com/Fafauzif/Competition-Proposal-Skill.git refs/Competition-Proposal-Skill
git -C refs/Competition-Proposal-Skill checkout --detach 1538659efd5350db87938c6e1746623ea6d6d8d3

git clone https://github.com/Fafauzif/Design-with-Character.git refs/Design-with-Character
git -C refs/Design-with-Character checkout --detach 40ba7e9ef8211fe461579ff7e409cee3598d80a4
```

The official Proposal Workflow package is at `refs/Competition-Proposal-Skill/chatgpt-work/proposal-workflow.zip` after cloning. Start from its `START_HERE.md`. The separately supplied [historical Sell the Finished Idea ZIP](https://chatgpt.com/library?file_id=libfile_150ea231d644819196b71f1201269d3d02&account_id=personal) was unavailable in the revision session. The checked-in Competition Proposal Skill guidance includes this approach. Use BPC Studio's reference atlas, Ruang Rapi example, and ReFeel and Dua case lessons for style and reasoning. Their numbers do not transfer to LihatDulu.

Other historic upstream references include [Brush](https://github.com/ArthurBrussee/brush), [Taste Skill](https://github.com/Leonxlnx/taste-skill), [Playwright CLI](https://github.com/microsoft/playwright-cli), [Vercel agent skills](https://github.com/vercel-labs/agent-skills), and [Awesome Design.md](https://github.com/voltagent/awesome-design-md).

## Proposal exemplars and uploaded framework

- **EverWear**, `refs/Ideanation_Kucing_Cimit_watermark_HQ.pdf`. Product and segment figures around physical PDF pp. 6–12, marketing pp. 17–18, and visual appendices pp. 24–29.
- **Thrifty**, `refs/PROPOSAL_UISP_HQ.pdf`. Product reveal pp. 7–8, marketing pp. 17–20, and workflow exhibits pp. 25–28.
- **FRAMEWORK BCC**, `upload/02-FRAMEWORK-BCC.pptx`. Market sizing slide 91, STP 96, personas 97–98, AIDA 99–100, and value propositions and canvas among 8, 110, and 111. Use the layout and adapt it to the proposal with LihatDulu's colors and evidence.
- Original [Filebin reference drop](https://filebin.net/w2gx02xckqd8eqeb). The reference PDFs are included locally so it can expire without affecting the handoff.

## Product proof

- [Competition judge PR #6](https://github.com/Fafauzif/Lihatdulu/pull/6) and [pinned source](https://github.com/Fafauzif/Lihatdulu/tree/29961f0).
- [Chair result fixture](https://github.com/Fafauzif/Lihatdulu/blob/29961f0/public/demo/kursi/job.json), [viewer HTML](https://github.com/Fafauzif/Lihatdulu/blob/29961f0/docs/handoff/explore/chair-explore.html), [refinement notes](https://github.com/Fafauzif/Lihatdulu/blob/29961f0/docs/handoff/refinement.md), and [local seven-take manifest](https://github.com/Fafauzif/Lihatdulu/blob/cbf69f0/docs/handoff/scan-evidence-manifest.json).
- [Public demo home](https://lihatdulu-sooty.vercel.app/) and [verified but expiring revised proposal copy](https://filebin.net/lihatdulu-890072a5c375b56d/LihatDulu_UISP16_Proposal_Revised.docx). Prefer the archived DOCX over the old Filebin URL.

The proposal's References section contains its linked research and original publications. The historical context includes earlier source provenance, survey design, figure notes, and additional attachments stored or linked in the prior work.

## Rebuild when needed

Ordinary revision is possible directly in Word. The following are optional when recomposing figures or repeating the original document assembly. Run commands from this repository root in a working copy. The build script rebuilds from the commented proposal (3), so it will replace the clean output with the revision embodied in the script. Keep subsequent edits in the new DOCX or port them back to the script before rebuilding.

```sh
python -m pip install python-docx Pillow lxml pymupdf
python revision/chart_assets.py
python revision/build.py
```

The placed visuals ship ready to use. For fresh exports, the exhibit and marketing generators use Inkscape. Software screenshot regeneration uses a pinned LihatDulu checkout at `revision/product/checkout`, Node and a local Chromium/Playwright environment. Run `npm ci` and `npm run build` in the pinned checkout before using `revision/product/capture.py`. The product figure script also reads a condition photo from that checkout. The original nine TeX exhibits can be regenerated with XeLaTeX per `revision/assets/README.md`.

After changing the Word document, export a PDF with fields refreshed. Inspect the desk review copy, then use `python revision/review.py path/to/render-folder` for page grids and `python revision/cache_toc.py path/to/render-folder` to validate and cache matching page labels. Use the packaged figures, links and cover placeholders if the rendering environment differs.
