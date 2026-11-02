"""
endpoints_fuzzy.py
==================
Dedicated endpoints for Mamdani Fuzzy Inference testing and inspection.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.fuzzy_service import diabetes_fuzzy, heart_fuzzy

router = APIRouter(prefix="/api/fuzzy", tags=["Fuzzy Inference"])

class DiabetesFuzzyReq(BaseModel):
    glucose: float
    bmi: float
    bp: float
    age: float

class HeartFuzzyReq(BaseModel):
    age: float
    chol: float
    bp: float
    hr: float
    oldpeak: float

@router.post("/diabetes")
def eval_fuzzy_diabetes(req: DiabetesFuzzyReq):
    try:
        return diabetes_fuzzy.evaluate(req.glucose, req.bmi, req.bp, req.age)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/heart")
def eval_fuzzy_heart(req: HeartFuzzyReq):
    try:
        return heart_fuzzy.evaluate(req.age, req.chol, req.bp, req.hr, req.oldpeak)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
