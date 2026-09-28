import logging
import numpy as np
from typing import Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.config import settings

logger = logging.getLogger(__name__)

class SemanticSimilarityService:
    """
    Computes semantic similarity between resume and job description using Sentence Transformers.
    If the pretrained model cannot be downloaded or initialized (e.g. offline environment),
    it provides a clear fallback using TF-IDF n-gram cosine similarity and documents the limitation.
    """

    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.model = None
        self.is_fallback = False
        self.fallback_reason: Optional[str] = None
        self._initialize_model()

    def _initialize_model(self):
        """Attempts to load SentenceTransformer model, with graceful fallback on failure."""
        try:
            logger.info("Attempting to load SentenceTransformer model: %s...", self.model_name)
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            self.is_fallback = False
            self.fallback_reason = None
            logger.info("SentenceTransformer '%s' loaded successfully.", self.model_name)
        except Exception as e:
            logger.warning(
                "Could not load SentenceTransformer ('%s'): %s. Activating TF-IDF Cosine Similarity Fallback.",
                self.model_name,
                str(e)
            )
            self.model = None
            self.is_fallback = True
            self.fallback_reason = (
                f"Sentence Transformers model '{self.model_name}' could not be initialized or downloaded "
                f"({str(e)}). Fallen back to TF-IDF n-gram Cosine Similarity."
            )

    def calculate_similarity(self, text_a: str, text_b: str) -> Tuple[float, str, bool, Optional[str]]:
        """
        Calculates similarity between two texts.
        Returns:
            similarity_score: float (0.0 to 100.0)
            model_used: str identifier
            is_fallback: bool
            fallback_reason: Optional[str]
        """
        if not text_a.strip() or not text_b.strip():
            return 0.0, "None", False, "One or both input texts were empty."

        # Case 1: SentenceTransformer is available
        if self.model is not None and not self.is_fallback:
            try:
                # Generate dense semantic embeddings
                embeddings = self.model.encode(
                    [text_a, text_b],
                    convert_to_numpy=True,
                    normalize_embeddings=True
                )
                # Cosine similarity between normalized vectors is dot product
                raw_sim = float(np.dot(embeddings[0], embeddings[1]))
                # Cosine similarity is in [-1, 1]; for natural language text embeddings it's typically [0, 1]
                score = round(max(0.0, min(1.0, raw_sim)) * 100.0, 2)
                return score, f"Sentence-Transformers ({self.model_name})", False, None
            except Exception as e:
                logger.error("Inference with SentenceTransformer failed: %s. Switching to fallback.", str(e))
                self.is_fallback = True
                self.fallback_reason = f"Runtime inference failure with SentenceTransformer: {str(e)}"

        # Case 2: TF-IDF Fallback
        score = self._calculate_tfidf_similarity(text_a, text_b)
        return (
            score,
            "TF-IDF Sublinear N-Gram Cosine Similarity (Fallback)",
            True,
            self.fallback_reason or "Operating in TF-IDF fallback mode."
        )

    def _calculate_tfidf_similarity(self, text_a: str, text_b: str) -> float:
        """Fallback method using TF-IDF n-grams (unigrams + bigrams) and cosine similarity."""
        try:
            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2),
                sublinear_tf=True,
                max_features=5000
            )
            tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
            sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            raw_sim = float(sim_matrix[0][0])
            return round(max(0.0, min(1.0, raw_sim)) * 100.0, 2)
        except Exception as e:
            logger.error("TF-IDF calculation failed: %s", str(e))
            return 0.0
