# Resume–Job Description Matching Using NLP 🚀

A production-grade, full-stack AI/ML application that evaluates resume alignment with job descriptions using an end-to-end Natural Language Processing (NLP) pipeline.

Built with **Python**, **FastAPI**, **Sentence-Transformers**, **PyMuPDF**, **python-docx**, **scikit-learn**, **React**, **Vite**, **Tailwind CSS**, and **SQLite**.

---

## 🌟 Key Features

- **Multi-Format Document Extraction**:
  - Native parsing for **PDF** files via PyMuPDF (`fitz`).
  - Native parsing for **DOCX** files via `python-docx` (paragraphs and tables).
  - Plain text (**TXT**) and manual paste support with character/word counters.
- **Real NLP Pipeline (No Hardcoded or Mock Data)**:
  - **Sentence-Transformers Embeddings**: Uses `all-MiniLM-L6-v2` dense vectors for contextual semantic similarity.
  - **Graceful TF-IDF Fallback**: Automatic fallback to Sublinear N-gram TF-IDF Cosine Similarity if offline or model download is restricted, with explicit diagnostics.
  - **Skill Taxonomy Extraction**: Scans against 100+ industry skills across Programming Languages, AI/Data Science, Frameworks, Cloud/DevOps, Databases, and Architecture.
  - **Keyword & Vocabulary Overlap**: Calculates Jaccard token overlap and job requirement lexical coverage.
- **Dynamic Composite Match Scoring (0–100)**:
  - Default weighting:
    - **45%** Semantic Similarity (Contextual Embeddings)
    - **40%** Skill Coverage (Matched vs. Missing Skills with Critical weighting)
    - **15%** Lexical Keyword Overlap
- **Actionable Gap Analysis & Recommendations**:
  - Categorized missing skills (Critical vs. Secondary).
  - Formatting suggestions, action verbs, and quantifiable achievements advice.
  - Estimated match score impact for each recommendation (e.g. `+12-18% Match`).
- **Interactive Professional Dashboard**:
  - Radial SVG animated score gauge with dynamic color themes (Emerald / Blue / Amber / Rose).
  - Searchable and category-filterable skill chips with one-click copy.
  - Pre-loaded sample presets (NLP Engineer, Full Stack Developer, DevOps Engineer).
  - Print / Export PDF summary report.
- **Persistent Analysis History in SQLite**:
  - Automatically records all analyses using asynchronous `aiosqlite`.
  - View full historical reports.
  - Delete individual records or clear history.

---

## 🏗️ Architecture

```
                          ┌────────────────────────┐
                          │   React + Vite + TW    │
                          │   Frontend Dashboard   │
                          └───────────┬────────────┘
                                      │ REST API / JSON / Multipart
                                      ▼
                          ┌────────────────────────┐
                          │    FastAPI Backend     │
                          │    (uvicorn:8001)      │
                          └───────────┬────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│ Document Parser  │        │  NLP Pipeline    │        │  SQLite Database │
│ - PyMuPDF (PDF)  │        │ - Sentence-      │        │ - aiosqlite      │
│ - python-docx    │        │   Transformers   │        │ - Analysis       │
│ - TXT Extractor  │        │ - Skill Taxonomy │        │   History        │
└──────────────────┘        │ - TF-IDF Fallback│        └──────────────────┘
                            │ - Scikit-Learn   │
                            └──────────────────┘
```

---

## 📂 Project Structure

```
DL PROJECT/
├── backend/
│   ├── app/
│   │   ├── config.py              # Application settings and scoring weights
│   │   ├── database.py            # SQLite async database schema & CRUD
│   │   ├── main.py                # FastAPI app, lifespan, CORS, middleware
│   │   ├── models/                # Database models
│   │   ├── schemas/
│   │   │   └── analysis.py        # Pydantic validation schemas
│   │   ├── services/
│   │   │   ├── extractor.py       # PyMuPDF & python-docx file extractors
│   │   │   ├── preprocessor.py    # NLP text cleaning & section detector
│   │   │   ├── similarity.py      # Sentence-Transformers & TF-IDF fallback
│   │   │   ├── skill_extractor.py # 100+ skill taxonomy & matcher
│   │   │   ├── matcher.py         # End-to-end weighted composite pipeline
│   │   │   └── recommender.py     # Actionable recommendation engine
│   │   └── routers/
│   │       ├── analyze.py         # File & text analysis endpoints
│   │       ├── history.py         # History listing & deletion endpoints
│   │       └── health.py          # Health check & role sample presets
│   ├── data/
│   │   └── resume_matcher.db      # SQLite database
│   ├── sample_data/
│   │   ├── sample_resume_ml_nlp_engineer.pdf
│   │   ├── sample_resume_full_stack.docx
│   │   └── sample_resume_devops.txt
│   ├── tests/
│   │   ├── test_extractor.py      # PDF, DOCX, TXT extraction tests
│   │   ├── test_similarity.py     # Semantic embeddings & TF-IDF tests
│   │   ├── test_matcher.py        # Skills extraction & pipeline tests
│   │   └── test_api.py            # FastAPI integration & CRUD tests
│   ├── requirements.txt           # Python dependencies
│   └── .env.example               # Configurable environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── ResumeUploader.jsx
│   │   │   ├── JobDescriptionInput.jsx
│   │   │   ├── ScoreGauge.jsx
│   │   │   ├── SkillsComparison.jsx
│   │   │   ├── RecommendationsView.jsx
│   │   │   ├── AnalysisDashboard.jsx
│   │   │   ├── HistoryModal.jsx
│   │   │   └── SampleSelector.jsx
│   │   ├── services/
│   │   │   └── api.js             # Fetch API client
│   │   ├── App.jsx                # Main application UI
│   │   ├── index.css              # Custom Tailwind CSS & glassmorphic styling
│   │   └── main.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vite.config.js
├── README.md
├── start.bat                      # One-click launcher for both services
├── run_backend.bat                # Launch FastAPI backend
└── run_frontend.bat               # Launch Vite React frontend
```

---

## ⚡ Quick Start

### 1. Launch Everything (Windows One-Click)
Double-click `start.bat` in the project root, or execute:
```powershell
.\start.bat
```
This automatically launches:
- **Backend**: `http://127.0.0.1:8001` (API Docs: `http://127.0.0.1:8001/docs`)
- **Frontend**: `http://127.0.0.1:5173`

---

### 2. Manual Launch

#### Backend:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001 --reload
```

#### Frontend:
```bash
cd frontend
npm run dev
```

---

## 🧪 Running Automated Tests

All 14 tests in the test suite validate file extraction, NLP sentence embeddings, skill taxonomy matching, TF-IDF fallback, and API endpoints.

```bash
python -m pytest backend/tests -v
```

---

## 📖 API Documentation

Once the backend is running, open your browser to:
- **Interactive Swagger UI**: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8001/redoc](http://127.0.0.1:8001/redoc)

### Primary Endpoints:
- `POST /api/analyze/file`: Multipart upload (`.pdf`, `.docx`, `.txt`) + `job_description`.
- `POST /api/analyze/text`: JSON payload (`resume_text`, `job_description`, `job_title`).
- `GET /api/history`: Returns list of past analysis records from SQLite.
- `GET /api/history/{id}`: Returns full detailed analysis report.
- `DELETE /api/history/{id}`: Deletes an analysis record.
- `DELETE /api/history`: Clears all history.
- `GET /api/samples`: Returns pre-configured sample resumes & job descriptions.
- `GET /api/health`: System health, active NLP model, and fallback status.
