"""
Tests for the resume JSON validator.

Run:
    cd resume_skill
    python -m pytest tests/ -v
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.schemas.resume_schema import (
    EducationEntry,
    ExperienceEntry,
    HeaderData,
    ResumeMetadata,
    SkillsData,
    TailoredResume,
)
from src.validation.validate_output import validate


def _good_resume() -> TailoredResume:
    return TailoredResume(
        candidate_level="senior_ic",
        target_role="Senior Data Analyst",
        target_company="Stripe",
        section_order=["header", "summary", "skills", "experience", "education"],
        header=HeaderData(
            name="Jane Doe",
            email="jane@example.com",
            phone="(555) 123-4567",
        ),
        summary="Analyst with 5 years building SQL pipelines for fintech products.",
        skills=SkillsData(core=["SQL", "Python"]),
        experience=[
            ExperienceEntry(
                title="Senior Analyst",
                company="Acme",
                dates="2021 – Present",
                bullets=["Built dbt models tracking 300K monthly events, reducing reporting lag by 2 days."],
            )
        ],
        projects=[],
        education=[
            EducationEntry(school="UC Berkeley", degree="B.S. Statistics", dates="2016–2020")
        ],
        metadata=ResumeMetadata(humanization_pass_complete=True),
    )


class TestValidatorPasses:
    def test_clean_resume_passes(self):
        r = validate(_good_resume())
        assert r.passed, r.report()

    def test_report_string_contains_pass(self):
        r = validate(_good_resume())
        assert "PASS" in r.report()


class TestValidatorErrors:
    def test_missing_name_fails(self):
        resume = _good_resume()
        resume.header.name = ""
        r = validate(resume)
        assert not r.passed
        assert any("name" in e.lower() for e in r.errors)

    def test_missing_email_fails(self):
        resume = _good_resume()
        resume.header.email = ""
        r = validate(resume)
        assert not r.passed
        assert any("email" in e.lower() for e in r.errors)

    def test_missing_phone_fails(self):
        resume = _good_resume()
        resume.header.phone = ""
        r = validate(resume)
        assert not r.passed
        assert any("phone" in e.lower() for e in r.errors)

    def test_duplicate_bullet_fails(self):
        resume = _good_resume()
        resume.experience.append(
            ExperienceEntry(
                title="Analyst",
                company="Brex",
                dates="2020–2021",
                bullets=[
                    "Built dbt models tracking 300K monthly events, reducing reporting lag by 2 days.",
                    "Some other bullet.",
                ],
            )
        )
        r = validate(resume)
        assert not r.passed
        assert any("duplicate" in e.lower() for e in r.errors)

    def test_missing_header_in_section_order_fails(self):
        resume = _good_resume()
        resume.section_order = ["summary", "experience", "education"]
        r = validate(resume)
        assert not r.passed
        assert any("header" in e.lower() for e in r.errors)


class TestValidatorWarnings:
    def test_banned_phrase_warns(self):
        resume = _good_resume()
        resume.summary = "Responsible for managing data pipelines."
        r = validate(resume)
        assert len(r.warnings) > 0

    def test_placeholder_warns(self):
        resume = _good_resume()
        resume.summary = "TODO: write summary here"
        r = validate(resume)
        assert any("TODO" in w or "banned" in w.lower() for w in r.warnings)

    def test_humanization_not_done_warns(self):
        resume = _good_resume()
        resume.metadata.humanization_pass_complete = False
        r = validate(resume)
        assert any("humanization" in w.lower() for w in r.warnings)

    def test_bad_linkedin_url_warns(self):
        resume = _good_resume()
        resume.header.linkedin = "not-a-url"
        r = validate(resume)
        # Should flag malformed URL
        assert not r.passed or len(r.errors) > 0 or len(r.warnings) > 0

    def test_empty_target_role_warns(self):
        resume = _good_resume()
        resume.target_role = ""
        r = validate(resume)
        assert any("target_role" in w for w in r.warnings)
