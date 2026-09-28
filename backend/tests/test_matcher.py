import pytest
from backend.app.services.skill_extractor import SkillExtractionService
from backend.app.services.matcher import ResumeMatcherPipeline

def test_skill_extraction():
    service = SkillExtractionService()
    text = "Candidate has strong knowledge of Python, React, Docker, Kubernetes, and PostgreSQL."
    skills = service.extract_skills(text)
    skill_names = {s["name"] for s in skills}
    
    assert "Python" in skill_names
    assert "React" in skill_names
    assert "Docker" in skill_names
    assert "Kubernetes" in skill_names
    assert "PostgreSQL" in skill_names

def test_skill_comparison():
    service = SkillExtractionService()
    resume_skills = [
        {"name": "Python", "category": "Programming Languages"},
        {"name": "FastAPI", "category": "Frameworks & Libraries"},
    ]
    job_skills = [
        {"name": "Python", "category": "Programming Languages"},
        {"name": "FastAPI", "category": "Frameworks & Libraries"},
        {"name": "Kubernetes", "category": "Cloud & DevOps"},
    ]
    matched, missing, score = service.compare_skills(resume_skills, job_skills)
    matched_names = {m["name"] for m in matched}
    missing_names = {m["name"] for m in missing}

    assert "Python" in matched_names
    assert "FastAPI" in matched_names
    assert "Kubernetes" in missing_names
    assert 50.0 <= score <= 90.0

def test_full_pipeline_analysis():
    pipeline = ResumeMatcherPipeline()
    resume = "Experienced Python developer with expertise in FastAPI, PostgreSQL, Docker, and RESTful APIs."
    job_desc = "Seeking a Backend Engineer proficient in Python, FastAPI, Docker, and AWS."

    result = pipeline.analyze(
        resume_text=resume,
        job_description=job_desc,
        resume_filename="test_resume.txt",
        job_title="Backend Engineer"
    )

    assert result.scores.overall_score > 0
    assert result.scores.semantic_score > 0
    assert len(result.matched_skills) > 0
    assert len(result.recommendations) > 0
