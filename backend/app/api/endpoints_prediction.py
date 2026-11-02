"""
endpoints_prediction.py
=======================
Endpoints for Diabetes & Heart Disease Hybrid Predictions and counterfactual simulation.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import DiabetesInput, HeartInput, SimulationRequest
from app.models.db_models import Assessment
from app.services.hybrid_service import hybrid_engine

router = APIRouter(prefix="/api/predict", tags=["Predictions"])

@router.post("/diabetes")
def predict_diabetes_route(payload: DiabetesInput, db: Session = Depends(get_db)):
    data = payload.dict()
    w_ann = data.pop("ann_weight", 0.70)
    w_fuzzy = data.pop("fuzzy_weight", 0.30)

    try:
        result = hybrid_engine.predict_diabetes(data, w_ann=w_ann, w_fuzzy=w_fuzzy)
        
        # Persist to database
        db_record = Assessment(
            assessment_type="diabetes",
            input_values=data,
            ann_score=result["ann"]["score"],
            fuzzy_score=result["fuzzy"]["fuzzy_score"],
            hybrid_score=result["hybrid"]["score"],
            risk_category=result["hybrid"]["category"],
            selected_features=result["ga_selected_features"],
            explainability=result["explainability"]
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        result["record_id"] = db_record.id
        result["timestamp"] = db_record.created_at.isoformat()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/heart")
def predict_heart_route(payload: HeartInput, db: Session = Depends(get_db)):
    data = payload.dict()
    w_ann = data.pop("ann_weight", 0.70)
    w_fuzzy = data.pop("fuzzy_weight", 0.30)

    try:
        result = hybrid_engine.predict_heart(data, w_ann=w_ann, w_fuzzy=w_fuzzy)

        db_record = Assessment(
            assessment_type="heart",
            input_values=data,
            ann_score=result["ann"]["score"],
            fuzzy_score=result["fuzzy"]["fuzzy_score"],
            hybrid_score=result["hybrid"]["score"],
            risk_category=result["hybrid"]["category"],
            selected_features=result["ga_selected_features"],
            explainability=result["explainability"]
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        result["record_id"] = db_record.id
        result["timestamp"] = db_record.created_at.isoformat()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulate")
def simulate_counterfactual(payload: SimulationRequest):
    disease = payload.disease.lower()
    merged = {**payload.base_inputs, **payload.overrides}

    try:
        if disease == "diabetes":
            res = hybrid_engine.predict_diabetes(merged)
        elif disease == "heart":
            res = hybrid_engine.predict_heart(merged)
        else:
            raise HTTPException(status_code=400, detail="Invalid disease type. Must be 'diabetes' or 'heart'.")

        return {
            "status": "success",
            "disease": disease,
            "simulated_hybrid_score": res["hybrid"]["score"],
            "simulated_category": res["hybrid"]["category"],
            "ann_score": res["ann"]["score"],
            "fuzzy_score": res["fuzzy"]["fuzzy_score"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
