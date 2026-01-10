"""
Admin endpoints for database management.
"""
from fastapi import APIRouter, Depends, Header, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.config import get_settings
from app.services.data_seeder import run_all_seeds

router = APIRouter(tags=["admin"])



@router.post("/seed")
async def seed_database(
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
    db: AsyncSession = Depends(get_db)
):
    """Seed the database with initial data.
    
    Requires X-Admin-Key header matching ADMIN_API_KEY env var.
    """
    settings = get_settings()
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    
    await run_all_seeds(db)
    
    return {
        "success": True,
        "message": "Database seeded successfully",
        "seeded": ["indices", "stocks", "etfs", "index_components"]
    }


@router.post("/sync")
async def sync_prices(
    background_tasks: BackgroundTasks,
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
    db: AsyncSession = Depends(get_db)
):
    """Sync real-time prices from Yahoo Finance.
    
    Requires X-Admin-Key header matching ADMIN_API_KEY env var.
    """
    settings = get_settings()
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    
    # Run sync in background
    background_tasks.add_task(run_price_sync, db)
    
    return {
        "success": True,
        "message": "Price sync started in background",
    }


async def run_price_sync(db: AsyncSession):
    """Background task to sync prices."""
    try:
        from sqlalchemy import select
        from app.models import Stock, ETF, LatestQuote
        from app.services.yahoo_finance import get_yahoo_service
        
        yahoo = get_yahoo_service()
        
        # 1. Get all symbols
        stocks = (await db.execute(select(Stock))).scalars().all()
        etfs = (await db.execute(select(ETF))).scalars().all()
        
        all_symbols = [s.symbol for s in stocks] + [e.symbol for e in etfs]
        type_map = {s.symbol: "stock" for s in stocks}
        type_map.update({e.symbol: "etf" for e in etfs})
        
        # 2. Batch process
        batch_size = 50
        for i in range(0, len(all_symbols), batch_size):
            batch = all_symbols[i:i+batch_size]
            print(f"Syncing batch {i} to {i+batch_size}...")
            
            try:
                quotes = await yahoo.batch_get_quotes(batch)
                
                for sym, data in quotes.items():
                    if not data:
                        continue
                        
                    # Upsert LatestQuote
                    stmt = select(LatestQuote).where(LatestQuote.symbol == sym)
                    result = await db.execute(stmt)
                    quote_obj = result.scalar_one_or_none()
                    
                    if not quote_obj:
                        quote_obj = LatestQuote(
                            symbol=sym, 
                            symbol_type=type_map.get(sym, "stock")
                        )
                        db.add(quote_obj)
                    
                    # Update fields
                    quote_obj.price = data.get("price")
                    quote_obj.change_amount = data.get("change")
                    quote_obj.change_percent = data.get("change_percent")
                    quote_obj.open_price = data.get("open")
                    quote_obj.high_price = data.get("day_high")
                    quote_obj.low_price = data.get("day_low")
                    quote_obj.volume = data.get("volume")
                    quote_obj.market_cap = data.get("market_cap")
                    quote_obj.pe_ratio = data.get("pe_ratio")
                    quote_obj.week_52_high = data.get("fifty_two_week_high")
                    quote_obj.week_52_low = data.get("fifty_two_week_low")
                    quote_obj.trend = data.get("trend") # calculated by service
                    
                await db.commit()
                
            except Exception as e:
                print(f"Error syncing batch {i}: {e}")
                continue
                
        print("Price sync completed")
        
    except Exception as e:
        print(f"Sync failed: {e}")

