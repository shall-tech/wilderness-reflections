# Editorial Decisions

## 2026-07-14 - Initial intake baseline

- The repository contained no prior manuscript batch, so intake begins at the front cover.
- PDF pages 1-8 were visually inspected to establish the original page sequence.
- The first batch stops after "The Bridge Builder" on original page 9 so each commit remains small and reviewable.
- The booklet attribution "William Allen Droomgule" is preserved in the manuscript. The spelling appeared questionable but was treated as a source-text issue rather than an OCR error; the later verification pass documented the correction in metadata.

## 2026-07-20 - Verification pass begins

- Source verification updates metadata and research notes without silently rewriting the booklet transcription.
- The page-9 spelling "William Allen Droomgule" is confirmed as a booklet error for Will Allen Dromgoole. It remains preserved in `BOOKLET_AUTHOR` and the displayed attribution, with the correction recorded in `VERIFIED_AUTHOR`.
- Retitled, rearranged, or modernized selections are labeled by relationship rather than normalized to an external edition.
