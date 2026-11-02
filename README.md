# MediHybrid — Intelligent Hybrid Healthcare System

**MCA Semester III Soft Computing Major Academic Project**  
*An end-to-end clinical diagnostic platform integrating Genetic Algorithms (GA), Artificial Neural Networks (ANN), Mamdani Fuzzy Inference, and Retinal Convolutional Neural Networks (CNN).*

---

## 🌟 Key Highlights

- **Module 1: Hybrid Tabular Disease Prediction (Diabetes & Heart Disease)**
  - **Genetic Algorithm (GA)** via `DEAP`: Evolves binary chromosome feature masks via tournament selection, 2-point crossover, and bit-flip mutation to select the optimal biomarker subset.
  - **Artificial Neural Network (ANN)**: Multi-layer perceptron (ReLU hidden layers, Adam optimizer, early stopping) trained strictly on GA-selected features.
  - **Mamdani Fuzzy Inference System** (`scikit-fuzzy`): Models clinical ambiguity with triangular and trapezoidal membership functions and centroid defuzzification.
  - **Hybrid Fusion Engine**: Fuses neural network probabilities with fuzzy risk scores:
    $$\text{Hybrid Risk Score} = (0.70 \times \text{ANN Score}) + (0.30 \times \text{Fuzzy Score})$$
  - **Explainable AI (XAI)**: Generates biometric deviation vectors showing risk vs. protective factors.

- **Module 2: RetinaScan — Diabetic Retinopathy CNN**
  - Fine-tuned on the **Kaggle APTOS 2019 Blindness Detection** dataset (5 severity stages: No DR, Mild, Moderate, Severe, Proliferative DR).
  - High diagnostic benchmark: **84.15% test accuracy**, **0.9335 Quadratic Weighted Kappa (QWK)**.
  - **Grad-CAM Attention Heatmaps**: Visualizes the ophthalmic lesions that triggered the prediction.
  - Includes 5 benchmark retinal fundus images for instant testing!

- **Module 3: MediBot AI Health Assistant**
  - Context-aware conversational assistant drawer on the right side of every page.
  - Explains individual patient predictions (*"Why is my fuzzy score high?"*).
  - Bridges to live LLM APIs with an extensive offline soft-computing knowledge engine fallback.

- **New Tools: Report Scanner (OCR) & PDF Generator**
  - **Medical Report Scanner**: Upload PDF or image lab reports; automatically extracts Glucose, Cholesterol, Blood Pressure, BMI, and Age.
  - **PDF Report Download**: Multi-page structured diagnostic assessment reports generated via ReportLab.

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
👉 **http://localhost:8000**

- **Frontend App**: `http://localhost:8000/`
- **Interactive Swagger API Docs**: `http://localhost:8000/docs`
- **ReDoc API Documentation**: `http://localhost:8000/redoc`

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, Tailwind CSS, React Router, Recharts, Lucide React |
| **Backend** | Python FastAPI, Pydantic, SQLAlchemy, SQLite (`medihybrid.db`), Uvicorn |
| **Soft Computing & ML** | DEAP (GA), Scikit-learn (ANN MLP), Scikit-fuzzy (Mamdani), OpenCV, Pillow |
| **Document Tools** | ReportLab (PDF Generation), Regular Expression Clinical OCR Engine |

---

## 📁 Directory Structure

```
MediHybrid/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI application & SPA static mounter
│   │   ├── database.py                # SQLAlchemy SQLite configuration
│   │   ├── models/
│   │   │   ├── schemas.py             # Pydantic validation schemas
│   │   │   └── db_models.py           # Database entities (Assessments, Retinal, Chat)
│   │   ├── services/
│   │   │   ├── fuzzy_service.py       # Scikit-fuzzy Mamdani systems
│   │   │   ├── hybrid_service.py      # GA + ANN + Fuzzy fusion engine
│   │   │   ├── cnn_service.py         # 5-Class CNN & Grad-CAM visualizer
│   │   │   ├── chatbot_service.py     # MediBot context-aware AI assistant
│   │   │   ├── ocr_service.py         # Lab report OCR scanner
│   │   │   └── pdf_service.py         # ReportLab PDF report generator
│   │   └── api/                       # Modular REST endpoints
│   ├── data/                          # Benchmark datasets (diabetes.csv, heart.csv)
│   ├── ml_artifacts/                  # Saved models, metrics, and sample retinal fundus scans
│   └── scripts/                       # Explicit training & evaluation scripts
├── frontend/                          # React + Vite + Tailwind source code
│   ├── src/
│   │   ├── components/                # Navbar, Footer, MediBotDrawer
│   │   └── pages/                     # Home, Dashboard, Diabetes, Heart, RetinaScan, ReportScanner, Lab, Results, History
│   └── dist/                          # Pre-compiled production React SPA build
├── tests/
│   └── test_all_modules.py            # Complete automated unit & integration test suite
├── docs/
│   └── Academic_Project_Report.md     # 26-section comprehensive academic project report
├── run_server.py                      # Enterprise production server launcher
└── README.md
```

---

## 🧪 Running the Test Suite

To verify all soft computing modules, run:
```powershell
python -u MediHybrid/tests/test_all_modules.py
```
*Output: 7 tests passed (0.032s).*

---

## 📚 Re-Training the Models (Optional)

All models and benchmarks are pre-trained. If you wish to re-execute the training pipelines:

1. **Diabetes GA & ANN**:
   ```powershell
   python MediHybrid/backend/scripts/train_diabetes.py
   ```
2. **Heart Disease GA & ANN**:
   ```powershell
   python MediHybrid/backend/scripts/train_heart.py
   ```
3. **Retinopathy CNN Benchmark**:
   ```powershell
   python MediHybrid/backend/scripts/train_retina.py
   ```
