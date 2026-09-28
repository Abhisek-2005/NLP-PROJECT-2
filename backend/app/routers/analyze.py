import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.app.schemas.analysis import AnalysisResponse, TextAnalysisRequest
from backend.app.services.extractor import DocumentExtractorService
from backend.app.services.matcher import matcher_pipeline
from backend.app.database import save_analysis

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analyze", tags=["Analysis"])

@router.post("/file", response_model=AnalysisResponse, summary="Analyze Resume File against Job Description")
async def analyze_file(
    resume_file: UploadFile = File(..., description="PDF or DOCX or TXT resume document"),
    job_description: str = Form(..., min_length=20, description="Job description text"),
    job_title: str = Form("Target Role", description="Job title or role name")
):
    """
    Extracts text from uploaded resume (PDF/DOCX/TXT), runs the NLP pipeline
    against the provided job description, calculates match score, and saves to history.
    """
    if not resume_file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file missing filename.")

    content = await resume_file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Extract text from file
    resume_text = DocumentExtractorService.extract(resume_file.filename, content)
    if len(resume_text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Extracted resume text is too short or empty.")

    # Execute NLP pipeline
    result = matcher_pipeline.analyze(
        resume_text=resume_text,
        job_description=job_description,
        resume_filename=resume_file.filename,
        job_title=job_title
    )

    # Persist in SQLite
    try:
        record = {
            "id": result.id,
            "resume_filename": result.resume_filename,
            "job_title": result.job_title,
            "overall_score": result.scores.overall_score,
            "semantic_score": result.scores.semantic_score,
            "skill_score": result.scores.skill_score,
            "keyword_score": result.scores.keyword_score,
            "model_used": result.model_used,
            "matched_skills": [s.model_dump() for s in result.matched_skills],
            "missing_skills": [s.model_dump() for s in result.missing_skills],
            "all_resume_skills": [s.model_dump() for s in result.all_resume_skills],
            "all_job_skills": [s.model_dump() for s in result.all_job_skills],
            "recommendations": [r.model_dump() for r in result.recommendations],
            "resume_preview": result.resume_preview,
            "job_preview": result.job_preview,
        }
        await save_analysis(record)
    except Exception as e:
        logger.error("Failed to save analysis to history: %s", str(e))

    return result

@router.post("/text", response_model=AnalysisResponse, summary="Analyze Pasted Resume Text against Job Description")
async def analyze_text(request: TextAnalysisRequest):
    """
    Runs the NLP matching pipeline directly on provided resume text and job description.
    """
    result = matcher_pipeline.analyze(
        resume_text=request.resume_text,
        job_description=request.job_description,
        resume_filename=request.resume_filename or "Pasted_Resume.txt",
        job_title=request.job_title or "Target Role"
    )

    # Persist in SQLite
    try:
        record = {
            "id": result.id,
            "resume_filename": result.resume_filename,
            "job_title": result.job_title,
            "overall_score": result.scores.overall_score,
            "semantic_score": result.scores.semantic_score,
            "skill_score": result.scores.skill_score,
            "keyword_score": result.scores.keyword_score,
            "model_used": result.model_used,
            "matched_skills": [s.model_dump() for s in result.matched_skills],
            "missing_skills": [s.model_dump() for s in result.missing_skills],
            "all_resume_skills": [s.model_dump() for s in result.all_resume_skills],
            "all_job_skills": [s.model_dump() for s in result.all_job_skills],
            "recommendations": [r.model_dump() for r in result.recommendations],
            "resume_preview": result.resume_preview,
            "job_preview": result.job_preview,
        }
        await save_analysis(record)
    except Exception as e:
        logger.error("Failed to save analysis to history: %s", str(e))

    return result
