"""
schemas.py
==========
Pydantic input and output validation schemas for MediHybrid API.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class DiabetesInput(BaseModel):
    Pregnancies: int = Field(..., ge=0, le=25, description="Number of pregnancies")
    Glucose: float = Field(..., ge=40, le=300, description="Fasting plasma glucose (mg/dL)")
    BloodPressure: float = Field(..., ge=40, le=200, description="Diastolic blood pressure (mm Hg)")
    SkinThickness: float = Field(..., ge=5, le=100, description="Triceps skin fold thickness (mm)")
    Insulin: float = Field(..., ge=10, le=900, description="2-Hour serum insulin (mu U/ml)")
    BMI: float = Field(..., ge=12.0, le=70.0, description="Body Mass Index (weight in kg/(height in m)^2)")
    DiabetesPedigreeFunction: float = Field(..., ge=0.05, le=3.0, description="Diabetes pedigree function score")
    Age: int = Field(..., ge=18, le=120, description="Age in years")
    ann_weight: Optional[float] = Field(0.70, ge=0.0, le=1.0)
    fuzzy_weight: Optional[float] = Field(0.30, ge=0.0, le=1.0)

class HeartInput(BaseModel):
    age: int = Field(..., ge=20, le=100, description="Age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex (1 = male; 0 = female)")
    cp: int = Field(..., ge=1, le=4, description="Chest pain type (1-4)")
    trestbps: float = Field(..., ge=80, le=220, description="Resting blood pressure (mm Hg)")
    chol: float = Field(..., ge=100, le=550, description="Serum cholesterol (mg/dL)")
    fbs: int = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dL (1 = true; 0 = false)")
    restecg: int = Field(..., ge=0, le=2, description="Resting ECG results (0-2)")
    thalach: float = Field(..., ge=60, le=220, description="Maximum heart rate achieved")
    exang: int = Field(..., ge=0, le=1, description="Exercise induced angina (1 = yes; 0 = no)")
    oldpeak: float = Field(..., ge=0.0, le=6.5, description="ST depression induced by exercise relative to rest")
    slope: int = Field(..., ge=1, le=3, description="Slope of the peak exercise ST segment (1-3)")
    ca: int = Field(..., ge=0, le=3, description="Number of major vessels (0-3)")
    thal: int = Field(..., ge=3, le=7, description="Thal (3 = normal; 6 = fixed defect; 7 = reversible defect)")
    ann_weight: Optional[float] = Field(0.70, ge=0.0, le=1.0)
    fuzzy_weight: Optional[float] = Field(0.30, ge=0.0, le=1.0)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default-session"
    context_data: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    provider: str

class SimulationRequest(BaseModel):
    disease: str # "diabetes" or "heart"
    base_inputs: Dict[str, Any]
    overrides: Dict[str, Any]
