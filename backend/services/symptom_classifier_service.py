import os
import pickle
from pathlib import Path

# pyrefly: ignore [missing-import]
class SymptomClassifierService:
    _pipeline = None

    @classmethod
    def _load_model(cls):
        if cls._pipeline is None:
            # Resolve path to triage-ai/models_weights/symptom_classifier.pkl
            base_dir = Path(__file__).resolve().parent.parent.parent
            model_path = base_dir / "models_weights" / "symptom_classifier.pkl"
            
            if model_path.exists():
                try:
                    with open(model_path, "rb") as f:
                        cls._pipeline = pickle.load(f)
                    print(f"Loaded custom symptom classifier from {model_path}")
                except Exception as e:
                    print(f"Error loading local model weights: {e}")
            else:
                print(f"Warning: Model weights not found at {model_path}. Run training first.")
        return cls._pipeline

    @classmethod
    def predict(cls, text: str) -> str:
        """
        Predicts the severity ('critical', 'moderate', 'low') of a symptom description.
        """
        pipeline = cls._load_model()
        if pipeline is None:
            return "unknown"
        try:
            prediction = pipeline.predict([text])
            return str(prediction[0])
        except Exception as e:
            print(f"Error during prediction: {e}")
            return "unknown"
