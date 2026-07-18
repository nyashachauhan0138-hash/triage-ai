import sys
import os
from pathlib import Path

# Automatically re-execute using the project's virtual environment if run with system python
try:
    import librosa
    import scipy
    import sklearn
except ImportError:
    script_dir = Path(__file__).resolve().parent
    venv_python = (script_dir.parent.parent / ".venv" / "bin" / "python").absolute()
    if venv_python.exists() and Path(sys.executable).absolute() != venv_python:
        print(f"Required libraries not found in current environment. Re-running script using virtualenv python: {venv_python}")
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)
    else:
        print("Error: Missing required machine learning libraries (librosa, scipy, scikit-learn).")
        sys.exit(1)

# pyrefly: ignore [missing-import]
import pickle
import numpy as np
from scipy.io.wavfile import write as wav_write
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Directory configs
SCRIPT_DIR = Path(__file__).resolve().parent
DATASETS_DIR = SCRIPT_DIR / "datasets" / "voice"
WEIGHTS_DIR = SCRIPT_DIR.parent / "models_weights"
os.makedirs(DATASETS_DIR, exist_ok=True)
os.makedirs(WEIGHTS_DIR, exist_ok=True)

def generate_mock_audio():
    """
    Generates mock WAV audio files. 
    Stressed audio is simulated with higher frequencies and jitter.
    Calm audio is simulated with lower, steady frequencies.
    """
    print("Generating mock audio files for training...")
    sr = 22050
    duration = 3.0  # 3 seconds
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    
    # Generate 10 Calm samples
    for i in range(10):
        # Calm: Steady low frequency sine wave around 120Hz + slight noise
        freq = 120 + np.random.uniform(-5, 5)
        wave = np.sin(2 * np.pi * freq * t) + np.random.normal(0, 0.05, len(t))
        wave = wave / np.max(np.abs(wave))  # normalize
        # Convert to 16-bit PCM for wav_write
        wave_int16 = (wave * 32767).astype(np.int16)
        wav_write(os.path.join(DATASETS_DIR, f"calm_{i}.wav"), sr, wave_int16)

    # Generate 10 Stressed samples
    for i in range(10):
        # Stressed: Higher frequency (e.g., 250Hz) + fast frequency modulation (jitter) + noise
        modulator = 10 * np.sin(2 * np.pi * 5 * t)
        freq = 250 + modulator + np.random.uniform(-10, 10)
        wave = np.sin(2 * np.pi * freq * t) + np.random.normal(0, 0.15, len(t))
        wave = wave / np.max(np.abs(wave))  # normalize
        # Convert to 16-bit PCM for wav_write
        wave_int16 = (wave * 32767).astype(np.int16)
        wav_write(os.path.join(DATASETS_DIR, f"stressed_{i}.wav"), sr, wave_int16)
        
    print(f"Mock audio generated in: {DATASETS_DIR}")

def extract_features(file_path):
    """
    Extracts acoustic features from a WAV file using librosa.
    """
    try:
        y, sr = librosa.load(file_path, sr=22050)
        # 1. Extract 13 MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs.T, axis=0)
        
        # 2. Extract Spectral Centroid (mean brightness)
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        centroid_mean = np.mean(centroid)
        
        # 3. Extract Root-Mean-Square (RMS) Energy (amplitude/volume)
        rms = librosa.feature.rms(y=y)
        rms_mean = np.mean(rms)
        
        # Concatenate features into a single 15-dimensional vector
        features = np.hstack([mfccs_mean, centroid_mean, rms_mean])
        return features
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def train_voice_model():
    # 1. Generate datasets if they don't exist
    if len(os.listdir(DATASETS_DIR)) < 20:
        generate_mock_audio()
        
    # 2. Extract features and build dataset
    print("\nExtracting acoustic features from WAV files...")
    X = []
    y = []
    
    for filename in os.listdir(DATASETS_DIR):
        if filename.endswith(".wav"):
            path = os.path.join(DATASETS_DIR, filename)
            features = extract_features(path)
            if features is not None:
                X.append(features)
                # Label is 1 for stressed, 0 for calm
                label = 1 if "stressed" in filename else 0
                y.append(label)
                
    X = np.array(X)
    y = np.array(y)
    
    print(f"Dataset compiled. Feature matrix shape: {X.shape}, Label shape: {y.shape}")
    
    # 3. Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train Neural Network (MLP Classifier)
    print("Training Multi-Layer Perceptron neural network...")
    clf = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=500, random_state=42)
    clf.fit(X_train, y_train)
    
    # 5. Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc * 100:.2f}%")
    
    # 6. Save Model weights
    output_path = os.path.join(WEIGHTS_DIR, "voice_classifier.pkl")
    print(f"Exporting voice model to: {output_path}")
    with open(output_path, "wb") as f:
        pickle.dump(clf, f)
    print("Voice model saved successfully!")

if __name__ == "__main__":
    train_voice_model()
