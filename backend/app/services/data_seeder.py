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


# Sample S&P 500 stocks (top 50 by market cap)
SP500_TOP50 = [
    {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology"},
    {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology"},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary"},
    {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology"},
    {"symbol": "META", "name": "Meta Platforms Inc.", "sector": "Technology"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Discretionary"},
    {"symbol": "BRK.B", "name": "Berkshire Hathaway Inc.", "sector": "Financials"},
    {"symbol": "UNH", "name": "UnitedHealth Group Inc.", "sector": "Healthcare"},
    {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare"},
    {"symbol": "V", "name": "Visa Inc.", "sector": "Financials"},
    {"symbol": "XOM", "name": "Exxon Mobil Corporation", "sector": "Energy"},
    {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financials"},
    {"symbol": "WMT", "name": "Walmart Inc.", "sector": "Consumer Staples"},
    {"symbol": "PG", "name": "Procter & Gamble Co.", "sector": "Consumer Staples"},
    {"symbol": "MA", "name": "Mastercard Inc.", "sector": "Financials"},
    {"symbol": "HD", "name": "Home Depot Inc.", "sector": "Consumer Discretionary"},
    {"symbol": "CVX", "name": "Chevron Corporation", "sector": "Energy"},
    {"symbol": "LLY", "name": "Eli Lilly and Company", "sector": "Healthcare"},
    {"symbol": "ABBV", "name": "AbbVie Inc.", "sector": "Healthcare"},
    {"symbol": "MRK", "name": "Merck & Co. Inc.", "sector": "Healthcare"},
    {"symbol": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare"},
    {"symbol": "AVGO", "name": "Broadcom Inc.", "sector": "Technology"},
    {"symbol": "KO", "name": "Coca-Cola Company", "sector": "Consumer Staples"},
    {"symbol": "PEP", "name": "PepsiCo Inc.", "sector": "Consumer Staples"},
    {"symbol": "COST", "name": "Costco Wholesale Corporation", "sector": "Consumer Staples"},
    {"symbol": "TMO", "name": "Thermo Fisher Scientific Inc.", "sector": "Healthcare"},
    {"symbol": "BAC", "name": "Bank of America Corp.", "sector": "Financials"},
    {"symbol": "CSCO", "name": "Cisco Systems Inc.", "sector": "Technology"},
    {"symbol": "MCD", "name": "McDonald's Corporation", "sector": "Consumer Discretionary"},
    {"symbol": "ABT", "name": "Abbott Laboratories", "sector": "Healthcare"},
    {"symbol": "ACN", "name": "Accenture plc", "sector": "Technology"},
    {"symbol": "CRM", "name": "Salesforce Inc.", "sector": "Technology"},
    {"symbol": "DHR", "name": "Danaher Corporation", "sector": "Healthcare"},
    {"symbol": "ORCL", "name": "Oracle Corporation", "sector": "Technology"},
    {"symbol": "NKE", "name": "Nike Inc.", "sector": "Consumer Discretionary"},
    {"symbol": "AMD", "name": "Advanced Micro Devices Inc.", "sector": "Technology"},
    {"symbol": "ADBE", "name": "Adobe Inc.", "sector": "Technology"},
    {"symbol": "NFLX", "name": "Netflix Inc.", "sector": "Communication Services"},
    {"symbol": "INTC", "name": "Intel Corporation", "sector": "Technology"},
    {"symbol": "DIS", "name": "Walt Disney Company", "sector": "Communication Services"},
    {"symbol": "VZ", "name": "Verizon Communications Inc.", "sector": "Communication Services"},
    {"symbol": "T", "name": "AT&T Inc.", "sector": "Communication Services"},
    {"symbol": "CMCSA", "name": "Comcast Corporation", "sector": "Communication Services"},
    {"symbol": "QCOM", "name": "QUALCOMM Inc.", "sector": "Technology"},
    {"symbol": "TXN", "name": "Texas Instruments Inc.", "sector": "Technology"},
    {"symbol": "PM", "name": "Philip Morris International", "sector": "Consumer Staples"},
    {"symbol": "NEE", "name": "NextEra Energy Inc.", "sector": "Utilities"},
    {"symbol": "HON", "name": "Honeywell International Inc.", "sector": "Industrials"},
    {"symbol": "IBM", "name": "International Business Machines", "sector": "Technology"},
]


async def seed_sample_stocks(db: AsyncSession):
    """Seed sample stocks for S&P 500."""
    count = 0
    for item in SP500_TOP50:
        existing = await db.execute(
            select(Stock).where(Stock.symbol == item["symbol"])
        )
        if not existing.scalar_one_or_none():
            db.add(Stock(
                symbol=item["symbol"],
                name=item["name"],
                sector=item.get("sector"),
            ))
            count += 1
    
    await db.commit()
    logger.info(f"Seeded {count} sample stocks")


async def seed_index_components(db: AsyncSession):
    """Add stocks to index components."""
    # Add all sample stocks to SPX (S&P 500)
    for i, item in enumerate(SP500_TOP50):
        existing = await db.execute(
            select(IndexComponent).where(
                IndexComponent.index_symbol == "SPX",
                IndexComponent.stock_symbol == item["symbol"]
            )
        )
        if not existing.scalar_one_or_none():
            db.add(IndexComponent(
                index_symbol="SPX",
                stock_symbol=item["symbol"],
                weight=round((50 - i) / 500 * 100, 4),  # Simulated weight
            ))
    
    # Add top tech stocks to NDX (Nasdaq 100)
    tech_stocks = [s for s in SP500_TOP50 if s["sector"] == "Technology"][:30]
    for i, item in enumerate(tech_stocks):
        existing = await db.execute(
            select(IndexComponent).where(
                IndexComponent.index_symbol == "NDX",
                IndexComponent.stock_symbol == item["symbol"]
            )
        )
        if not existing.scalar_one_or_none():
            db.add(IndexComponent(
                index_symbol="NDX",
                stock_symbol=item["symbol"],
                weight=round((30 - i) / 100 * 100, 4),
            ))
    
    await db.commit()
    logger.info("Seeded index components")


async def run_all_seeds(db: AsyncSession):
    """Run all seed functions."""
    await seed_indices(db)
    await seed_top50_etfs(db)
    await seed_sample_stocks(db)
    await seed_index_components(db)
    logger.info("All seeds completed")
