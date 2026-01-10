"""
Analysis-related schemas.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnalysisBase(BaseModel):
    """Base analysis schema."""
    symbol: str
    symbol_type: str  # 'stock' or 'etf'
    title: str
    title_th: Optional[str] = None
    summary_th: Optional[str] = None
    content_th: str


class AnalysisCreate(AnalysisBase):
    """Schema for creating analysis."""
    trend_opinion: Optional[str] = None
    target_price: Optional[Decimal] = None
    author: Optional[str] = None


class AnalysisUpdate(BaseModel):
    """Schema for updating analysis."""
    title: Optional[str] = None
    title_th: Optional[str] = None
    summary_th: Optional[str] = None
    content_th: Optional[str] = None
    trend_opinion: Optional[str] = None
    target_price: Optional[Decimal] = None
    status: Optional[str] = None  # 'draft', 'published'


class AnalysisResponse(AnalysisBase):
    """Full analysis response schema."""
    id: int
    trend_opinion: Optional[str] = None
    target_price: Optional[Decimal] = None
    author: Optional[str] = None
    status: str = "draft"
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class AnalysisListItem(BaseModel):
    """Analysis item for list views."""
    id: int
    symbol: str
    symbol_type: str
    title: str
    title_th: Optional[str] = None
    summary_th: Optional[str] = None
    author: Optional[str] = None
    status: str
    published_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
