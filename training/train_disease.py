import sys
import os
from pathlib import Path

# Self-bootstrapping redirection to the project virtual environment
try:
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier
    import pickle
except ImportError:
    script_dir = Path(__file__).resolve().parent
    venv_python = (script_dir.parent.parent / ".venv" / "bin" / "python").absolute()
    if venv_python.exists() and Path(sys.executable).absolute() != venv_python:
        print(f"Required training libraries not found. Re-running script using virtualenv python: {venv_python}")
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)
    else:
        print("Error: Missing required machine learning libraries (pandas, scikit-learn).")
        sys.exit(1)

# Resolve directories
SCRIPT_DIR = Path(__file__).resolve().parent
WEIGHTS_DIR = SCRIPT_DIR.parent / "models_weights"
os.makedirs(WEIGHTS_DIR, exist_ok=True)

# Training dataset containing symptom descriptions mapped to suspected conditions
data = {
    "description": [
        # Heart Attack (Myocardial Infarction)
        "severe crushing chest pain radiating to the left arm and sweating",
        "i have tightness in my chest left arm hurts and i am perspiring",
        "crushing pressure in chest shortness of breath and cold sweat",
        "left arm pain with severe heavy chest pain and trouble breathing",
        
        # Dengue Fever
        "high fever with severe joint pain body aches and a skin rash",
        "running a high temperature pain behind eyes joint aches and red spots",
        "severe muscle aches high fever retro-orbital eye pain and body rash",
        "extreme joint pain and hot fever with red rash spots on skin",
        
        # Urinary Tract Infection (UTI)
        "burning sensation while urinating frequent urination cloudy urine",
        "hurts to pee need to go to the toilet constantly lower stomach discomfort",
        "painful urination cloudy strong-smelling urine and constant urge to pee",
        "frequent urination burning urination lower abdominal cramps",
        
        # Appendicitis
        "abdominal pain starting near navel moving to right lower quadrant with nausea",
        "sharp pain in right lower stomach loss of appetite fever and vomiting",
        "rlq pain stomach hurts loss of appetite and nausea",
        "abdominal cramps migrated to the right lower stomach tender to touch",
        
        # Pneumonia
        "cough with yellow phlegm high fever and difficulty breathing",
        "coughing up yellow mucus fever chills and chest pain when deep breathing",
        "shortness of breath high fever productive cough with thick phlegm",
        "chest pain productive cough with mucus and cold chills",
        
        # Migraine
        "severe pulsating headache on one side of head with nausea and light sensitivity",
        "throbbing headache sensitive to light and sound with vomiting",
        "intense unilateral headache visual aura nausea and sound sensitivity",
        "pulsating severe headache with blurry vision and light sensitivity",
        
        # Common Cold
        "mild cough runny nose sneezing and scratchy sore throat",
        "congestion sneezing runny nose with minor throat irritation",
        "runny nose sore throat sneezing and mild cough",
        "congestion runny nose sore throat and sneezing"
    ],
    "disease": [
        "Myocardial Infarction", "Myocardial Infarction", "Myocardial Infarction", "Myocardial Infarction",
        "Dengue", "Dengue", "Dengue", "Dengue",
        "Urinary Tract Infection", "Urinary Tract Infection", "Urinary Tract Infection", "Urinary Tract Infection",
        "Appendicitis", "Appendicitis", "Appendicitis", "Appendicitis",
        "Pneumonia", "Pneumonia", "Pneumonia", "Pneumonia",
        "Migraine", "Migraine", "Migraine", "Migraine",
        "Common Cold", "Common Cold", "Common Cold", "Common Cold"
    ]
}

def train_disease_model():
    print("=== Training Symptom-to-Disease ML Model ===")
    df = pd.DataFrame(data)
    print(f"Dataset Size: {len(df)} samples.")

    # Vectorize symptom text descriptions
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    X = vectorizer.fit_transform(df["description"])
    y = df["disease"]

    # Train a Random Forest Classifier
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(X, y)
    print("Model training completed successfully.")

    # Save vectorizer and classifier
    model_output_path = WEIGHTS_DIR / "disease_classifier.pkl"
    vectorizer_output_path = WEIGHTS_DIR / "disease_vectorizer.pkl"

    with open(model_output_path, "wb") as f:
        pickle.dump(classifier, f)
    with open(vectorizer_output_path, "wb") as f:
        pickle.dump(vectorizer, f)

    print(f"Disease model saved to: {model_output_path}")
    print(f"Vectorizer saved to: {vectorizer_output_path}")

if __name__ == "__main__":
    train_disease_model()
