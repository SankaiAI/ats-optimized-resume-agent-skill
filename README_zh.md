# resume-skill — build-tailored-resume

[English](./README.md) | 中文

一个 Claude Code 技能插件，将你的完整简历母版和目标职位描述转化为一份精致、定向的 Word 文档（.docx）。

安装后，在 Claude Code 中输入以下命令即可调用：
```
/build-tailored-resume
```

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

提供输入后，插件会按以下流程运行。必要阶段始终执行，可选阶段仅在有价值时才运行。

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

以下三种方法均支持选择**全局安装**（所有项目可用）或**项目级安装**（仅当前项目可用）。

---

### 方法一 — 插件市场（最简单）

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

脚本会自动安装 `resume-skill` CLI 并将 `SKILL.md` 复制到正确位置。

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
pip install .
```

**第三步 — 将 SKILL.md 复制到正确位置**

选择你的作用域：

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

在项目根目录执行：

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

仅本机使用（不提交）时，添加到 `.gitignore`：
```bash
echo ".claude/skills/" >> .gitignore
```

安装后调用：
```
/build-tailored-resume
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
