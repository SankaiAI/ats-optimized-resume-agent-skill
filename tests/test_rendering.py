"""
Tests for the DOCX renderer.

Run:
    cd resume_skill
    python -m pytest tests/ -v
"""

import json
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.rendering.config import RenderConfig
from src.rendering.render_docx import ResumeRenderer
from src.schemas.resume_schema import (
    EducationEntry,
    ExperienceEntry,
    HeaderData,
    ProjectEntry,
    ResumeMetadata,
    SkillsData,
    TailoredResume,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _minimal_resume() -> TailoredResume:
    return TailoredResume(
        candidate_level="senior_ic",
        target_role="Senior Data Analyst",
        target_company="Acme Corp",
        section_order=["header", "summary", "skills", "experience", "education"],
        header=HeaderData(
            name="Jane Doe",
            email="jane@example.com",
            phone="(555) 123-4567",
            location="San Francisco, CA",
            linkedin="https://linkedin.com/in/janedoe",
            github="https://github.com/janedoe",
        ),
        summary="Experienced analyst with strong SQL and Python skills.",
        skills=SkillsData(
            core=["SQL", "Python", "dbt"],
            tools=["BigQuery", "Looker"],
            methods=["A/B Testing", "Cohort Analysis"],
            domains=["Product Analytics"],
        ),
        experience=[
            ExperienceEntry(
                title="Senior Data Analyst",
                company="TechCorp",
                location="San Francisco, CA",
                dates="Jan 2021 – Present",
                bullets=[
                    "Built SQL pipelines tracking user activation across 1,000 accounts.",
                    "Designed A/B test framework, improving conversion by 12%.",
                ],
            )
        ],
        projects=[
            ProjectEntry(
                name="Open Source Dashboard",
                subtitle="Python, Streamlit",
                dates="2023",
                bullets=["Built dashboard with 200 monthly users."],
                url="https://github.com/janedoe/dashboard",
            )
        ],
        education=[
            EducationEntry(
                school="UC Berkeley",
                degree="B.S. Statistics",
                dates="2016 – 2020",
                location="Berkeley, CA",
            )
        ],
        metadata=ResumeMetadata(humanization_pass_complete=True),
    )


def _sample_resume_from_json() -> TailoredResume:
    json_path = ROOT / "examples" / "sample_resume_json.json"
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return TailoredResume.from_dict(data)


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestRendererSmoke:
    """Smoke tests — does the renderer run without crashing?"""

    def test_minimal_resume_renders(self):
        resume = _minimal_resume()
        renderer = ResumeRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "test_output.docx"
            result = renderer.render(resume, str(out))
            assert out.exists(), "Output file was not created"
            assert out.stat().st_size > 1000, "Output file is suspiciously small"

    def test_sample_json_renders(self):
        json_path = ROOT / "examples" / "sample_resume_json.json"
        if not json_path.exists():
            pytest.skip("sample_resume_json.json not found")
        resume = _sample_resume_from_json()
        renderer = ResumeRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "sample_output.docx"
            result = renderer.render(resume, str(out))
            assert out.exists()
            assert out.stat().st_size > 5000

    def test_output_is_valid_zip(self):
        """DOCX files are ZIP archives — basic structural check."""
        import zipfile
        resume = _minimal_resume()
        renderer = ResumeRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "test.docx"
            renderer.render(resume, str(out))
            assert zipfile.is_zipfile(str(out)), "Output is not a valid ZIP/DOCX"

    def test_docx_contains_word_document_xml(self):
        """Verify word/document.xml exists inside the DOCX."""
        import zipfile
        resume = _minimal_resume()
        renderer = ResumeRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "test.docx"
            renderer.render(resume, str(out))
            with zipfile.ZipFile(str(out)) as z:
                names = z.namelist()
                assert "word/document.xml" in names


class TestRendererConfig:
    """Test that RenderConfig values are applied."""

    def test_custom_font_name_in_xml(self):
        """Check that the custom font name appears somewhere in the document XML."""
        import zipfile
        resume = _minimal_resume()
        config = RenderConfig(font_name="Times New Roman")
        renderer = ResumeRenderer(config=config)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "test.docx"
            renderer.render(resume, str(out))
            with zipfile.ZipFile(str(out)) as z:
                xml = z.read("word/document.xml").decode("utf-8")
                # Font name should appear somewhere in the XML
                assert "Times New Roman" in xml or "TimesNewRoman" in xml.replace(" ", "")

    def test_no_border_config(self):
        """Renderer runs cleanly with borders disabled."""
        resume = _minimal_resume()
        config = RenderConfig(show_section_bottom_border=False)
        renderer = ResumeRenderer(config=config)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "no_border.docx"
            result = renderer.render(resume, str(out))
            assert Path(out).exists()


class TestSectionOrder:
    """Test that section_order controls what gets rendered."""

    def test_skip_summary_when_not_in_order(self):
        resume = _minimal_resume()
        resume.section_order = ["header", "skills", "experience", "education"]
        resume.summary = "This should not appear"
        renderer = ResumeRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "no_summary.docx"
            renderer.render(resume, str(out))
            import zipfile
            with zipfile.ZipFile(str(out)) as z:
                xml = z.read("word/document.xml").decode("utf-8")
                assert "This should not appear" not in xml

    def test_education_first_order(self):
        """New-grad ordering: education before experience."""
        resume = _minimal_resume()
        resume.section_order = ["header", "education", "experience", "skills"]
        renderer = ResumeRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "edu_first.docx"
            # Should not crash
            renderer.render(resume, str(out))
            assert Path(out).exists()


class TestHyperlinks:
    """Test that hyperlinks make it into the document."""

    def test_linkedin_url_in_relationships(self):
        import zipfile
        resume = _minimal_resume()
        renderer = ResumeRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "links.docx"
            renderer.render(resume, str(out))
            with zipfile.ZipFile(str(out)) as z:
                rels_files = [n for n in z.namelist() if n.endswith(".rels")]
                all_rels = ""
                for rf in rels_files:
                    all_rels += z.read(rf).decode("utf-8")
                assert "linkedin.com" in all_rels, "LinkedIn URL not found in relationships"

    def test_project_url_in_relationships(self):
        import zipfile
        resume = _minimal_resume()
        renderer = ResumeRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "proj_links.docx"
            renderer.render(resume, str(out))
            with zipfile.ZipFile(str(out)) as z:
                rels_files = [n for n in z.namelist() if n.endswith(".rels")]
                all_rels = ""
                for rf in rels_files:
                    all_rels += z.read(rf).decode("utf-8")
                assert "github.com" in all_rels


class TestSchemaRoundtrip:
    """Test TailoredResume serialization."""

    def test_from_dict_to_dict_roundtrip(self):
        original = _minimal_resume()
        as_dict = original.to_dict()
        restored = TailoredResume.from_dict(as_dict)
        assert restored.header.name == original.header.name
        assert restored.candidate_level == original.candidate_level
        assert len(restored.experience) == len(original.experience)
        assert restored.experience[0].bullets == original.experience[0].bullets
