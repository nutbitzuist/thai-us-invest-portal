
import asyncio
import sys
import os
from datetime import datetime

# Add the backend directory to sys.path so we can import app modules
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(backend_dir)

from sqlalchemy import select
from app.database import get_session_maker
from app.models.analysis import Analysis
from scripts.data.seed_content_aapl import aapl_analysis
from scripts.data.seed_content_msft import msft_analysis
from scripts.data.seed_content_nvda import nvda_analysis
from scripts.data.seed_content_spy import spy_analysis

async def seed_data():
    print("Starting analysis data seed...")
    
    session_maker = get_session_maker()
    
    data_map = [
        {
            "symbol": "AAPL",
            "type": "stock",
            "title": "Apple Inc. Deep Dive Analysis",
            "title_th": "เจาะลึก Apple Inc. (AAPL): อาณาจักรผลไม้ที่ครองโลก",
            "content": aapl_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "MSFT",
            "type": "stock",
            "title": "Microsoft Deep Dive Analysis",
            "title_th": "เจาะลึก Microsoft (MSFT): ยักษ์ใหญ่ที่ตื่นจากการหลับใหลสู่ผู้นำ AI",
            "content": msft_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "NVDA",
            "type": "stock",
            "title": "NVIDIA Deep Dive Analysis",
            "title_th": "เจาะลึก NVIDIA (NVDA): ผู้สร้างสมองของ AI",
            "content": nvda_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "SPY",
            "type": "etf",
            "title": "SPY ETF Analysis",
            "title_th": "เจาะลึก SPY ETF: กองทุนดัชนี S&P 500 ที่ดีที่สุด?",
            "content": spy_analysis,
            "author": "Antigravity AI"
        }
    ]

    async with session_maker() as session:
        for item in data_map:
            print(f"Processing {item['symbol']}...")
            
            # Check if exists
            result = await session.execute(
                select(Analysis).where(
                    Analysis.symbol == item['symbol'],
                    Analysis.symbol_type == item['type']
                )
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"Updating {item['symbol']}...")
                existing.content_th = item['content']
                existing.title_th = item['title_th']
                existing.updated_at = datetime.utcnow()
                existing.status = "published"
                existing.published_at = datetime.utcnow()
            else:
                print(f"Creating {item['symbol']}...")
                new_analysis = Analysis(
                    symbol=item['symbol'],
                    symbol_type=item['type'],
                    title=item['title'],
                    title_th=item['title_th'],
                    content_th=item['content'],
                    author=item['author'],
                    status="published",
                    published_at=datetime.utcnow()
                )
                session.add(new_analysis)
        
        await session.commit()
        print("Data seed completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
