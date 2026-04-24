from typing import Dict, List

from app.services.s3_service import get_s3_document_text, list_s3_documents

CHUNK_SIZE = 800


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> List[str]:
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end
    return chunks


def retrieve_docs(question: str) -> List[Dict[str, str]]:
    candidates = []

    for key in list_s3_documents():
        content = get_s3_document_text(key)
        chunks = chunk_text(content)

        for chunk in chunks:
            candidates.append(
                {
                    "filename": key,
                    "chunk": chunk,
                }
            )

    return candidates