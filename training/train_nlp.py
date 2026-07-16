import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Define folder outputs
WEIGHTS_DIR = "../models_weights"
os.makedirs(WEIGHTS_DIR, exist_ok=True)

# 2. Mock dataset representing patient symptoms and triage severities
data = {
    "symptom": [
        "chest pain and pressure, tightness in left arm",
        "shortness of breath, heavy chest, trouble breathing",
        "sudden numbness in face and left side body, speech slurred",
        "severe headache and high fever with stiff neck",
        "coughing up blood, sharp pain when inhaling",
        
        "mild cough and runny nose, slight throat irritation",
        "scratched my elbow playing football, minor bleeding",
        "feeling tired and mild headache after long screen time",
        "stubbed my toe, slight swelling but can walk",
        "dry throat, sneezing, feel like a common cold",
        
        "stomach pain and vomiting after eating street food",
        "sprained my ankle, swollen and painful to press",
        "moderate fever 101F, body aches and chills",
        "persistent back pain for two weeks, dull ache",
        "burn on hand from hot tea, minor blistering"
    ],
    "severity": [
        "critical", "critical", "critical", "critical", "critical",
        "low", "low", "low", "low", "low",
        "moderate", "moderate", "moderate", "moderate", "moderate"
    ]
}

def train_triage_model():
    print("=== TriageAI Custom Model Training ===")
    
    # Load into pandas DataFrame
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} training samples.")
    
    # Split features and labels
    X = df["symptom"]
    y = df["severity"]
    
    # Split into train & test splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define vectorizer + classifier pipeline
    print("Building TF-IDF + Logistic Regression pipeline...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
        ('clf', LogisticRegression(C=1.0, random_state=42))
    ])
    
    # Train the model
    print("Fitting model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = pipeline.predict(X_test)
    print("\nEvaluation Metrics:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Save the trained model weights
    output_path = os.path.join(WEIGHTS_DIR, "symptom_classifier.pkl")
    print(f"Exporting model to: {output_path}")
    with open(output_path, "wb") as f:
        pickle.dump(pipeline, f)
        
    print("Model saved successfully!")

if __name__ == "__main__":
    train_triage_model()
