# Editorial Conventions

## Intake transcription

- The scanned booklet is the authority for wording, order, titles, and booklet attributions.
- Obvious OCR substitutions are corrected while transcribing; apparent errors printed in the booklet are preserved and flagged for verification.
- Original page boundaries are represented by hidden Original Booklet Page comments.
- Verse lineation and paragraph breaks follow the scan. Decorative type and running footers are not reproduced in the manuscript.
- Untitled works receive a descriptive title in square brackets for repository navigation; the metadata records that the title is editorial.
- Intake records use STATUS: NEEDS RESEARCH, RELATIONSHIP: Unknown, and SOURCE_CONFIDENCE: Low until a separate verification pass is completed.

## Source verification

- Verification changes metadata, not the transcribed booklet text. Differences from an authoritative or well-supported source are described as variants, adaptations, excerpts, or paraphrases.
- `STATUS: VERIFIED` means that the work and attribution have been identified with high confidence; it does not mean the booklet reproduces the source verbatim.
- `STATUS: ATTRIBUTION UNRESOLVED` means a focused search found conflicting or inadequate evidence; the entry has been checked but should not be presented as author-verified.
- `SOURCE_VERIFIED: Yes` records a source comparison. `SOURCE_CONFIDENCE` describes the strength of the available evidence.
- Booklet titles and attributions remain exactly as printed in `TITLE` and `BOOKLET_AUTHOR`; corrected identities belong in `VERIFIED_AUTHOR`, `RELATIONSHIP`, and `NOTES`.
- Verification sources and comparison findings are recorded in `research/verification-log.md` so the manuscript metadata remains compact.

## Source-corrected edition

- Files in `edited/` form a separate reading edition. They never replace or silently modify the scan-faithful files in `manuscript/`.
- The edited edition preserves the booklet's selection boundaries. A booklet excerpt remains an excerpt; it is not expanded into the complete work.
- `WORK_SCOPE` uses one or more controlled values: `Complete`, `Excerpt`, `Abridged`, `Adapted`, `Composite`, or `Fragment`.
- A reader-facing scope line identifies excerpts and other non-complete forms beneath each title.
- `EDITION_STATUS: Source restored` means the displayed wording follows the cited source witness within the booklet's selection boundaries.
- `EDITION_STATUS: Booklet text retained` means reliable source wording could not be reproduced or established. The reason is stated in `EDITION_NOTE`.
- `EDITION_STATUS: Source identified; text not reproduced` means the original work is identified, but its text is omitted because a reliable reproducible witness or publication right is unavailable.
- Titles, author names, and work identities follow the verified source when confidence is sufficient. Unresolved attributions remain explicitly unresolved.
- For translated works, `TEXT_WITNESS` names the selected translation. The edition does not blend translations.
- Public-domain source text may be reproduced. A copyrighted source is identified and linked, but an unlicensed complete work or substantial replacement text is not copied into the repository.
- Every edited entry retains its original `WR-ID` so it can be reconciled with the manuscript and verification log.

## Scan mapping

The current source PDF contains 84 scanned leaves. The first content sequence is:

| PDF page | Original booklet page | Content |
| ---: | ---: | --- |
| 1 | Cover | Front cover |
| 2 | Unnumbered | Introduction |
| 3 | Unnumbered | Blank |
| 4 | Unnumbered | Table of contents |
| 5 | Unnumbered | Section artwork |
| 6 | 7 | Life divider |
| 7 | 8 | Blank |
| 8 | 9 | Life content begins |

The scan order around pages 20-21 is reversed: PDF page 19 contains original page 21, while PDF page 20 contains original page 20. The canonical manuscript restores the printed page order.

The scan moves directly from the Knowledge and Wisdom divider on original page 31 to content on original page 33. Original page 32 is treated as the customary blank reverse of the divider, but no separate scanned leaf is present.

Near the Beauty section, the scan moves from original page 51 to the Beauty divider on original page 53, then directly to content on original page 55. Original pages 52 and 54 are treated as blank reverses, but neither is present as a separate scanned leaf.

At the transition from Beauty to Wilderness, the scan moves from original page 63 directly to the Wilderness divider on original page 65. Original page 64 is treated as the blank reverse of the preceding content leaf, but no separate scanned leaf is present.

The scan moves directly from the Wilderness divider on original page 65 to content on original page 67. Original page 66 is treated as the customary blank reverse of the divider, but no separate scanned leaf is present.

At the transition from Wilderness to the Author Index, the scan moves from original page 79 directly to the Author Index divider on original page 81. Original page 80 is treated as the blank reverse of the preceding content leaf, but no separate scanned leaf is present.

The updated scan supplies the complete Author Index on original pages 82-84 and the complete First Line Index on original pages 86-90. It ends with Sources on original page 91. Blank reverse leaves omitted during scanning are represented only by the inferred-page notes above.
