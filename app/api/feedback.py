from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth.auth import get_current_user
from app.db.dynamodb import save_feedback

router = APIRouter()


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: str


@router.post("/feedback")
def feedback(payload: FeedbackRequest, user=Depends(get_current_user)):
    if payload.rating not in {"up", "down"}:
        raise HTTPException(status_code=400, detail="rating must be 'up' or 'down'")

    try:
        item = save_feedback(
            question=payload.question,
            answer=payload.answer,
            rating=payload.rating,
            username=user["sub"],
        )
    except Exception as exc:
        return {
            "message": "Feedback received, but DynamoDB write failed",
            "error": str(exc),
        }

    return {
        "message": "Feedback saved",
        "item": item,
    }