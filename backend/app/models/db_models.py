"""
db_models.py
============
SQLAlchemy database models for MediHybrid:
- Assessment (Diabetes & Heart Disease records)
- RetinalAssessment (Diabetic Retinopathy CNN analysis logs)
- ChatLog (MediBot conversation history)
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from app.database import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assessment_type = Column(String(50), index=True) # "diabetes" or "heart"
    input_values = Column(JSON, nullable=False)
    ann_score = Column(Float, nullable=False)
    fuzzy_score = Column(Float, nullable=False)
    hybrid_score = Column(Float, nullable=False)
    risk_category = Column(String(50), nullable=False)
    selected_features = Column(JSON, nullable=True)
    explainability = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class RetinalAssessment(Base):
    __tablename__ = "retinal_assessments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_filename = Column(String(255), nullable=False)
    predicted_class = Column(Integer, nullable=False)
    predicted_class_name = Column(String(100), nullable=False)
    model_confidence = Column(Float, nullable=False)
    class_probabilities = Column(JSON, nullable=False)
    model_version = Column(String(100), default="EfficientNet-B0 (APTOS)")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(100), index=True)
    user_message = Column(Text, nullable=False)
    assistant_response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
