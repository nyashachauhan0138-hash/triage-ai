# pyrefly: ignore [missing-import]
import os
import pickle
import librosa
import numpy as np
from pathlib import Path

class VoiceService:
    _clf = None

    @classmethod
    def _load_model(cls):
        if cls._clf is None:
            # Resolve path to triage-ai/models_weights/voice_classifier.pkl
            base_dir = Path(__file__).resolve().parent.parent.parent
            model_path = base_dir / "models_weights" / "voice_classifier.pkl"
            
            if model_path.exists():
                try:
                    with open(model_path, "rb") as f:
                        cls._clf = pickle.load(f)
                    print(f"Loaded custom voice classifier from {model_path}")
                except Exception as e:
                    print(f"Error loading voice model weights: {e}")
            else:
                print(f"Warning: Voice model weights not found at {model_path}. Run training first.")
        return cls._clf

    @staticmethod
    def analyze(audio_path):
        # 1. Fallback / baseline values
        pitch = 120.0
        energy = 0.05
        centroid_mean = 1000.0
        
        try:
            y, sr = librosa.load(audio_path, sr=22050)
            if len(y) == 0:
                raise ValueError("Empty audio signal")

            # Extract raw parameters for fallback or features
            try:
                yin_pitch = librosa.yin(y, fmin=50, fmax=300)
                pitch = np.mean(yin_pitch) if len(yin_pitch) > 0 else 120.0
                if np.isnan(pitch):
                    pitch = 120.0
            except Exception:
                pass

            try:
                rms_vals = librosa.feature.rms(y=y)
                energy = np.mean(rms_vals) if len(rms_vals) > 0 else 0.05
                if np.isnan(energy):
                    energy = 0.05
            except Exception:
                pass

            # Extract features for classifier
            clf = VoiceService._load_model()
            if clf is not None:
                try:
                    # 13 MFCCs
                    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                    mfccs_mean = np.mean(mfccs.T, axis=0)
                    
                    # Spectral Centroid
                    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
                    centroid_mean = np.mean(centroid)
                    
                    # Package features
                    features = np.hstack([mfccs_mean, centroid_mean, energy])
                    
                    # Predict probability of stress (class 1)
                    prob_stressed = clf.predict_proba([features])[0][1]
                    stress_score = int(prob_stressed * 100)
                    print(f"Custom voice model predicted stress probability: {prob_stressed:.4f}")
                except Exception as eval_err:
                    print(f"Prediction failed, falling back to rule-based logic: {eval_err}")
                    # Rule-based calculation if inference fails
                    stress_score = int(min(100, (energy * 1000) + (pitch / 4)))
            else:
                # Rule-based calculation if model not loaded
                stress_score = int(min(100, (energy * 1000) + (pitch / 4)))

        except Exception as e:
            print(f"Error in VoiceService: {e}")
            stress_score = 50

        # Map score to emotion string
        emotion = "calm"
        if stress_score > 75:
            emotion = "high stress"
        elif stress_score > 45:
            emotion = "anxious"

        return {
            "stress_score": stress_score,
            "emotion": emotion
        }