[English](#english) | [中文](#chinese)

---

<a id="english"></a>

# resume-skill — build-tailored-resume

A Claude Code skill that transforms a master resume and a target job description into a polished, tailored Word document (.docx).

Once installed, invoke it in Claude Code with:
```
/build-tailored-resume
```

---

## ⚡ For AI Coding Agents — Read This First

> **If you are an AI coding agent (Claude Code, Cursor, Windsurf, OpenClaw, or similar):**
> The user wants to install this repository as a usable skill. This skill requires both a `SKILL.md` copy and a Python CLI install (`python-docx`, `lxml`). Run the single command below that matches the user's OS and scope — the install script handles both steps automatically.
>
> **Claude Code — Mac / Linux (global, all projects):**
> ```bash
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume && chmod +x /tmp/build-tailored-resume/install.sh && /tmp/build-tailored-resume/install.sh --user
> ```
>
> **Claude Code — Mac / Linux (project-level, current project only):**
> ```bash
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume && chmod +x /tmp/build-tailored-resume/install.sh && /tmp/build-tailored-resume/install.sh --project
> ```
>
> **Claude Code — Windows (global, all projects):**
> ```powershell
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git $env:TEMP\build-tailored-resume; & "$env:TEMP\build-tailored-resume\install.ps1" -Scope user
> ```
>
> **Claude Code — Windows (project-level, current project only):**
> ```powershell
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git $env:TEMP\build-tailored-resume; & "$env:TEMP\build-tailored-resume\install.ps1" -Scope project
> ```
>
> **OpenClaw or other agents — Mac / Linux (global):**
> ```bash
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume && chmod +x /tmp/build-tailored-resume/install.sh && /tmp/build-tailored-resume/install.sh --user
> ```
>
> After install completes, confirm with `resume-skill --help`, then tell the user:
> *"The build-tailored-resume skill is installed. Type `/build-tailored-resume` to get started. Have your master resume and the target job description ready."*

---

## Table of Contents

- [For AI Coding Agents](#-for-ai-coding-agents--read-this-first)
- [What you need to provide](#what-you-need-to-provide)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Method 0 — Agent-Assisted (fastest)](#method-0--agent-assisted-fastest)
  - [Method 1 — Direct Clone](#method-1--direct-clone)
  - [Method 2 — Install Script](#method-2--install-script-recommended-for-most-users)
  - [Method 3 — Manual Install](#method-3--manual-install)
  - [Method 4 — Plugin Marketplace](#method-4--plugin-marketplace)
- [Update](#update)
  - [Agent-Assisted Update](#agent-assisted-update-fastest)
  - [Manual Update](#manual-update)
- [Verify the install](#verify-the-install)
- [Uninstall](#uninstall)

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

Choose one of the five methods below. All of them let you pick between **global** (available in all your projects) or **project-based** (current project only).

---

### Method 0 — Agent-Assisted (fastest)

Copy one of the prompts below and paste it directly into your coding agent (Claude Code, Cursor, Windsurf, etc.). Your agent will detect your OS and run the install automatically.

**Global install — available in all your projects (recommended):**

```
Please install the build-tailored-resume Claude Code skill for me globally. Clone the repo at https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git into a temporary directory, then run the install script with the user/global flag — install.sh --user on Mac/Linux, or install.ps1 -Scope user on Windows. After install, confirm it works by running resume-skill --help.
```

**Project-level install — current project only:**

```
Please install the build-tailored-resume Claude Code skill for this project only. Clone the repo at https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git into a temporary directory, then run the install script with the project flag — install.sh --project on Mac/Linux, or install.ps1 -Scope project on Windows. After install, confirm it works by running resume-skill --help.
```

Then invoke it:
```
/build-tailored-resume
```

---

### Method 1 — Direct Clone

Clone the repository directly into your skills directory. Requires two commands: one to clone, one to install the Python CLI.

**Global — all projects:**

Mac / Linux:
```bash
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git ~/.claude/skills/build-tailored-resume
pip install ~/.claude/skills/build-tailored-resume/renderer
```

Windows (PowerShell):
```powershell
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git "$HOME\.claude\skills\build-tailored-resume"
pip install "$HOME\.claude\skills\build-tailored-resume\renderer"
```

**Project-level — current project only:**

Mac / Linux:
```bash
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git .claude/skills/build-tailored-resume
pip install .claude/skills/build-tailored-resume/renderer
```

Windows (PowerShell):
```powershell
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git ".claude\skills\build-tailored-resume"
pip install ".claude\skills\build-tailored-resume\renderer"
```

Then invoke it:
```
/build-tailored-resume
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
pip install renderer/
```

**Step 3 — Copy SKILL.md to the right location**

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

To keep it local only, add it to `.gitignore`:
```bash
echo ".claude/skills/" >> .gitignore
```

Then invoke it:
```
/build-tailored-resume
```

---

### Method 4 — Plugin Marketplace

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

## Update

### Agent-Assisted Update (fastest)

Copy one of the prompts below and paste it into your coding agent. It will pull the latest changes and reinstall everything automatically.

**Global install:**

```
Please update my build-tailored-resume Claude Code skill to the latest version. Clone the latest repo from https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git into a temporary directory, then run the install script with the user/global flag — install.sh --user on Mac/Linux, or install.ps1 -Scope user on Windows. After update, confirm with resume-skill --help.
```

**Project-level install:**

```
Please update my build-tailored-resume Claude Code skill to the latest version. Clone the latest repo from https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git into a temporary directory, then run the install script with the project flag — install.sh --project on Mac/Linux, or install.ps1 -Scope project on Windows. After update, confirm with resume-skill --help.
```

---

### Manual Update

**If you installed via Method 1 (Direct Clone):**

Pull the latest changes and reinstall the Python CLI:

```bash
# Mac/Linux
cd ~/.claude/skills/build-tailored-resume   # global
# or: cd .claude/skills/build-tailored-resume  # project-level
git pull
pip install renderer/ --upgrade
```

```powershell
# Windows (PowerShell)
cd "$HOME\.claude\skills\build-tailored-resume"   # global
# or: cd ".claude\skills\build-tailored-resume"   # project-level
git pull
pip install renderer\ --upgrade
```

**If you installed via Method 2 (Install Script):**

Re-clone and re-run the script — it overwrites `SKILL.md` and upgrades the Python CLI in one step:

```bash
# Mac/Linux
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume
chmod +x /tmp/build-tailored-resume/install.sh
/tmp/build-tailored-resume/install.sh --user      # or --project
```

```powershell
# Windows (PowerShell)
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git $env:TEMP\build-tailored-resume
& "$env:TEMP\build-tailored-resume\install.ps1" -Scope user   # or -Scope project
```

**If you installed via Method 3 (Manual):**

Re-clone, reinstall the Python CLI, and copy the updated `SKILL.md`:

```bash
# Mac/Linux
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume
pip install /tmp/build-tailored-resume/renderer --upgrade
cp /tmp/build-tailored-resume/SKILL.md ~/.claude/skills/build-tailored-resume/SKILL.md   # global
# or: cp /tmp/build-tailored-resume/SKILL.md .claude/skills/build-tailored-resume/SKILL.md  # project
```

```powershell
# Windows (PowerShell)
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git $env:TEMP\build-tailored-resume
pip install "$env:TEMP\build-tailored-resume\renderer" --upgrade
Copy-Item "$env:TEMP\build-tailored-resume\SKILL.md" "$HOME\.claude\skills\build-tailored-resume\SKILL.md"   # global
# or: Copy-Item "$env:TEMP\build-tailored-resume\SKILL.md" ".claude\skills\build-tailored-resume\SKILL.md"   # project
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

---

<a id="chinese"></a>

# resume-skill — build-tailored-resume

一个 Claude Code 技能插件，将你的完整简历母版和目标职位描述转化为一份精致、定向的 Word 文档（.docx）。

安装后，在 Claude Code 中输入以下命令即可调用：
```
/build-tailored-resume
```

---

## ⚡ 致 AI 编程代理 — 请优先阅读此节

> **如果你是 AI 编程代理（Claude Code、Cursor、Windsurf、OpenClaw 或同类工具）：**
> 用户希望将此仓库安装为可用技能。此技能需要同时完成 `SKILL.md` 复制和 Python CLI 安装（`python-docx`、`lxml`）。请根据用户的操作系统和安装范围，运行下方对应的单条命令——安装脚本会自动处理两个步骤。
>
> **Claude Code — Mac / Linux（全局，所有项目可用）：**
> ```bash
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume && chmod +x /tmp/build-tailored-resume/install.sh && /tmp/build-tailored-resume/install.sh --user
> ```
>
> **Claude Code — Mac / Linux（项目级，仅当前项目）：**
> ```bash
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume && chmod +x /tmp/build-tailored-resume/install.sh && /tmp/build-tailored-resume/install.sh --project
> ```
>
> **Claude Code — Windows（全局，所有项目可用）：**
> ```powershell
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git $env:TEMP\build-tailored-resume; & "$env:TEMP\build-tailored-resume\install.ps1" -Scope user
> ```
>
> **Claude Code — Windows（项目级，仅当前项目）：**
> ```powershell
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git $env:TEMP\build-tailored-resume; & "$env:TEMP\build-tailored-resume\install.ps1" -Scope project
> ```
>
> **OpenClaw 或其他代理 — Mac / Linux（全局）：**
> ```bash
> git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume && chmod +x /tmp/build-tailored-resume/install.sh && /tmp/build-tailored-resume/install.sh --user
> ```
>
> 安装完成后，运行 `resume-skill --help` 确认成功，然后告知用户：
> *"build-tailored-resume 技能已安装完成。输入 `/build-tailored-resume` 即可开始使用。请准备好你的简历母版和目标职位描述。"*

---

## 目录

- [致 AI 编程代理](#-致-ai-编程代理--请优先阅读此节)
- [你需要提供什么](#你需要提供什么)
- [工作流程](#工作流程)
- [环境要求](#环境要求)
- [安装方法](#安装方法)
  - [方法零 — 代理辅助安装（最快速）](#方法零--代理辅助安装最快速)
  - [方法一 — 直接克隆](#方法一--直接克隆)
  - [方法二 — 安装脚本](#方法二--安装脚本推荐大多数用户)
  - [方法三 — 手动安装](#方法三--手动安装)
  - [方法四 — 插件市场](#方法四--插件市场)
- [更新](#更新)
  - [代理辅助更新](#代理辅助更新最快速)
  - [手动更新](#手动更新)
- [验证安装](#验证安装)
- [卸载](#卸载)

---

## 你需要提供什么

### 必填项

| 输入内容 | 说明 |
|---------|------|
| **简历母版** | 你所有的工作经历、项目、技能和量化成果的完整记录——越详细越好。插件从中筛选和改写，不会凭空捏造内容。支持格式：`.docx`、`.pdf`、`.txt`、`.md` 或直接粘贴文字。 |
| **职位描述（JD）** | 你申请职位的完整 JD。可以粘贴文字，或上传 `.md` / `.txt` 文件。 |
| **目标公司名称** | 招聘方的公司名称。 |

### 选填项（未提供时插件自动推断）

| 输入内容 | 效果 |
|---------|------|
| LinkedIn / GitHub / 作品集链接 | 以可点击超链接的形式出现在简历头部 |
| 职级偏好 | 控制章节顺序和子弹点深度。可选：`new_grad`（应届）、`entry_level`（初级）、`mid_level`（中级）、`senior_ic`（高级独贡）、`manager`（管理层）、`director`（总监） |
| 页数偏好 | `one_page`（单页）或 `two_page`（双页），默认按内容自适应 |
| 风格偏好 | `conservative`（保守正式）、`modern_professional`（现代专业）、`technical`（技术导向）、`analytical`（数据分析） |
| 需要重点突出或排除的经历 | 覆盖插件默认的筛选逻辑 |
| 你能自信捍卫的量化数据 | 防止插件在改写时削弱你确认准确的数字 |

### 简历母版的填写建议

- **包含所有内容** — 你认为不相关的岗位、老项目、兼职经历都写进去，插件来决定取舍。
- **保留原始子弹点，不用提前润色** — 插件会替你改写，粗糙的输入没关系。
- **尽量加上数字** — 哪怕是估算值（"约 50 名用户"、"每周节省约 3 小时"）。插件不会捏造你没有提供的指标。

---

## 工作流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                           用户输入                                   │
│              简历母版  +  职位描述  +  目标公司名称                    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               v
                 ┌─────────────────────────┐
                 │   阶段 1：信息整理        │  规范化所有输入。
                 │   （必要）               │  仅在关键信息缺失时
                 │                         │  追问用户。
                 └────────────┬────────────┘
                              │ 关卡 1：候选人信息 + JD + 公司名称均已就绪
                              v
                 ┌─────────────────────────┐
                 │   阶段 2：JD 分析        │  提取必要技能、ATS 关键词、
                 │   （必要）               │  职级信号、行业语言。
                 └────────────┬────────────┘
                              │ 关卡 2：关键词与职级已识别
                              │
                    ┌─────────┴──────────┐
                    │                    │
                    v                    v
       ┌────────────────────┐  ┌─────────────────────┐
       │ 阶段 2a：公司调研   │  │ 阶段 2b：团队推断    │
       │ （可选）            │  │ （可选）             │
       │                    │  │                     │
       │ 当 JD 中公司背景    │  │ 当 JD 暗示团队结构   │
       │ 不明显时触发。      │  │ 或汇报关系时触发。   │
       │ 使用网络搜索。      │  │                     │
       └────────────────────┘  └─────────────────────┘
                    │                    │
                    └─────────┬──────────┘
                              v
                 ┌─────────────────────────┐
                 │   阶段 3：策略制定        │  确定：主打优势、淡化内容、
                 │   （必要）               │  首页叙事、章节顺序、
                 │                         │  是否包含摘要、页数目标。
                 └────────────┬────────────┘
                              │ 关卡 3：策略已定，章节顺序已设置
                              v
                 ┌─────────────────────────┐
                 │   阶段 4：内容定制        │  按匹配度（而非时间顺序）
                 │   （必要）               │  筛选子弹点，以人性化
                 │                         │  专业风格改写，完成
                 │                         │  去 AI 化检查。
                 └────────────┬────────────┘
                              │ 关卡 4：所有子弹点已改写 + 去 AI 化检查通过
                              │         + 无无依据声明
                              v
                 ┌─────────────────────────┐
                 │   阶段 5：ATS 检查        │  验证 JD 关键词自然出现。
                 │   （必要）               │  检查章节标题、日期、
                 │                         │  联系方式格式。
                 └────────────┬────────────┘
                              │ 关卡 5：所有 ATS 检查通过
                              v
                 ┌─────────────────────────┐
                 │   阶段 6：渲染生成        │  生成 JSON 结构数据。
                 │   （必要）               │  执行 resume-skill render。
                 │                         │  输出 .docx 文件。
                 └────────────┬────────────┘
                              │ 关卡 6：schema 验证通过 + DOCX 已生成
                              v
                 ┌─────────────────────────┐
                 │   阶段 7：最终验证        │  检查：无占位符文字、
                 │   （必要）               │  章节顺序符合策略、
                 │                         │  子弹点数量匹配页数目标。
                 └────────────┬────────────┘
                              │
                              v
              ┌───────────────────────────────┐
              │              输出              │
              │  tailored_resume.docx         │
              │  + 策略摘要                   │
              │  + 匹配的 ATS 关键词           │
              │  + 诚实标注的潜在不足          │
              └───────────────────────────────┘
```

**执行顺序强制保障。** 插件不允许：
- 在 JD 分析完成前起草任何内容
- 在子弹点筛选和改写完成前执行 ATS 检查
- 在内容验证通过前渲染 DOCX
- 在 JSON schema 验证通过前交付最终文件

---

## 环境要求

- Python 3.10 或更高版本
- `pip` 已加入系统 PATH
- 已安装 Claude Code

---

## 安装方法

以下五种方法均支持选择**全局安装**（所有项目可用）或**项目级安装**（仅当前项目可用）。

---

### 方法零 — 代理辅助安装（最快速）

复制以下任意一段提示词，直接粘贴到你的编程代理（Claude Code、Cursor、Windsurf 等）的对话框中。代理会自动识别你的操作系统并完成安装。

**全局安装 — 所有项目可用（推荐）：**

```
请帮我全局安装 build-tailored-resume 这个 Claude Code 技能。将仓库 https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git 克隆到一个临时目录，然后用全局参数运行安装脚本——Mac/Linux 运行 install.sh --user，Windows 运行 install.ps1 -Scope user。安装完成后运行 resume-skill --help 确认安装成功。
```

**项目级安装 — 仅当前项目可用：**

```
请帮我为当前项目安装 build-tailored-resume 这个 Claude Code 技能。将仓库 https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git 克隆到一个临时目录，然后用项目参数运行安装脚本——Mac/Linux 运行 install.sh --project，Windows 运行 install.ps1 -Scope project。安装完成后运行 resume-skill --help 确认安装成功。
```

安装后调用：
```
/build-tailored-resume
```

---

### 方法一 — 直接克隆

将仓库直接克隆到技能目录。需要两条命令：克隆仓库 + 安装 Python CLI。

**全局 — 所有项目可用：**

Mac / Linux：
```bash
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git ~/.claude/skills/build-tailored-resume
pip install ~/.claude/skills/build-tailored-resume/renderer
```

Windows（PowerShell）：
```powershell
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git "$HOME\.claude\skills\build-tailored-resume"
pip install "$HOME\.claude\skills\build-tailored-resume\renderer"
```

**项目级 — 仅当前项目：**

Mac / Linux：
```bash
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git .claude/skills/build-tailored-resume
pip install .claude/skills/build-tailored-resume/renderer
```

Windows（PowerShell）：
```powershell
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git ".claude\skills\build-tailored-resume"
pip install ".claude\skills\build-tailored-resume\renderer"
```

安装后调用：
```
/build-tailored-resume
```

---

### 方法二 — 安装脚本（推荐大多数用户）

**第一步 — 下载**

```bash
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git
cd ats-optimized-resume-agent-skill
```

**第二步 — 运行脚本**

Mac / Linux：
```bash
chmod +x install.sh
./install.sh
```

Windows（PowerShell）：
```powershell
.\install.ps1
```

脚本会提示你选择作用域：

```
[1] User    — 所有项目可用（推荐）
[2] Project — 仅当前项目，通过 git 与团队共享
[3] Local   — 仅当前项目，不提交到 git
```

也可以直接传入参数跳过交互提示：

```bash
./install.sh --user       # Mac/Linux
./install.sh --project
./install.sh --local

.\install.ps1 -Scope user      # Windows
.\install.ps1 -Scope project
.\install.ps1 -Scope local
```

安装后调用：
```
/build-tailored-resume
```

---

### 方法三 — 手动安装

**第一步 — 下载**

```bash
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git
cd ats-optimized-resume-agent-skill
```

**第二步 — 安装 Python CLI**

```bash
pip install renderer/
```

**第三步 — 将 SKILL.md 复制到正确位置**

**全局 — 所有项目可用：**

```bash
# Mac/Linux
mkdir -p ~/.claude/skills/build-tailored-resume
cp SKILL.md ~/.claude/skills/build-tailored-resume/SKILL.md
```

```powershell
# Windows（PowerShell）
New-Item -ItemType Directory -Force "$HOME\.claude\skills\build-tailored-resume"
Copy-Item SKILL.md "$HOME\.claude\skills\build-tailored-resume\SKILL.md"
```

**项目级 — 仅当前项目：**

```bash
# Mac/Linux
mkdir -p .claude/skills/build-tailored-resume
cp /path/to/resume-skill/SKILL.md .claude/skills/build-tailored-resume/SKILL.md
```

```powershell
# Windows（PowerShell）
New-Item -ItemType Directory -Force ".claude\skills\build-tailored-resume"
Copy-Item C:\path\to\resume-skill\SKILL.md ".claude\skills\build-tailored-resume\SKILL.md"
```

与团队共享时，提交该文件：
```bash
git add .claude/skills/build-tailored-resume/SKILL.md
git commit -m "Add build-tailored-resume skill"
```

仅本机使用时，添加到 `.gitignore`：
```bash
echo ".claude/skills/" >> .gitignore
```

安装后调用：
```
/build-tailored-resume
```

---

### 方法四 — 插件市场

在 Claude Code 中运行：

```
/plugin install resume-skill
```

按提示选择作用域，或直接传入参数：

```bash
/plugin install resume-skill              # 全局 — 所有项目可用
/plugin install resume-skill --project    # 仅当前项目，提交到 git
/plugin install resume-skill --local      # 仅当前项目，不提交
```

安装后调用：
```
/resume-skill:build-tailored-resume
```

---

## 更新

### 代理辅助更新（最快速）

复制以下提示词，粘贴到你的编程代理对话框中，代理会自动拉取最新版本并重新安装。

**全局安装：**

```
请帮我将 build-tailored-resume Claude Code 技能更新到最新版本。将仓库 https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git 克隆到临时目录，然后用全局参数运行安装脚本——Mac/Linux 运行 install.sh --user，Windows 运行 install.ps1 -Scope user。完成后运行 resume-skill --help 确认更新成功。
```

**项目级安装：**

```
请帮我将当前项目的 build-tailored-resume Claude Code 技能更新到最新版本。将仓库 https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git 克隆到临时目录，然后用项目参数运行安装脚本——Mac/Linux 运行 install.sh --project，Windows 运行 install.ps1 -Scope project。完成后运行 resume-skill --help 确认更新成功。
```

---

### 手动更新

**方法一（直接克隆）安装的用户：**

拉取最新代码并重新安装 Python CLI：

```bash
# Mac/Linux
cd ~/.claude/skills/build-tailored-resume   # 全局
# 或: cd .claude/skills/build-tailored-resume  # 项目级
git pull
pip install renderer/ --upgrade
```

```powershell
# Windows（PowerShell）
cd "$HOME\.claude\skills\build-tailored-resume"   # 全局
# 或: cd ".claude\skills\build-tailored-resume"   # 项目级
git pull
pip install renderer\ --upgrade
```

**方法二（安装脚本）安装的用户：**

重新克隆并运行脚本——一步完成 `SKILL.md` 覆盖和 Python CLI 升级：

```bash
# Mac/Linux
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume
chmod +x /tmp/build-tailored-resume/install.sh
/tmp/build-tailored-resume/install.sh --user      # 或 --project
```

```powershell
# Windows（PowerShell）
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git $env:TEMP\build-tailored-resume
& "$env:TEMP\build-tailored-resume\install.ps1" -Scope user   # 或 -Scope project
```

**方法三（手动安装）安装的用户：**

重新克隆、升级 Python CLI，并手动覆盖 `SKILL.md`：

```bash
# Mac/Linux
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git /tmp/build-tailored-resume
pip install /tmp/build-tailored-resume/renderer --upgrade
cp /tmp/build-tailored-resume/SKILL.md ~/.claude/skills/build-tailored-resume/SKILL.md   # 全局
# 或: cp /tmp/build-tailored-resume/SKILL.md .claude/skills/build-tailored-resume/SKILL.md  # 项目级
```

```powershell
# Windows（PowerShell）
git clone https://github.com/SankaiAI/ats-optimized-resume-agent-skill.git $env:TEMP\build-tailored-resume
pip install "$env:TEMP\build-tailored-resume\renderer" --upgrade
Copy-Item "$env:TEMP\build-tailored-resume\SKILL.md" "$HOME\.claude\skills\build-tailored-resume\SKILL.md"   # 全局
# 或: Copy-Item "$env:TEMP\build-tailored-resume\SKILL.md" ".claude\skills\build-tailored-resume\SKILL.md"   # 项目级
```

---

## 验证安装

打开新的 Claude Code 会话，输入 `/`，确认 **`/build-tailored-resume`** 出现在列表中。

在终端中验证：
```bash
resume-skill --help
```

---

## 卸载

**Mac / Linux：**
```bash
rm -rf ~/.claude/skills/build-tailored-resume    # 全局作用域
rm -rf .claude/skills/build-tailored-resume       # 项目作用域
pip uninstall resume-skill
```

**Windows（PowerShell）：**
```powershell
Remove-Item -Recurse -Force "$HOME\.claude\skills\build-tailored-resume"   # 全局
Remove-Item -Recurse -Force ".claude\skills\build-tailored-resume"          # 项目
pip uninstall resume-skill
```
