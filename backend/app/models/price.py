"""
Price-related models: LatestQuote, StockPrice, ETFPrice.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, BigInteger, Numeric, Date, DateTime, UniqueConstraint, Index as SQLIndex
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LatestQuote(Base):
    """Latest price quote for stocks and ETFs."""
    
    __tablename__ = "latest_quotes"
    __table_args__ = (
        SQLIndex("idx_latest_quotes_symbol", "symbol"),
        SQLIndex("idx_latest_quotes_type", "symbol_type"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    symbol_type: Mapped[str] = mapped_column(String(10), nullable=False)  # 'stock' or 'etf'
    
    # Price data
    price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    change_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    change_percent: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 4), nullable=True)
    open_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    high_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    low_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    volume: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    
    # Fundamentals
    market_cap: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    pe_ratio: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    eps: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 4), nullable=True)
    
    # Ranges
    week_52_high: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    week_52_low: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    avg_volume_10d: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    dividend_yield: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 4), nullable=True)
    
    # Technical indicators
    sma_50: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    sma_200: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    trend: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 'uptrend', 'downtrend', 'sideways'
    
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    
    def __repr__(self) -> str:
        return f"<LatestQuote {self.symbol}: {self.price}>"


class StockPrice(Base):
    """Historical daily price data for stocks."""
    
    __tablename__ = "stock_prices"
    __table_args__ = (
        UniqueConstraint("symbol", "date", name="uq_stock_price_date"),
        SQLIndex("idx_stock_prices_symbol_date", "symbol", "date"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(10), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # OHLCV data
    open: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    high: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    low: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    close: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    adj_close: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    volume: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    
    def __repr__(self) -> str:
        return f"<StockPrice {self.symbol} {self.date}: {self.close}>"


class ETFPrice(Base):
    """Historical daily price data for ETFs."""
    
    __tablename__ = "etf_prices"
    __table_args__ = (
        UniqueConstraint("symbol", "date", name="uq_etf_price_date"),
        SQLIndex("idx_etf_prices_symbol_date", "symbol", "date"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(10), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # OHLCV data
    open: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    high: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    low: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    close: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    adj_close: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    volume: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    
    def __repr__(self) -> str:
        return f"<ETFPrice {self.symbol} {self.date}: {self.close}>"
