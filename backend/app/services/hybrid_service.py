"""
hybrid_service.py
=================
Module 1: Hybrid Fusion & Explainability Service
Combines Artificial Neural Network (ANN) classification probabilities with
Mamdani Fuzzy Inference Risk Scores via configurable weighted fusion.
Generates feature attribution impact vectors (Explainable AI / XAI).
All outputs are strictly converted to standard Python native types (JSON-serializable).
"""

import os
import joblib
import numpy as np
import pandas as pd
from app.services.fuzzy_service import diabetes_fuzzy, heart_fuzzy

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ml_artifacts")

# Clinical metadata and healthy references for explainability
DIABETES_SPECS = {
    "Pregnancies": {"name": "Pregnancies", "unit": "count", "ref": 1, "weight_dir": 1},
    "Glucose": {"name": "Fasting Glucose", "unit": "mg/dL", "ref": 95, "weight_dir": 1},
    "BloodPressure": {"name": "Diastolic Blood Pressure", "unit": "mm Hg", "ref": 72, "weight_dir": 1},
    "SkinThickness": {"name": "Triceps Skin Fold", "unit": "mm", "ref": 23, "weight_dir": 1},
    "Insulin": {"name": "Serum Insulin", "unit": "μU/mL", "ref": 85, "weight_dir": 1},
    "BMI": {"name": "Body Mass Index", "unit": "kg/m²", "ref": 22.5, "weight_dir": 1},
    "DiabetesPedigreeFunction": {"name": "Genetic Pedigree Function", "unit": "score", "ref": 0.35, "weight_dir": 1},
    "Age": {"name": "Age", "unit": "years", "ref": 30, "weight_dir": 1}
}

HEART_SPECS = {
    "age": {"name": "Age", "unit": "years", "ref": 45, "weight_dir": 1},
    "sex": {"name": "Biological Sex", "unit": "code", "ref": 0, "weight_dir": 1},
    "cp": {"name": "Chest Pain Type", "unit": "grade 1-4", "ref": 1, "weight_dir": 1},
    "trestbps": {"name": "Resting Systolic BP", "unit": "mm Hg", "ref": 120, "weight_dir": 1},
    "chol": {"name": "Serum Cholesterol", "unit": "mg/dL", "ref": 190, "weight_dir": 1},
    "fbs": {"name": "Fasting Blood Sugar > 120", "unit": "binary", "ref": 0, "weight_dir": 1},
    "restecg": {"name": "Resting ECG", "unit": "code 0-2", "ref": 0, "weight_dir": 1},
    "thalach": {"name": "Max Heart Rate Achieved", "unit": "bpm", "ref": 160, "weight_dir": -1},
    "exang": {"name": "Exercise Induced Angina", "unit": "binary", "ref": 0, "weight_dir": 1},
    "oldpeak": {"name": "ST Depression", "unit": "mm", "ref": 0.2, "weight_dir": 1},
    "slope": {"name": "Slope of Peak ST", "unit": "code 1-3", "ref": 1, "weight_dir": 1},
    "ca": {"name": "Major Vessels Colored", "unit": "count 0-3", "ref": 0, "weight_dir": 1},
    "thal": {"name": "Thalassemia Scan", "unit": "code 3,6,7", "ref": 3, "weight_dir": 1}
}

def to_native(obj):
    """
    Recursively converts NumPy types (np.bool_, np.floating, np.integer, np.ndarray)
    to native Python types (bool, float, int, list) to guarantee strict JSON serializability.
    """
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return [to_native(x) for x in obj.tolist()]
    elif isinstance(obj, dict):
        return {str(k): to_native(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [to_native(x) for x in obj]
    return obj

class HybridAssessmentEngine:
    def __init__(self):
        self.diabetes_ann = None
        self.diabetes_bundle = None
        self.heart_ann = None
        self.heart_bundle = None
        self.load_models()

    def load_models(self):
        d_ann_path = os.path.join(ARTIFACTS_DIR, "diabetes_ann.pkl")
        d_scl_path = os.path.join(ARTIFACTS_DIR, "diabetes_scaler.pkl")
        if os.path.exists(d_ann_path) and os.path.exists(d_scl_path):
            self.diabetes_ann = joblib.load(d_ann_path)
            self.diabetes_bundle = joblib.load(d_scl_path)

        h_ann_path = os.path.join(ARTIFACTS_DIR, "heart_ann.pkl")
        h_scl_path = os.path.join(ARTIFACTS_DIR, "heart_scaler.pkl")
        if os.path.exists(h_ann_path) and os.path.exists(h_scl_path):
            self.heart_ann = joblib.load(h_ann_path)
            self.heart_bundle = joblib.load(h_scl_path)

    def _compute_explainability(self, model, scaler_bundle, input_row, specs):
        all_features = scaler_bundle["all_features"]
        selected_mask = scaler_bundle["selected_mask"]
        scaler = scaler_bundle["scaler"]

        mean_vals = scaler.mean_
        std_vals = scaler.scale_
        first_layer_weights = np.abs(model.coefs_[0]).mean(axis=1)

        contributions = []
        sel_idx = 0

        for i, feat in enumerate(all_features):
            is_selected = bool(selected_mask[i])
            val = float(input_row.get(feat, mean_vals[i]))
            z_score = float((val - mean_vals[i]) / (std_vals[i] if std_vals[i] != 0 else 1.0))
            
            spec = specs.get(feat, {"name": feat, "unit": "", "ref": float(mean_vals[i]), "weight_dir": 1})
            weight_dir = float(spec.get("weight_dir", 1))

            if is_selected:
                weight = float(first_layer_weights[sel_idx])
                sel_idx += 1
            else:
                weight = 0.05

            raw_impact = float(z_score * weight * weight_dir)
            is_risk = bool(raw_impact > 0.08)
            is_protective = bool(raw_impact < -0.08)

            contributions.append({
                "feature": str(feat),
                "label": str(spec["name"]),
                "value": round(val, 2),
                "unit": str(spec["unit"]),
                "reference": float(spec["ref"]),
                "ga_selected": is_selected,
                "z_score": round(z_score, 2),
                "impact_score": round(raw_impact, 3),
                "is_risk_factor": is_risk,
                "is_protective": is_protective,
                "summary": f"Elevated vs baseline ({spec['ref']} {spec['unit']})" if is_risk else (
                    f"Protective healthy level ({spec['ref']} {spec['unit']})" if is_protective else "Neutral median level"
                )
            })

        contributions.sort(key=lambda x: abs(x["impact_score"]), reverse=True)
        return contributions

    def predict_diabetes(self, inputs: dict, w_ann: float = 0.70, w_fuzzy: float = 0.30):
        if self.diabetes_ann is None:
            self.load_models()
            if self.diabetes_ann is None:
                raise RuntimeError("Diabetes model not trained yet. Run train_diabetes.py first.")

        all_feats = self.diabetes_bundle["all_features"]
        sel_mask = self.diabetes_bundle["selected_mask"]
        scaler = self.diabetes_bundle["scaler"]
        medians = self.diabetes_bundle.get("medians", {})
        zero_invalid = self.diabetes_bundle.get("zero_invalid_cols", [])

        row_vals = []
        for feat in all_feats:
            val = float(inputs.get(feat, 0))
            if feat in zero_invalid and val == 0:
                val = float(medians.get(feat, 0))
            row_vals.append(val)

        X_raw = np.array([row_vals])
        X_scaled = scaler.transform(X_raw)
        X_ga = X_scaled[:, sel_mask]

        ann_prob = float(self.diabetes_ann.predict_proba(X_ga)[0, 1])
        ann_score = round(float(ann_prob * 100), 2)

        fuzzy_res = diabetes_fuzzy.evaluate(
            glucose=float(inputs.get("Glucose", 95)),
            bmi=float(inputs.get("BMI", 22.5)),
            bp=float(inputs.get("BloodPressure", 75)),
            age=float(inputs.get("Age", 30))
        )
        fuzzy_score = float(fuzzy_res["fuzzy_score"])

        total_w = float(w_ann + w_fuzzy)
        norm_w_ann = float(w_ann / total_w)
        norm_w_fuzzy = float(w_fuzzy / total_w)
        hybrid_score = round(float((norm_w_ann * ann_score) + (norm_w_fuzzy * fuzzy_score)), 2)

        if hybrid_score < 35.0:
            category = "Low Experimental Risk"
            recommendation = "Metrics remain within low risk parameters. Maintain balanced nutrition, hydration, and periodic routine checkups."
        elif hybrid_score < 65.0:
            category = "Moderate / Borderline Risk"
            recommendation = "Metabolic markers indicate borderline strain. Lifestyle interventions and preventive glycemic monitoring are advised."
        else:
            category = "Elevated Risk"
            recommendation = "Significant biomarker convergence detected. Clinical diagnostic evaluation with an endocrinologist is strongly suggested."

        explainability = self._compute_explainability(
            self.diabetes_ann, self.diabetes_bundle, inputs, DIABETES_SPECS
        )

        selected_feats = [str(f) for f in self.diabetes_bundle["selected_features"]]

        result = {
            "disease": "Diabetes Risk Assessment",
            "ann": {
                "score": ann_score,
                "probability": round(ann_prob, 4),
                "class_prediction": int(ann_prob >= 0.5)
            },
            "fuzzy": fuzzy_res,
            "hybrid": {
                "score": hybrid_score,
                "weights": {"ann_weight": round(norm_w_ann, 2), "fuzzy_weight": round(norm_w_fuzzy, 2)},
                "category": category,
                "recommendation": recommendation
            },
            "ga_selected_features": selected_feats,
            "explainability": explainability,
            "inputs": {k: float(v) if isinstance(v, (int, float)) else v for k, v in inputs.items()}
        }
        return to_native(result)

    def predict_heart(self, inputs: dict, w_ann: float = 0.70, w_fuzzy: float = 0.30):
        if self.heart_ann is None:
            self.load_models()
            if self.heart_ann is None:
                raise RuntimeError("Heart disease model not trained yet. Run train_heart.py first.")

        all_feats = self.heart_bundle["all_features"]
        sel_mask = self.heart_bundle["selected_mask"]
        scaler = self.heart_bundle["scaler"]

        row_vals = [float(inputs.get(feat, 0)) for feat in all_feats]
        X_raw = np.array([row_vals])
        X_scaled = scaler.transform(X_raw)
        X_ga = X_scaled[:, sel_mask]

        ann_prob = float(self.heart_ann.predict_proba(X_ga)[0, 1])
        ann_score = round(float(ann_prob * 100), 2)

        fuzzy_res = heart_fuzzy.evaluate(
            age=float(inputs.get("age", 45)),
            chol=float(inputs.get("chol", 200)),
            bp=float(inputs.get("trestbps", 120)),
            hr=float(inputs.get("thalach", 150)),
            oldpeak=float(inputs.get("oldpeak", 0.5))
        )
        fuzzy_score = float(fuzzy_res["fuzzy_score"])

        total_w = float(w_ann + w_fuzzy)
        norm_w_ann = float(w_ann / total_w)
        norm_w_fuzzy = float(w_fuzzy / total_w)
        hybrid_score = round(float((norm_w_ann * ann_score) + (norm_w_fuzzy * fuzzy_score)), 2)

        if hybrid_score < 35.0:
            category = "Low Experimental Risk"
            recommendation = "Cardiovascular indicators are in the favorable baseline range. Continue regular aerobic activity and heart-healthy diet."
        elif hybrid_score < 65.0:
            category = "Moderate / Borderline Risk"
            recommendation = "Mild cardiac stress markers observed. Consider monitoring lipid profile and resting blood pressure quarterly."
        else:
            category = "Elevated Risk"
            recommendation = "Pronounced ischemic or hemodynamic risk markers identified. Medical consultation with a cardiologist is recommended."

        explainability = self._compute_explainability(
            self.heart_ann, self.heart_bundle, inputs, HEART_SPECS
        )

        selected_feats = [str(f) for f in self.heart_bundle["selected_features"]]

        result = {
            "disease": "Heart Disease Risk Assessment",
            "ann": {
                "score": ann_score,
                "probability": round(ann_prob, 4),
                "class_prediction": int(ann_prob >= 0.5)
            },
            "fuzzy": fuzzy_res,
            "hybrid": {
                "score": hybrid_score,
                "weights": {"ann_weight": round(norm_w_ann, 2), "fuzzy_weight": round(norm_w_fuzzy, 2)},
                "category": category,
                "recommendation": recommendation
            },
            "ga_selected_features": selected_feats,
            "explainability": explainability,
            "inputs": {k: float(v) if isinstance(v, (int, float)) else v for k, v in inputs.items()}
        }
        return to_native(result)

# Singleton instance
hybrid_engine = HybridAssessmentEngine()
