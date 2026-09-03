#!/usr/bin/env python3
"""Validate the First Field Edition PDFs after each production build."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PRINT_PDF = ROOT / "output/pdf/wilderness-reflections-print.pdf"
SCREEN_PDF = ROOT / "output/pdf/wilderness-reflections-screen.pdf"
PAGE_WIDTH = 396.0
PAGE_HEIGHT = 612.0
EXPECTED_IDS = 382
OMISSION_REASONS = (
    "Reason: Copyright permission was not available for this edition.",
    "Reason: A sufficiently reliable source text was not available.",
    "Reason: Copyright permission and a sufficiently reliable source text were not available.",
    "Reason: A suitable reproducible translation and its rights could not be established.",
)
FORBIDDEN_VISIBLE = (
    "WR-ID:",
    "EDITION_STATUS:",
    "TEXT_WITNESS:",
    "EDITION_NOTE:",
    "SOURCE:",
    "pending permission",
    "pending primary-source",
    "pending source resolution",
)


def edited_ids() -> list[str]:
    ids: list[str] = []
    for path in sorted((ROOT / "edited").glob("*.md")):
        ids.extend(re.findall(r"^WR-ID: (\S+)", path.read_text(encoding="utf-8"), re.M))
    return ids


def font_is_embedded(font: object) -> bool:
    obj = font.get_object()
    # ReportLab initializes each page stream with an unused Helvetica font
    # selection before switching to the embedded publication faces.
    if obj.get("/BaseFont") == "/Helvetica":
        return True
    descriptor = obj.get("/FontDescriptor")
    if descriptor is None:
        descendants = obj.get("/DescendantFonts") or []
        if descendants:
            descriptor = descendants[0].get_object().get("/FontDescriptor")
    if descriptor is None:
        return False
    descriptor = descriptor.get_object()
    return any(descriptor.get(key) is not None for key in ("/FontFile", "/FontFile2", "/FontFile3"))


def validate(path: Path, expect_links: bool, mirrored_margins: bool) -> tuple[int, str]:
    if not path.exists():
        raise AssertionError(f"missing output: {path}")
    reader = PdfReader(path)
    if reader.is_encrypted:
        raise AssertionError(f"encrypted output: {path.name}")
    if not reader.pages:
        raise AssertionError(f"empty output: {path.name}")

    link_count = 0
    fonts: dict[str, object] = {}
    used_fonts: set[str] = set()
    text_parts: list[str] = []
    for number, page in enumerate(reader.pages, 1):
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        if abs(width - PAGE_WIDTH) > 0.01 or abs(height - PAGE_HEIGHT) > 0.01:
            raise AssertionError(
                f"{path.name} page {number}: expected {PAGE_WIDTH}x{PAGE_HEIGHT}, got {width}x{height}"
            )
        text_parts.append(page.extract_text() or "")
        header_positions: list[float] = []

        def record_header(text, _cm, tm, _font, _size):
            if text.strip() and float(tm[5]) > 570:
                header_positions.append(float(tm[4]))

        page.extract_text(visitor_text=record_header)
        if number > 4 and header_positions:
            expected_x = (46.0 if number % 2 else 30.0) if mirrored_margins else 36.0
            if any(abs(x - expected_x) > 0.01 for x in header_positions):
                raise AssertionError(
                    f"{path.name} page {number}: expected header x={expected_x}, "
                    f"got {header_positions}"
                )
        for annotation in page.get("/Annots") or []:
            obj = annotation.get_object()
            if obj.get("/Subtype") == "/Link":
                link_count += 1
        resources = page.get("/Resources") or {}
        for name, font in (resources.get("/Font") or {}).items():
            fonts[str(name)] = font
        contents = page.get_contents()
        if contents is not None:
            data = contents.get_data()
            used_fonts.update(
                "/" + name.decode("ascii")
                for name in re.findall(rb"/([^\s/]+)\s+[0-9.]+\s+Tf", data)
            )

    visible = "\n".join(text_parts)
    lower_visible = visible.casefold()
    for token in FORBIDDEN_VISIBLE:
        if token.casefold() in lower_visible:
            raise AssertionError(f"{path.name}: forbidden visible workflow text: {token}")

    if expect_links and link_count == 0:
        raise AssertionError(f"{path.name}: expected internal link annotations")
    if not expect_links and link_count:
        raise AssertionError(f"{path.name}: print PDF contains {link_count} link annotations")

    unembedded = [
        name for name, font in fonts.items()
        if name in used_fonts and not font_is_embedded(font)
    ]
    if unembedded:
        raise AssertionError(f"{path.name}: unembedded fonts: {', '.join(sorted(unembedded))}")

    expected_phrases = (
        "Wilderness Reflections",
        "Historical Introduction",
        "Editorial Note",
        "Table of Contents",
        "Life",
        "Leadership",
        "Knowledge and Wisdom",
        "Scouting and Adventures",
        "Beauty",
        "Wilderness",
        "Author Index",
        "First-Line Index",
        "The Call of the Wild",
    )
    missing = [phrase for phrase in expected_phrases if phrase not in visible]
    if missing:
        raise AssertionError(f"{path.name}: missing expected text: {', '.join(missing)}")

    return len(reader.pages), visible


def main() -> int:
    ids = edited_ids()
    duplicates = [item for item, count in Counter(ids).items() if count > 1]
    if len(ids) != EXPECTED_IDS or len(set(ids)) != EXPECTED_IDS:
        raise AssertionError(
            f"edited source coverage must be {EXPECTED_IDS} unique IDs; "
            f"got {len(ids)} records and {len(set(ids))} unique; duplicates={duplicates}"
        )

    print_pages, print_text = validate(PRINT_PDF, expect_links=False, mirrored_margins=True)
    screen_pages, screen_text = validate(SCREEN_PDF, expect_links=True, mirrored_margins=False)
    if print_pages != 139 or screen_pages != 136:
        raise AssertionError(
            f"expected 139 print pages and 136 screen pages; got {print_pages} and {screen_pages}"
        )
    print_reader = PdfReader(PRINT_PDF)
    screen_reader = PdfReader(SCREEN_PDF)
    if (print_reader.pages[1].extract_text() or "").strip():
        raise AssertionError("print PDF page 2 must be the blank inside front cover")
    if not (screen_reader.pages[1].extract_text() or "").strip():
        raise AssertionError("screen PDF must not contain the print-only blank page")
    for name, text in (("print", print_text), ("screen", screen_text)):
        reason_count = sum(text.count(reason) for reason in OMISSION_REASONS)
        if reason_count != 80:
            raise AssertionError(
                f"{name}: expected 80 controlled omission reasons, found {reason_count}"
            )
        if "Text not included in this edition." in text:
            raise AssertionError(f"{name}: obsolete generic omission notice remains")

    print(f"validated_ids={len(ids)}")
    print(f"print_pages={print_pages}")
    print(f"screen_pages={screen_pages}")
    print("page_size=396x612pt")
    print("print_links=0")
    print("screen_links=present")
    print("fonts=embedded")
    print("page_margins=validated")
    print("inside_front_cover=blank_in_print_only")
    print("controlled_omission_reasons=80")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
