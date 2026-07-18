import os
import pickle
from pathlib import Path
from typing import Dict

class DiseaseClassifierService:
    _classifier = None
    _vectorizer = None

    @classmethod
    def _load_model(cls):
        if cls._classifier is None or cls._vectorizer is None:
            base_dir = Path(__file__).resolve().parent.parent.parent
            model_path = base_dir / "models_weights" / "disease_classifier.pkl"
            vec_path = base_dir / "models_weights" / "disease_vectorizer.pkl"
            
            if model_path.exists() and vec_path.exists():
                try:
                    with open(model_path, "rb") as f:
                        cls._classifier = pickle.load(f)
                    with open(vec_path, "rb") as f:
                        cls._vectorizer = pickle.load(f)
                    print("Loaded custom symptom-to-disease classifier successfully.")
                except Exception as e:
                    print(f"Error loading disease classifier: {e}")
            else:
                print(f"Warning: Disease model/vectorizer not found at {model_path}. Run training first.")
        return cls._classifier, cls._vectorizer

    @classmethod
    def predict(cls, text: str) -> Dict[str, float]:
        """
        Predicts the probability distribution of potential conditions based on the symptom text.
        """
        clf, vec = cls._load_model()
        if clf is None or vec is None:
            return {}
        try:
            X = vec.transform([text])
            probs = clf.predict_proba(X)[0]
            classes = clf.classes_
            
            # Map classes to their predicted probabilities
            results = {str(c): float(p) for c, p in zip(classes, probs) if p > 0.0}
            return results
        except Exception as e:
            print(f"Error during disease classification: {e}")
            return {}
