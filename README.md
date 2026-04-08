# resume-skill — build-tailored-resume

A Claude Code skill that transforms a master resume and a target job description into a polished, tailored Word document (.docx).

Once installed, invoke it in Claude Code with:
```
/build-tailored-resume
```

---

## What you need to provide

### Required

| Input | What it should contain |
|-------|------------------------|
| **Master resume** | Every role, bullet, project, skill, and metric you have ever done — the more complete, the better. The skill selects and rewrites from this pool; it does not invent. Accepted formats: `.docx`, `.pdf`, `.txt`, `.md`, or pasted text. |
| **Job description** | The full JD for the role you are applying to. Paste it as text or drop a `.md`/`.txt` file. |
| **Company name** | The name of the hiring company. |

### Optional (the skill infers these if not provided)

| Input | Effect |
|-------|--------|
| LinkedIn / GitHub / portfolio URL | Added as clickable links in the header |
| Career level | Controls section order and bullet depth. One of: `new_grad`, `entry_level`, `mid_level`, `senior_ic`, `manager`, `director` |
| Page preference | `one_page` or `two_page`. Defaults to what fits the content. |
| Tone | `conservative`, `modern_professional`, `technical`, or `analytical` |
| Roles or projects to emphasize or exclude | Overrides the skill's default selection logic |
| Metrics you are confident defending | Prevents the skill from softening numbers that are accurate |

### Tips for your master resume

- **Include everything** — roles you think are irrelevant, old projects, side work. The skill decides what to cut.
- **Keep raw bullets, not polished ones** — the skill rewrites for you. Messy input is fine.
- **Add numbers wherever you have them** — even rough ones ("~50 users", "saved about 3 hours/week"). The skill will not invent metrics you do not provide.

---

## How it works

Once you provide your inputs, the skill runs through a guardrailed pipeline. Required stages always run. Optional stages run only when they add value.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER PROVIDES                               │
│            master resume  +  job description  +  company            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               v
                 ┌─────────────────────────┐
                 │   STAGE 1: INTAKE       │  Normalize all inputs.
                 │   (required)            │  Ask only if something
                 │                         │  critical is missing.
                 └────────────┬────────────┘
                              │ GATE 1: candidate data + JD + company exist
                              v
                 ┌─────────────────────────┐
                 │   STAGE 2: JD ANALYSIS  │  Extract required skills,
                 │   (required)            │  ATS keywords, seniority
                 │                         │  signals, domain language.
                 └────────────┬────────────┘
                              │ GATE 2: keywords + seniority identified
                              │
                    ┌─────────┴──────────┐
                    │                    │
                    v                    v
       ┌────────────────────┐  ┌─────────────────────┐
       │ STAGE 2a: COMPANY  │  │ STAGE 2b: TEAM      │
       │ RESEARCH           │  │ INFERENCE           │
       │ (optional)         │  │ (optional)          │
       │                    │  │                     │
       │ Runs when company  │  │ Runs when JD hints  │
       │ context is not     │  │ at team structure   │
       │ obvious from JD.   │  │ or reporting line.  │
       │ Uses web search.   │  │                     │
       └────────────────────┘  └─────────────────────┘
                    │                    │
                    └─────────┬──────────┘
                              v
                 ┌─────────────────────────┐
                 │   STAGE 3: STRATEGY     │  Decide: which strengths
                 │   (required)            │  to lead with, what to
                 │                         │  downplay, section order,
                 │                         │  page target, summary Y/N.
                 └────────────┬────────────┘
                              │ GATE 3: strategy written, section order set
                              v
                 ┌─────────────────────────┐
                 │   STAGE 4: CONTENT      │  Select bullets by fit
                 │   TAILORING             │  (not recency). Rewrite
                 │   (required)            │  in human-professional
                 │                         │  style. Humanization pass.
                 └────────────┬────────────┘
                              │ GATE 4: all bullets rewritten + humanization
                              │         pass complete + no unsupported claims
                              v
                 ┌─────────────────────────┐
                 │   STAGE 5: ATS CHECK    │  Verify JD keywords land
                 │   (required)            │  naturally. Check headings,
                 │                         │  dates, contact format.
                 └────────────┬────────────┘
                              │ GATE 5: all ATS checks pass
                              v
                 ┌─────────────────────────┐
                 │   STAGE 6: RENDER       │  Generate JSON schema.
                 │   (required)            │  Run resume-skill render.
                 │                         │  Produce .docx file.
                 └────────────┬────────────┘
                              │ GATE 6: schema validation PASS + DOCX written
                              v
                 ┌─────────────────────────┐
                 │   STAGE 7: VALIDATE     │  Final checks: no placeholders,
                 │   (required)            │  section order matches strategy,
                 │                         │  bullet counts fit page target.
                 └────────────┬────────────┘
                              │
                              v
              ┌───────────────────────────────┐
              │          OUTPUT               │
              │  tailored_resume.docx         │
              │  + strategy summary           │
              │  + ATS keywords matched       │
              │  + any honest gaps flagged    │
              └───────────────────────────────┘
```

**Sequencing is enforced.** The skill cannot:
- Draft bullets before JD analysis is complete
- Run the ATS check before bullets are selected and rewritten
- Render the DOCX before content validation passes
- Deliver the final file before JSON schema validation passes

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
cd ats-optimized-resume-agent-skill
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
