"""
endpoints_chat.py
=================
MediBot AI Assistant Chatbot endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import ChatRequest, ChatResponse
from app.models.db_models import ChatLog
from app.services.chatbot_service import chatbot

router = APIRouter(prefix="/api/chat", tags=["AI Chatbot"])

@router.post("", response_model=ChatResponse)
def chat_with_medibot(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        reply = chatbot.generate_reply(req.message, req.context_data)

        # Log conversation
        log = ChatLog(
            session_id=req.session_id,
            user_message=req.message,
            assistant_response=reply
        )
        db.add(log)
        db.commit()

        return ChatResponse(
            reply=reply,
            session_id=req.session_id,
            provider=chatbot.provider
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    logs = db.query(ChatLog).filter(ChatLog.session_id == session_id).order_by(ChatLog.created_at.asc()).all()
    return [
        {
            "id": l.id,
            "user": l.user_message,
            "bot": l.assistant_response,
            "timestamp": l.created_at.isoformat()
        }
        for l in logs
    ]
