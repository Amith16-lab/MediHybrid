"""
endpoints_dashboard.py
======================
Dashboard analytics & assessment history endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db_models import Assessment, RetinalAssessment

router = APIRouter(prefix="/api", tags=["Dashboard & History"])

@router.get("/dashboard")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_assessments = db.query(Assessment).count()
    diabetes_count = db.query(Assessment).filter(Assessment.assessment_type == "diabetes").count()
    heart_count = db.query(Assessment).filter(Assessment.assessment_type == "heart").count()
    retina_count = db.query(RetinalAssessment).count()

    # Risk distributions
    low_risk = db.query(Assessment).filter(Assessment.hybrid_score < 35.0).count()
    mod_risk = db.query(Assessment).filter(Assessment.hybrid_score >= 35.0, Assessment.hybrid_score < 65.0).count()
    high_risk = db.query(Assessment).filter(Assessment.hybrid_score >= 65.0).count()

    # Recent activity
    recent_assessments = db.query(Assessment).order_by(Assessment.created_at.desc()).limit(8).all()
    recent_retina = db.query(RetinalAssessment).order_by(RetinalAssessment.created_at.desc()).limit(5).all()

    return {
        "status": "success",
        "counts": {
            "total_assessments": total_assessments + retina_count,
            "tabular_assessments": total_assessments,
            "diabetes_assessments": diabetes_count,
            "heart_assessments": heart_count,
            "retinal_scans": retina_count
        },
        "risk_distribution": {
            "low_risk": low_risk,
            "moderate_risk": mod_risk,
            "high_risk": high_risk
        },
        "recent_activity": [
            {
                "id": a.id,
                "type": a.assessment_type,
                "score": a.hybrid_score,
                "category": a.risk_category,
                "timestamp": a.created_at.strftime("%Y-%m-%d %H:%M")
            }
            for a in recent_assessments
        ],
        "recent_retinal_activity": [
            {
                "id": r.id,
                "filename": r.original_filename,
                "class_name": r.predicted_class_name,
                "confidence": round(r.model_confidence * 100, 1),
                "timestamp": r.created_at.strftime("%Y-%m-%d %H:%M")
            }
            for r in recent_retina
        ]
    }

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(Assessment).order_by(Assessment.created_at.desc()).limit(100).all()
    return [
        {
            "id": r.id,
            "type": r.assessment_type,
            "input_values": r.input_values,
            "ann_score": r.ann_score,
            "fuzzy_score": r.fuzzy_score,
            "hybrid_score": r.hybrid_score,
            "category": r.risk_category,
            "selected_features": r.selected_features,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]

@router.get("/history/{record_id}")
def get_history_detail(record_id: int, db: Session = Depends(get_db)):
    r = db.query(Assessment).filter(Assessment.id == record_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Record not found.")
    return {
        "id": r.id,
        "type": r.assessment_type,
        "input_values": r.input_values,
        "ann_score": r.ann_score,
        "fuzzy_score": r.fuzzy_score,
        "hybrid_score": r.hybrid_score,
        "category": r.risk_category,
        "selected_features": r.selected_features,
        "explainability": r.explainability,
        "created_at": r.created_at.isoformat()
    }

@router.delete("/history/{record_id}")
def delete_history_record(record_id: int, db: Session = Depends(get_db)):
    r = db.query(Assessment).filter(Assessment.id == record_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Record not found.")
    db.delete(r)
    db.commit()
    return {"status": "deleted", "id": record_id}
