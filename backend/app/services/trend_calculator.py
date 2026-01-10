"""
Trend calculation service.
"""
from typing import Optional


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


def get_trend_thai(trend: str) -> str:
    """Get Thai translation of trend."""
    translations = {
        'uptrend': 'ขาขึ้น',
        'downtrend': 'ขาลง', 
        'sideways': 'ไซด์เวย์',
    }
    return translations.get(trend, 'ไซด์เวย์')


def get_trend_color(trend: str) -> str:
    """Get color code for trend."""
    colors = {
        'uptrend': '#00C851',
        'downtrend': '#FF4444',
        'sideways': '#FFBB33',
    }
    return colors.get(trend, '#FFBB33')
