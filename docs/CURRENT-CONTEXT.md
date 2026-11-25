# Current context for LihatDulu UISP16

## Resume from this revision

The latest document is `revision/output/LihatDulu_UISP16_Proposal_Revised.docx`. It is the clean Indonesian revision made from proposal (3). Proposal (3) and the separate comment export preserve the original review trail. The full earlier context remains in `upload/LihatDulu_MASTER_AI_CONTEXT_2026-11-25_Updated.md`.

The revision was explicitly authorized after the review plan. Future decisions should follow the next user's scope and protect already confirmed choices unless the user reopens them. Historical instructions to wait for approval applied to that completed revision stage.

## Current business design

LihatDulu is a secondhand household furniture marketplace. A buyer checks real condition photos, seller-entered dimensions, location, and how the item can be received. 3D or the dimension-based room preview appears where supported. The seller retains inventory until handover. Buyers pick up the item or choose third-party delivery for supported routes. The order retains the listing evidence for discrepancies at handover. Listing standards should work with original photos, dimensions, and condition notes when reconstruction is weak.

Launch near **UI Depok** in one serviceable kos cluster. Repeat furniture resellers anchor inventory and people moving out supply additional items. Start with a dense enough local catalog of tables, chairs, racks, and cabinets. Repeat in nearby clusters before expanding more widely.

Revenue on completed marketplace orders consists of a fixed **buyer service fee** and a percentage **seller commission**. Standard listings are free, delivery is a separate pass-through in the model, and fully canceled or refunded orders do not contribute these fees. B2B embedded catalogs/subscriptions come later and should be modeled separately, with API access tied to technical and support readiness.

| Horizon | Marketing execution | Expansion criterion |
|---|---|---|
| 0–6 months | Recruit repeat resellers, help outgoing renters list, and send incoming renters to the curated UI-area catalog | Complete listings, available stock, and orders that can be fulfilled locally |
| 6–12 months | Local creator content **“Muat Nggak?”** uses a real space constraint and takes the viewer to a real item or local collection | Fulfilled orders, acquisition cost per fulfilled order, and repeat seller activity |
| Year 2 onward | **Bursa Pindahan LihatDulu**, with taped-out kos layout, tagged secondhand furniture, QR to item, scheduled pickup reservations, and an assisted listing desk | Track published listings and fulfilled orders attributable to the event within 30 days, with cost per fulfilled order |

The offline campaign image is a **concept mockup**, not event documentation. Keep sample listing prices and QR artwork separate from verified prices and real campaign links. Use current product screenshots for product claims.

## Evidence

- Interim survey snapshot as of 25 November 2026. 50 respondents, 46 mahasiswa and four others. Of the 15 who considered a specific furniture listing, 13 struggled to judge condition, nine struggled to judge room fit, and eight cited pickup/delivery uncertainty. Eleven sought more information. All 15 in this module were students. Use the paired analysis in `survey-analysis/analysis.md` for more detail.
- The paired condition demo showed higher self-reported confidence for 29 of 50, no change for 14, and lower confidence for seven. Baseline and reveal were in a fixed order with multiple details changed. These responses are neither observed sales nor a causal test of one feature. Keep actual shopping behavior separate from the demo when updating.
- The revised CSV retains ordinal, multi-select, open text, column order, and row order. Exact collection timestamps were replaced with stable IDs. Preserve the order of identical question headers when analyzing the paired phases.
- Seller interview was still pending and the seller persona is a working profile. No interview findings or partner commitments were fabricated.
- Product proof uses screens from `29961f0`. The Sora example demonstrates the intended inspection and room workflow. The separate chair demo used an external KIRI Engine reconstruction for its GLB. It produced an approximately 1.95 MB refined file from 101 frames in about 1 minute 45 seconds under that recorded setup. Gaps remained and the viewer prioritized original photos. The revised proposal identifies that provenance in Appendix C.
- The proposed LihatDulu-managed reconstruction path builds on actual local **FFmpeg → COLMAP → Brush → SPZ** experiments. The seven recordings were of one physical chair, and some outputs showed fragments or haze. Do not attribute the vendor-assisted GLB results to the local stack. Use the appendix and historical source manifests for detail.
- National BPS context was updated to approximately Rp11.63 trillion annualized broad furniture spending, from Rp3,376 per capita per month × 287,198,400 × 12. It is a category spending benchmark, not used-furniture GMV or platform revenue. Base TAM/SAM/SOM on annual platform revenue from used-furniture orders. Model buyer fee × completed orders plus seller rate × goods GMV. Scope national TAM, serviceable Jabodetabek SAM, and capacity-constrained year-three SOM. Replace the earlier 1%-of-SAM GMV shortcut. A fee workbook and defensible used-furniture transaction inputs are still needed.

## Remaining work before submission

1. Bring in the teammate's finance workbook. Populate Bab V and Appendix E, sync the Executive Summary, and reconcile purchase volume, tariffs, GMV, revenue, expenses, cash, and funding with Bab III, Bab IV, and the revenue sizing.
2. Add the seller interview and a clean final survey export when available. Update Appendix B, §1.3 and persona grounding. Keep the initial ZIP snapshot as a reproducible baseline.
3. The user will design the blank cover. Complete or attach the official signed authorship material as required. Check the organizer's actual rules and deadline before submission.
4. After figures or copy change, render again, update the table of contents and confirm appendix links. The 31-page review render in this pack was checked in LibreOffice, with Liberation Serif used locally for Times New Roman. The Word styles specify Times New Roman.
5. Any website URL or judging QR needs a fresh anonymous route check. The historical 25 November check saw the public homepage return 200 and several deep routes return 404. Release branch evidence and successful local builds do not establish deployment.

The live Word revision was rendered and checked, with 28 placed figures, 22 native tables, and 38 cached TOC page labels. Library writeback was blocked by the account's storage limit. The last verified Filebin copy was scheduled to expire on 2 December 2026 at 21:51 WIB. The local copy inside this handoff is the durable working artifact.
