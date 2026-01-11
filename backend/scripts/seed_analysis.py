
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
from scripts.data.seed_content_googl import googl_analysis
from scripts.data.seed_content_amzn import amzn_analysis
from scripts.data.seed_content_meta import meta_analysis
from scripts.data.seed_content_tsla import tsla_analysis
from scripts.data.seed_content_amd import amd_analysis
from scripts.data.seed_content_nflx import nflx_analysis
from scripts.data.seed_content_qqq import qqq_analysis

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
        },
        {
            "symbol": "GOOGL",
            "type": "stock",
            "title": "Alphabet Inc. Deep Dive Analysis",
            "title_th": "เจาะลึก Alphabet (GOOGL): เจ้าแห่งการค้นหาและข้อมูลของโลก",
            "content": googl_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "AMZN",
            "type": "stock",
            "title": "Amazon.com Deep Dive Analysis",
            "title_th": "เจาะลึก Amazon (AMZN): จากร้านหนังสือสู่จักรวรรดิ E-commerce และ Cloud",
            "content": amzn_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "META",
            "type": "stock",
            "title": "Meta Platforms Deep Dive Analysis",
            "title_th": "เจาะลึก Meta Platforms (META): อาณาจักร Social Media ที่ใหญ่ที่สุด",
            "content": meta_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "TSLA",
            "type": "stock",
            "title": "Tesla Deep Dive Analysis",
            "title_th": "เจาะลึก Tesla (TSLA): มากกว่าแค่รถยนต์ไฟฟ้า มันคือ AI และหุ่นยนต์",
            "content": tsla_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "AMD",
            "type": "stock",
            "title": "AMD Deep Dive Analysis",
            "title_th": "เจาะลึก AMD: ผู้ท้าชิงบัลลังก์ชิปเซตที่น่ากลัวที่สุด",
            "content": amd_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "NFLX",
            "type": "stock",
            "title": "Netflix Deep Dive Analysis",
            "title_th": "เจาะลึก Netflix (NFLX): ราชาแห่งสตรีมมิ่งที่เปลี่ยนพฤติกรรมคนทั้งโลก",
            "content": nflx_analysis,
            "author": "Antigravity AI"
        },
        {
            "symbol": "QQQ",
            "type": "etf",
            "title": "Invesco QQQ Deep Dive Analysis",
            "title_th": "เจาะลึก QQQ: กองทุนรวมหุ้นเทคโนโลยีแห่งอนาคต",
            "content": qqq_analysis,
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
        print(f"Data seed completed successfully! ({len(data_map)} items processed)")
        return len(data_map)

if __name__ == "__main__":
    asyncio.run(seed_data())
