from typing import List


def rank_chunks(chunks: List[str], query: str, limit: int = 3) -> List[str]:
    """
    Very simple ranking:
    score by number of query word matches inside each chunk.
    """
    query_terms = [term.lower() for term in query.split() if term.strip()]

    scored = []
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(chunk_lower.count(term) for term in query_terms)
        scored.append((chunk, score))

    scored.sort(key=lambda item: item[1], reverse=True)
    ranked = [chunk for chunk, score in scored if score > 0]

    if not ranked:
        ranked = chunks[:limit]

    return ranked[:limit]