from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text

from app.auth.deps import get_current_profile
from app.database import engine
from app.schemas.companies import CompanyCreate, CompanyOut
from app.schemas.hub import (
    ArticleOut,
    CompanyHubOut,
    FilingOut,
    MacroSignalOut,
)
from app.services.briefing_store import load_ticker_items
from app.services.macro import build_macro_signals
from app.services.sec_filings import fetch_recent_filings

router = APIRouter(prefix="/companies", tags=["companies"])


def _row_to_company(row) -> CompanyOut:
    return CompanyOut(
        id=str(row["id"]),
        ticker=row["ticker"],
        name=row["name"],
        exchange=row["exchange"],
    )


@router.get("/search", response_model=list[CompanyOut])
def search_companies(
    q: str = Query(min_length=1, max_length=64),
    _profile: dict = Depends(get_current_profile),
):
    """Search seeded/local companies by ticker or name."""
    pattern = f"%{q.strip()}%"
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT id, ticker, name, exchange
                FROM investory.companies
                WHERE ticker ILIKE :q OR name ILIKE :q
                ORDER BY ticker
                LIMIT 25
                """
            ),
            {"q": pattern},
        ).mappings().all()
    return [_row_to_company(row) for row in rows]


@router.get("/{ticker}/hub", response_model=CompanyHubOut)
def get_company_hub(
    ticker: str,
    profile: dict = Depends(get_current_profile),
):
    """
    Per-ticker educational hub: stored digest items, Yahoo articles,
    SEC filings, and macro/politics context.
    """
    ticker_u = ticker.strip().upper()
    with engine.connect() as conn:
        company = conn.execute(
            text(
                """
                SELECT id, ticker, name, exchange
                FROM investory.companies
                WHERE ticker = :ticker
                """
            ),
            {"ticker": ticker_u},
        ).mappings().first()
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        on_watchlist = conn.execute(
            text(
                """
                SELECT 1
                FROM investory.watchlist_items
                WHERE user_id = :user_id AND company_id = :company_id
                """
            ),
            {"user_id": profile["id"], "company_id": company["id"]},
        ).first()
        if on_watchlist is None:
            raise HTTPException(
                status_code=403,
                detail="Add this company to your watchlist to open its hub",
            )

        articles = conn.execute(
            text(
                """
                SELECT id, title, url, summary, provider, category, published_at
                FROM investory.articles
                WHERE ticker = :ticker
                ORDER BY created_at DESC
                LIMIT 12
                """
            ),
            {"ticker": ticker_u},
        ).mappings().all()

    today = date.today().isoformat()
    briefing, items = load_ticker_items(profile["id"], ticker_u, today)

    if briefing and items:
        status = "ready"
        note = briefing.note
        briefing_date = briefing.date
    elif briefing:
        status = "pending"
        note = "Daily digest exists, but no items for this ticker yet."
        briefing_date = briefing.date
    else:
        status = "pending"
        note = "Updates appear after the daily refresh."
        briefing_date = None

    filings = [
        FilingOut(
            form=f.form,
            title=f.title,
            url=f.url,
            filed_at=f.filed_at,
        )
        for f in fetch_recent_filings(ticker_u, limit=5)
    ]
    macro = [
        MacroSignalOut(
            theme=s.theme,
            headline=s.headline,
            why_it_may_matter=s.why_it_may_matter,
            source_url=s.source_url,
        )
        for s in build_macro_signals(ticker_u, limit=3)
    ]

    return CompanyHubOut(
        company=_row_to_company(company),
        briefing_date=briefing_date,
        status=status,
        note=note,
        items=items,
        articles=[
            ArticleOut(
                id=str(row["id"]),
                title=row["title"],
                url=row["url"],
                summary=row["summary"],
                provider=row["provider"],
                category=row["category"] or "other",
                published_at=row["published_at"].isoformat()
                if row["published_at"]
                else None,
            )
            for row in articles
        ],
        filings=filings,
        macro_signals=macro,
    )


@router.post("", response_model=CompanyOut, status_code=201)
def upsert_company(
    body: CompanyCreate,
    _profile: dict = Depends(get_current_profile),
):
    """Create or update a company by ticker (handy before external data APIs)."""
    ticker = body.ticker.strip().upper()
    with engine.begin() as conn:
        row = conn.execute(
            text(
                """
                INSERT INTO investory.companies (ticker, name, exchange)
                VALUES (:ticker, :name, :exchange)
                ON CONFLICT (ticker) DO UPDATE
                    SET name = EXCLUDED.name,
                        exchange = COALESCE(EXCLUDED.exchange, investory.companies.exchange),
                        updated_at = now()
                RETURNING id, ticker, name, exchange
                """
            ),
            {
                "ticker": ticker,
                "name": body.name.strip(),
                "exchange": body.exchange.strip() if body.exchange else None,
            },
        ).mappings().first()

    if row is None:
        raise HTTPException(status_code=500, detail="Could not upsert company")
    return _row_to_company(row)
