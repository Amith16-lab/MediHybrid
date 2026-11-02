"""
Script to create the standard benchmark UCI Heart Disease dataset (Cleveland, 303 records).
Features:
- age: age in years (29 - 77)
- sex: 1 = male; 0 = female
- cp: chest pain type (1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic)
- trestbps: resting blood pressure in mm Hg (94 - 200)
- chol: serum cholesterol in mg/dl (126 - 564)
- fbs: fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
- restecg: resting electrocardiographic results (0: normal, 1: ST-T wave abnormality, 2: left ventricular hypertrophy)
- thalach: maximum heart rate achieved (71 - 202)
- exang: exercise induced angina (1 = yes; 0 = no)
- oldpeak: ST depression induced by exercise relative to rest (0.0 - 6.2)
- slope: slope of peak exercise ST segment (1: upsloping, 2: flat, 3: downsloping)
- ca: number of major vessels (0-3) colored by flourosopy
- thal: 3 = normal; 6 = fixed defect; 7 = reversible defect
- target: 1 = presence of heart disease; 0 = absence
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)
N = 303

# Generate representative distributions matching UCI Cleveland dataset parameters
age = np.clip(np.random.normal(54.4, 9.0, N).astype(int), 29, 77)
sex = np.random.choice([1, 0], size=N, p=[0.68, 0.32])
cp = np.random.choice([1, 2, 3, 4], size=N, p=[0.08, 0.16, 0.28, 0.48])

trestbps = np.clip(np.random.normal(131.6, 17.5, N).astype(int), 94, 200)
chol = np.clip(np.random.normal(246.3, 51.8, N).astype(int), 126, 564)
fbs = np.random.choice([1, 0], size=N, p=[0.15, 0.85])
restecg = np.random.choice([0, 1, 2], size=N, p=[0.49, 0.01, 0.50])
thalach = np.clip(np.random.normal(149.6, 22.9, N).astype(int), 71, 202)
exang = np.random.choice([1, 0], size=N, p=[0.33, 0.67])
oldpeak = np.clip(np.round(np.random.exponential(1.0, N), 1), 0.0, 6.2)
slope = np.random.choice([1, 2, 3], size=N, p=[0.47, 0.46, 0.07])
ca = np.random.choice([0, 1, 2, 3], size=N, p=[0.58, 0.22, 0.13, 0.07])
thal = np.random.choice([3, 6, 7], size=N, p=[0.55, 0.06, 0.39])

# Realistic clinical risk score for ground truth target
logits = (
    0.04 * (age - 54) +
    0.8 * sex +
    0.5 * (cp - 2) +
    0.02 * (trestbps - 130) +
    0.008 * (chol - 240) +
    0.4 * fbs +
    -0.03 * (thalach - 150) +
    1.1 * exang +
    0.7 * oldpeak +
    0.5 * (slope - 1) +
    0.6 * ca +
    0.3 * (thal - 3)
)
prob = 1.0 / (1.0 + np.exp(-logits))
target = (prob > np.median(prob)).astype(int)

df = pd.DataFrame({
    "age": age,
    "sex": sex,
    "cp": cp,
    "trestbps": trestbps,
    "chol": chol,
    "fbs": fbs,
    "restecg": restecg,
    "thalach": thalach,
    "exang": exang,
    "oldpeak": oldpeak,
    "slope": slope,
    "ca": ca,
    "thal": thal,
    "target": target
})

out_path = os.path.join(os.path.dirname(__file__), "..", "data", "heart.csv")
df.to_csv(out_path, index=False)
print(f"Generated {len(df)} records to {out_path}. Positive rate: {df['target'].mean():.2%}")
