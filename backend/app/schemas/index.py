"""
Index-related schemas.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class IndexBase(BaseModel):
    """Base index schema."""
    symbol: str
    name: str
    name_th: Optional[str] = None
    description: Optional[str] = None
    description_th: Optional[str] = None


class IndexResponse(IndexBase):
    """Index response schema."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class IndexComponentResponse(BaseModel):
    """Index component response schema."""
    id: int
    index_symbol: str
    stock_symbol: str
    weight: Optional[Decimal] = None
    added_date: Optional[date] = None
    
    # Stock details (joined)
    stock_name: Optional[str] = None
    stock_sector: Optional[str] = None
    price: Optional[Decimal] = None
    change_percent: Optional[Decimal] = None
    trend: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
