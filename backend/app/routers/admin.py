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


@router.post("/seed_analysis")
async def seed_analysis_data(
    x_admin_key: str = Header(..., alias="X-Admin-Key"),
):
    """
    Seed stock analysis data manually.
    """
    settings = get_settings()
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    
    try:
        # Import here to avoid potential circular/startup issues
        from scripts.seed_analysis import seed_data
        await seed_data()
        return {"success": True, "message": "Analysis data seeded successfully"}
    except Exception as e:
        logger.error(f"Error seeding analysis data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/migrate_schema")
async def migrate_schema(
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
    db: AsyncSession = Depends(get_db)
):
    """Run schema migration to add profile columns."""
    settings = get_settings()
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    
    from sqlalchemy import text
    
    # Add columns if they don't exist
    columns = [
        "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS ceo VARCHAR(255)",
        "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS employees INTEGER",
        "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS headquarters VARCHAR(255)",
        "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS founded_year INTEGER",
        "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS analysis_data TEXT",
    ]
    
    try:
        for col_sql in columns:
            await db.execute(text(col_sql))
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"message": "Schema migration completed"}


@router.post("/sync_profile")
async def sync_profile(
    background_tasks: BackgroundTasks,
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
    db: AsyncSession = Depends(get_db)
):
    """Sync detailed profile data from Yahoo Finance."""
    settings = get_settings()
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    
    background_tasks.add_task(run_profile_sync, db)
    return {"message": "Profile sync started"}


async def run_profile_sync(db: AsyncSession):
    """Background task to sync profiles."""
    try:
        from sqlalchemy import select
        from app.models import Stock
        from app.services.yahoo_finance import get_yahoo_service
        import asyncio
        
        yahoo = get_yahoo_service()
        stocks = (await db.execute(select(Stock))).scalars().all()
        
        print(f"Starting profile sync for {len(stocks)} stocks...")
        
        for i, stock in enumerate(stocks):
            try:
                info = await yahoo.get_stock_info(stock.symbol)
                if info:
                    stock.ceo = info.get('ceo')
                    stock.employees = info.get('employees')
                    stock.headquarters = info.get('headquarters')
                    stock.description = info.get('description') # Update description too
                    # stock.website already exists
                    stock.website = info.get('website')
                    
                if i % 10 == 0:
                    await db.commit()
                    print(f"Synced {i}/{len(stocks)}")
                
                # Rate limit manual
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"Error syncing {stock.symbol}: {e}")
                continue
                
        await db.commit()
        print("Profile sync completed")
        
    except Exception as e:
        print(f"Profile sync failed: {e}")


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
                    quote_obj.change_amount = data.get("change_amount") # Fix: yahoo returns keys like 'change_amount' or 'change'?
                    # Check yahoo_finance.py get_quote: 'change_amount': round(change, 4)
                    # batch_get_quotes returns result of get_quote.
                    # Keys: price, change_amount, change_percent...
                    # Previous code used data.get("change") which might be wrong if key is 'change_amount'.
                    # I will fix keys here too.
                    quote_obj.change_amount = data.get("change_amount")
                    quote_obj.change_percent = data.get("change_percent")
                    quote_obj.open_price = data.get("open_price")
                    quote_obj.high_price = data.get("high_price")
                    quote_obj.low_price = data.get("low_price")
                    quote_obj.volume = data.get("volume")
                    quote_obj.market_cap = data.get("market_cap")
                    quote_obj.pe_ratio = data.get("pe_ratio")
                    quote_obj.week_52_high = data.get("week_52_high")
                    quote_obj.week_52_low = data.get("week_52_low")
                    quote_obj.trend = data.get("trend") 
                    
                await db.commit()
                
            except Exception as e:
                print(f"Error syncing batch {i}: {e}")
                continue
                
        print("Price sync completed")
        
    except Exception as e:
        print(f"Sync failed: {e}")

