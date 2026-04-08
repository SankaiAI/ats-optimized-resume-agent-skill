# Privacy Policy

**Last updated: April 7, 2026**

## Overview

The `tailored-resume` Claude Code plugin ("the Plugin") runs entirely on your local machine. It does not collect, transmit, or store any personal data on external servers.

## Data processed

When you use the Plugin, the following data stays on your machine:

- Your master resume (provided by you as input)
- The job description (provided by you as input)
- The generated tailored resume JSON and .docx output files

## What we do NOT do

- We do not collect any data from your resume or job description.
- We do not send your resume or any personal information to any third-party service.
- We do not use analytics, tracking, or telemetry of any kind.
- We do not store or log any inputs or outputs.

## Claude / Anthropic

This Plugin runs as a Claude Code skill. When you invoke `/build-tailored-resume`, your resume and job description are passed to Claude (Anthropic's AI) as part of the conversation context running in your local Claude Code session. Anthropic's own privacy policy governs how Claude processes that data:

https://www.anthropic.com/privacy

## Third-party dependencies

The Plugin uses the following open-source Python libraries locally:

- [python-docx](https://python-docx.readthedocs.io/) — DOCX generation
- [lxml](https://lxml.de/) — XML processing

Neither library transmits data externally.

## Contact

For questions about this privacy policy, open an issue at:
https://github.com/SankaiAI/ats-optimized-resume-agent-skill/issues
