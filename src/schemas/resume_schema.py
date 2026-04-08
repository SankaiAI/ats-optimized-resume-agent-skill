"""
Resume data schema — typed dataclasses for structured resume JSON.

The LLM produces a dict matching this schema. The renderer consumes it.
Both sides agree on this contract; neither side hard-codes the other's logic.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class HeaderData:
    name: str
    email: str
    phone: str
    location: str = ""
    linkedin: str = ""
    github: str = ""
    website: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "HeaderData":
        return cls(
            name=d.get("name", ""),
            email=d.get("email", ""),
            phone=d.get("phone", ""),
            location=d.get("location", ""),
            linkedin=d.get("linkedin", ""),
            github=d.get("github", ""),
            website=d.get("website", ""),
        )


@dataclass
class SkillsData:
    core: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "SkillsData":
        return cls(
            core=d.get("core", []),
            tools=d.get("tools", []),
            methods=d.get("methods", []),
            domains=d.get("domains", []),
        )


@dataclass
class ExperienceLink:
    label: str
    url: str

    @classmethod
    def from_dict(cls, d: dict) -> "ExperienceLink":
        return cls(label=d.get("label", ""), url=d.get("url", ""))


@dataclass
class ExperienceEntry:
    title: str
    company: str
    location: str = ""
    dates: str = ""
    bullets: List[str] = field(default_factory=list)
    links: List[ExperienceLink] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "ExperienceEntry":
        return cls(
            title=d.get("title", ""),
            company=d.get("company", ""),
            location=d.get("location", ""),
            dates=d.get("dates", ""),
            bullets=d.get("bullets", []),
            links=[ExperienceLink.from_dict(lk) for lk in d.get("links", [])],
        )


@dataclass
class ProjectEntry:
    name: str
    subtitle: str = ""
    location: str = ""
    dates: str = ""
    bullets: List[str] = field(default_factory=list)
    url: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "ProjectEntry":
        return cls(
            name=d.get("name", ""),
            subtitle=d.get("subtitle", ""),
            location=d.get("location", ""),
            dates=d.get("dates", ""),
            bullets=d.get("bullets", []),
            url=d.get("url", ""),
        )


@dataclass
class EducationEntry:
    school: str
    location: str = ""
    dates: str = ""
    degree: str = ""
    details: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "EducationEntry":
        return cls(
            school=d.get("school", ""),
            location=d.get("location", ""),
            dates=d.get("dates", ""),
            degree=d.get("degree", ""),
            details=d.get("details", []),
        )


@dataclass
class ResumeMetadata:
    page_target: str = "one_page"   # one_page | two_page | auto
    tone: str = "modern_professional"
    ats_focus: bool = True
    humanization_pass_complete: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> "ResumeMetadata":
        return cls(
            page_target=d.get("page_target", "one_page"),
            tone=d.get("tone", "modern_professional"),
            ats_focus=d.get("ats_focus", True),
            humanization_pass_complete=d.get("humanization_pass_complete", False),
        )


@dataclass
class TailoredResume:
    candidate_level: str
    target_role: str
    target_company: str
    section_order: List[str]
    header: HeaderData
    summary: str
    skills: SkillsData
    experience: List[ExperienceEntry]
    projects: List[ProjectEntry]
    education: List[EducationEntry]
    certifications: List[str] = field(default_factory=list)
    awards: List[str] = field(default_factory=list)
    metadata: ResumeMetadata = field(default_factory=ResumeMetadata)

    @classmethod
    def from_dict(cls, d: dict) -> "TailoredResume":
        return cls(
            candidate_level=d.get("candidate_level", "mid_level"),
            target_role=d.get("target_role", ""),
            target_company=d.get("target_company", ""),
            section_order=d.get("section_order", [
                "header", "summary", "skills", "experience", "projects", "education"
            ]),
            header=HeaderData.from_dict(d.get("header", {})),
            summary=d.get("summary", ""),
            skills=SkillsData.from_dict(d.get("skills", {})),
            experience=[ExperienceEntry.from_dict(e) for e in d.get("experience", [])],
            projects=[ProjectEntry.from_dict(p) for p in d.get("projects", [])],
            education=[EducationEntry.from_dict(e) for e in d.get("education", [])],
            certifications=d.get("certifications", []),
            awards=d.get("awards", []),
            metadata=ResumeMetadata.from_dict(d.get("metadata", {})),
        )

    def to_dict(self) -> dict:
        """Serialize back to raw dict (for saving JSON artifacts)."""
        import dataclasses
        return dataclasses.asdict(self)
