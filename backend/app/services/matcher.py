import uuid
import datetime
from typing import Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from backend.app.config import settings
from backend.app.services.preprocessor import TextPreprocessor
from backend.app.services.skill_extractor import SkillExtractionService
from backend.app.services.similarity import SemanticSimilarityService
from backend.app.services.recommender import RecommenderService
from backend.app.schemas.analysis import (
    AnalysisResponse,
    ScoreBreakdown,
    SkillItem,
    TextStats
)

class ResumeMatcherPipeline:
    """End-to-end NLP matching pipeline for resumes and job descriptions."""

    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.skill_service = SkillExtractionService()
        self.similarity_service = SemanticSimilarityService()
        self.recommender_service = RecommenderService()

    def calculate_keyword_overlap(self, resume_text: str, job_text: str) -> float:
        """
        Calculates lexical/keyword overlap using Jaccard similarity and TF-IDF key term overlap.
        """
        resume_tokens = set(self.preprocessor.tokenize(resume_text, remove_stopwords=True))
        job_tokens = set(self.preprocessor.tokenize(job_text, remove_stopwords=True))

        if not job_tokens or not resume_tokens:
            return 0.0

        # Jaccard index
        intersection = resume_tokens.intersection(job_tokens)
        union = resume_tokens.union(job_tokens)
        jaccard = (len(intersection) / max(1, len(union))) * 100.0

        # Overlap relative to the job requirements (recall)
        job_coverage = (len(intersection) / max(1, len(job_tokens))) * 100.0

        # Hybrid keyword score (weighted towards job coverage)
        keyword_score = round(0.70 * job_coverage + 0.30 * jaccard, 2)
        return min(100.0, max(0.0, keyword_score))

    def analyze(
        self,
        resume_text: str,
        job_description: str,
        resume_filename: str = "Uploaded_Resume",
        job_title: str = "Target Position"
    ) -> AnalysisResponse:
        """
        Executes complete NLP pipeline:
        1. Text normalization & section extraction
        2. Skill extraction for both documents
        3. Skill comparison (matched vs missing)
        4. Semantic embedding similarity via Sentence-Transformers (or TF-IDF fallback)
        5. Keyword overlap computation
        6. Weighted aggregate match score computation
        7. Tailored recommendations generation
        """
        analysis_id = str(uuid.uuid4())
        created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # 1. Clean & normalize texts
        clean_resume = self.preprocessor.normalize_text(resume_text)
        clean_job = self.preprocessor.normalize_text(job_description)

        sections = self.preprocessor.extract_sections(clean_resume)
        resume_words = len(clean_resume.split())
        job_words = len(clean_job.split())

        # 2. Extract skills
        resume_skills_raw = self.skill_service.extract_skills(clean_resume)
        job_skills_raw = self.skill_service.extract_skills(clean_job)

        # 3. Compare skills
        matched_raw, missing_raw, skill_score = self.skill_service.compare_skills(
            resume_skills_raw, job_skills_raw
        )

        # 4. Calculate semantic similarity using Sentence Transformers (or fallback)
        semantic_score, model_name, is_fallback, fallback_reason = self.similarity_service.calculate_similarity(
            clean_resume, clean_job
        )

        # 5. Keyword overlap
        keyword_score = self.calculate_keyword_overlap(clean_resume, clean_job)

        # 6. Weighted composite score
        w_sem = settings.SEMANTIC_WEIGHT
        w_sk = settings.SKILL_WEIGHT
        w_kw = settings.KEYWORD_WEIGHT

        overall_score = round(
            (w_sem * semantic_score) + (w_sk * skill_score) + (w_kw * keyword_score),
            1
        )
        overall_score = max(0.0, min(100.0, overall_score))

        # 7. Convert skill items to schema
        matched_skills = [
            SkillItem(name=s["name"], category=s["category"], is_matched=True, importance=s["importance"])
            for s in matched_raw
        ]
        missing_skills = [
            SkillItem(name=s["name"], category=s["category"], is_matched=False, importance=s["importance"])
            for s in missing_raw
        ]
        all_resume_skills = [
            SkillItem(name=s["name"], category=s["category"], is_matched=True, importance=s.get("importance", "Normal"))
            for s in resume_skills_raw
        ]
        all_job_skills = [
            SkillItem(name=s["name"], category=s["category"], is_matched=False, importance=s.get("importance", "Important"))
            for s in job_skills_raw
        ]

        # 8. Generate recommendations
        recommendations = self.recommender_service.generate_recommendations(
            overall_score=overall_score,
            semantic_score=semantic_score,
            skill_score=skill_score,
            keyword_score=keyword_score,
            matched_skills=matched_raw,
            missing_skills=missing_raw,
            sections_found=sections,
            resume_word_count=resume_words
        )

        # 9. Compute text statistics
        resume_tokens = set(self.preprocessor.tokenize(clean_resume, remove_stopwords=True))
        job_tokens = set(self.preprocessor.tokenize(clean_job, remove_stopwords=True))
        common_count = len(resume_tokens.intersection(job_tokens))

        stats = TextStats(
            resume_word_count=resume_words,
            job_word_count=job_words,
            resume_character_count=len(clean_resume),
            job_character_count=len(clean_job),
            common_keywords_count=common_count,
            total_skills_detected_resume=len(resume_skills_raw),
            total_skills_detected_job=len(job_skills_raw)
        )

        score_breakdown = ScoreBreakdown(
            overall_score=overall_score,
            semantic_score=semantic_score,
            skill_score=skill_score,
            keyword_score=keyword_score,
            semantic_weight=w_sem,
            skill_weight=w_sk,
            keyword_weight=w_kw
        )

        return AnalysisResponse(
            id=analysis_id,
            created_at=created_at,
            resume_filename=resume_filename,
            job_title=job_title,
            scores=score_breakdown,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            all_resume_skills=all_resume_skills,
            all_job_skills=all_job_skills,
            recommendations=recommendations,
            model_used=model_name,
            is_fallback=is_fallback,
            fallback_reason=fallback_reason,
            text_stats=stats,
            resume_preview=clean_resume[:400] + ("..." if len(clean_resume) > 400 else ""),
            job_preview=clean_job[:400] + ("..." if len(clean_job) > 400 else "")
        )

# Global pipeline instance
matcher_pipeline = ResumeMatcherPipeline()
