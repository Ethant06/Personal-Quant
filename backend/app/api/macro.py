from fastapi import APIRouter, Depends

from app.auth.deps import get_current_profile
from app.schemas.macro import MacroIndicatorOut
from app.services.fred import list_macro_indicators

router = APIRouter(prefix="/macro", tags=["macro"])


@router.get("/indicators", response_model=list[MacroIndicatorOut])
def get_macro_indicators(_profile: dict = Depends(get_current_profile)):
    """
    Curated FRED series for beginner macro context (rates, inflation, jobs, oil).
    Live values require FRED_API_KEY; otherwise returns series links + notes.
    """
    return [
        MacroIndicatorOut(
            series_id=i.series_id,
            title=i.title,
            theme=i.theme,
            latest_value=i.latest_value,
            latest_date=i.latest_date,
            source_url=i.source_url,
            note=i.note,
        )
        for i in list_macro_indicators()
    ]
