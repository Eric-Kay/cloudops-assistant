from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.upload import router as upload_router
from app.api.feedback import router as feedback_router

app = FastAPI(title="CloudOps Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(upload_router, prefix="/api", tags=["upload"])
app.include_router(feedback_router, prefix="/api", tags=["feedback"])


@app.get("/health")
def health():
    return {"status": "ok"}