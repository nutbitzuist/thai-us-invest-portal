"""
Helper utilities.
"""
from datetime import datetime, time
from decimal import Decimal
from typing import Optional

import pytz


def calculate_trend(
    price: Optional[float],
    sma_50: Optional[float],
    sma_200: Optional[float]
) -> str:
    """
    Calculate trend based on price and moving averages.
    
    Uptrend: Price > SMA50 > SMA200 (bullish)
    Downtrend: Price < SMA50 < SMA200 (bearish)
    Sideways: Everything else (consolidating)
    
    Args:
        price: Current price
        sma_50: 50-day simple moving average
        sma_200: 200-day simple moving average
    
    Returns:
        'uptrend', 'downtrend', or 'sideways'
    """
    if price is None or sma_50 is None or sma_200 is None:
        return "sideways"
    
    if price > sma_50 and sma_50 > sma_200:
        return "uptrend"
    elif price < sma_50 and sma_50 < sma_200:
        return "downtrend"
    else:
        return "sideways"


def is_market_open() -> bool:
    """
    Check if US stock market is currently open.
    
    Market hours: 9:30 AM - 4:00 PM ET, Monday-Friday
    
    Returns:
        True if market is open, False otherwise
    """
    et = pytz.timezone('America/New_York')
    now = datetime.now(et)
    
    # Weekend check
    if now.weekday() >= 5:
        return False
    
    # Market hours: 9:30 AM - 4:00 PM ET
    market_open = time(9, 30)
    market_close = time(16, 0)
    
    return market_open <= now.time() <= market_close


def format_market_cap(value: Optional[int]) -> Optional[str]:
    """
    Format market cap for display.
    
    Args:
        value: Market cap in dollars
    
    Returns:
        Formatted string (e.g., "2.85T", "150B", "5.2M")
    """
    if value is None:
        return None
    
    if value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    elif value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    else:
        return f"{value:,}"


def format_volume(value: Optional[int]) -> Optional[str]:
    """
    Format volume for display.
    
    Args:
        value: Volume
    
    Returns:
        Formatted string (e.g., "52M", "1.2B")
    """
    if value is None:
        return None
    
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"
    else:
        return str(value)
