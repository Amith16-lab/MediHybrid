"""
endpoints_retina.py
===================
Endpoints for Diabetic Retinopathy Fundus Image Upload & CNN Analysis.
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db_models import RetinalAssessment
from app.services.cnn_service import retina_service

router = APIRouter(prefix="/api/retina", tags=["Retinopathy Detection"])

@router.post("/predict")
async def analyze_retina_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate extension
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG files are supported.")

    try:
        content = await file.read()
        res = retina_service.analyze_image(content, filename=file.filename)

        # Log into database
        db_log = RetinalAssessment(
            original_filename=file.filename,
            predicted_class=res["predicted_class_id"],
            predicted_class_name=res["predicted_class_name"],
            model_confidence=res["model_confidence"],
            class_probabilities=res["class_probabilities"],
            model_version=res["model_version"]
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)

        res["record_id"] = db_log.id
        res["timestamp"] = db_log.created_at.isoformat()
        return res
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing error: {str(e)}")

@router.get("/metrics")
def get_retina_metrics():
    if retina_service.metrics:
        return retina_service.metrics
    return {"status": "not_available", "message": "Run train_retina.py to compute metrics."}
