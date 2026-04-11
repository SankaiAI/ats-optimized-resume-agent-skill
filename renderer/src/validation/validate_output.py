"""
Resume JSON validation — runs before the DOCX renderer.

Catches missing fields, broken URLs, placeholder text, duplicate bullets,
and banned wording patterns so rendering doesn't produce a broken document.
"""

from __future__ import annotations

import re
import urllib.parse
from dataclasses import dataclass, field
from typing import List

from ..schemas.resume_schema import TailoredResume

# ── Wording patterns to flag ─────────────────────────────────────────────────

BANNED_PHRASES = [
    r"\bresponsible for\b",
    r"\bhelped (with|to)\b",
    r"\bassisted (with|in)\b",
    r"\bsupported\b.{0,30}\bteam\b",  # "supported the team" duty-dump pattern
    r"\bpassionate (about|for)\b",
    r"\bresults[- ]driven\b",
    r"\bvisionary\b",
    r"\bdynamic professional\b",
    r"\bthrive[sd]? in\b",
    r"\bfast[- ]paced environment\b",
    r"\bimproved performance\b(?!\s+by)",    # vague, no metric
    r"\benhanced efficiency\b(?!\s+by)",
    r"\bTODO\b",
    r"\bPLACEHOLDER\b",
    r"\bXXX\b",
    r"\bTBD\b",
    r"\[\[",  # unclosed template brackets
]

VALID_URL_SCHEMES = {"http", "https", "mailto"}


@dataclass
class ValidationResult:
    passed: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def error(self, msg: str):
        self.errors.append(msg)
        self.passed = False

    def warn(self, msg: str):
        self.warnings.append(msg)

    def report(self) -> str:
        lines = []
        status = "PASS" if self.passed else "FAIL"
        lines.append(f"Validation: {status}")
        if self.errors:
            lines.append(f"\nErrors ({len(self.errors)}):")
            for e in self.errors:
                lines.append(f"  ✗ {e}")
        if self.warnings:
            lines.append(f"\nWarnings ({len(self.warnings)}):")
            for w in self.warnings:
                lines.append(f"  ⚠ {w}")
        if self.passed and not self.warnings:
            lines.append("  All checks passed.")
        return "\n".join(lines)


def _check_url(url: str) -> bool:
    """Return True if URL looks plausible."""
    if not url:
        return True  # empty is fine (optional fields)
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.scheme in VALID_URL_SCHEMES and bool(parsed.netloc or parsed.path)
    except Exception:
        return False


def _check_banned(text: str) -> List[str]:
    """Return list of banned phrases found in text."""
    hits = []
    for pattern in BANNED_PHRASES:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append(pattern)
    return hits


def validate(resume: TailoredResume) -> ValidationResult:
    """
    Run all validation checks on a TailoredResume.

    Returns a ValidationResult with .passed, .errors, .warnings, and .report().
    """
    r = ValidationResult()

    # ── Required header fields ────────────────────────────────────────────
    h = resume.header
    if not h.name.strip():
        r.error("header.name is empty")
    if not h.email.strip():
        r.error("header.email is empty")
    if not h.phone.strip():
        r.error("header.phone is empty")

    # ── URL validity ─────────────────────────────────────────────────────
    for field_name, url in [
        ("header.linkedin", h.linkedin),
        ("header.github", h.github),
        ("header.website", h.website),
    ]:
        if url and not _check_url(url):
            r.error(f"Possibly malformed URL in {field_name}: {url!r}")

    for exp in resume.experience:
        for lk in exp.links:
            if lk.url and not _check_url(lk.url):
                r.warn(f"Possibly malformed URL in experience link: {lk.url!r}")

    for proj in resume.projects:
        if proj.url and not _check_url(proj.url):
            r.warn(f"Possibly malformed URL in project {proj.name!r}: {proj.url!r}")

    # ── No placeholder text ────────────────────────────────────────────────
    all_text_fields = [resume.summary] + [
        b for exp in resume.experience for b in exp.bullets
    ] + [
        b for proj in resume.projects for b in proj.bullets
    ]

    for text in all_text_fields:
        hits = _check_banned(text)
        if hits:
            snippet = text[:80].replace("\n", " ")
            for hit in hits:
                r.warn(f"Banned phrase pattern {hit!r} in: \"{snippet}...\"")

    # ── No duplicate bullets ───────────────────────────────────────────────
    all_bullets = [b for exp in resume.experience for b in exp.bullets]
    seen = set()
    for b in all_bullets:
        normalized = b.strip().lower()
        if normalized in seen:
            r.error(f"Duplicate bullet detected: \"{b[:80]}\"")
        seen.add(normalized)

    # ── Section order sanity ───────────────────────────────────────────────
    valid_sections = {
        "header", "summary", "skills", "experience",
        "projects", "education", "certifications", "awards"
    }
    for s in resume.section_order:
        if s not in valid_sections:
            r.warn(f"Unknown section name in section_order: {s!r}")

    if "header" not in resume.section_order:
        r.error("section_order must include 'header'")

    # ── Candidate level sanity ─────────────────────────────────────────────
    valid_levels = {
        "new_grad", "entry_level", "mid_level",
        "senior_ic", "manager", "director", "auto"
    }
    if resume.candidate_level not in valid_levels:
        r.warn(f"Unrecognized candidate_level: {resume.candidate_level!r}")

    # ── Humanization pass ─────────────────────────────────────────────────
    if not resume.metadata.humanization_pass_complete:
        r.warn("metadata.humanization_pass_complete is False — run humanization pass before finalizing")

    # ── Target fields present ─────────────────────────────────────────────
    if not resume.target_role:
        r.warn("target_role is empty")
    if not resume.target_company:
        r.warn("target_company is empty")

    return r
