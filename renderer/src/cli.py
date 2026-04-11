"""
CLI entry point — installed as the `resume-skill` command via pip.

Usage (after `pip install .`):
    resume-skill render  --input resume.json --output resume.docx
    resume-skill validate --input resume.json

skill.md calls this command so it works from any working directory,
regardless of where the package source lives.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .rendering.config import RenderConfig
from .rendering.render_docx import ResumeRenderer
from .schemas.resume_schema import TailoredResume
from .utils.utils import load_json
from .validation.validate_output import validate


def _render_cmd(args):
    raw = load_json(args.input)
    resume = TailoredResume.from_dict(raw)

    if not args.skip_validation:
        result = validate(resume)
        print(result.report())
        if not result.passed:
            print("\nValidation failed. Fix errors before rendering.", file=sys.stderr)
            sys.exit(1)

    renderer = ResumeRenderer(config=RenderConfig())
    out = renderer.render(resume, args.output)
    print(f"DOCX saved: {out}")


def _validate_cmd(args):
    raw = load_json(args.input)
    resume = TailoredResume.from_dict(raw)
    result = validate(resume)
    print(result.report())
    sys.exit(0 if result.passed else 1)


def main():
    parser = argparse.ArgumentParser(
        prog="resume-skill",
        description="Resume skill CLI - render and validate tailored resume JSON",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ── render ────────────────────────────────────────────────────────────
    render_p = sub.add_parser("render", help="Render resume JSON → .docx")
    render_p.add_argument("--input", "-i", required=True, help="Path to resume JSON")
    render_p.add_argument("--output", "-o", required=True, help="Output .docx path")
    render_p.add_argument("--skip-validation", action="store_true")
    render_p.set_defaults(func=_render_cmd)

    # ── validate ──────────────────────────────────────────────────────────
    val_p = sub.add_parser("validate", help="Validate resume JSON only")
    val_p.add_argument("--input", "-i", required=True, help="Path to resume JSON")
    val_p.set_defaults(func=_validate_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
