#!/usr/bin/env python3
"""Build the 5.5 x 8.5-inch First Field Edition PDFs."""

from __future__ import annotations

import html
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import portrait
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf"
TMP = ROOT / "tmp/pdfs"
PAGE = portrait((5.5 * inch, 8.5 * inch))
GEORGIA = Path("/System/Library/Fonts/Supplemental")
SECTION_FILES = (
    ("Life", "02-life.md"),
    ("Leadership", "03-leadership.md"),
    ("Knowledge and Wisdom", "04-knowledge-and-wisdom.md"),
    ("Scouting and Adventures", "05-scouting-and-adventures.md"),
    ("Beauty", "06-beauty.md"),
    ("Wilderness", "07-wilderness.md"),
)
OMITTED_STATUS = "Source identified; text not reproduced"


@dataclass
class Entry:
    wr_id: str
    section: str
    title: str
    author: str
    scope: str
    status: str
    blocks: list[str]
    first_line: str


class Marker(Flowable):
    def __init__(self, kind: str, key: str, label: str = "") -> None:
        super().__init__()
        self.kind = kind
        self.key = key
        self.label = label
        self.width = self.height = 0

    def draw(self) -> None:
        return


class EditionDoc(BaseDocTemplate):
    def __init__(self, path: Path, screen: bool) -> None:
        super().__init__(
            str(path), pagesize=PAGE, title="Wilderness Reflections — First Field Edition",
            author="Wilderness Reflections preservation project",
            subject="Source-corrected reading edition",
        )
        self.screen = screen
        self.entry_pages: dict[str, int] = {}
        self.section_pages: dict[str, int] = {}
        self.current_section = ""
        self._install_templates()

    def _install_templates(self) -> None:
        width, height = PAGE
        top, bottom = 40, 38
        if self.screen:
            odd_left = odd_right = even_left = even_right = 36
        else:
            odd_left, odd_right = 46, 30
            even_left, even_right = 30, 46

        def frame(name: str, left: float, right: float) -> Frame:
            return Frame(left, bottom, width - left - right, height - top - bottom,
                         id=name, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

        odd = PageTemplate("Odd", [frame("odd", odd_left, odd_right)], self._on_page,
                           autoNextPageTemplate="Even")
        even = PageTemplate("Even", [frame("even", even_left, even_right)], self._on_page,
                            autoNextPageTemplate="Odd")
        self.addPageTemplates([odd, even])

    def _on_page(self, canvas, doc) -> None:
        canvas.saveState()
        page = doc.page
        if page > 4:
            canvas.setFont("Georgia", 7.4)
            canvas.setFillColor(colors.HexColor("#555555"))
            if self.current_section:
                canvas.drawString(doc.pageTemplate.frames[0]._x1, PAGE[1] - 25, self.current_section)
            canvas.drawCentredString(PAGE[0] / 2, 22, str(page))
        canvas.restoreState()

    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, Marker):
            if flowable.kind == "entry":
                self.entry_pages[flowable.key] = self.page
                if self.screen:
                    self.canv.bookmarkPage(flowable.key)
            elif flowable.kind == "section":
                self.section_pages[flowable.key] = self.page
                self.current_section = flowable.label
                if self.screen:
                    name = "section-" + re.sub(r"[^a-z0-9]+", "-", flowable.key.casefold()).strip("-")
                    self.canv.bookmarkPage(name)
                    self.canv.addOutlineEntry(flowable.label, name, level=0, closed=False)
            elif flowable.kind == "header":
                self.current_section = flowable.label


def register_fonts() -> None:
    fonts = {
        "Georgia": "Georgia.ttf",
        "Georgia-Bold": "Georgia Bold.ttf",
        "Georgia-Italic": "Georgia Italic.ttf",
        "Georgia-BoldItalic": "Georgia Bold Italic.ttf",
    }
    for name, filename in fonts.items():
        pdfmetrics.registerFont(TTFont(name, str(GEORGIA / filename)))
    pdfmetrics.registerFontFamily(
        "Georgia", normal="Georgia", bold="Georgia-Bold",
        italic="Georgia-Italic", boldItalic="Georgia-BoldItalic",
    )


def clean_inline(value: str) -> str:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return value.replace("<br>", " ").replace("<br/>", " ")


def italic_text(line: str) -> str | None:
    line = line.strip()
    if len(line) >= 2 and line.startswith("*") and line.endswith("*"):
        return line[1:-1].strip()
    return None


def visible_text(value: str) -> str:
    value = re.sub(r"[*_`]", "", value)
    value = value.replace("\\", " ").replace("<br>", " ").replace("<br/>", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" []")


def parse_entries() -> list[Entry]:
    entries: list[Entry] = []
    pattern = re.compile(r"<!--\n(?P<meta>WR-ID: .*?)\n-->\n(?P<body>.*?)(?=\n<!--\nWR-ID:|\Z)", re.S)
    for section, filename in SECTION_FILES:
        text = (ROOT / "edited" / filename).read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            meta = dict(re.findall(r"^([A-Z_ -]+): (.*)$", match.group("meta"), re.M))
            body = re.sub(r"<!--.*?-->", "", match.group("body"), flags=re.S).strip()
            lines = body.splitlines()
            title_line = next((line for line in lines if line.startswith("## ")), None)
            if not title_line:
                raise ValueError(f"{meta['WR-ID']}: missing title")
            title = clean_inline(title_line[3:])
            content = lines[lines.index(title_line) + 1:]
            while content and not content[-1].strip():
                content.pop()
            author = clean_inline(meta.get("VERIFIED_AUTHOR", "Unknown"))
            if content and italic_text(content[-1]) is not None:
                content.pop()
            blocks = [block.strip() for block in re.split(r"\n\s*\n", "\n".join(content)) if block.strip()]
            status = meta.get("EDITION_STATUS", "Booklet text retained")
            first_line = ""
            if status != OMITTED_STATUS:
                for block in blocks:
                    candidate = visible_text(block.splitlines()[0])
                    if not candidate or italic_text(block) is not None:
                        continue
                    if candidate.casefold().startswith(("text omitted", "the source-corrected text")):
                        continue
                    first_line = candidate
                    break
            entries.append(Entry(
                wr_id=meta["WR-ID"], section=section, title=title, author=author,
                scope=meta.get("WORK_SCOPE", ""), status=status,
                blocks=blocks, first_line=first_line,
            ))
    ids = [entry.wr_id for entry in entries]
    if len(ids) != 382 or len(set(ids)) != 382:
        raise ValueError(f"expected 382 unique entries, got {len(ids)} records / {len(set(ids))} unique")
    omitted = sum(entry.status == OMITTED_STATUS for entry in entries)
    if omitted != 83:
        raise ValueError(f"expected 83 omitted selections, got {omitted}")
    return entries


def styles():
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Georgia",
            fontSize=9.35, leading=12.25, spaceAfter=6, textColor=colors.HexColor("#202020"),
            allowWidows=0, allowOrphans=0),
        "verse": ParagraphStyle("Verse", parent=base["BodyText"], fontName="Georgia",
            fontSize=9.15, leading=11.7, spaceAfter=6, leftIndent=5, textColor=colors.HexColor("#202020")),
        "title": ParagraphStyle("EntryTitle", parent=base["Heading2"], fontName="Georgia-Bold",
            fontSize=12.2, leading=14.4, spaceBefore=8, spaceAfter=3, keepWithNext=True),
        "scope": ParagraphStyle("Scope", parent=base["BodyText"], fontName="Georgia-Italic",
            fontSize=7.7, leading=9.7, textColor=colors.HexColor("#555555"), spaceAfter=5, keepWithNext=True),
        "author": ParagraphStyle("Author", parent=base["BodyText"], fontName="Georgia-Italic",
            fontSize=8.6, leading=10.5, alignment=TA_LEFT, spaceBefore=2, spaceAfter=8),
        "display": ParagraphStyle("Display", parent=base["Title"], fontName="Georgia-Bold",
            fontSize=27, leading=31, alignment=TA_CENTER, textColor=colors.HexColor("#173f32")),
        "subtitle": ParagraphStyle("Subtitle", parent=base["BodyText"], fontName="Georgia-Italic",
            fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#555555")),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontName="Georgia-Bold",
            fontSize=19, leading=23, textColor=colors.HexColor("#173f32"), spaceAfter=12),
        "front": ParagraphStyle("Front", parent=base["BodyText"], fontName="Georgia",
            fontSize=9.5, leading=13, spaceAfter=8),
        "toc": ParagraphStyle("TOC", parent=base["BodyText"], fontName="Georgia",
            fontSize=10, leading=15, leftIndent=8, rightIndent=8),
        "index": ParagraphStyle("Index", parent=base["BodyText"], fontName="Georgia",
            fontSize=7.8, leading=9.7, spaceAfter=1.7),
        "indexnote": ParagraphStyle("IndexNote", parent=base["BodyText"], fontName="Georgia-Italic",
            fontSize=7.8, leading=10, textColor=colors.HexColor("#555555"), spaceAfter=8),
    }


def paragraph_markup(block: str) -> str:
    lines = block.splitlines()
    rendered: list[str] = []
    for line in lines:
        line = line.rstrip()
        line = re.sub(r"\\$", "", line)
        line = re.sub(r"<br\s*/?>", "", line, flags=re.I)
        rendered.append(html.escape(line.strip()))
    text = "<br/>".join(rendered)
    if text.startswith("*") and text.endswith("*"):
        text = f"<i>{text[1:-1]}</i>"
    return text


def page_ref(label: str, wr_id: str, page: int, screen: bool) -> str:
    content = f"{html.escape(label)} <font color='#666666'>· {page}</font>"
    return f'<link href="#{wr_id}" color="#173f32">{content}</link>' if screen else content


def build_story(entries: list[Entry], st: dict, screen: bool,
                entry_pages: dict[str, int] | None = None,
                section_pages: dict[str, int] | None = None) -> list[Flowable]:
    story: list[Flowable] = []
    # Cover
    story += [Spacer(1, 120), Paragraph("Wilderness<br/>Reflections", st["display"]), Spacer(1, 32),
              Paragraph("The wisdom of the wise<br/>And the experience of the ages,<br/>May be preserved by quotation.", st["subtitle"]),
              Spacer(1, 8), Paragraph("— Isaac Disraeli", st["subtitle"]), Spacer(1, 95),
              Paragraph("FIRST FIELD EDITION · 2026", st["subtitle"]), PageBreak()]
    # Edition note/title page
    story += [Paragraph("Wilderness Reflections", st["h1"]),
              Paragraph("First Field Edition · Source-Corrected Reading Edition", st["subtitle"]), Spacer(1, 20),
              Paragraph("Editorial Note", st["h1"]),
              Paragraph("This edition preserves the historic booklet’s order and selection boundaries while restoring verified source wording where a reliable, reproducible witness is available.", st["front"]),
              Paragraph("Some selections are identified but not reproduced because publication permission or a sufficiently reliable reproducible text was unavailable. Their titles, attributions, scope, original positions, and index entries are retained, with a neutral omission notice in place of the selection text.", st["front"]),
              Paragraph("The historical transcription remains preserved separately. This reading edition corrects verified author identities and source wording without silently rewriting unresolved material.", st["front"]),
              Spacer(1, 18), Paragraph("Prepared for Philmont Leadership Challenge faculty.<br/>Oklahoma City · 2026", st["subtitle"]), PageBreak()]
    # Historical introduction
    story += [Paragraph("Historical Introduction", st["h1"]),
              Paragraph("The following introduction is preserved from the historic booklet.", st["scope"]),
              Paragraph("This collection is for the Philmont staff; past, present, and future. It has been an ongoing project since 1985. Started by Susie Dobbs, Laura Lampe, and Ed Ohnemus and edited into 5 editions by Russ Riegel. This is an expansion of their work to be enjoyed by all scouters.", st["front"]),
              Paragraph("To staff of past summers, whether riding the tube or rail, walking in a stand of aspen or skyscrapers, I hope this brings life to your memories of summers in New Mexico. To you during this summer, I feel that many of these quotes will help in your teachings and relating to the beauty around you. And to those working in future summers, I feel that many of these quotes will help you in the understanding of what Philmont has meant to me and other staff members.", st["front"]),
              Paragraph("The quotations have been arranged placing favorites first in each section.", st["front"]), PageBreak()]
    # Contents: one stable page in draft and final.
    story += [Paragraph("Table of Contents", st["h1"]), Spacer(1, 6)]
    for section, _ in SECTION_FILES:
        page = (section_pages or {}).get(section, "—")
        story.append(Paragraph(f"{html.escape(section)} <font color='#666666'>· {page}</font>", st["toc"]))
    story += [Spacer(1, 8), Paragraph("Author Index", st["toc"]), Paragraph("First-Line Index", st["toc"])]

    for section, _ in SECTION_FILES:
        story += [Marker("header", section, section), PageBreak(),
                  Marker("section", section, section), Spacer(1, 145),
                  Paragraph(section, st["display"]), Spacer(1, 18),
                  Paragraph("Source-Corrected Edition", st["subtitle"]), PageBreak()]
        for entry in (item for item in entries if item.section == section):
            entry_story: list[Flowable] = [Marker("entry", entry.wr_id, entry.title)]
            anchor = f'<a name="{entry.wr_id}"/>' if screen else ""
            entry_story.append(Paragraph(anchor + html.escape(entry.title), st["title"]))
            if entry.scope:
                entry_story.append(Paragraph(html.escape(entry.scope), st["scope"]))
            if entry.status == OMITTED_STATUS:
                entry_story.append(Paragraph("Text not included in this edition.", st["body"]))
            else:
                for block in entry.blocks:
                    workflow_text = visible_text(block).casefold()
                    if (
                        "pending permission" in workflow_text
                        or "pending primary" in workflow_text
                        or "pending source" in workflow_text
                        or "source-corrected text is not reproduced" in workflow_text
                        or "not reproduced here" in workflow_text
                    ):
                        entry_story.append(Paragraph("Additional text not included in this edition.", st["scope"]))
                        continue
                    if italic_text(block) is not None:
                        entry_story.append(Paragraph(paragraph_markup(block), st["scope"]))
                    else:
                        is_verse = len(block.splitlines()) > 1
                        entry_story.append(Paragraph(paragraph_markup(block), st["verse"] if is_verse else st["body"]))
            entry_story.append(Paragraph(html.escape(entry.author), st["author"]))
            entry_story.append(HRFlowable(width="100%", thickness=0.35, color=colors.HexColor("#b8b8b0"), spaceAfter=3))
            visible_length = sum(len(visible_text(block)) for block in entry.blocks)
            story.append(KeepTogether(entry_story) if visible_length < 700 else entry_story[0])
            if visible_length >= 700:
                story.extend(entry_story[1:])

    if entry_pages is not None:
        story += [Marker("header", "Author Index", "Author Index"), PageBreak(),
                  Marker("section", "Author Index", "Author Index"),
                  Paragraph("Author Index", st["h1"]),
                  Paragraph("Verified or qualified creator credits are shown as recorded in the edition. Page numbers refer to this edition.", st["indexnote"])]
        author_rows: list[tuple[str, Entry]] = sorted(
            ((entry.author, entry) for entry in entries),
            key=lambda item: (item[0].casefold(), item[1].title.casefold()),
        )
        for author, entry in author_rows:
            label = f"{author} — {entry.title}"
            story.append(Paragraph(page_ref(label, entry.wr_id, entry_pages[entry.wr_id], screen), st["index"]))

        story += [Marker("header", "First-Line Index", "First-Line Index"), PageBreak(),
                  Marker("section", "First-Line Index", "First-Line Index"),
                  Paragraph("First-Line Index", st["h1"]),
                  Paragraph("† marks a selection whose text is not reproduced; its title is indexed in place of a protected or unavailable first line.", st["indexnote"])]
        first_rows: list[tuple[str, Entry]] = []
        for entry in entries:
            label = entry.first_line if entry.first_line else f"† [Text not reproduced] — {entry.title}"
            if len(label) > 92:
                label = label[:89].rstrip() + "..."
            first_rows.append((label, entry))
        for label, entry in sorted(first_rows, key=lambda item: item[0].lstrip("† [").casefold()):
            story.append(Paragraph(page_ref(label, entry.wr_id, entry_pages[entry.wr_id], screen), st["index"]))

        story += [Marker("header", "About This Edition", "About This Edition"), PageBreak(),
                  Marker("section", "About This Edition", "About This Edition"),
                  Paragraph("About This Edition", st["h1"]),
                  Paragraph("Wilderness Reflections began as a Philmont staff collection in 1985 and grew through several historical editions. This First Field Edition was prepared from a page-verified transcription of the surviving booklet and a selection-by-selection source review.", st["front"]),
                  Paragraph("The repository preserves the scan-faithful transcription, source evidence, unresolved attribution questions, and the canonical source-corrected Markdown used for this publication. Eighty-three identified selections are represented without their source text because permission or a sufficiently reliable reproducible witness was unavailable.", st["front"]),
                  Paragraph("First Field Edition · 2026", st["subtitle"])]
    return story


def build_one(path: Path, entries: list[Entry], screen: bool,
              entry_pages: dict[str, int] | None = None,
              section_pages: dict[str, int] | None = None) -> EditionDoc:
    doc = EditionDoc(path, screen=screen)
    doc.build(build_story(entries, styles(), screen, entry_pages, section_pages))
    return doc


def main() -> None:
    register_fonts()
    entries = parse_entries()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    for screen, name in ((False, "print"), (True, "screen")):
        draft = build_one(TMP / f"{name}-pagination.pdf", entries, screen)
        final_path = OUTPUT / f"wilderness-reflections-{name}.pdf"
        final = build_one(final_path, entries, screen, draft.entry_pages, draft.section_pages)
        if final.entry_pages != draft.entry_pages:
            raise RuntimeError(f"{name}: body pagination changed between passes")
        if len(final.entry_pages) != 382:
            raise RuntimeError(f"{name}: expected 382 entry destinations")
        print(f"built {final_path.relative_to(ROOT)} ({final.page} pages)")


if __name__ == "__main__":
    main()
