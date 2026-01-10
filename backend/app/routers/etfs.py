"""
ETFs API endpoints.
"""
from typing import Optional
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models import ETF, ETFHolding, LatestQuote, Analysis
from app.services.yahoo_finance import get_yahoo_service
from app.services.cache import get_cache_service, quote_key, etf_key, etf_holdings_key

router = APIRouter(prefix="/etfs", tags=["ETFs"])


@router.get("")
async def list_etfs(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get paginated list of ETFs."""
    base_query = select(ETF, LatestQuote).outerjoin(
        LatestQuote, ETF.symbol == LatestQuote.symbol
    ).where(ETF.is_active == True)
    
    if category:
        base_query = base_query.where(ETF.category == category)
    
    # Count
    count_query = select(func.count()).select_from(base_query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    # Paginate
    offset = (page - 1) * per_page
    base_query = base_query.order_by(ETF.symbol).offset(offset).limit(per_page)
    
    result = await db.execute(base_query)
    rows = result.all()
    
    etfs = []
    for etf, quote in rows:
        etfs.append({
            "symbol": etf.symbol,
            "name": etf.name,
            "name_th": etf.name_th,
            "category": etf.category,
            "provider": etf.provider,
            "expense_ratio": float(etf.expense_ratio) if etf.expense_ratio else None,
            "aum": etf.aum,
            "price": float(quote.price) if quote and quote.price else None,
            "change_percent": float(quote.change_percent) if quote and quote.change_percent else None,
            "trend": quote.trend if quote else None,
        })
    
    return {
        "success": True,
        "data": etfs,
        "meta": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": ceil(total / per_page) if total > 0 else 0,
        }
    }


@router.get("/top50")
async def get_top50_etfs(
    db: AsyncSession = Depends(get_db),
):
    """Get top 50 ETFs list."""
    result = await db.execute(
        select(ETF, LatestQuote)
        .outerjoin(LatestQuote, ETF.symbol == LatestQuote.symbol)
        .where(ETF.is_active == True)
        .order_by(ETF.id)
        .limit(50)
    )
    rows = result.all()
    
    etfs = []
    for etf, quote in rows:
        etfs.append({
            "symbol": etf.symbol,
            "name": etf.name,
            "name_th": etf.name_th,
            "category": etf.category,
            "provider": etf.provider,
            "expense_ratio": float(etf.expense_ratio) if etf.expense_ratio else None,
            "aum": etf.aum,
            "price": float(quote.price) if quote and quote.price else None,
            "change_percent": float(quote.change_percent) if quote and quote.change_percent else None,
            "trend": quote.trend if quote else None,
        })
    
    return {"success": True, "data": etfs}


@router.get("/{symbol}")
async def get_etf(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    """Get complete ETF details."""
    symbol = symbol.upper()
    
    # Check cache
    cache = await get_cache_service()
    cached = await cache.get(etf_key(symbol))
    if cached:
        return {"success": True, "data": cached}
    
    result = await db.execute(
        select(ETF).where(ETF.symbol == symbol)
    )
    etf = result.scalar_one_or_none()
    
    if not etf:
        raise HTTPException(status_code=404, detail=f"ETF '{symbol}' not found")
    
    data = {
        "symbol": etf.symbol,
        "name": etf.name,
        "name_th": etf.name_th,
        "category": etf.category,
        "expense_ratio": float(etf.expense_ratio) if etf.expense_ratio else None,
        "aum": etf.aum,
        "description": etf.description,
        "description_th": etf.description_th,
        "provider": etf.provider,
        "inception_date": etf.inception_date.isoformat() if etf.inception_date else None,
    }
    
    await cache.set(etf_key(symbol), data, 'etf')
    return {"success": True, "data": data}


@router.get("/{symbol}/quote")
async def get_etf_quote(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    """Get latest price quote for an ETF."""
    symbol = symbol.upper()
    
    # Check cache
    cache = await get_cache_service()
    cached = await cache.get(quote_key(symbol))
    if cached:
        return {"success": True, "data": cached}
    
    # Get from database
    result = await db.execute(
        select(LatestQuote).where(LatestQuote.symbol == symbol)
    )
    quote = result.scalar_one_or_none()
    
    if quote:
        data = {
            "symbol": quote.symbol,
            "price": float(quote.price) if quote.price else None,
            "change_amount": float(quote.change_amount) if quote.change_amount else None,
            "change_percent": float(quote.change_percent) if quote.change_percent else None,
            "volume": quote.volume,
            "week_52_high": float(quote.week_52_high) if quote.week_52_high else None,
            "week_52_low": float(quote.week_52_low) if quote.week_52_low else None,
            "dividend_yield": float(quote.dividend_yield) if quote.dividend_yield else None,
            "sma_50": float(quote.sma_50) if quote.sma_50 else None,
            "sma_200": float(quote.sma_200) if quote.sma_200 else None,
            "trend": quote.trend,
            "updated_at": quote.updated_at.isoformat() if quote.updated_at else None,
        }
        await cache.set(quote_key(symbol), data, 'quote')
        return {"success": True, "data": data}
    
    # Fetch from Yahoo Finance
    yf_service = get_yahoo_service()
    quote_data = await yf_service.get_quote(symbol)
    
    if not quote_data:
        raise HTTPException(status_code=404, detail=f"Quote for '{symbol}' not found")
    
    await cache.set(quote_key(symbol), quote_data, 'quote')
    return {"success": True, "data": quote_data}


@router.get("/{symbol}/holdings")
async def get_etf_holdings(
    symbol: str,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get top holdings of an ETF."""
    symbol = symbol.upper()
    
    # Check cache
    cache = await get_cache_service()
    cached = await cache.get(etf_holdings_key(symbol))
    if cached:
        return {"success": True, "data": cached[:limit]}
    
    result = await db.execute(
        select(ETFHolding)
        .where(ETFHolding.etf_symbol == symbol)
        .order_by(ETFHolding.weight.desc().nullslast())
        .limit(limit)
    )
    holdings = result.scalars().all()
    
    data = [
        {
            "holding_symbol": h.holding_symbol,
            "holding_name": h.holding_name,
            "weight": float(h.weight) if h.weight else None,
            "shares": h.shares,
        }
        for h in holdings
    ]
    
    await cache.set(etf_holdings_key(symbol), data, 'etf_holdings')
    return {"success": True, "data": data}


@router.get("/{symbol}/analysis")
async def get_etf_analysis(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    """Get Thai analysis content for an ETF."""
    symbol = symbol.upper()
    
    result = await db.execute(
        select(Analysis)
        .where(Analysis.symbol == symbol)
        .where(Analysis.symbol_type == "etf")
        .where(Analysis.status == "published")
        .order_by(Analysis.published_at.desc())
        .limit(1)
    )
    analysis = result.scalar_one_or_none()
    
    if not analysis:
        return {"success": True, "data": None}
    
    return {
        "success": True,
        "data": {
            "id": analysis.id,
            "title": analysis.title,
            "title_th": analysis.title_th,
            "summary_th": analysis.summary_th,
            "content_th": analysis.content_th,
            "trend_opinion": analysis.trend_opinion,
            "author": analysis.author,
            "published_at": analysis.published_at.isoformat() if analysis.published_at else None,
        }
    }
