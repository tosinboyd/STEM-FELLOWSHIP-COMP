# === IMPORTS ===
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib


# === LOAD & PREPROCESS DATA ===
df = pd.read_csv("data.csv")
df['label'] = df['class'].map({'H': 0, 'P': 1})
df = df.dropna()

X = df.drop(columns=['ID', 'class', 'label']).values
y = df['label'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# === RANDOM FOREST TRAINING ===
rf_model = RandomForestClassifier(n_estimators=93, random_state=42)
rf_model.fit(X_train, y_train)

# === RISK CATEGORIZATION FUNCTION ===
def classify_risk(risk):
    if risk < 0.33:
        return "Low Risk"
    elif risk < 0.66:
        return "Medium Risk"
    else:
        return "High Risk"

# === RANDOM FOREST PROBABILITY PREDICTIONS ===
y_probs_rf = rf_model.predict_proba(X_test)[:, 1]

low_risk_rf = (y_probs_rf <= 0.33)
medium_risk_rf = (y_probs_rf > 0.33) & (y_probs_rf <= 0.66)
high_risk_rf = (y_probs_rf > 0.66)

# Save
joblib.dump(rf_model, "model.pkl")

# Load
model = joblib.load("model.pkl")
