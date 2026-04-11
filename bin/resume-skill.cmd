@echo off
REM resume-skill.cmd — Windows wrapper for the resume renderer.
REM Claude Code adds bin\ to PATH automatically when the plugin is installed.

SET PLUGIN_ROOT=%CLAUDE_PLUGIN_ROOT%
IF "%PLUGIN_ROOT%"=="" SET PLUGIN_ROOT=%~dp0..

python -c "import docx" 2>nul || pip install python-docx lxml --quiet

SET PYTHONPATH=%PLUGIN_ROOT%\renderer;%PYTHONPATH%
python "%PLUGIN_ROOT%\renderer\src\cli.py" %*
