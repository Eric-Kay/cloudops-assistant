from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth.auth import authenticate_user, get_current_user
from app.monitoring.metrics import track_latency
from app.services.bedrock_service import build_prompt, call_bedrock
from app.services.ranking_service import rank_chunks
from app.services.retrieval_service import retrieve_docs

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    question: str


@router.post("/login")
def login(payload: LoginRequest):
    token = authenticate_user(payload.username, payload.password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/chat")
@track_latency
def chat(payload: ChatRequest, user=Depends(get_current_user)):
    candidates = retrieve_docs(payload.question)

    if not candidates:
        raise HTTPException(
            status_code=400,
            detail="No uploaded documents found. Upload at least one document first.",
        )

    ranked_texts = rank_chunks(
        [item["chunk"] for item in candidates],
        payload.question,
        limit=3,
    )

    ranked_candidates = []
    for ranked_text in ranked_texts:
        for item in candidates:
            if item["chunk"] == ranked_text:
                ranked_candidates.append(item)
                break

    prompt = build_prompt(payload.question, ranked_candidates)

    try:
        answer = call_bedrock(prompt)
    except Exception as exc:
        answer = (
            "Bedrock call failed. Check AWS credentials, region, model access, "
            f"and Bedrock permissions. Details: {str(exc)}"
        )

    return {
        "user": user["sub"],
        "question": payload.question,
        "answer": answer,
        "sources": [
            {"filename": item["filename"], "snippet": item["chunk"][:200]}
            for item in ranked_candidates
        ],
    }