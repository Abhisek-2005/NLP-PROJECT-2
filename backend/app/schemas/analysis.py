from pydantic import BaseModel, Field
from typing import Optional

class TextAnalysisRequest(BaseModel):
    resume_text: str = Field(..., min_length=20, description="Raw text of the resume")
    job_description: str = Field(..., min_length=20, description="Job description text")
    job_title: Optional[str] = Field("Target Role", description="Job title or role name")
    resume_filename: Optional[str] = Field("Pasted_Resume.txt", description="Display name for resume")

class SkillItem(BaseModel):
    name: str
    category: str
    is_matched: bool = False
    importance: Optional[str] = "Normal"  # Critical, Important, Nice-to-have

class ScoreBreakdown(BaseModel):
    overall_score: float = Field(..., ge=0, le=100)
    semantic_score: float = Field(..., ge=0, le=100)
    skill_score: float = Field(..., ge=0, le=100)
    keyword_score: float = Field(..., ge=0, le=100)
    semantic_weight: float
    skill_weight: float
    keyword_weight: float

class RecommendationItem(BaseModel):
    id: str
    category: str  # Critical Skills, Formatting, Action Verbs, Section Strength, Keyword Density
    title: str
    message: str
    priority: str  # high, medium, low
    impact: str    # "+5-10% Match", etc.

class TextStats(BaseModel):
    resume_word_count: int
    job_word_count: int
    resume_character_count: int
    job_character_count: int
    common_keywords_count: int
    total_skills_detected_resume: int
    total_skills_detected_job: int

class AnalysisResponse(BaseModel):
    id: str
    created_at: Optional[str] = None
    resume_filename: str
    job_title: str
    scores: ScoreBreakdown
    matched_skills: list[SkillItem]
    missing_skills: list[SkillItem]
    all_resume_skills: list[SkillItem]
    all_job_skills: list[SkillItem]
    recommendations: list[RecommendationItem]
    model_used: str
    is_fallback: bool
    fallback_reason: Optional[str] = None
    text_stats: TextStats
    resume_preview: Optional[str] = None
    job_preview: Optional[str] = None

class HistorySummaryItem(BaseModel):
    id: str
    created_at: str
    resume_filename: str
    job_title: str
    overall_score: float
    semantic_score: float
    skill_score: float
    keyword_score: float
    model_used: str

class DeleteResponse(BaseModel):
    success: bool
    message: str
