import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)
SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "nlp_model" in data

def test_samples_endpoint():
    response = client.get("/api/samples")
    assert response.status_code == 200
    samples = response.json()
    assert len(samples) >= 3
    assert any(s["id"] == "ml-nlp-engineer" for s in samples)

def test_analyze_text_endpoint():
    payload = {
        "resume_text": "Experienced Python Software Engineer with expertise in FastAPI, PostgreSQL, Docker, and REST APIs.",
        "job_description": "We are seeking a Backend Developer with Python, FastAPI, Docker, and PostgreSQL experience.",
        "job_title": "Backend Python Developer"
    }
    response = client.post("/api/analyze/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert data["scores"]["overall_score"] >= 60.0
    assert len(data["matched_skills"]) >= 2
    assert len(data["recommendations"]) > 0

def test_analyze_file_endpoint():
    pdf_path = SAMPLE_DIR / "sample_resume_ml_nlp_engineer.pdf"
    assert pdf_path.exists()
    
    with open(pdf_path, "rb") as f:
        files = {"resume_file": ("sample_resume.pdf", f, "application/pdf")}
        data = {
            "job_description": "We need an NLP Engineer with PyTorch, Transformers, Python, and Docker experience.",
            "job_title": "NLP Engineer"
        }
        response = client.post("/api/analyze/file", files=files, data=data)
    
    assert response.status_code == 200
    result = response.json()
    assert result["resume_filename"] == "sample_resume.pdf"
    assert result["scores"]["overall_score"] > 50.0

def test_history_crud_endpoints():
    # 1. First trigger an analysis to ensure history has an item
    payload = {
        "resume_text": "DevOps Engineer skilled in Kubernetes, Docker, Terraform, and AWS CI/CD pipelines.",
        "job_description": "Hiring a DevOps Engineer with Kubernetes, AWS, and Terraform proficiency.",
        "job_title": "DevOps Engineer"
    }
    analyze_resp = client.post("/api/analyze/text", json=payload)
    assert analyze_resp.status_code == 200
    record_id = analyze_resp.json()["id"]

    # 2. Get history list
    hist_resp = client.get("/api/history")
    assert hist_resp.status_code == 200
    hist_list = hist_resp.json()
    assert any(item["id"] == record_id for item in hist_list)

    # 3. Get single item by ID
    single_resp = client.get(f"/api/history/{record_id}")
    assert single_resp.status_code == 200
    assert single_resp.json()["id"] == record_id

    # 4. Delete the item
    del_resp = client.delete(f"/api/history/{record_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["success"] is True

    # 5. Verify deletion
    single_after_del = client.get(f"/api/history/{record_id}")
    assert single_after_del.status_code == 404
