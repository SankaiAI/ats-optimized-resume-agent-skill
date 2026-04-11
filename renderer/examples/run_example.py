"""
run_example.py — generates a sample .docx using the pre-built resume JSON.

Run from the resume_skill/ directory:
    cd resume_skill
    python examples/run_example.py

Or from anywhere:
    python examples/run_example.py --out path/to/output.docx

What this does:
  1. Loads examples/sample_resume_json.json (pre-built tailored resume)
  2. Validates the JSON
  3. Calls ResumeRenderer to produce a Word document
  4. Saves to examples/output/alex_chen_stripe.docx by default

The sample JSON represents Alex Chen's resume tailored for a Stripe
Senior Data Analyst role. See sample_master_resume.md and sample_jd.md
for the source material.

To test your own resume JSON:
    python examples/run_example.py --json path/to/your_resume.json --out output.docx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make src importable
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.rendering.config import RenderConfig
from src.rendering.render_docx import ResumeRenderer
from src.schemas.resume_schema import TailoredResume
from src.utils.utils import load_json
from src.validation.validate_output import validate


DEFAULT_JSON = ROOT / "examples" / "sample_resume_json.json"
DEFAULT_OUT = ROOT / "examples" / "output" / "alex_chen_stripe.docx"


def parse_args():
    p = argparse.ArgumentParser(description="Generate sample resume DOCX")
    p.add_argument("--json", default=str(DEFAULT_JSON),
                   help="Path to resume JSON (default: sample_resume_json.json)")
    p.add_argument("--out", default=str(DEFAULT_OUT),
                   help="Output .docx path")
    return p.parse_args()


def main():
    args = parse_args()

    print("=" * 60)
    print("Resume DOCX Generator — Example Run")
    print("=" * 60)

    # ── Load ─────────────────────────────────────────────────────────────────
    json_path = Path(args.json)
    if not json_path.exists():
        print(f"ERROR: JSON file not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    print(f"\nLoading: {json_path.name}")
    raw = load_json(json_path)
    resume = TailoredResume.from_dict(raw)
    print(f"Candidate: {resume.header.name}")
    print(f"Target:    {resume.target_role} @ {resume.target_company}")
    print(f"Level:     {resume.candidate_level}")
    print(f"Sections:  {' → '.join(resume.section_order)}")

    # ── Validate ─────────────────────────────────────────────────────────────
    print("\n── Validation ──────────────────────────────────────────────")
    result = validate(resume)
    print(result.report())
    if not result.passed:
        print("\nValidation errors found. Rendering anyway for inspection...\n")

    # ── Render ───────────────────────────────────────────────────────────────
    print("\n── Rendering DOCX ──────────────────────────────────────────")

    # Customize the renderer config here if desired
    config = RenderConfig(
        # FONTS — change these to swap the entire document font
        font_name="Calibri",
        font_name_heading="Calibri",
        name_font_size=22,
        body_font_size=10,
        section_title_size=11,

        # SPACING — tightened to help fit more content per page
        section_spacing_before=6,
        section_spacing_after=1,
        bullet_spacing_after=1,
        role_spacing_before=3,

        # BORDERS — set show_section_bottom_border=False to remove divider lines
        show_section_bottom_border=True,
        section_border_color="1F3864",
        section_border_size=12,

        # PAGE MARGINS — slightly tighter top/bottom to recover vertical space
        margin_top_inches=0.55,
        margin_bottom_inches=0.55,
        margin_left_inches=0.75,
        margin_right_inches=0.75,
    )

    renderer = ResumeRenderer(config=config)
    out_path = renderer.render(resume, args.out)

    print(f"\nDOCX saved: {out_path}")
    print("\nOpen the file in Microsoft Word or LibreOffice to review.")
    print("=" * 60)


if __name__ == "__main__":
    main()
