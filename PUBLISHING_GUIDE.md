# Publishing & Installation Guide

This guide walks you through finalizing each of the three installation options.
Complete them in order, or jump to whichever you need.

---

## Option A — Claude Code Plugin Marketplace

### What you need before starting
- A GitHub account
- Git installed locally
- The `resume_skill/` folder from this project

---

### Step 1 — Create the GitHub repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `resume-skill`
   - **Description:** `Claude Code plugin — tailors a master resume to a job description and generates a polished .docx`
   - **Visibility:** Public (required for the official marketplace)
   - Do NOT initialize with README (you already have one)
3. Click **Create repository**

---

### Step 2 — Push the plugin to GitHub

Open a terminal in the `resume_skill/` folder and run:

```bash
git init
git add .
git commit -m "Initial release: resume-skill Claude Code plugin v0.1.0"
git remote add origin https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git
git branch -M main
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

---

### Step 3 — Update `plugin.json` with your real URLs

Open `.claude-plugin/plugin.json` and replace the placeholder URLs:

```json
{
  "name": "resume-skill",
  "version": "0.1.0",
  "description": "Transforms a master resume and job description into a tailored, ATS-optimized Word document (.docx) with human-sounding bullets and deterministic table-based layout.",
  "author": {
    "name": "YOUR NAME",
    "url": "https://github.com/YOUR-USERNAME"
  },
  "repository": "https://github.com/SankaiAI/ats-optimized-resume-agent-skill",
  "homepage": "https://github.com/SankaiAI/ats-optimized-resume-agent-skill#readme",
  "license": "MIT",
  "keywords": ["resume", "docx", "ats", "job-search", "career"],
  "skills": "./skills/"
}
```

Then commit and push:

```bash
git add .claude-plugin/plugin.json
git commit -m "Update plugin.json with real author and repository URLs"
git push
```

---

### Step 4 — Test the plugin locally before submitting

Run this from outside the `resume_skill/` folder to load the plugin for one session:

```bash
claude --plugin-dir ./resume_skill
```

Inside Claude Code, verify:
- `/resume-skill:build-tailored-resume` appears in the skill list (type `/` to see)
- Running it starts the resume workflow
- `resume-skill render --help` works in the terminal (the `bin/` wrapper is active)

If anything is broken, fix it before submitting to the marketplace.

You can also run the official validator:
```bash
claude plugin validate ./resume_skill
```

Fix any errors it reports.

---

### Step 5 — Submit to the official marketplace

Go to one of these two submission forms (both go to the same place):
- https://claude.ai/settings/plugins/submit
- https://platform.claude.com/plugins/submit

Fill in the form:
- **Plugin name:** `resume-skill`
- **Repository URL:** `https://github.com/SankaiAI/ats-optimized-resume-agent-skill`
- **Description:** paste from `plugin.json`
- **Category:** Productivity
- **Keywords:** resume, docx, ats, job-search, career
- **License:** MIT

Submit and wait for Anthropic review. No timeline is published; check back in a few days.

---

### Step 6 — After approval: how users install it

Once listed, users install from inside Claude Code:

```bash
# Recommended: user scope (available in all their projects)
/plugin install resume-skill

# Or with explicit scope:
/plugin install resume-skill --project    # shared with team via .claude/settings.json
/plugin install resume-skill --local      # this machine only, not committed
```

Or via the CLI:
```bash
claude plugin install resume-skill --scope user
claude plugin install resume-skill --scope project
claude plugin install resume-skill --scope local
```

After install, reload plugins without restarting:
```bash
/reload-plugins
```

Then invoke the skill:
```
/resume-skill:build-tailored-resume
```

---

### Step 6 (alternative) — Self-hosted community marketplace

If you don't want to wait for official approval, or want to distribute to a specific team, host your own marketplace instead.

**1. Create a new GitHub repo** (e.g. `YOUR-USERNAME/my-claude-plugins`)

**2. Inside that repo, create `.claude-plugin/marketplace.json`:**

```json
{
  "name": "my-claude-plugins",
  "owner": {
    "name": "YOUR NAME",
    "email": "your@email.com"
  },
  "metadata": {
    "description": "My personal Claude Code plugin collection",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "resume-skill",
      "description": "Transforms a master resume and job description into a tailored .docx",
      "version": "0.1.0",
      "source": {
        "source": "github",
        "repo": "SankaiAI/ats-optimized-resume-agent-skill",
        "ref": "main"
      },
      "author": {
        "name": "YOUR NAME"
      },
      "homepage": "https://github.com/SankaiAI/ats-optimized-resume-agent-skill#readme",
      "repository": "https://github.com/SankaiAI/ats-optimized-resume-agent-skill",
      "license": "MIT",
      "keywords": ["resume", "docx", "ats"],
      "category": "productivity"
    }
  ]
}
```

**3. Push and share.**

Users add your marketplace and install from it:

```bash
# Add your marketplace (user scope):
/plugin marketplace add YOUR-USERNAME/my-claude-plugins

# Or project scope (stored in .claude/settings.json, committed to git):
/plugin marketplace add YOUR-USERNAME/my-claude-plugins --scope project

# Install the plugin from it:
/plugin install resume-skill@my-claude-plugins

# With scope:
/plugin install resume-skill@my-claude-plugins --scope project
```

---

### Releasing updates

When you push a new version:

1. Update `"version"` in `.claude-plugin/plugin.json`
2. Commit and push a new git tag:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```
3. Update `"ref": "v0.2.0"` in your `marketplace.json` if self-hosting
4. Users update with:
   ```bash
   /plugin update resume-skill
   # or
   claude plugin update resume-skill
   ```

---

## Option B — Install Script

This option installs the standalone skill (without the plugin system). Users get
`/build-tailored-resume` with no namespace prefix.

### Prerequisites

- Python 3.10+ and `pip` in PATH
- PowerShell (Windows) or Bash (Mac/Linux)
- Claude Code installed

---

### Windows — install.ps1

Run from inside the `resume_skill/` folder.

**Interactive (recommended — prompts you to choose):**
```powershell
.\install.ps1
```
You will see:
```
[1] User    — available in ALL your projects (recommended)
[2] Project — current project only, shared with your team
[3] Local   — current project only, NOT committed to git

Enter 1, 2, or 3:
```

**Non-interactive (pass scope directly):**
```powershell
.\install.ps1 -Scope user      # all your projects
.\install.ps1 -Scope project   # current project, committed to git
.\install.ps1 -Scope local     # current project, gitignored
```

**What the script does:**
1. Runs `pip install .` → registers `resume-skill` in PATH
2. Creates the skill subdirectory and copies `SKILL.md` into it

**Where SKILL.md lands:**

| Scope | Path |
|---|---|
| user | `C:\Users\<you>\.claude\skills\build-tailored-resume\SKILL.md` |
| project | `<project-root>\.claude\skills\build-tailored-resume\SKILL.md` |
| local | `<project-root>\.claude\skills\build-tailored-resume\SKILL.md` |

The script auto-detects `<project-root>` by walking up from the current directory
until it finds a `.git` or `.claude` folder.

---

### Mac/Linux — install.sh

**Interactive (recommended):**
```bash
chmod +x install.sh
./install.sh
```
Same menu as Windows — enter 1, 2, or 3.

**Non-interactive:**
```bash
./install.sh --user       # all your projects
./install.sh --project    # current project, committed to git
./install.sh --local      # current project, gitignored
```

---

### Verify the install worked

```bash
# 1. CLI is registered
resume-skill --help

# 2. Validate and render work end-to-end
resume-skill validate --input examples/sample_resume_json.json
resume-skill render --input examples/sample_resume_json.json --output test_out.docx

# 3. SKILL.md is in the right place (user scope example)
#    Windows:
dir "%USERPROFILE%\.claude\skills\build-tailored-resume\"
#    Mac/Linux:
ls ~/.claude/skills/build-tailored-resume/
```

Claude Code picks up the skill immediately — no restart needed. Open a new conversation and type `/` to confirm `/build-tailored-resume` appears in the list.

---

### Uninstall

```powershell
# Remove the skill file
Remove-Item -Recurse -Force "$HOME\.claude\skills\build-tailored-resume"

# Remove the CLI (optional)
pip uninstall resume-skill
```

```bash
# Mac/Linux
rm -rf ~/.claude/skills/build-tailored-resume
pip uninstall resume-skill
```

---

## Option C — Manual Install

No script — just two commands. Use this when you want full control, are
behind a corporate proxy that blocks scripts, or just prefer doing it yourself.

### Prerequisites
- Python 3.10+ and `pip` in PATH
- Claude Code installed
- The `resume_skill/` folder from this repo (downloaded or cloned)

---

### Step 1 — Install the Python CLI

Run from anywhere — just point pip at the `resume_skill/` folder:

**Windows (PowerShell or CMD):**
```powershell
pip install C:\path\to\resume_skill
```

**Mac/Linux:**
```bash
pip install /path/to/resume_skill
```

Verify it worked:
```bash
resume-skill --help
# Should print: usage: resume-skill [-h] {render,validate} ...
```

---

### Step 2 — Copy SKILL.md to the right location

Choose your scope and run the matching commands.

#### User scope — available in all your projects

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills\build-tailored-resume"
Copy-Item C:\path\to\resume_skill\SKILL.md "$HOME\.claude\skills\build-tailored-resume\SKILL.md"
```

**Windows (CMD):**
```cmd
mkdir "%USERPROFILE%\.claude\skills\build-tailored-resume"
copy C:\path\to\resume_skill\SKILL.md "%USERPROFILE%\.claude\skills\build-tailored-resume\SKILL.md"
```

**Mac/Linux:**
```bash
mkdir -p ~/.claude/skills/build-tailored-resume
cp /path/to/resume_skill/SKILL.md ~/.claude/skills/build-tailored-resume/SKILL.md
```

---

#### Project scope — shared with your team via git

Run from inside your project root (the repo you want the skill available in):

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path ".claude\skills\build-tailored-resume"
Copy-Item C:\path\to\resume_skill\SKILL.md ".claude\skills\build-tailored-resume\SKILL.md"
```

**Mac/Linux:**
```bash
mkdir -p .claude/skills/build-tailored-resume
cp /path/to/resume_skill/SKILL.md .claude/skills/build-tailored-resume/SKILL.md
```

Commit the result so your whole team gets the skill:
```bash
git add .claude/skills/build-tailored-resume/SKILL.md
git commit -m "Add build-tailored-resume skill"
```

---

#### Local scope — this machine only, not committed

Same copy commands as project scope, but add the directory to `.gitignore` so it is never committed:

```bash
# After copying SKILL.md as shown above:
echo ".claude/skills/" >> .gitignore
```

Claude Code uses `.claude/settings.local.json` for local-scope tracking — no extra step needed beyond keeping the file out of git.

---

### Step 3 — Verify

```bash
# 1. CLI works
resume-skill --help

# 2. Validate a resume JSON
resume-skill validate --input /path/to/resume_skill/examples/sample_resume_json.json

# 3. Render to DOCX
resume-skill render \
  --input /path/to/resume_skill/examples/sample_resume_json.json \
  --output ~/Desktop/test_resume.docx
```

Open Claude Code, type `/`, and confirm `/build-tailored-resume` appears in the list.
Claude Code detects the skill immediately — no restart required.

---

### Step 4 — Uninstall

```powershell
# Windows: remove skill file
Remove-Item -Recurse -Force "$HOME\.claude\skills\build-tailored-resume"

# Remove CLI (optional — only if you don't use it elsewhere)
pip uninstall resume-skill
```

```bash
# Mac/Linux
rm -rf ~/.claude/skills/build-tailored-resume
pip uninstall resume-skill
```

---

### Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `resume-skill: command not found` after pip install | pip Scripts folder not in PATH | Add `%APPDATA%\Python\Python3xx\Scripts` (Win) or `~/.local/bin` (Mac/Linux) to PATH |
| `/build-tailored-resume` missing from Claude Code | SKILL.md not in the right subdirectory | Check the path — must be `…/build-tailored-resume/SKILL.md`, not `…/SKILL.md` flat |
| `ModuleNotFoundError: resume_skill` when running CLI | pip install didn't complete cleanly | Run `pip install /path/to/resume_skill` again and check for errors |
| Render fails with `PermissionError` on the output `.docx` | File is open in Word | Close Word first, then re-run |

---

## Quick reference — scope locations

| Scope | SKILL.md path | Settings file |
|---|---|---|
| user | `~/.claude/skills/build-tailored-resume/SKILL.md` | `~/.claude/settings.json` |
| project | `.claude/skills/build-tailored-resume/SKILL.md` | `.claude/settings.json` |
| local | `.claude/skills/build-tailored-resume/SKILL.md` | `.claude/settings.local.json` |

Plugin cache (Option A only): `~/.claude/plugins/cache/resume-skill/`
