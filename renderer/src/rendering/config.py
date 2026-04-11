"""
RenderConfig — all layout knobs in one place.

===== HOW TO CUSTOMIZE =====

FONTS
-----
  font_name             Body text font (bullets, contact line, etc.)
  font_name_heading     Section title font
  name_font_size        Candidate name at the top (points)
  contact_font_size     Contact line / URL text (points)
  section_title_size    Section heading text (points)
  body_font_size        Bullet and role text (points)

SPACING
-------
  section_spacing_before   Space above each section title (points)
  section_spacing_after    Space below section title / before content (points)
  bullet_spacing_before    Space above each bullet (points)
  bullet_spacing_after     Space below each bullet (points)
  role_spacing_before      Space above each job/edu heading row (points)
  line_spacing             Line spacing multiplier (1.0 = single, 1.15 = Word default)

BORDERS & COLORS
-----------------
  show_section_bottom_border   True = draw a line under section titles
  section_border_color         Hex color for section divider lines (no #)
  section_border_size          Border weight in half-points (12 = 1.5pt, 6 = 0.75pt)
  name_color                   Hex for candidate name
  section_title_color          Hex for section title text
  link_color                   Hex for hyperlinks

PAGE
----
  page_width_inches    Total page width
  page_height_inches   Total page height
  margin_top_inches    Top margin
  margin_bottom_inches Bottom margin
  margin_left_inches   Left margin
  margin_right_inches  Right margin

SECTION ORDER
-------------
  default_section_order   Fallback when resume JSON has no section_order field.
                          List elements: header | summary | skills | experience |
                                         projects | education | certifications | awards

  The JSON field metadata.section_order (or top-level section_order) overrides this.
  So you can change order per resume without touching this file.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class RenderConfig:
    # ── FONTS ──────────────────────────────────────────────────────────────
    font_name: str = "Calibri"
    font_name_heading: str = "Calibri"

    name_font_size: int = 22        # pt  ← resize candidate name
    contact_font_size: int = 10     # pt
    section_title_size: int = 11    # pt  ← section headers
    body_font_size: int = 10        # pt  ← bullets and body text
    role_title_size: int = 10       # pt  ← job title / company line

    # ── SPACING ────────────────────────────────────────────────────────────
    section_spacing_before: int = 6    # pt  ← gap before section title
    section_spacing_after: int = 1     # pt  ← gap after section title
    bullet_spacing_before: int = 0     # pt
    bullet_spacing_after: int = 1      # pt
    role_spacing_before: int = 3       # pt  ← gap before each job heading
    line_spacing: float = 1.0          # multiplier

    # ── BORDERS & COLORS ───────────────────────────────────────────────────
    show_section_bottom_border: bool = True    # ← toggle section divider lines
    section_border_color: str = "1F3864"       # hex (no #) — dark navy
    section_border_size: int = 12              # half-points (12 = 1.5pt)

    name_color: str = "1F3864"                 # hex for candidate name
    section_title_color: str = "1F3864"        # hex for section heading text
    body_color: str = "000000"
    link_color: str = "0563C1"                 # standard Word hyperlink blue

    # ── PAGE ───────────────────────────────────────────────────────────────
    page_width_inches: float = 8.5
    page_height_inches: float = 11.0
    margin_top_inches: float = 0.60
    margin_bottom_inches: float = 0.60
    margin_left_inches: float = 0.75
    margin_right_inches: float = 0.75

    # ── SECTION ORDER ──────────────────────────────────────────────────────
    # Overridden per resume by section_order in the resume JSON.
    default_section_order: List[str] = field(default_factory=lambda: [
        "header",
        "summary",
        "skills",
        "experience",
        "projects",
        "education",
        "certifications",
        "awards",
    ])

    # ── BULLET INDENT (inches from left margin) ────────────────────────────
    bullet_indent_left: float = 0.25
    bullet_hanging: float = 0.15
