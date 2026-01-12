
import asyncio
import os
import sys

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import get_db_session
from app.models import Stock, Analysis
from app.services.ai_service import get_ai_service

async def generate_all_analysis(limit=20, offset=0, target_symbol=None):
    print(f"Starting AI Analysis Generation (Limit: {limit}, Offset: {offset})...")
    
    ai_service = get_ai_service()
    if not ai_service.client:
        print("Error: OPENAI_API_KEY is not set. Please set it in your .env file.")
        return

    async for db in get_db_session():
        try:
            # Build query with consistent ordering
            query = select(Stock).order_by(Stock.id)
            
            if target_symbol:
                query = query.where(Stock.symbol == target_symbol)
            else:
                query = query.offset(offset).limit(limit)

            result = await db.execute(query)
            stocks = result.scalars().all()
            
            total = len(stocks)
            print(f"Found {total} stocks to analyze in this batch.")

            for i, stock in enumerate(stocks):
                print(f"[{i+1}/{total}] Analyzing {stock.symbol} ({stock.name})...")
                
                # Check if analysis exists
                stmt = select(Analysis).where(
                    Analysis.symbol == stock.symbol,
                    Analysis.symbol_type == 'stock'
                )
                existing = (await db.execute(stmt)).scalar_one_or_none()

                # Generate content
                content = await ai_service.generate_stock_analysis(stock.name, stock.symbol)
                
                if content:
                    if existing:
                        print(f"  - Updating existing analysis for {stock.symbol}")
                        existing.content_th = content
                        existing.status = 'published'
                        existing.author = 'AI Analyst'
                    else:
                        print(f"  - Creating new analysis for {stock.symbol}")
                        new_analysis = Analysis(
                            symbol=stock.symbol,
                            symbol_type='stock',
                            title=f"วิเคราะห์หุ้น {stock.symbol}: {stock.name}",
                            title_th=f"เจาะลึก {stock.name} ({stock.symbol})",
                            content_th=content,
                            status='published',
                            author='AI Analyst'
                        )
                        db.add(new_analysis)
                    
                    # Commit every item to save progress
                    await db.commit()
                else:
                    print(f"  - Failed to generate content for {stock.symbol}")
                
                # Sleep briefly to be nice to API
                await asyncio.sleep(1)

        except Exception as e:
            print(f"Error: {e}")
            await db.rollback()
        finally:
            print("Done.")
            return

    parser = argparse.ArgumentParser(description='Generate stock analysis using AI')
    parser.add_argument('--limit', type=int, default=20, help='Number of stocks to process')
    parser.add_argument('--offset', type=int, default=0, help='Offset for pagination')
    parser.add_argument('--symbol', type=str, help='Specific stock symbol to analyze')
    
    args = parser.parse_args()
    
    asyncio.run(generate_all_analysis(limit=args.limit, offset=args.offset, target_symbol=args.symbol))
