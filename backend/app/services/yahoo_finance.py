"""
Yahoo Finance service for fetching stock and ETF data.
"""
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any
import logging

import yfinance as yf
import pandas as pd

from app.config import get_settings
from app.utils.helpers import calculate_trend

logger = logging.getLogger(__name__)
settings = get_settings()


class YahooFinanceService:
    """Service for fetching data from Yahoo Finance."""
    
    def __init__(self):
        self.rate_limit = settings.yfinance_rate_limit
        self._last_request_time = None
    
    async def _rate_limit_wait(self):
        """Wait to respect rate limiting."""
        if self._last_request_time:
            elapsed = (datetime.now() - self._last_request_time).total_seconds()
            if elapsed < 1.0 / self.rate_limit:
                await asyncio.sleep(1.0 / self.rate_limit - elapsed)
        self._last_request_time = datetime.now()
    
    def _run_sync(self, func, *args, **kwargs):
        """Run synchronous yfinance call."""
        return func(*args, **kwargs)
    
    async def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get latest quote for a symbol.
        
        Args:
            symbol: Stock or ETF symbol
            
        Returns:
            Quote data dictionary or None if not found
        """
        await self._rate_limit_wait()
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info or 'regularMarketPrice' not in info:
                return None
            
            # Get historical data for moving averages
            hist = ticker.history(period="1y")
            
            sma_50 = None
            sma_200 = None
            
            if len(hist) >= 50:
                sma_50 = float(hist['Close'].tail(50).mean())
            if len(hist) >= 200:
                sma_200 = float(hist['Close'].tail(200).mean())
            
            price = info.get('regularMarketPrice') or info.get('currentPrice')
            prev_close = info.get('regularMarketPreviousClose', price)
            change = (price - prev_close) if price and prev_close else 0
            change_pct = (change / prev_close * 100) if prev_close else 0
            
            trend = calculate_trend(price, sma_50, sma_200)
            
            return {
                'symbol': symbol.upper(),
                'price': price,
                'change_amount': round(change, 4),
                'change_percent': round(change_pct, 4),
                'open_price': info.get('regularMarketOpen'),
                'high_price': info.get('regularMarketDayHigh'),
                'low_price': info.get('regularMarketDayLow'),
                'volume': info.get('regularMarketVolume'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'eps': info.get('trailingEps'),
                'week_52_high': info.get('fiftyTwoWeekHigh'),
                'week_52_low': info.get('fiftyTwoWeekLow'),
                'avg_volume_10d': info.get('averageVolume10days'),
                'dividend_yield': info.get('dividendYield'),
                'sma_50': sma_50,
                'sma_200': sma_200,
                'trend': trend,
            }
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {e}")
            return None
    
    async def get_stock_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed stock information.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Stock info dictionary
        """
        await self._rate_limit_wait()
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info:
                return None
            
            return {
                'symbol': symbol.upper(),
                'name': info.get('longName') or info.get('shortName', ''),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'description': info.get('longBusinessSummary'),
                'website': info.get('website'),
                'exchange': info.get('exchange'),
                'country': info.get('country', 'USA'),
            }
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {e}")
            return None
    
    async def get_etf_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get ETF information including holdings.
        
        Args:
            symbol: ETF symbol
            
        Returns:
            ETF info dictionary
        """
        await self._rate_limit_wait()
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info:
                return None
            
            # Get top holdings if available
            holdings = []
            try:
                if hasattr(ticker, 'major_holders'):
                    holder_data = ticker.institutional_holders
                    if holder_data is not None and not holder_data.empty:
                        for _, row in holder_data.head(20).iterrows():
                            holdings.append({
                                'holding_name': row.get('Holder', ''),
                                'weight': None,
                                'shares': row.get('Shares', 0)
                            })
            except:
                pass
            
            return {
                'symbol': symbol.upper(),
                'name': info.get('longName') or info.get('shortName', ''),
                'category': info.get('category'),
                'expense_ratio': info.get('annualReportExpenseRatio'),
                'aum': info.get('totalAssets'),
                'description': info.get('longBusinessSummary'),
                'holdings': holdings,
            }
        except Exception as e:
            logger.error(f"Error fetching ETF info for {symbol}: {e}")
            return None
    
    async def get_history(
        self, 
        symbol: str, 
        period: str = "1y"
    ) -> List[Dict[str, Any]]:
        """
        Get historical price data.
        
        Args:
            symbol: Stock or ETF symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
            
        Returns:
            List of OHLCV data
        """
        await self._rate_limit_wait()
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return []
            
            result = []
            for date, row in hist.iterrows():
                result.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(row['Open'], 4),
                    'high': round(row['High'], 4),
                    'low': round(row['Low'], 4),
                    'close': round(row['Close'], 4),
                    'volume': int(row['Volume']),
                })
            
            return result
        except Exception as e:
            logger.error(f"Error fetching history for {symbol}: {e}")
            return []
    
    async def batch_get_quotes(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        Get quotes for multiple symbols.
        
        Args:
            symbols: List of stock/ETF symbols
            
        Returns:
            Dictionary mapping symbols to their quote data
        """
        results = {}
        for symbol in symbols:
            quote = await self.get_quote(symbol)
            if quote:
                results[symbol] = quote
        return results


# Singleton instance
_yahoo_service: Optional[YahooFinanceService] = None


def get_yahoo_service() -> YahooFinanceService:
    """Get Yahoo Finance service singleton."""
    global _yahoo_service
    if _yahoo_service is None:
        _yahoo_service = YahooFinanceService()
    return _yahoo_service
