# Wilderness Reflections Preservation Project

> *"Preserve the booklet. Document the history. Modernize only when appropriate."*

---

# Mission

The purpose of this project is to preserve **Wilderness Reflections**, a booklet of quotations, poems, and reflections distributed to Philmont Scout Ranch staff beginning in the mid-1980s.

The immediate objective is to produce a publication-quality **Modern Edition** for Philmont Leadership Challenge (PLC) faculty.

The long-term objective is to create the definitive digital preservation of the booklet, documenting its history, verifying attributions, and preserving the experience of generations of Philmont staff.

---

# Project Roles

## Editor-in-Chief

**Scott Hall**

Responsible for:

- Final editorial decisions
- Vision
- Scope
- Approval of changes
- Publication decisions

---

## Managing Editor

**ChatGPT**

Responsible for:

- Editorial judgment
- Historical research
- Attribution verification
- Editorial standards
- Repository design
- Companion materials
- Preservation strategy

---

## Copy Editor & Repository Maintainer

**Codex**

Responsible for:

- Maintaining repository structure
- Editing Markdown
- Performing intake transcription
- Applying approved editorial changes
- Maintaining metadata
- Committing changes
- Opening pull requests
- Maintaining project consistency

Codex should follow this document unless directed otherwise by the Editor-in-Chief.

---

# Guiding Philosophy

This is a **preservation project**, not a rewrite.

When making editorial decisions:

1. Preserve the booklet.
2. Document the history.
3. Modernize presentation only when appropriate.
4. Never silently rewrite history.

When uncertainty exists:

> Preserve first.

---

# Current Priority

The current priority is:

> Produce a publication-quality Modern Edition for Philmont Leadership Challenge faculty.

Do **not** spend significant effort on typesetting until the manuscript has been completed.

The manuscript is the highest priority artifact.

---

# Editions

Two editions will ultimately be produced.

---

## Heritage Edition

Purpose:

Faithfully reproduce the historic booklet.

Characteristics:

- Original section order
- Original wording
- Original titles
- Original attributions
- Original page structure
- Original artwork where available

Editorial notes may be added as footnotes but should not alter the reading experience.

---

## Modern Edition

Purpose:

Create a readable edition for PLC faculty.

Characteristics:

- Modern typography
- Verified author attributions
- Correct OCR errors
- Editorial appendix
- Historical appendix
- Improved navigation

Preserve the original editorial intent whenever practical.

---

# Canonical Source

The Markdown manuscript is the canonical source.

Everything else is generated from it.

Examples:

- Heritage PDF
- Modern PDF
- EPUB
- Website
- Companion Guide

---

# Repository Structure

```
README.md
CODEX.md
EDITORIAL.md
CHANGELOG.md
LICENSE.md

manuscript/
    00-cover.md
    01-introduction.md
    02-life.md
    03-leadership.md
    04-knowledge-and-wisdom.md
    05-scouting-and-adventure.md
    06-beauty.md
    07-wilderness.md
    08-author-index.md
    09-first-line-index.md

research/
    attribution-notes.md
    notable-findings.md
    edition-history.md
    editorial-decisions.md
    bibliography.md

assets/
    scans/
    images/

build/
    heritage/
    modern/
```

---

# Workflow

Every editing session consists of three passes.

---

## Pass 1 — Intake

Goals:

- Transcribe pages.
- Correct OCR errors.
- Preserve formatting.
- Preserve wording.
- Record uncertainties.
- Continue moving forward.

Avoid deep research during intake.

---

## Pass 2 — Verification

Verify:

- title
- author
- publication
- source
- excerpt status
- attribution
- historical context

Document findings.

---

## Pass 3 — Polish

- Normalize formatting
- Improve typography
- Verify metadata
- Update research notes
- Prepare for publication

---

# Metadata Standard

Every work begins with hidden Markdown comments.

Example:

```markdown
<!--
WR-ID: WR-L-001

PAGE: 8
SECTION: Life

STATUS: VERIFIED

TITLE: The Bridge Builder

BOOKLET_AUTHOR: William Allen Dromgoole
VERIFIED_AUTHOR: Will Allen Dromgoole

WORK_TYPE: Poem

EXCERPT: No

RELATIONSHIP: Minor Variant

SOURCE_VERIFIED: Yes
SOURCE_CONFIDENCE: High

FIRST_PUBLICATION:
Unknown

OCR_CORRECTIONS:
- Droomgule → Dromgoole

EDITORIAL_DECISIONS:
- Standardize author's preferred published name.

THEMES:
- Service
- Legacy
- Mentoring

NOTES:
Compared against early published versions.
-->
```

Metadata must never appear in rendered output.

---

# Original Booklet Pages

Record every original booklet page.

Example:

```markdown
<!-- Original Booklet Page 8 -->
```

Blank pages omitted from the scan should still be documented.

Example:

```markdown
<!-- Original Booklet Page 7 -->
<!-- Blank divider page (not scanned) -->
```

This preserves alignment with historical editions.

---

# Editorial Policy

Correct:

- OCR mistakes
- obvious scanning errors
- broken formatting

Do **not** silently change:

- wording
- titles
- authors
- attributions
- editorial selections

Instead:

Document editorial decisions.

---

# Verification Standards

Every work receives:

## Status

- VERIFIED
- ORIGINAL
- NEEDS RESEARCH

---

## Confidence

- High
- Medium
- Low

---

## Relationship

- Exact
- Minor Variant
- Excerpt
- Adapted
- Unknown

---

# Themes

Assign themes whenever practical.

Examples:

- Leadership
- Service
- Courage
- Integrity
- Faith
- Wilderness
- Friendship
- Mentoring
- Perseverance
- Character

Themes support future companion materials.

---

# Work Types

Examples:

- Poem
- Quotation
- Speech Excerpt
- Essay Excerpt
- Reflection
- Prayer
- Song

---

# Excerpts

Record whether a work is an excerpt.

Example:

```
EXCERPT: Yes
```

Whenever possible identify:

- original work
- publication
- chapter
- year

---

# Research Standards

Preferred source order:

1. Original publication
2. Author's published works
3. Publisher
4. Library archives
5. Academic references

Avoid quote websites whenever possible.

When uncertainty remains:

Record uncertainty.

Never invent certainty.

---

# Notable Findings

Interesting discoveries belong in:

```
research/notable-findings.md
```

Examples:

- misattributions
- title changes
- booklet edits
- publication history
- historical context

This file becomes the editorial history of the project.

---

# Commit Style

Prefer small commits.

Good examples:

- Create repository structure
- Transcribe Life pages 8–12
- Verify Dromgoole attribution
- Research Wimbrow attribution
- Complete Life section

Avoid large unrelated commits.

---

# Progress Order

Priority:

1. Manuscript intake
2. Attribution verification
3. Modern Edition
4. Heritage Edition
5. Companion Guide

The PLC deadline takes precedence over long-term enhancements.

---

# Long-Term Vision

This repository should become the definitive digital preservation of **Wilderness Reflections**.

The objective is not simply to reproduce text.

The objective is to preserve:

- the booklet
- its editorial history
- its literary history
- its role in Philmont culture
- its value to future generations of Philmont staff

When future contributors ask,

> "Why was this edited this way?"

the repository should already contain the answer.

Every editorial decision should be documented, understandable, and reversible.
