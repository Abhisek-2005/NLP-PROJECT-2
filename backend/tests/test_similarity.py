import pytest
from backend.app.services.similarity import SemanticSimilarityService

def test_semantic_similarity_identical_text():
    service = SemanticSimilarityService()
    text = "Senior Python Engineer with experience in FastAPI and Docker."
    score, model_name, is_fallback, reason = service.calculate_similarity(text, text)
    assert score >= 95.0, f"Identical texts should have very high similarity score (got {score})"
    assert model_name is not None

def test_semantic_similarity_different_text():
    service = SemanticSimilarityService()
    text_a = "Expert in deep learning, neural networks, PyTorch, and transformer models."
    text_b = "Chef specialized in Italian cuisine, pasta making, and restaurant hospitality."
    score, model_name, is_fallback, reason = service.calculate_similarity(text_a, text_b)
    assert score < 50.0, f"Unrelated texts should have low similarity (got {score})"

def test_tfidf_fallback_directly():
    service = SemanticSimilarityService()
    text_a = "Machine learning engineer with Python and TensorFlow experience."
    text_b = "Data scientist specializing in machine learning with Python."
    score = service._calculate_tfidf_similarity(text_a, text_b)
    assert 20.0 <= score <= 100.0
