"""
ETF and ETFHolding models.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Text, Boolean, BigInteger, ForeignKey, UniqueConstraint, Index as SQLIndex
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ETF(Base):
    """Exchange-Traded Fund information."""
    
    __tablename__ = "etfs"
    __table_args__ = (
        SQLIndex("idx_etfs_symbol", "symbol"),
        SQLIndex("idx_etfs_category", "category"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_th: Mapped[Optional[str]] = mapped_column(String(255))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    expense_ratio: Mapped[Optional[Decimal]] = mapped_column()
    aum: Mapped[Optional[int]] = mapped_column(BigInteger)  # Assets Under Management
    description: Mapped[Optional[str]] = mapped_column(Text)
    description_th: Mapped[Optional[str]] = mapped_column(Text)
    provider: Mapped[Optional[str]] = mapped_column(String(100))
    inception_date: Mapped[Optional[date]] = mapped_column()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    holdings: Mapped[list["ETFHolding"]] = relationship(
        back_populates="etf",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<ETF {self.symbol}: {self.name}>"


class ETFHolding(Base):
    """Individual holding within an ETF."""
    
    __tablename__ = "etf_holdings"
    __table_args__ = (
        UniqueConstraint("etf_symbol", "holding_symbol", name="uq_etf_holding"),
        SQLIndex("idx_etf_holdings_etf", "etf_symbol"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    etf_symbol: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("etfs.symbol", ondelete="CASCADE"),
        nullable=False
    )
    holding_symbol: Mapped[Optional[str]] = mapped_column(String(10))
    holding_name: Mapped[Optional[str]] = mapped_column(String(255))
    weight: Mapped[Optional[Decimal]] = mapped_column()
    shares: Mapped[Optional[int]] = mapped_column(BigInteger)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    etf: Mapped["ETF"] = relationship(back_populates="holdings")
    
    def __repr__(self) -> str:
        return f"<ETFHolding {self.etf_symbol}/{self.holding_symbol}>"
