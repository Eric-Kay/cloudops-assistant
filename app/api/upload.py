from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.auth.auth import get_current_user
from app.services.s3_service import list_s3_documents, upload_file_to_s3
from app.services.versioning_service import version_filename

ALLOWED_EXTENSIONS = {".txt", ".md", ".log"}

router = APIRouter()


@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {sorted(ALLOWED_EXTENSIONS)}",
        )

    safe_name = version_filename(file.filename)
    content = file.file.read()

    upload_file_to_s3(
        file_name=safe_name,
        content=content,
        content_type=file.content_type or "text/plain",
    )

    return {
        "message": "File uploaded successfully",
        "uploaded_by": user["sub"],
        "filename": safe_name,
    }


@router.get("/documents")
def list_documents(user=Depends(get_current_user)):
    docs = list_s3_documents()
    return {"uploaded_by": user["sub"], "documents": docs}