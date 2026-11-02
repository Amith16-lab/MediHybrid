"""
endpoints_algorithms.py
=======================
Endpoints for Algorithm Laboratory:
Provides detailed parameters, curves, chromosomes, and membership data for:
- Genetic Algorithm (GA)
- Artificial Neural Network (ANN)
- Mamdani Fuzzy Inference System
- Convolutional Neural Network (CNN)
"""

import os
import json
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Algorithm Laboratory & System Health"])

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ml_artifacts")

def _load_json(filename):
    path = os.path.join(ARTIFACTS_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "MediHybrid Intelligent Healthcare Engine",
        "modules": {
            "module1_hybrid_ga_ann_fuzzy": "online",
            "module2_retina_cnn": "online",
            "module3_medibot": "online",
            "medical_report_ocr": "online"
        },
        "database": "sqlite/sqlalchemy",
        "api_framework": "FastAPI"
    }

@router.get("/models/metrics")
def get_all_metrics():
    return {
        "diabetes": _load_json("diabetes_metrics.json"),
        "heart": _load_json("heart_metrics.json"),
        "retina": _load_json("retina_metrics.json")
    }

@router.get("/models/features")
def get_features_comparison():
    return {
        "diabetes_ga": _load_json("diabetes_ga.json"),
        "heart_ga": _load_json("heart_ga.json")
    }

@router.get("/algorithms/ga")
def get_ga_lab_data():
    return {
        "diabetes": _load_json("diabetes_ga.json"),
        "heart": _load_json("heart_ga.json"),
        "hyperparameters": {
            "population_size": 20,
            "generations": 10,
            "crossover_probability": 0.60,
            "mutation_probability": 0.20,
            "selection_strategy": "Tournament Selection (size=3)",
            "fitness_function": "5-Fold Stratified Cross-Validated ROC-AUC with Parsimony Penalty"
        }
    }

@router.get("/algorithms/ann")
def get_ann_lab_data():
    return {
        "diabetes": _load_json("diabetes_metrics.json"),
        "heart": _load_json("heart_metrics.json")
    }

@router.get("/algorithms/cnn")
def get_cnn_lab_data():
    return _load_json("retina_metrics.json")

@router.get("/algorithms/fuzzy")
def get_fuzzy_lab_data():
    # Returns coordinates for membership curves for dynamic frontend rendering
    return {
        "diabetes": {
            "glucose": {
                "universe": [40, 260],
                "curves": [
                    {"name": "Normal", "type": "trapezoidal", "points": [40, 40, 90, 110]},
                    {"name": "Moderate", "type": "triangular", "points": [100, 125, 150]},
                    {"name": "High", "type": "trapezoidal", "points": [140, 170, 260, 260]}
                ]
            },
            "bmi": {
                "universe": [12, 60],
                "curves": [
                    {"name": "Normal", "type": "trapezoidal", "points": [12, 12, 20, 25]},
                    {"name": "Overweight", "type": "triangular", "points": [24, 27.5, 31]},
                    {"name": "Obese", "type": "trapezoidal", "points": [29, 35, 60, 60]}
                ]
            },
            "risk_output": {
                "universe": [0, 100],
                "curves": [
                    {"name": "Low Risk", "type": "trapezoidal", "points": [0, 0, 20, 35]},
                    {"name": "Moderate Risk", "type": "triangular", "points": [25, 50, 75]},
                    {"name": "High Risk", "type": "trapezoidal", "points": [65, 80, 100, 100]}
                ]
            }
        },
        "heart": {
            "cholesterol": {
                "universe": [100, 500],
                "curves": [
                    {"name": "Desirable", "type": "trapezoidal", "points": [100, 100, 180, 200]},
                    {"name": "Borderline", "type": "triangular", "points": [190, 225, 250]},
                    {"name": "High", "type": "trapezoidal", "points": [240, 280, 500, 500]}
                ]
            },
            "st_depression": {
                "universe": [0, 6.5],
                "curves": [
                    {"name": "Normal", "type": "trapezoidal", "points": [0, 0, 0.8, 1.5]},
                    {"name": "Elevated", "type": "trapezoidal", "points": [1.2, 2.5, 6.5, 6.5]}
                ]
            }
        }
    }
