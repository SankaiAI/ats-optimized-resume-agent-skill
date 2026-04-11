# install.ps1 — installs the build-tailored-resume Claude Code skill (Windows)
#
# Usage:
#   .\install.ps1                 # interactive prompt — asks which scope
#   .\install.ps1 -Scope user     # user scope  — available in ALL your projects
#   .\install.ps1 -Scope project  # project scope — shared via .claude/settings.json
#   .\install.ps1 -Scope local    # local scope  — this machine only, not committed

param(
    [ValidateSet("user", "project", "local", "")]
    [string]$Scope = ""
)

$SkillName = "build-tailored-resume"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "============================================================"
Write-Host "  build-tailored-resume - Claude Code Skill Installer"
Write-Host "============================================================"

# ── Interactive scope selection when no flag given ────────────────────────────
if ($Scope -eq "") {
    Write-Host ""
    Write-Host "  Where do you want to install this skill?"
    Write-Host ""
    Write-Host "  [1] User    - available in ALL your projects (recommended)"
    Write-Host "                installs to: $HOME\.claude\skills\"
    Write-Host ""
    Write-Host "  [2] Project - current project only, shared with your team"
    Write-Host "                installs to: <project-root>\.claude\skills\"
    Write-Host "                committed to git via .claude/settings.json"
    Write-Host ""
    Write-Host "  [3] Local   - current project only, NOT committed to git"
    Write-Host "                installs to: <project-root>\.claude\skills\"
    Write-Host "                stays on this machine only"
    Write-Host ""

    do {
        $Choice = Read-Host "  Enter 1, 2, or 3"
    } while ($Choice -notin @("1", "2", "3"))

    $Scope = @{ "1" = "user"; "2" = "project"; "3" = "local" }[$Choice]
    Write-Host ""
}

Write-Host "  Scope: $Scope"

# ── Determine target skills directory ─────────────────────────────────────────
if ($Scope -eq "user") {
    $SkillsDir = Join-Path $HOME ".claude\skills"
} else {
    # Walk up to find project root (.git or .claude directory)
    $ProjectRoot = (Get-Location).Path
    while ($true) {
        if ((Test-Path (Join-Path $ProjectRoot ".git")) -or (Test-Path (Join-Path $ProjectRoot ".claude"))) {
            break
        }
        $Parent = Split-Path $ProjectRoot -Parent
        if ($Parent -eq $ProjectRoot) { break }   # reached filesystem root
        $ProjectRoot = $Parent
    }
    $SkillsDir = Join-Path $ProjectRoot ".claude\skills"

    if ($Scope -eq "local") {
        Write-Host "  Note: Add .claude/skills/ to .gitignore to keep this local."
    }
}

$Dest = Join-Path $SkillsDir $SkillName
Write-Host "  Target: $Dest\SKILL.md"
Write-Host ""

# ── Step 1: pip install the Python package ────────────────────────────────────
Write-Host "[1/2] Installing resume-skill Python package..."
pip install "$ScriptDir\renderer" --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Error "pip install failed. Ensure Python and pip are in PATH."
    exit 1
}
Write-Host "      Done - 'resume-skill' CLI is now available in PATH."

# ── Step 2: Copy SKILL.md into named subdirectory ─────────────────────────────
Write-Host ""
Write-Host "[2/2] Copying SKILL.md -> $Dest\SKILL.md"
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Copy-Item (Join-Path $ScriptDir "SKILL.md") (Join-Path $Dest "SKILL.md") -Force
Write-Host "      Done."

Write-Host ""
Write-Host "============================================================"
Write-Host "  Installation complete!"
Write-Host ""
Write-Host "  Verify:           resume-skill --help"
Write-Host "  Use in Claude:    /build-tailored-resume"
Write-Host "============================================================"
Write-Host ""
