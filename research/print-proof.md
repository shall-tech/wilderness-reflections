# First Field Edition Digital Proof

## Status

Digital proof completed August 1, 2026.

- Print PDF: `output/pdf/wilderness-reflections-print.pdf`
- Screen/archive PDF: `output/pdf/wilderness-reflections-screen.pdf`
- Print length: 137 pages
- Screen length: 135 pages
- Finished page size: 5.5 × 8.5 inches (396 × 612 points)

The page-count difference is intentional. The print file uses mirrored coil-safe margins; the screen file uses balanced margins and internal navigation, producing slightly different line and page breaks. Each file has its own regenerated table of contents and index references.

## Content assembly

- Historical cover epigraph retained.
- Historical introduction retained and explicitly labeled.
- Present-edition editorial and rights note added.
- All six source-corrected thematic sections included.
- All 382 selections retained in their canonical order.
- Eighty-three selections carry the neutral notice `Text not included in this edition.` under the approved rights/source-witness policy.
- Repository-facing workflow language is suppressed from the reading edition.
- Author and first-line indexes regenerated from final pagination.
- Omitted selections remain discoverable in both indexes without reproducing protected first lines.

## Automated validation

- 382 unique edited IDs confirmed.
- Exact 396 × 612-point MediaBox confirmed on every page.
- Georgia publication faces embedded.
- Print PDF contains no link annotations.
- Screen PDF contains internal navigation and section bookmarks.
- No visible `WR-ID`, edition-status, text-witness, source, or editorial-note metadata.
- No visible “pending permission” workflow language.
- Eighty-three neutral omission notices confirmed.
- Both PDFs are unencrypted and contain extractable text.
- `git diff --check` passes.

## Visual validation

All 137 print pages were rendered to PNG at 110 dpi. Seven full-book contact sheets were reviewed, followed by full-size inspection of:

- cover and editorial-note pages;
- first body page;
- long poems and prose selections;
- section transitions;
- author-index opening;
- first-line-index opening;
- final edition note.

The initial proof exposed and corrected visible HTML break tags, double-escaped index text, stale running headers, and short-entry page splits. The final render shows no clipping, overlap, metadata leakage, broken characters, or visible markup.

## Remaining physical proof

The digital files are ready for a local physical proof. Before authorizing the complete run, inspect:

1. finished trim size and duplex orientation;
2. coil-punch clearance on both odd and even pages;
3. text size and contrast on the selected 60–70 lb uncoated stock;
4. long-poem line breaks and index legibility;
5. printed-cover order under the clear plastic front sheet;
6. dark poly back sheet and coil closure.

Any physical-proof corrections should be made through the build script and revalidated before production.
