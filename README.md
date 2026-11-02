# MediHybrid — Intelligent Hybrid Healthcare System

**MCA Semester III Soft Computing Major Academic Project**

An end-to-end clinical diagnostic platform integrating Genetic Algorithms (GA), Artificial Neural Networks (ANN), Mamdani Fuzzy Inference, and Retinal Convolutional Neural Networks (CNN).

---

## 🌟 Key Highlights

### Module 1: Hybrid Tabular Disease Prediction (Diabetes & Heart Disease)

- **Genetic Algorithm (GA)** via `DEAP`: Evolves binary chromosome feature masks using tournament selection, 2-point crossover, and bit-flip mutation to select the optimal biomarker subset.
- **Artificial Neural Network (ANN):** Multi-layer perceptron with ReLU hidden layers, Adam optimizer, and early stopping, trained strictly on GA-selected features.
- **Mamdani Fuzzy Inference System** (`scikit-fuzzy`): Models clinical ambiguity using triangular and trapezoidal membership functions and centroid defuzzification.
- **Hybrid Fusion Engine:** Combines neural network probabilities with fuzzy risk scores:

  \[
  \text{Hybrid Risk Score} = (0.70 \times \text{ANN Score}) + (0.30 \times \text{Fuzzy Score})
  \]

- **Explainable AI (XAI):** Generates biometric deviation vectors showing risk and protective factors.

### Module 2: RetinaScan — Diabetic Retinopathy CNN

- Fine-tuned on the **Kaggle APTOS 2019 Blindness Detection** dataset.
- Identifies five severity stages:
  1. No DR
  2. Mild
  3. Moderate
  4. Severe
  5. Proliferative DR
- Reported benchmark performance:
  - **84.15% test accuracy**
  - **0.9335 Quadratic Weighted Kappa (QWK)**
- **Grad-CAM Attention Heatmaps:** Visualizes retinal regions influencing predictions.
- Includes five benchmark retinal fundus images for instant testing.

### Module 3: MediBot AI Health Assistant

- Context-aware conversational assistant drawer available on every page.
- Explains individual patient predictions, such as "Why is my fuzzy score high?"
- Integrates live LLM APIs with an offline soft-computing knowledge engine fallback.

### Module 4: Medical Report Scanner (OCR) & PDF Generator

- **Medical Report Scanner:** Upload PDF or image-based lab reports and automatically extract Glucose, Cholesterol, Blood Pressure, BMI, and Age.
- **PDF Report Generator:** Creates structured, multi-page diagnostic assessment reports using ReportLab.

---

## 🚀 Quick Start (Single-Command Run)

### Option 1: One-Click Launcher (Windows)

Double-click `start_medihybrid.bat` in the project root directory.

### Option 2: Python Command Line

```powershell
cd MediHybrid
python run_server.py
```

Open your browser and navigate to:

**http://localhost:8000/**

Available application endpoints:

- **Frontend Application:** http://localhost:8000/
- **Interactive Swagger API Docs:** http://localhost:8000/docs
- **ReDoc API Documentation:** http://localhost:8000/redoc

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, React Router, Recharts, Lucide React |
| Backend | Python FastAPI, Pydantic, SQLAlchemy, SQLite (`medihybrid.db`), Uvicorn |
| Soft Computing & ML | DEAP (GA), Scikit-learn (ANN MLP), Scikit-fuzzy (Mamdani), OpenCV, Pillow |
| Document Tools | ReportLab (PDF Generation), Regular Expression Clinical OCR Engine |

---

## 📁 Directory Structure

```text
MediHybrid/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── schemas.py
│   │   │   └── db_models.py
│   │   ├── services/
│   │   │   ├── fuzzy_service.py
│   │   │   ├── hybrid_service.py
│   │   │   ├── cnn_service.py
│   │   │   ├── chatbot_service.py
│   │   │   ├── ocr_service.py
│   │   │   └── pdf_service.py
│   │   └── api/
│   ├── data/
│   ├── ml_artifacts/
│   └── scripts/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── pages/
│   └── dist/
├── tests/
│   └── test_all_modules.py
├── docs/
│   └── Academic_Project_Report.md
├── run_server.py
└── README.md
```

---

## 🧪 Running the Test Suite

To verify the soft-computing modules, execute:

```powershell
python -u MediHybrid/tests/test_all_modules.py
```

**Previously reported test result:** 7 tests passed (0.032s).

---

## 📚 Re-Training the Models (Optional)

All models and benchmarks are provided as pre-trained artifacts. To execute the training pipelines again:

### 1. Diabetes GA & ANN

```powershell
python MediHybrid/backend/scripts/train_diabetes.py
```

### 2. Heart Disease GA & ANN

```powershell
python MediHybrid/backend/scripts/train_heart.py
```

### 3. Retinopathy CNN Benchmark

```powershell
python MediHybrid/backend/scripts/train_retina.py
```

---

## ⚠️ Disclaimer

MediHybrid is an academic project developed for educational and research purposes. Its predictions are experimental and should not be considered a substitute for professional medical diagnosis, clinical evaluation, or treatment.

---

**Developed as part of the MCA Semester III Soft Computing Major Academic Project.**