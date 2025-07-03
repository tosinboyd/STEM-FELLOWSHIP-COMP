import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# === Load data ===
df = pd.read_csv("data.csv")

# === Map class labels ===
df['label'] = df['class'].map({'H': 0, 'P': 1})
df = df.dropna()

# === Function to average across tasks 1, 2, 12 ===
def avg_feature(col_base):
    return df[[f"{col_base}1", f"{col_base}2", f"{col_base}12"]].mean(axis=1)

# === Compute unified 14 features ===
df["total_time"] = avg_feature("total_time")
df["air_time"] = avg_feature("air_time")
df["paper_time"] = avg_feature("paper_time")
df["mean_speed"] = avg_feature("mean_speed_in_air") + avg_feature("mean_speed_on_paper") / 2
df["mean_acc"] = avg_feature("mean_acc_in_air") + avg_feature("mean_acc_on_paper") / 2
df["pressure_mean"] = avg_feature("pressure_mean")
df["pressure_var"] = avg_feature("pressure_var")
df["num_of_pendown"] = avg_feature("num_of_pendown")
df["max_x"] = avg_feature("max_x_extension")
df["max_y"] = avg_feature("max_y_extension")
df["GMRTP"] = avg_feature("gmrt_in_air") + avg_feature("gmrt_on_paper") / 2
df["mean_jerk"] = avg_feature("mean_jerk_in_air") + avg_feature("mean_jerk_on_paper") / 2
df["disp_index"] = avg_feature("disp_index")
# (Average CISP omitted or proxied by disp_index)

# === Final 14 features ===
features_14 = [
    "total_time",
    "air_time",
    "paper_time",
    "mean_speed",
    "mean_acc",
    "pressure_mean",
    "pressure_var",
    "num_of_pendown",
    "max_x",
    "max_y",
    "GMRTP",
    "mean_jerk",
    "disp_index"
]

X = df[features_14].values
y = df["label"].values

# === Normalize and split ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.35, stratify=y, random_state=42
)

# === Train and export model ===
rf_model = RandomForestClassifier(n_estimators=93, random_state=42)
rf_model.fit(X_train, y_train)

print(f"✅ Test accuracy: {rf_model.score(X_test, y_test):.3f}")

# === Save model and scaler ===
joblib.dump(rf_model, "model14.pkl")
joblib.dump(scaler, "scaler14.pkl")
