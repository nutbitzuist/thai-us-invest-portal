"""
Stock-related schemas.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StockBase(BaseModel):
    """Base stock schema."""
    symbol: str
    name: str
    name_th: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


class StockResponse(StockBase):
    """Full stock response schema."""
    id: int
    description: Optional[str] = None
    description_th: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    country: str = "USA"
    exchange: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class StockQuoteResponse(BaseModel):
    """Stock quote with market data."""
    symbol: str
    price: Optional[Decimal] = None
    change_amount: Optional[Decimal] = None
    change_percent: Optional[Decimal] = None
    open_price: Optional[Decimal] = None
    high_price: Optional[Decimal] = None
    low_price: Optional[Decimal] = None
    volume: Optional[int] = None
    market_cap: Optional[int] = None
    pe_ratio: Optional[Decimal] = None
    eps: Optional[Decimal] = None
    week_52_high: Optional[Decimal] = None
    week_52_low: Optional[Decimal] = None
    avg_volume_10d: Optional[int] = None
    dividend_yield: Optional[Decimal] = None
    sma_50: Optional[Decimal] = None
    sma_200: Optional[Decimal] = None
    trend: Optional[str] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class StockListItem(BaseModel):
    """Stock item for list views."""
    symbol: str
    name: str
    name_th: Optional[str] = None
    sector: Optional[str] = None
    price: Optional[Decimal] = None
    change_percent: Optional[Decimal] = None
    trend: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
