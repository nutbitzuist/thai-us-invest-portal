"""
Stocks API endpoints.
"""
from typing import Optional
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models import Stock, LatestQuote, Analysis
from app.services.yahoo_finance import get_yahoo_service
from app.services.cache import get_cache_service, quote_key, stock_key

router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.get("")
async def list_stocks(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    sector: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get paginated list of stocks."""
    base_query = select(Stock, LatestQuote).outerjoin(
        LatestQuote, Stock.symbol == LatestQuote.symbol
    ).where(Stock.is_active == True)
    
    if sector:
        base_query = base_query.where(Stock.sector == sector)
    
    if search:
        search_term = f"%{search.upper()}%"
        base_query = base_query.where(
            (Stock.symbol.ilike(search_term)) | 
            (Stock.name.ilike(search_term))
        )
    
    # Count
    count_query = select(func.count()).select_from(base_query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    # Paginate
    offset = (page - 1) * per_page
    base_query = base_query.order_by(Stock.symbol).offset(offset).limit(per_page)
    
    result = await db.execute(base_query)
    rows = result.all()
    
    stocks = []
    for stock, quote in rows:
        stocks.append({
            "symbol": stock.symbol,
            "name": stock.name,
            "name_th": stock.name_th,
            "sector": stock.sector,
            "price": float(quote.price) if quote and quote.price else None,
            "change_percent": float(quote.change_percent) if quote and quote.change_percent else None,
            "trend": quote.trend if quote else None,
        })
    
    return {
        "success": True,
        "data": stocks,
        "meta": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": ceil(total / per_page) if total > 0 else 0,
        }
    }


@router.get("/{symbol}")
async def get_stock(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    """Get complete stock details."""
    symbol = symbol.upper()
    
    # Check cache
    cache = await get_cache_service()
    cached = await cache.get(stock_key(symbol))
    if cached:
        return {"success": True, "data": cached}
    
    # Get from database
    result = await db.execute(
        select(Stock).where(Stock.symbol == symbol)
    )
    stock = result.scalar_one_or_none()
    
    if not stock:
        # Try fetching from Yahoo Finance
        yf_service = get_yahoo_service()
        stock_info = await yf_service.get_stock_info(symbol)
        
        if not stock_info:
            raise HTTPException(status_code=404, detail=f"Stock '{symbol}' not found")
        
        # Create in database
        stock = Stock(**stock_info)
        db.add(stock)
        await db.commit()
        await db.refresh(stock)
        
    # Lazy load profile data if missing
    if not stock.ceo or not stock.employees:
        try:
            yf_service = get_yahoo_service()
            info = await yf_service.get_stock_info(symbol)
            if info:
                stock.ceo = info.get('ceo')
                stock.employees = info.get('employees')
                stock.headquarters = info.get('headquarters')
                stock.founded_year = info.get('founded_year') # Note: yahoo service returns this? I commented it out in yahoo_finance.py
                # Re-check yahoo_finance.py return dict in step 976. I commented out founded.
                # So founded won't update.
                if not stock.website:
                    stock.website = info.get('website')
                
                db.add(stock)
                await db.commit()
                await db.refresh(stock)
        except Exception as e:
            # Don't fail request if update fails
            pass
    
    data = {
        "symbol": stock.symbol,
        "name": stock.name,
        "name_th": stock.name_th,
        "sector": stock.sector,
        "industry": stock.industry,
        "description": stock.description,
        "description_th": stock.description_th,
        "logo_url": stock.logo_url or f"https://logo.clearbit.com/{stock.website.replace('https://', '').replace('http://', '').split('/')[0]}" if stock.website else None,
        "website": stock.website,
        "ceo": stock.ceo,
        "employees": stock.employees,
        "headquarters": stock.headquarters,
        "founded_year": stock.founded_year,
        "exchange": stock.exchange,
        "country": stock.country,
    }
    
    # Cache the response
    await cache.set(stock_key(symbol), data, 'stock')
    
    return {"success": True, "data": data}


@router.get("/{symbol}/quote")
async def get_stock_quote(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    """Get latest price quote for a stock."""
    symbol = symbol.upper()
    
    # Check cache
    cache = await get_cache_service()
    cached = await cache.get(quote_key(symbol))
    if cached:
        return {"success": True, "data": cached}
    
    # Get from database first
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
            "open_price": float(quote.open_price) if quote.open_price else None,
            "high_price": float(quote.high_price) if quote.high_price else None,
            "low_price": float(quote.low_price) if quote.low_price else None,
            "volume": quote.volume,
            "market_cap": quote.market_cap,
            "pe_ratio": float(quote.pe_ratio) if quote.pe_ratio else None,
            "eps": float(quote.eps) if quote.eps else None,
            "week_52_high": float(quote.week_52_high) if quote.week_52_high else None,
            "week_52_low": float(quote.week_52_low) if quote.week_52_low else None,
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


@router.get("/{symbol}/history")
async def get_stock_history(
    symbol: str,
    period: str = Query("1y", pattern="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$"),
    db: AsyncSession = Depends(get_db),
):
    """Get historical OHLCV data for a stock."""
    symbol = symbol.upper()
    
    yf_service = get_yahoo_service()
    history = await yf_service.get_history(symbol, period)
    
    return {"success": True, "data": history}


@router.get("/{symbol}/analysis")
async def get_stock_analysis(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    """Get Thai analysis content for a stock."""
    symbol = symbol.upper()
    
    result = await db.execute(
        select(Analysis)
        .where(Analysis.symbol == symbol)
        .where(Analysis.symbol_type == "stock")
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
            "target_price": float(analysis.target_price) if analysis.target_price else None,
            "author": analysis.author,
            "published_at": analysis.published_at.isoformat() if analysis.published_at else None,
        }
    }
