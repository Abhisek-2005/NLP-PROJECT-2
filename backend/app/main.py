import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.config import settings
from backend.app.database import init_db
from backend.app.routers import analyze_router, history_router, health_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("resume_matcher")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup and shutdown routines."""
    logger.info("Starting up Resume–Job Description Matching API...")
    # Initialize SQLite database schema
    await init_db()
    logger.info("Database initialization verified.")
    yield
    logger.info("Shutting down Resume–Job Description Matching API...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## Real-Time NLP Resume–Job Description Matching Engine
    
    This production-ready API provides:
    - **Document Extraction**: PyMuPDF (.pdf), python-docx (.docx), and plain text (.txt).
    - **NLP Skill Taxonomy Extraction**: Recognizes over 100+ technical skills and soft skills.
    - **Dense Semantic Similarity**: Utilizes Sentence-Transformers (`all-MiniLM-L6-v2`) with automatic TF-IDF fallback.
    - **Lexical Keyword Overlap**: Jaccard index + job coverage metrics.
    - **Weighted Match Scoring**: Dynamic composite scoring (0-100).
    - **Actionable Gap Analysis**: Detailed recommendations for closing candidate skill gaps.
    - **Persistent History**: Asynchronous SQLite history with deletion and lookup.
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Error Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred while processing your request.", "error": str(exc)}
    )

# Include Routers
app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(analyze_router, prefix=settings.API_V1_PREFIX)
app.include_router(history_router, prefix=settings.API_V1_PREFIX)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API v{settings.VERSION}",
        "docs": "/docs",
        "api_health": f"{settings.API_V1_PREFIX}/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
