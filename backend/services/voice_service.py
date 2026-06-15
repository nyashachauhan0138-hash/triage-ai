# pyrefly: ignore [missing-import]
import librosa
# pyrefly: ignore [missing-import]
import numpy as np


class VoiceService:

    @staticmethod
    def analyze(audio_path):
        try:
            y, sr = librosa.load(audio_path)
            if len(y) == 0:
                raise ValueError("Empty audio signal")

            try:
                pitch = np.mean(
                    librosa.yin(
                        y,
                        fmin=50,
                        fmax=300
                    )
                )
                if np.isnan(pitch):
                    pitch = 120.0
            except Exception:
                pitch = 120.0

            try:
                energy = np.mean(
                    librosa.feature.rms(y=y)
                )
                if np.isnan(energy):
                    energy = 0.05
            except Exception:
                energy = 0.05

            stress_score = int(
                min(
                    100,
                    (energy * 1000) + (pitch / 4)
                )
            )
        except Exception as e:
            print(f"Error in VoiceService: {e}")
            stress_score = 50

        emotion = "calm"

        if stress_score > 75:
            emotion = "high stress"

        elif stress_score > 45:
            emotion = "anxious"

        return {
            "stress_score": stress_score,
            "emotion": emotion
        }