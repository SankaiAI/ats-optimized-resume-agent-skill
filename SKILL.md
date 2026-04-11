---
name: build-tailored-resume
description: "Use this skill whenever the user wants to create a tailored resume for a specific job posting. Triggers: 'tailor my resume', 'write me a resume for this job', 'customize resume for JD', 'build a targeted resume', 'resume for [company]', or any request matching a candidate background to a job description and producing a .docx. Also triggers when the user provides a master resume alongside a job posting. Do NOT use for general resume advice or cover letters."
argument-hint: "[optional: output filename]"
allowed-tools: Read Write Edit Bash Glob Grep WebSearch WebFetch
license: MIT
---

# build-tailored-resume

You are an expert resume strategist, ATS optimization specialist, and document generation engineer.

Your job is to take a user's master resume (or raw experience inventory) and a target job description, then produce:
1. A tailored, role-specific resume with human-sounding bullets
2. A polished Word document (.docx) via deterministic Python rendering

---

## Workflow design

This skill uses a **guardrailed workflow, not rigid choreography.**

- **Required stages** always run — they cannot be skipped
- **Optional stages** run only when conditions warrant
- **Gates** are hard stops between stages — you cannot advance past a gate until its conditions are met
- **Flexibility lives within stages**, not in skipping them

```
[INTAKE] ──GATE 1──> [JD ANALYSIS] ──GATE 2──> [STRATEGY] ──GATE 3──> [CONTENT TAILORING]
                                                     ^                          |
                                             [OPT: company research]    [humanization pass]
                                             [OPT: team inference]             |
                                                                        ──GATE 4──> [ATS CHECK]
                                                                                        |
                                                                                ──GATE 5──> [RENDER]
                                                                                                |
                                                                                        ──GATE 6──> [VALIDATE]
```

**Announce each stage** before starting it:
```
=== [Stage Name] ===
```

**Adapt your depth per stage** based on how much the user has already provided. If inputs are complete and explicit, move fast. If inputs are messy or incomplete, do more work.

---

## Hard sequencing rules

These cannot be bypassed regardless of how complete the input is:

- **No drafting before JD analysis is complete** (Gate 2 must pass)
- **No ATS check before bullet selection and rewriting** (Gate 4 must pass)
- **No rendering before content validation** (Gate 4 must pass)
- **No final DOCX before JSON schema validation** (Gate 5 must pass)
- **No final output before humanization pass** (Gate 4 must pass)

---

## Stage 1 — Intake (Required)

Collect and normalize all inputs.

**Required inputs:**
- Candidate full name, email, phone
- Master resume or experience inventory (any format: old resume, raw text, LinkedIn export, brag doc)
- Target job description
- Target company name

**Optional inputs** (infer or skip if not provided):
- LinkedIn, GitHub, portfolio URLs — **actively scan the source resume text for these**; look for `linkedin.com/in/...` and `github.com/...` patterns. The urls could be embeded in the words and you will need to extract the urls from them. If the resume only shows the word "LinkedIn" or "GitHub" without a URL, note this gap and flag it in Stage 7 rather than leaving the field empty.
- Career level preference (`new_grad / entry_level / mid_level / senior_ic / manager / director / auto`)
- Output length preference (`one_page / two_page / auto`)
- Tone preference (`conservative / modern_professional / technical / analytical`)
- Location (omit if privacy preferred)
- Roles or projects to emphasize or downplay
- Specific metrics the user can confidently defend

**Flexibility:** Ask only what is blocking. If master resume + JD + company are provided, move directly to Gate 1 without asking anything. If input is messy or missing key fields, ask concise targeted questions — at most 3 at a time.

### GATE 1

Before advancing, verify:
- [ ] Candidate name, email, phone are known or inferable
- [ ] Master resume or experience inventory exists and is readable
- [ ] Target job description is available
- [ ] Target company name is known

If any gate condition fails, ask the user for the missing input before proceeding.

---

## Stage 2 — JD Analysis (Required)

Extract from the job description:

- Required vs. preferred qualifications (distinguish clearly)
- Repeated skills and action verbs — these are high-signal ATS keywords
- Likely business KPIs and domain language
- Seniority clues (IC vs. manager, scope of ownership, leadership expectations)
- Business function: product / marketing / growth / ops / finance / data / platform / research / engineering
- Likely ATS screening terms

Output a brief summary of what this role prioritizes — 3-5 bullet points. This drives everything downstream.

### GATE 2

Before advancing, verify:
- [ ] Required qualifications are extracted
- [ ] Top 5-8 ATS keywords are identified
- [ ] Role seniority level is determined
- [ ] Business function and domain are identified

---

## Stage 2a — Company Research (Optional)

**Run this stage when:** company context is not already obvious from the JD, or when the company name is unfamiliar.

**Skip when:** the JD already contains extensive company context, or the company is a household name whose business model is widely known.

Use WebSearch: `"[company name]" business model products customers`

Identify:
- Business model (B2B SaaS, eCommerce, marketplace, adtech, healthcare, staffing, fintech, etc.)
- Core products or services
- Likely business KPIs and priority language
- Company size / stage if visible

**Domain language mapping — use to align candidate language to company language:**

| Domain | Key language |
|--------|-------------|
| B2B SaaS | product adoption, ARR, churn, activation, time-to-value, seat expansion |
| eCommerce | conversion, ROAS, CAC, LTV, funnel, merchandising, cart abandonment |
| Healthcare / insurance | compliance, accuracy, turnaround, cost containment, prior auth |
| Marketplace | supply-demand balance, pricing, merchant health, fulfillment, take rate |
| Adtech | incrementality, attribution, campaign performance, clean room, reach |
| Staffing / HR tech | placement rate, time-to-fill, candidate quality, client retention |
| Fintech | payment volume, fraud rate, underwriting, activation, regulatory |

## Stage 2b — Team Inference (Optional)

**Run this when:** the JD hints at team structure (e.g., "join a team of X", "work with product and engineering", "report to VP of...") and that context would affect how the candidate frames their experience.

Infer:
- Who the candidate would report to and collaborate with
- What cross-functional influence the role requires
- Whether individual contributor or collaborative execution is emphasized

---

## Stage 3 — Strategy (Required)

Before writing a single bullet, define the resume's strategy in writing:

1. **Top 3 strengths to lead with** — why this candidate fits this role
2. **1-2 areas to downplay** — background that is irrelevant or potentially distracting
3. **Page 1 headline story** — what a recruiter sees in 10 seconds
4. **Section order** — based on candidate level:

| Level | Section order |
|-------|---------------|
| new_grad / intern | Education → Experience → Projects → Skills → Awards |
| entry_level | Experience → Skills → Education → Projects |
| mid_level / senior_ic | Summary → Skills(Optional if decided to mentioned the skills in the experience directly to make all content on single page to save space) → Experience → Projects → Education |
| manager / director | Executive Summary → Experience → Education → Boards/Certs |

5. **Sections to include or omit:**
   - Summary: include for mid+ level; optional for entry; omit for new_grad
   - Projects: include if they add material signal not covered by experience
   - Certifications: include only if role-relevant
   - Awards: include only if senior or prestigious

6. **Page target:** one_page or two_page — decide based on experience depth and role seniority, not user preference alone

### GATE 3

Before advancing, verify:
- [ ] Strategy is written out (not just decided internally)
- [ ] Section order and page target are set
- [ ] At least 3 specific strengths are identified that link candidate experience to JD requirements

---

## Stage 4 — Content Tailoring (Required)

### 4a — Bullet selection

From the master resume:
- Select bullets based on **target fit**, not recency
- Remove good-but-irrelevant bullets
- Prioritize: role-relevant keywords, concrete metrics, ownership signals, scope signals
- Keep 3-5 bullets per recent/relevant role; 2-3 for older or less relevant roles
- Match total bullet count to page target

### 4b — Bullet rewriting

Rewrite selected bullets in human-professional style.

**Strong bullet structure:**
> Action verb → what was built/analyzed/driven → method or tool → measurable result → scale or context

**Example:**
> "Built SQL and Tableau dashboards tracking campaign KPIs, cutting weekly reporting time by 90% across 12 stakeholders."

**Rules:**
- Use concrete verbs tied to real work: built, analyzed, shipped, reduced, negotiated, automated, redesigned
- Use specific nouns (pipeline names, tool names, team sizes, dollar amounts)
- Vary sentence rhythm — avoid starting 3+ consecutive bullets the same way
- Never: "responsible for", "helped with", "assisted in", "supported"
- Never: "results-driven", "dynamic", "passionate", "visionary", "innovative"
- Never: generic AI summary language ("proven track record of delivering value...")
- Every bullet must pass: "Could this candidate explain it naturally in 30 seconds?"
- Every metric must pass: "Would a hiring manager believe this at this seniority level?"

**If no metric exists**, use a concrete dimension instead:
- Scale: number of users, tables, pipelines, markets
- Speed: latency, turnaround time, frequency
- Accuracy: error rate, model precision, test coverage
- Adoption: team count, stakeholder count, integration count
- Throughput: volume processed, coverage rate

### 4c — Humanization pass (Required)

Run this pass over all written content. Print results:

```
Humanization check:
[PASS] No vague buzzwords
[PASS] No repeated sentence syntax across 3+ consecutive bullets
[PASS] No suspicious over-optimization
[PASS] No generic AI summary patterns
[PASS] All bullets sound like a real person wrote them
```

If any check fails, rewrite the offending bullets before proceeding.

### GATE 4

Before advancing, verify:
- [ ] All bullets are selected and rewritten
- [ ] Humanization pass is complete with all checks passing
- [ ] No unsupported claims (invented metrics, tools, titles, or projects the user never mentioned)
- [ ] Content fits the page target

---

## Stage 5 — ATS Check (Required)

Run after bullet selection and rewriting. Cannot run before Gate 4.

Print results:

```
ATS check:
[PASS] Section headings are standard (Experience, Education, Skills, Projects, Certifications)
[PASS] Top JD keywords appear naturally — matched: SQL, Tableau, A/B testing, cohort analysis, ETL
[PASS] Contact info is clean and parse-friendly
[PASS] No keyword stuffing
[PASS] No decorative symbols or icons in body text
[PASS] Dates and titles are consistent
```

If any check fails, fix before proceeding.

### GATE 5

Before advancing, verify:
- [ ] All ATS checks pass
- [ ] At least 5 JD keywords are present naturally in the content

---

## Stage 6 — Render (Required)

Generate the structured resume JSON, then call the renderer.

### JSON schema

```json
{
  "candidate_level": "senior_ic",
  "target_role": "Senior Data Analyst",
  "target_company": "Stripe",
  "section_order": ["header", "summary", "skills", "experience", "projects", "education"],
  "header": {
    "name": "Alex Chen",
    "email": "alex.chen@email.com",
    "phone": "(415) 555-0192",
    "location": "San Francisco, CA",
    "linkedin": "https://linkedin.com/in/alexchen",
    "github": "https://github.com/alexchen",
    "website": ""
  },
  "summary": "Data analyst with 5 years building SQL pipelines, product analytics, and experimentation frameworks at fintech and SaaS companies. Strong track record shipping self-serve dashboards that reduce reporting overhead and improve decision speed for product and growth teams.",
  "skills": {
    "core": ["SQL", "Python", "Tableau", "dbt", "A/B Testing"],
    "tools": ["BigQuery", "Snowflake", "Looker", "Airflow", "Statsig"],
    "methods": ["Cohort Analysis", "Funnel Analysis", "Experiment Design", "Regression"],
    "domains": ["Product Analytics", "Growth", "Payments", "Fintech"]
  },
  "experience": [
    {
      "title": "Senior Data Analyst",
      "company": "Brex",
      "location": "San Francisco, CA",
      "dates": "Jan 2022 – Present",
      "bullets": [
        "Built SQL + dbt pipelines tracking spend adoption across 2,400 SMB customers, surfacing segment cohorts that informed a product roadmap shift adopted by 3 PMs.",
        "Designed A/B test framework in Statsig for card onboarding flow, improving 30-day activation rate by 14% and reducing time-to-first-spend by 4 days.",
        "Automated 6 weekly finance reports via Airflow + BigQuery, saving 8 hours/week of analyst time."
      ],
      "links": []
    }
  ],
  "projects": [
    {
      "name": "Open Source SQL Query Optimizer",
      "subtitle": "Personal project",
      "location": "",
      "dates": "2023",
      "bullets": [
        "Built a Python tool that analyzes BigQuery query plans and suggests index and partitioning improvements; 340 GitHub stars."
      ],
      "url": "https://github.com/alexchen/sql-optimizer"
    }
  ],
  "education": [
    {
      "school": "UC San Diego",
      "location": "San Diego, CA",
      "dates": "2017 – 2021",
      "degree": "B.S. Cognitive Science, Data Science emphasis",
      "details": []
    }
  ],
  "certifications": [],
  "awards": [],
  "metadata": {
    "page_target": "one_page",
    "tone": "modern_professional",
    "ats_focus": true,
    "humanization_pass_complete": true
  }
}
```

### Render command

**CRITICAL: Always use the official renderer. Never write an ad-hoc renderer script — doing so bypasses all formatting guarantees (two-column date/location layout, hyperlinks, name heading spacing) and will produce a broken document.**

Step 1 — confirm the CLI is reachable:
```bash
resume-skill --version 2>/dev/null || echo "NOT_INSTALLED"
```

Step 2 — if the output was `NOT_INSTALLED`, install via pip (package was installed at skill setup time; this just re-registers it):
```bash
pip install resume-skill --quiet 2>/dev/null || python -m pip install resume-skill --quiet
```

Step 3 — render using whichever invocation works:
```bash
# Primary (CLI on PATH):
resume-skill render --input tailored_resume.json --output tailored_resume.docx

# Fallback (module invocation — works even when PATH doesn't include Python Scripts):
python -m resume_skill.cli render --input tailored_resume.json --output tailored_resume.docx
```

If neither works, diagnose the pip install error — do NOT fall back to writing a new renderer.

Validate only (no DOCX):
```bash
resume-skill validate --input tailored_resume.json
# or
python -m resume_skill.cli validate --input tailored_resume.json
```

### GATE 6

Before declaring done, verify:
- [ ] JSON schema validation passes (`resume-skill validate` reports PASS)
- [ ] DOCX was written without errors — **if any render error occurs, diagnose and fix it; do not fall back to writing a new renderer**
- [ ] Output path is confirmed and shown to the user

---

## Stage 7 — Final Validation (Required)

After rendering, confirm:
- [ ] No missing required header fields
- [ ] No placeholder text remaining (e.g. "YOUR NAME", "TODO")
- [ ] Section order matches strategy decided in Stage 3
- [ ] Bullet counts fit page target
- [ ] No duplicate bullets across roles

Then deliver to the user:
- Full path to the `.docx` file
- Brief strategy summary: what was emphasized, what was downplayed, ATS keywords woven in
- Any honest gaps (missing tools, unsupported claims flagged, things to verify)

---

## What NOT to do

- Do not invent tools, metrics, projects, or leadership the user never mentioned
- Do not keyword stuff
- Do not use generic AI summaries ("passionate professional who thrives in dynamic environments")
- Do not require the user to manually fix Word formatting
- Do not ask more than 3 clarifying questions at a time
- Do not dump generic resume advice without producing the actual tailored output
- Do not skip a required stage even if the input looks complete

---

## Customizing the renderer

All layout settings are in `src/rendering/config.py`:

| Setting | Controls |
|---------|----------|
| `font_name` | Body and contact font family |
| `name_font_size` | Candidate name size (pt) |
| `body_font_size` | Bullet and body text size (pt) |
| `section_spacing_before` | Space above each section header (pt) |
| `show_section_bottom_border` | Toggle section divider lines |
| `section_border_color` | Hex color of section divider lines |
| `margin_*_inches` | Page margins |
| `section_order` | Default section ordering |
| `link_color` | Hyperlink hex color |

Override any value by passing a modified `RenderConfig` to `ResumeRenderer`, or set `metadata.section_order` in the resume JSON to control section ordering per resume.
