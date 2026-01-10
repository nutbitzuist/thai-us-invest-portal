"""
Data seeder for loading initial data.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from app.models import Stock, ETF, Index, IndexComponent

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent / "data"



async def seed_indices(db: AsyncSession):
    """Seed indices table."""
    indices = [
        {
            "symbol": "SPX",
            "name": "S&P 500",
            "name_th": "ดัชนี S&P 500",
            "description_th": "ดัชนีหุ้น 500 บริษัทขนาดใหญ่ที่สุดของสหรัฐอเมริกา"
        },
        {
            "symbol": "NDX", 
            "name": "Nasdaq 100",
            "name_th": "ดัชนี Nasdaq 100",
            "description_th": "ดัชนีหุ้น 100 บริษัทเทคโนโลยีชั้นนำที่จดทะเบียนใน Nasdaq"
        }
    ]
    
    for item in indices:
        existing = await db.execute(
            select(Index).where(Index.symbol == item["symbol"])
        )
        if not existing.scalar_one_or_none():
            db.add(Index(**item))
    
    await db.commit()
    logger.info("Seeded indices")


async def seed_top50_etfs(db: AsyncSession):
    """Seed top 50 ETFs."""
    etf_file = DATA_DIR / "top50_etfs.json"
    
    if not etf_file.exists():
        logger.warning(f"ETF data file not found: {etf_file}")
        return
    
    with open(etf_file) as f:
        etfs = json.load(f)
    
    count = 0
    for item in etfs:
        existing = await db.execute(
            select(ETF).where(ETF.symbol == item["symbol"])
        )
        if not existing.scalar_one_or_none():
            db.add(ETF(
                symbol=item["symbol"],
                name=item["name"],
                category=item.get("category"),
                provider=item.get("provider"),
            ))
            count += 1
    
    await db.commit()
    logger.info(f"Seeded {count} ETFs")


async def seed_all_stocks(db: AsyncSession):
    """Seed all stocks from S&P 500 and Nasdaq 100 lists."""
    stocks_to_add = {}  # symbol -> dict
    
    # 1. Load S&P 500
    sp500_file = DATA_DIR / "sp500_tickers.json"
    if sp500_file.exists():
        with open(sp500_file) as f:
            data = json.load(f)
            # Structure: { "sectors": [ { "companies": [ ... ] } ] }
            for sector_data in data.get("sectors", []):
                sector_name = sector_data.get("sector")
                for comp in sector_data.get("companies", []):
                    # "ticker": "NVDA", "name": "Nvidia", "weight":...
                    sym = comp.get("ticker")
                    if sym:
                        stocks_to_add[sym] = {
                            "symbol": sym,
                            "name": comp.get("name"),
                            "sector": sector_name
                        }
    else:
        logger.warning(f"S&P 500 file missing: {sp500_file}")

    # 2. Load Nasdaq 100
    ndx_file = DATA_DIR / "nasdaq100_tickers.json"
    if ndx_file.exists():
        with open(ndx_file) as f:
            data = json.load(f)
            # Structure: [ { "Ticker": "ADBE", "Company": "Adobe", "GICS_Sector": ... } ]
            for comp in data:
                sym = comp.get("Ticker")
                if sym:
                    # Prefer existing data from SP500 if available (often better formatted sector)
                    if sym not in stocks_to_add:
                        stocks_to_add[sym] = {
                            "symbol": sym,
                            "name": comp.get("Company"),
                            "sector": comp.get("GICS_Sector")
                        }
    else:
        logger.warning(f"Nasdaq 100 file missing: {ndx_file}")

    # Insert into DB
    count = 0
    for sym, stock_data in stocks_to_add.items():
        existing = await db.execute(
            select(Stock).where(Stock.symbol == sym)
        )
        if not existing.scalar_one_or_none():
            db.add(Stock(
                symbol=stock_data["symbol"],
                name=stock_data["name"],
                sector=stock_data.get("sector"),
            ))
            count += 1
    
    await db.commit()
    logger.info(f"Seeded {count} new stocks (Total {len(stocks_to_add)} processed)")


async def seed_index_components(db: AsyncSession):
    """Add stocks to index components."""
    # 1. S&P 500 Components
    sp500_file = DATA_DIR / "sp500_tickers.json"
    if sp500_file.exists():
        with open(sp500_file) as f:
            data = json.load(f)
            for sector_data in data.get("sectors", []):
                for comp in sector_data.get("companies", []):
                    sym = comp.get("ticker")
                    weight = comp.get("weight")
                    if sym:
                        # Ensure weight handles percentage string "7.18" -> 7.18
                        try:
                            w_val = float(weight) if weight else 0.0
                        except ValueError:
                            w_val = 0.0
                            
                        existing = await db.execute(
                            select(IndexComponent).where(
                                IndexComponent.index_symbol == "SPX",
                                IndexComponent.stock_symbol == sym
                            )
                        )
                        if not existing.scalar_one_or_none():
                            db.add(IndexComponent(
                                index_symbol="SPX",
                                stock_symbol=sym,
                                weight=w_val
                            ))

    # 2. Nasdaq 100 Components
    ndx_file = DATA_DIR / "nasdaq100_tickers.json"
    if ndx_file.exists():
        with open(ndx_file) as f:
            data = json.load(f)
            # Calculate mock weights if not provided, or just add them
            # Nasdaq 100 is market-cap weighted but we might not have it in this JSON
            # We'll just add them.
            total_count = len(data)
            for i, comp in enumerate(data):
                sym = comp.get("Ticker")
                if sym:
                    existing = await db.execute(
                        select(IndexComponent).where(
                            IndexComponent.index_symbol == "NDX",
                            IndexComponent.stock_symbol == sym
                        )
                    )
                    if not existing.scalar_one_or_none():
                        db.add(IndexComponent(
                            index_symbol="NDX",
                            stock_symbol=sym,
                            weight=0.0 # Placeholder or calculate if market cap available
                        ))
    
    await db.commit()
    logger.info("Seeded index components")


async def run_all_seeds(db: AsyncSession):
    """Run all seed functions."""
    await seed_indices(db)
    await seed_top50_etfs(db)
    await seed_all_stocks(db)
    await seed_index_components(db)
    logger.info("All seeds completed")

