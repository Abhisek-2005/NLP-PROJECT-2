import aiosqlite
import json
import logging
from contextlib import asynccontextmanager
from typing import Any, Optional, AsyncGenerator
from backend.app.config import settings

logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[aiosqlite.Connection, None]:
    """Provides an async context manager for SQLite database connection with row factory."""
    settings.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = await aiosqlite.connect(settings.DB_PATH)
    conn.row_factory = aiosqlite.Row
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resume_filename TEXT NOT NULL,
            job_title TEXT NOT NULL,
            overall_score REAL NOT NULL,
            semantic_score REAL NOT NULL,
            skill_score REAL NOT NULL,
            keyword_score REAL NOT NULL,
            model_used TEXT NOT NULL,
            matched_skills TEXT NOT NULL,
            missing_skills TEXT NOT NULL,
            all_resume_skills TEXT NOT NULL,
            all_job_skills TEXT NOT NULL,
            recommendations TEXT NOT NULL,
            resume_preview TEXT,
            job_preview TEXT
        )
    """)
    await conn.commit()
    try:
        yield conn
    finally:
        await conn.close()

async def init_db():
    """Initializes SQLite database tables."""
    async with get_db_connection() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resume_filename TEXT NOT NULL,
                job_title TEXT NOT NULL,
                overall_score REAL NOT NULL,
                semantic_score REAL NOT NULL,
                skill_score REAL NOT NULL,
                keyword_score REAL NOT NULL,
                model_used TEXT NOT NULL,
                matched_skills TEXT NOT NULL,
                missing_skills TEXT NOT NULL,
                all_resume_skills TEXT NOT NULL,
                all_job_skills TEXT NOT NULL,
                recommendations TEXT NOT NULL,
                resume_preview TEXT,
                job_preview TEXT
            )
        """)
        await conn.commit()
    logger.info("Database initialized successfully at %s", settings.DB_PATH)

async def save_analysis(record: dict[str, Any]) -> str:
    """Inserts a new analysis record."""
    async with get_db_connection() as conn:
        await conn.execute(
            """
            INSERT INTO analysis_history (
                id, resume_filename, job_title, overall_score, semantic_score,
                skill_score, keyword_score, model_used, matched_skills,
                missing_skills, all_resume_skills, all_job_skills,
                recommendations, resume_preview, job_preview
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["resume_filename"],
                record["job_title"],
                record["overall_score"],
                record["semantic_score"],
                record["skill_score"],
                record["keyword_score"],
                record["model_used"],
                json.dumps(record["matched_skills"]),
                json.dumps(record["missing_skills"]),
                json.dumps(record["all_resume_skills"]),
                json.dumps(record["all_job_skills"]),
                json.dumps(record["recommendations"]),
                record.get("resume_preview", "")[:500],
                record.get("job_preview", "")[:500],
            ),
        )
        await conn.commit()
    return record["id"]

async def get_all_history(limit: int = 50) -> list[dict[str, Any]]:
    """Fetches list of historical analyses ordered by newest first."""
    async with get_db_connection() as conn:
        cursor = await conn.execute(
            """
            SELECT id, created_at, resume_filename, job_title,
                   overall_score, semantic_score, skill_score, keyword_score, model_used
            FROM analysis_history
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_analysis_by_id(analysis_id: str) -> Optional[dict[str, Any]]:
    """Fetches full analysis report by ID."""
    async with get_db_connection() as conn:
        cursor = await conn.execute(
            "SELECT * FROM analysis_history WHERE id = ?",
            (analysis_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return None
        data = dict(row)
        data["matched_skills"] = json.loads(data["matched_skills"])
        data["missing_skills"] = json.loads(data["missing_skills"])
        data["all_resume_skills"] = json.loads(data["all_resume_skills"])
        data["all_job_skills"] = json.loads(data["all_job_skills"])
        data["recommendations"] = json.loads(data["recommendations"])
        return data

async def delete_analysis_by_id(analysis_id: str) -> bool:
    """Deletes a record by ID."""
    async with get_db_connection() as conn:
        cursor = await conn.execute(
            "DELETE FROM analysis_history WHERE id = ?",
            (analysis_id,)
        )
        await conn.commit()
        return cursor.rowcount > 0

async def clear_all_history() -> int:
    """Deletes all history records."""
    async with get_db_connection() as conn:
        cursor = await conn.execute("DELETE FROM analysis_history")
        await conn.commit()
        return cursor.rowcount
