from fastapi import APIRouter, Depends

from app.auth.deps import get_current_profile
from app.services.classify import CATEGORIES

router = APIRouter(prefix="/classifications", tags=["classifications"])


@router.get("/categories")
def list_categories(_profile: dict = Depends(get_current_profile)):
    """PRD MVP category vocabulary for filters and UI chips."""
    return {
        "categories": list(CATEGORIES),
        "model": "heuristic_v1",
        "note": "Keyword classifier for MVP; LLM classification can replace this later.",
    }
