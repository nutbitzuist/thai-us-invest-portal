"""
Search API endpoint.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.database import get_db
from app.models import Stock, ETF, LatestQuote
from app.services.cache import get_cache_service, search_key

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("")
async def search(
    q: str = Query(..., min_length=1, max_length=50, description="Search query"),
    type: str = Query("all", pattern="^(all|stock|etf)$", description="Type filter"),
    db: AsyncSession = Depends(get_db),
):
    """Search for stocks and ETFs."""
    query = q.strip()
    search_term = f"%{query.upper()}%"
    
    # Check cache
    cache = await get_cache_service()
    cache_k = search_key(f"{query}:{type}")
    cached = await cache.get(cache_k)
    if cached:
        return {"success": True, "data": cached}
    
    stocks = []
    etfs = []
    
    # Search stocks
    if type in ("all", "stock"):
        stock_query = (
            select(Stock, LatestQuote)
            .outerjoin(LatestQuote, Stock.symbol == LatestQuote.symbol)
            .where(Stock.is_active == True)
            .where(
                or_(
                    Stock.symbol.ilike(search_term),
                    Stock.name.ilike(search_term)
                )
            )
            .order_by(Stock.symbol)
            .limit(20)
        )
        result = await db.execute(stock_query)
        rows = result.all()
        
        for stock, quote in rows:
            stocks.append({
                "symbol": stock.symbol,
                "name": stock.name,
                "name_th": stock.name_th,
                "sector": stock.sector,
                "type": "stock",
                "price": float(quote.price) if quote and quote.price else None,
                "change_percent": float(quote.change_percent) if quote and quote.change_percent else None,
                "trend": quote.trend if quote else None,
            })
    
    # Search ETFs
    if type in ("all", "etf"):
        etf_query = (
            select(ETF, LatestQuote)
            .outerjoin(LatestQuote, ETF.symbol == LatestQuote.symbol)
            .where(ETF.is_active == True)
            .where(
                or_(
                    ETF.symbol.ilike(search_term),
                    ETF.name.ilike(search_term)
                )
            )
            .order_by(ETF.symbol)
            .limit(20)
        )
        result = await db.execute(etf_query)
        rows = result.all()
        
        for etf, quote in rows:
            etfs.append({
                "symbol": etf.symbol,
                "name": etf.name,
                "name_th": etf.name_th,
                "category": etf.category,
                "type": "etf",
                "price": float(quote.price) if quote and quote.price else None,
                "change_percent": float(quote.change_percent) if quote and quote.change_percent else None,
                "trend": quote.trend if quote else None,
            })
    
    data = {"stocks": stocks, "etfs": etfs}
    await cache.set(cache_k, data, 'search')
    
    return {"success": True, "data": data}
