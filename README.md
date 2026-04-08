# resume-skill — build-tailored-resume

A Claude Code skill that transforms a master resume and a target job description into a polished, tailored Word document (.docx).

Once installed, invoke it in Claude Code with:
```
/build-tailored-resume
```

---

## Requirements

- Python 3.10 or later
- `pip` in PATH
- Claude Code installed

---

## Installation

Choose one of the three methods below. All of them let you pick between **global** (available in all your projects) or **project-based** (current project only).

---

### Method 1 — Plugin Marketplace (easiest)

Open Claude Code and run:

```
/plugin install resume-skill
```

Choose your scope when prompted, or pass it directly:

```bash
/plugin install resume-skill              # global — all your projects
/plugin install resume-skill --project    # current project only, committed to git
/plugin install resume-skill --local      # current project only, not committed
```

Then invoke it:
```
/resume-skill:build-tailored-resume
```

---

### Method 2 — Install Script (recommended for most users)

**Step 1 — Download**

```bash
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git
cd ats-optimized-resume-agent-skill
```

**Step 2 — Run the script**

Mac / Linux:
```bash
chmod +x install.sh
./install.sh
```

Windows (PowerShell):
```powershell
.\install.ps1
```

Both scripts ask you to choose a scope:

```
[1] User    — available in ALL your projects (recommended)
[2] Project — current project only, shared with your team via git
[3] Local   — current project only, NOT committed to git
```

The script installs the `resume-skill` CLI and copies `SKILL.md` to the correct location automatically.

You can also skip the prompt by passing the scope directly:

```bash
./install.sh --user       # Mac/Linux
./install.sh --project
./install.sh --local

.\install.ps1 -Scope user      # Windows
.\install.ps1 -Scope project
.\install.ps1 -Scope local
```

Then invoke it:
```
/build-tailored-resume
```

---

### Method 3 — Manual Install

**Step 1 — Download**

```bash
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git
cd resume-skill
```

**Step 2 — Install the Python CLI**

```bash
pip install .
```

**Step 3 — Copy SKILL.md to the right location**

Pick your scope:

**Global — available in all your projects:**

```bash
# Mac/Linux
mkdir -p ~/.claude/skills/build-tailored-resume
cp SKILL.md ~/.claude/skills/build-tailored-resume/SKILL.md
```

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force "$HOME\.claude\skills\build-tailored-resume"
Copy-Item SKILL.md "$HOME\.claude\skills\build-tailored-resume\SKILL.md"
```

**Project-based — current project only:**

Run from your project root:

```bash
# Mac/Linux
mkdir -p .claude/skills/build-tailored-resume
cp /path/to/resume-skill/SKILL.md .claude/skills/build-tailored-resume/SKILL.md
```

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force ".claude\skills\build-tailored-resume"
Copy-Item C:\path\to\resume-skill\SKILL.md ".claude\skills\build-tailored-resume\SKILL.md"
```

To share with your team, commit the file:
```bash
git add .claude/skills/build-tailored-resume/SKILL.md
git commit -m "Add build-tailored-resume skill"
```

To keep it local only (not committed), add it to `.gitignore` instead:
```bash
echo ".claude/skills/" >> .gitignore
```

Then invoke it:
```
/build-tailored-resume
```

---

## Verify the install

Open a new Claude Code session, type `/`, and confirm **`/build-tailored-resume`** appears in the list.

From the terminal:
```bash
resume-skill --help
```

---

## Uninstall

**Mac / Linux:**
```bash
rm -rf ~/.claude/skills/build-tailored-resume    # global scope
rm -rf .claude/skills/build-tailored-resume       # project scope
pip uninstall resume-skill
```

**Windows (PowerShell):**
```powershell
Remove-Item -Recurse -Force "$HOME\.claude\skills\build-tailored-resume"   # global
Remove-Item -Recurse -Force ".claude\skills\build-tailored-resume"          # project
pip uninstall resume-skill
```
