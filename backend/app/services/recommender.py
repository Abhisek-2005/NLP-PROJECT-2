import uuid
from typing import List, Dict, Any
from backend.app.schemas.analysis import RecommendationItem

class RecommenderService:
    """Generates actionable, tailored recommendations based on gaps between resume and JD."""

    @staticmethod
    def generate_recommendations(
        overall_score: float,
        semantic_score: float,
        skill_score: float,
        keyword_score: float,
        matched_skills: List[Dict[str, Any]],
        missing_skills: List[Dict[str, Any]],
        sections_found: Dict[str, str],
        resume_word_count: int
    ) -> List[RecommendationItem]:
        recommendations = []

        # 1. Missing Critical Technical Skills
        critical_missing = [s["name"] for s in missing_skills if s.get("importance") == "Critical"]
        if critical_missing:
            top_missing = critical_missing[:4]
            recommendations.append(
                RecommendationItem(
                    id=str(uuid.uuid4())[:8],
                    category="Critical Skills Gap",
                    title=f"Incorporate Missing Core Skills: {', '.join(top_missing)}",
                    message=(
                        f"The job description explicitly prioritizes {', '.join(top_missing)}. "
                        "If you have hands-on experience or coursework with these technologies, "
                        "explicitly feature them in your Skills section and Work Experience bullet points."
                    ),
                    priority="high",
                    impact="+12-18% Match Score"
                )
            )

        # 2. General Missing Skills
        important_missing = [s["name"] for s in missing_skills if s.get("importance") != "Critical"]
        if important_missing:
            top_important = important_missing[:5]
            recommendations.append(
                RecommendationItem(
                    id=str(uuid.uuid4())[:8],
                    category="Secondary Skills",
                    title=f"Highlight Supporting Tools & Methodologies: {', '.join(top_important)}",
                    message=(
                        f"Adding supporting keywords such as {', '.join(top_important)} "
                        "will significantly improve ATS parsing and keyword density."
                    ),
                    priority="medium",
                    impact="+5-8% Match Score"
                )
            )

        # 3. Semantic Alignment & Phrasing
        if semantic_score < 65.0:
            recommendations.append(
                RecommendationItem(
                    id=str(uuid.uuid4())[:8],
                    category="Semantic Alignment",
                    title="Align Contextual Phrasing with the Role",
                    message=(
                        "Your resume's domain vocabulary differs somewhat from the employer's expectations. "
                        "Mirror the terminology used in the job description (e.g. 'designed distributed microservices', "
                        "'built automated CI/CD pipelines', 'conducted A/B testing')."
                    ),
                    priority="high",
                    impact="+8-12% Match Score"
                )
            )

        # 4. Resume Length & Detail
        if resume_word_count < 250:
            recommendations.append(
                RecommendationItem(
                    id=str(uuid.uuid4())[:8],
                    category="Content Depth",
                    title="Expand Experience with Measurable Details",
                    message=(
                        f"Your resume contains only {resume_word_count} words. Standard professional resumes "
                        "typically range between 400 and 800 words. Expand on project outcomes, scale, and tools used."
                    ),
                    priority="high",
                    impact="+10-15% Match Score"
                )
            )
        elif resume_word_count > 1000:
            recommendations.append(
                RecommendationItem(
                    id=str(uuid.uuid4())[:8],
                    category="Conciseness",
                    title="Condense Content for Maximum Punch",
                    message=(
                        f"Your resume is {resume_word_count} words long. Aim for a concise 1-2 page format "
                        "by eliminating outdated experience and focusing on high-impact bullet points."
                    ),
                    priority="low",
                    impact="+3-5% Readability"
                )
            )

        # 5. Section Completeness Check
        essential_sections = ["skills", "experience", "education", "projects"]
        missing_sections = [s.capitalize() for s in essential_sections if s not in sections_found]
        if missing_sections:
            recommendations.append(
                RecommendationItem(
                    id=str(uuid.uuid4())[:8],
                    category="Resume Structure",
                    title=f"Add Standard Section Headers: {', '.join(missing_sections)}",
                    message=(
                        f"Automated ATS parsers look for standard headers like {', '.join(missing_sections)}. "
                        "Clearly separate your resume into distinct, identifiable blocks."
                    ),
                    priority="medium",
                    impact="+6-10% ATS Compatibility"
                )
            )

        # 6. Quantifiable Impact & Action Verbs
        recommendations.append(
            RecommendationItem(
                id=str(uuid.uuid4())[:8],
                category="Impact Phrasing",
                title="Use Quantifiable Metrics & Action Verbs",
                message=(
                    "Begin bullet points with active verbs (Engineered, Architected, Accelerated, Reduced) "
                    "and quantify your achievements using metrics (e.g., 'reduced latency by 35%', 'handled 5M+ daily requests')."
                ),
                priority="medium",
                impact="+5-10% Recruiter Appeal"
            )
        )

        return recommendations
