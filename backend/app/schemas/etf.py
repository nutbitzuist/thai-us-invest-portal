"""
ETF-related schemas.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ETFBase(BaseModel):
    """Base ETF schema."""
    symbol: str
    name: str
    name_th: Optional[str] = None
    category: Optional[str] = None


class ETFResponse(ETFBase):
    """Full ETF response schema."""
    id: int
    expense_ratio: Optional[Decimal] = None
    aum: Optional[int] = None
    description: Optional[str] = None
    description_th: Optional[str] = None
    provider: Optional[str] = None
    inception_date: Optional[date] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class ETFHoldingResponse(BaseModel):
    """ETF holding response schema."""
    id: int
    etf_symbol: str
    holding_symbol: Optional[str] = None
    holding_name: Optional[str] = None
    weight: Optional[Decimal] = None
    shares: Optional[int] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class ETFQuoteResponse(BaseModel):
    """ETF quote with market data."""
    symbol: str
    price: Optional[Decimal] = None
    change_amount: Optional[Decimal] = None
    change_percent: Optional[Decimal] = None
    volume: Optional[int] = None
    week_52_high: Optional[Decimal] = None
    week_52_low: Optional[Decimal] = None
    dividend_yield: Optional[Decimal] = None
    sma_50: Optional[Decimal] = None
    sma_200: Optional[Decimal] = None
    trend: Optional[str] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class ETFListItem(BaseModel):
    """ETF item for list views."""
    symbol: str
    name: str
    name_th: Optional[str] = None
    category: Optional[str] = None
    expense_ratio: Optional[Decimal] = None
    aum: Optional[int] = None
    price: Optional[Decimal] = None
    change_percent: Optional[Decimal] = None
    trend: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
