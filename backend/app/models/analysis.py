"""
Analysis model for Thai content.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Text, Index as SQLIndex
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Analysis(Base):
    """Thai language analysis content for stocks and ETFs."""
    
    __tablename__ = "analysis"
    __table_args__ = (
        SQLIndex("idx_analysis_symbol", "symbol", "symbol_type"),
        SQLIndex("idx_analysis_status", "status"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(10), nullable=False)
    symbol_type: Mapped[str] = mapped_column(String(10), nullable=False)  # 'stock' or 'etf'
    
    # Content
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    title_th: Mapped[Optional[str]] = mapped_column(String(255))
    summary_th: Mapped[Optional[str]] = mapped_column(Text)
    content_th: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Analysis
    trend_opinion: Mapped[Optional[str]] = mapped_column(String(20))  # Analyst's opinion
    target_price: Mapped[Optional[Decimal]] = mapped_column()
    
    # Metadata
    author: Mapped[Optional[str]] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="draft")  # 'draft', 'published'
    published_at: Mapped[Optional[datetime]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Analysis {self.symbol}: {self.title}>"
