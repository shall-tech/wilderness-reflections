# First Field Edition

The publication build assembles the source-corrected reading edition into two 5.5 × 8.5-inch PDFs:

- `output/pdf/wilderness-reflections-print.pdf` is the production file. It uses mirrored coil-safe margins and contains no link annotations.
- `output/pdf/wilderness-reflections-screen.pdf` is the archive and screen-reading file. It uses balanced margins and includes internal navigation.

The build reads the six canonical files in `edited/`. It does not alter or duplicate their selection text. The historical cover epigraph and introduction come from `manuscript/00-cover.md` and `manuscript/01-introduction.md`; the table of contents and both indexes are regenerated for the new pagination.

## Reader-facing omission policy

Every selection retains its title, attribution, scope, position, and index presence. When text is not reproduced, the build combines the scope with a clear status line:

> Complete work — text not included.

It then supplies one controlled reason covering copyright permission, source-text reliability, both limitations, or translation and reproduction-rights uncertainty. Repository workflow notes such as “pending permission” are not printed. The editorial note explains that the reason records a publication decision and does not imply that permission was formally denied.

## Build

Use the bundled Codex Python runtime:

```sh
/Users/shall/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_print_edition.py
/Users/shall/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/validate_print_edition.py
```

Intermediate pagination files and rendered QA images belong under `tmp/pdfs/`. Final PDFs belong under `output/pdf/`.

## Physical specification

- Finished size: 5.5 × 8.5 inches, portrait
- Duplex, black and white
- Mirrored inner margin: at least 0.625 inch
- Coil binding on the left
- 60–70 lb uncoated interior stock
- 80–100 lb matte or uncoated printed cover
- Clear plastic front sheet and dark poly back sheet

The first physical proof must be checked for gutter clearance, duplex orientation, text size, line breaks, cover order, and plastic-sheet placement before the production run.
