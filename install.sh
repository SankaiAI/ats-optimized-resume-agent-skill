#!/usr/bin/env bash
# install.sh — installs the build-tailored-resume Claude Code skill
#
# Usage:
#   ./install.sh              # interactive prompt — asks which scope
#   ./install.sh --user       # user scope  — available in ALL your projects
#   ./install.sh --project    # project scope — shared via .claude/settings.json
#   ./install.sh --local      # local scope  — this machine only, not committed

set -e

SKILL_NAME="build-tailored-resume"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCOPE=""
PROJECT_PATH=""

# ── Parse flags ───────────────────────────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    --user)             SCOPE="user"    ;;
    --project)          SCOPE="project" ;;
    --local)            SCOPE="local"   ;;
    --project-path=*)   PROJECT_PATH="${arg#*=}" ;;
  esac
done

echo ""
echo "============================================================"
echo "  build-tailored-resume - Claude Code Skill Installer"
echo "============================================================"

# ── Interactive scope selection when no flag given ────────────────────────────
if [[ -z "$SCOPE" ]]; then
  echo ""
  echo "  Where do you want to install this skill?"
  echo ""
  echo "  [1] User    - available in ALL your projects (recommended)"
  echo "                installs to: ~/.claude/skills/"
  echo ""
  echo "  [2] Project - current project only, shared with your team"
  echo "                installs to: <project-root>/.claude/skills/"
  echo "                committed to git via .claude/settings.json"
  echo ""
  echo "  [3] Local   - current project only, NOT committed to git"
  echo "                installs to: <project-root>/.claude/skills/"
  echo "                stays on this machine only"
  echo ""

  while true; do
    read -rp "  Enter 1, 2, or 3: " CHOICE
    case "$CHOICE" in
      1) SCOPE="user";    break ;;
      2) SCOPE="project"; break ;;
      3) SCOPE="local";   break ;;
      *) echo "  Please enter 1, 2, or 3." ;;
    esac
  done
  echo ""
fi

echo "  Scope: $SCOPE"

# ── Determine target skills directory ─────────────────────────────────────────
case "$SCOPE" in
  user)
    SKILLS_DIR="$HOME/.claude/skills"
    ;;
  project|local)
    if [[ -n "$PROJECT_PATH" ]]; then
      PROJECT_ROOT="$PROJECT_PATH"
    else
      PROJECT_ROOT="$(pwd)"
      while [[ "$PROJECT_ROOT" != "/" ]]; do
        if [[ -d "$PROJECT_ROOT/.git" || -d "$PROJECT_ROOT/.claude" ]]; then break; fi
        PROJECT_ROOT="$(dirname "$PROJECT_ROOT")"
      done
    fi
    SKILLS_DIR="$PROJECT_ROOT/.claude/skills"

    if [[ "$SCOPE" == "local" ]]; then
      echo "  Note: Add .claude/skills/ to .gitignore to keep this local."
    fi
    ;;
esac

DEST="$SKILLS_DIR/$SKILL_NAME"
echo "  Target: $DEST/SKILL.md"
echo ""

# ── Step 1: pip install the Python package ────────────────────────────────────
echo "[1/2] Installing resume-skill Python package..."
pip install "$SCRIPT_DIR/renderer" --quiet
echo "      Done - 'resume-skill' CLI is now available in PATH."

# ── Step 2: Copy SKILL.md into named subdirectory ─────────────────────────────
echo ""
echo "[2/2] Copying SKILL.md -> $DEST/SKILL.md"
mkdir -p "$DEST"
cp "$SCRIPT_DIR/SKILL.md" "$DEST/SKILL.md"
echo "      Done."

echo ""
echo "============================================================"
echo "  Installation complete!"
echo ""
echo "  Verify:         resume-skill --help"
echo "  Use in Claude:  /build-tailored-resume"
echo "============================================================"
echo ""
