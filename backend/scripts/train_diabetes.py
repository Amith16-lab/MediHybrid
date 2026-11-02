"""
train_diabetes.py
=================
Module 1: Soft-Computing Training Pipeline for Diabetes Risk Assessment
- Feature Selection: Genetic Algorithm implemented via DEAP
- Neural Network Classification: Multi-Layer Perceptron (ANN) with ReLU hidden layers
- Rigorous holdout test set evaluation with zero data leakage
"""

import os
import json
import random
import warnings
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)
from deap import base, creator, tools

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "diabetes.csv")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "..", "ml_artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

FEATURE_NAMES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]

ZERO_INVALID_COLS = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

def run_diabetes_pipeline():
    print("=" * 60)
    print(" [1/3] Loading and Preprocessing Diabetes Dataset...")
    print("=" * 60)
    
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} samples with {len(FEATURE_NAMES)} features.")

    train_df, test_df = train_test_split(df, test_size=0.20, random_state=42, stratify=df["Outcome"])
    train_df = train_df.copy()
    test_df = test_df.copy()

    medians = {}
    for col in ZERO_INVALID_COLS:
        non_zero_median = train_df[train_df[col] > 0][col].median()
        medians[col] = float(non_zero_median)
        train_df[col] = train_df[col].replace(0, non_zero_median)
        test_df[col] = test_df[col].replace(0, non_zero_median)

    X_train_raw = train_df[FEATURE_NAMES].values
    y_train = train_df["Outcome"].values
    X_test_raw = test_df[FEATURE_NAMES].values
    y_test = test_df["Outcome"].values

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_raw)
    X_test_scaled = scaler.transform(X_test_raw)

    print(f"Training set: {X_train_scaled.shape}, Test set: {X_test_scaled.shape}")

    # -------------------------------------------------------------
    # Genetic Algorithm (DEAP) for Feature Selection
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print(" [2/3] Running DEAP Genetic Algorithm for Feature Selection...")
    print("=" * 60)

    random.seed(42)
    np.random.seed(42)

    if hasattr(creator, "FitnessMax"):
        del creator.FitnessMax
    if hasattr(creator, "Individual"):
        del creator.Individual

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(FEATURE_NAMES))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval_features(individual):
        mask = [bool(bit) for bit in individual]
        if sum(mask) == 0:
            return (0.0,)
        X_sub = X_train_scaled[:, mask]
        clf = MLPClassifier(hidden_layer_sizes=(8,), solver="lbfgs", max_iter=60, random_state=42)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scores = cross_val_score(clf, X_sub, y_train, cv=cv, scoring="roc_auc")
        penalty = 0.005 * (sum(mask) / len(mask))
        fitness = float(np.mean(scores)) - penalty
        return (fitness,)

    toolbox.register("evaluate", eval_features)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.15)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=20)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("max", np.max)

    evolution_history = []
    CXPB, MUTPB, NGEN = 0.6, 0.2, 10

    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    hof.update(pop)
    best_init = float(hof[0].fitness.values[0])
    evolution_history.append({"generation": 0, "best_fitness": round(best_init, 4), "features_count": sum(hof[0])})

    for gen in range(1, NGEN + 1):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind)

        pop[:] = offspring
        hof.update(pop)
        record = stats.compile(pop)
        best_fit = float(record["max"])
        best_ind = hof[0]
        evolution_history.append({
            "generation": gen,
            "best_fitness": round(best_fit, 4),
            "features_count": sum(best_ind)
        })
        print(f" Gen {gen:02d}: Best Fitness = {best_fit:.4f} (Active Features: {sum(best_ind)})")

    best_individual = hof[0]
    selected_mask = [bool(bit) for bit in best_individual]
    selected_feature_names = [FEATURE_NAMES[i] for i, bit in enumerate(selected_mask) if bit]
    print(f"\n=> GA Selected {len(selected_feature_names)}/{len(FEATURE_NAMES)} Features: {selected_feature_names}")

    # -------------------------------------------------------------
    # Artificial Neural Network Training (Selected Features Only)
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print(" [3/3] Training Production Artificial Neural Network (ANN)...")
    print("=" * 60)

    X_train_ga = X_train_scaled[:, selected_mask]
    X_test_ga = X_test_scaled[:, selected_mask]

    ann = MLPClassifier(
        hidden_layer_sizes=(32, 16),
        activation="relu",
        solver="adam",
        learning_rate_init=0.01,
        max_iter=500,
        early_stopping=True,
        validation_fraction=0.15,
        n_iter_no_change=20,
        random_state=42
    )

    ann.fit(X_train_ga, y_train)

    y_pred = ann.predict(X_test_ga)
    y_prob = ann.predict_proba(X_test_ga)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_prob))
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = [int(v) for v in cm.ravel()]

    print(f" Test Accuracy  : {acc:.4f}")
    print(f" Test ROC-AUC   : {roc_auc:.4f}")
    print(f" Test Precision : {prec:.4f}")
    print(f" Test Recall    : {rec:.4f}")
    print(f" Test F1-Score  : {f1:.4f}")
    print(f" Confusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")

    ga_payload = {
        "disease": "Diabetes",
        "total_features": len(FEATURE_NAMES),
        "selected_count": len(selected_feature_names),
        "all_features": FEATURE_NAMES,
        "selected_features": selected_feature_names,
        "chromosome": [int(b) for b in best_individual],
        "evolution_history": evolution_history,
        "method": "DEAP Genetic Algorithm (Tournament Selection + 2-Point Crossover + Bit-Flip Mutation)"
    }
    with open(os.path.join(ARTIFACTS_DIR, "diabetes_ga.json"), "w", encoding="utf-8") as f:
        json.dump(ga_payload, f, indent=2)

    metrics_payload = {
        "disease": "Diabetes",
        "dataset": "Pima Indians Diabetes Database (UCI/Kaggle)",
        "samples_total": len(df),
        "test_samples": len(y_test),
        "test_metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4)
        },
        "confusion_matrix": {
            "true_negatives": tn,
            "false_positives": fp,
            "false_negatives": fn,
            "true_positives": tp
        },
        "training_curves": {
            "loss": [round(float(v), 5) for v in ann.loss_curve_],
            "validation_scores": [round(float(v), 4) for v in getattr(ann, "validation_scores_", [])]
        },
        "architecture": {
            "input_dim": len(selected_feature_names),
            "hidden_layers": [32, 16],
            "activations": ["relu", "relu", "sigmoid"],
            "optimizer": "Adam (learning_rate=0.01)",
            "iterations_completed": int(ann.n_iter_)
        }
    }
    with open(os.path.join(ARTIFACTS_DIR, "diabetes_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    scaler_bundle = {
        "scaler": scaler,
        "all_features": FEATURE_NAMES,
        "selected_features": selected_feature_names,
        "selected_mask": selected_mask,
        "medians": medians,
        "zero_invalid_cols": ZERO_INVALID_COLS
    }
    joblib.dump(ann, os.path.join(ARTIFACTS_DIR, "diabetes_ann.pkl"))
    joblib.dump(scaler_bundle, os.path.join(ARTIFACTS_DIR, "diabetes_scaler.pkl"))
    print("\nSaved all diabetes model artifacts to:", ARTIFACTS_DIR)

if __name__ == "__main__":
    run_diabetes_pipeline()
