"""
main.py — CLI entry point for the resume renderer.

Usage:
    python src/main.py --input path/to/resume.json --output path/to/resume.docx
    python src/main.py --input path/to/resume.json --output path/to/resume.docx --validate-only

The LLM (via skill.md) produces the JSON; this script turns it into a .docx.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Make src importable regardless of working directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rendering.config import RenderConfig
from src.rendering.render_docx import ResumeRenderer
from src.schemas.resume_schema import TailoredResume
from src.utils.utils import load_json
from src.validation.validate_output import validate


def parse_args():
    parser = argparse.ArgumentParser(
        description="Render a tailored resume JSON into a Word document (.docx)"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Path to the tailored resume JSON file"
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Path for the output .docx file"
    )
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Run validation but do not render the DOCX"
    )
    parser.add_argument(
        "--skip-validation", action="store_true",
        help="Skip validation and render directly"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # ── Load JSON ────────────────────────────────────────────────────────────
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    raw = load_json(input_path)
    resume = TailoredResume.from_dict(raw)

    # ── Validate ─────────────────────────────────────────────────────────────
    if not args.skip_validation:
        result = validate(resume)
        print(result.report())
        if not result.passed:
            print("\nValidation failed. Fix errors above before rendering.", file=sys.stderr)
            if not args.validate_only:
                sys.exit(1)

    if args.validate_only:
        return

    # ── Render ───────────────────────────────────────────────────────────────
    renderer = ResumeRenderer(config=RenderConfig())
    out = renderer.render(resume, args.output)
    print(f"\nDOCX saved to: {out}")


if __name__ == "__main__":
    main()
