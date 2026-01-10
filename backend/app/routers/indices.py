"""
Indices API endpoints.
"""
from typing import Optional
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Index, IndexComponent, Stock, LatestQuote
from app.services.cache import get_cache_service, index_components_key

router = APIRouter(prefix="/indices", tags=["Indices"])


@router.get("")
async def list_indices(
    db: AsyncSession = Depends(get_db),
):
    """Get all indices (S&P 500, Nasdaq 100)."""
    result = await db.execute(select(Index))
    indices = result.scalars().all()
    
    return {
        "success": True,
        "data": [
            {
                "symbol": idx.symbol,
                "name": idx.name,
                "name_th": idx.name_th,
                "description_th": idx.description_th,
            }
            for idx in indices
        ]
    }


@router.get("/{symbol}")
async def get_index(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    """Get index details by symbol."""
    symbol = symbol.upper()
    
    result = await db.execute(
        select(Index).where(Index.symbol == symbol)
    )
    index = result.scalar_one_or_none()
    
    if not index:
        raise HTTPException(status_code=404, detail=f"Index '{symbol}' not found")
    
    # Count components
    count_result = await db.execute(
        select(func.count(IndexComponent.id))
        .where(IndexComponent.index_symbol == symbol)
    )
    component_count = count_result.scalar() or 0
    
    return {
        "success": True,
        "data": {
            "symbol": index.symbol,
            "name": index.name,
            "name_th": index.name_th,
            "description_th": index.description_th,
            "component_count": component_count,
        }
    }


@router.get("/{symbol}/components")
async def get_index_components(
    symbol: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    sector: Optional[str] = None,
    sort: str = Query("weight", pattern="^(weight|name|change|trend)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get components of an index with pagination and filtering."""
    symbol = symbol.upper()
    
    # Check cache first
    cache = await get_cache_service()
    cache_key = f"{index_components_key(symbol)}:{page}:{per_page}:{sector}:{sort}:{order}:{search}"
    cached = await cache.get(cache_key)
    if cached:
        return cached
    
    # Base query - join with stocks and quotes
    base_query = (
        select(IndexComponent, Stock, LatestQuote)
        .join(Stock, IndexComponent.stock_symbol == Stock.symbol)
        .outerjoin(LatestQuote, Stock.symbol == LatestQuote.symbol)
        .where(IndexComponent.index_symbol == symbol)
    )
    
    # Apply filters
    if sector:
        base_query = base_query.where(Stock.sector == sector)
    
    if search:
        search_term = f"%{search.upper()}%"
        base_query = base_query.where(
            (Stock.symbol.ilike(search_term)) | 
            (Stock.name.ilike(search_term))
        )
    
    # Get total count
    count_query = select(func.count()).select_from(base_query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    # Apply sorting
    if sort == "weight":
        order_col = IndexComponent.weight
    elif sort == "name":
        order_col = Stock.name
    elif sort == "change":
        order_col = LatestQuote.change_percent
    else:  # trend
        order_col = LatestQuote.trend
    
    if order == "desc":
        base_query = base_query.order_by(order_col.desc().nullslast())
    else:
        base_query = base_query.order_by(order_col.asc().nullsfirst())
    
    # Apply pagination
    offset = (page - 1) * per_page
    base_query = base_query.offset(offset).limit(per_page)
    
    result = await db.execute(base_query)
    rows = result.all()
    
    components = []
    for component, stock, quote in rows:
        components.append({
            "symbol": stock.symbol,
            "name": stock.name,
            "name_th": stock.name_th,
            "sector": stock.sector,
            "weight": float(component.weight) if component.weight else None,
            "price": float(quote.price) if quote and quote.price else None,
            "change_percent": float(quote.change_percent) if quote and quote.change_percent else None,
            "trend": quote.trend if quote else None,
        })
    
    response = {
        "success": True,
        "data": components,
        "meta": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": ceil(total / per_page) if total > 0 else 0,
        }
    }
    
    # Cache the response
    await cache.set(cache_key, response, 'index_components')
    
    return response
