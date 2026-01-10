"""
Price-related models: LatestQuote, StockPrice, ETFPrice.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, BigInteger, UniqueConstraint, Index as SQLIndex
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
    price: Mapped[Optional[Decimal]] = mapped_column()
    change_amount: Mapped[Optional[Decimal]] = mapped_column()
    change_percent: Mapped[Optional[Decimal]] = mapped_column()
    open_price: Mapped[Optional[Decimal]] = mapped_column()
    high_price: Mapped[Optional[Decimal]] = mapped_column()
    low_price: Mapped[Optional[Decimal]] = mapped_column()
    volume: Mapped[Optional[int]] = mapped_column(BigInteger)
    
    # Fundamentals
    market_cap: Mapped[Optional[int]] = mapped_column(BigInteger)
    pe_ratio: Mapped[Optional[Decimal]] = mapped_column()
    eps: Mapped[Optional[Decimal]] = mapped_column()
    
    # Ranges
    week_52_high: Mapped[Optional[Decimal]] = mapped_column()
    week_52_low: Mapped[Optional[Decimal]] = mapped_column()
    avg_volume_10d: Mapped[Optional[int]] = mapped_column(BigInteger)
    dividend_yield: Mapped[Optional[Decimal]] = mapped_column()
    
    # Technical indicators
    sma_50: Mapped[Optional[Decimal]] = mapped_column()
    sma_200: Mapped[Optional[Decimal]] = mapped_column()
    trend: Mapped[Optional[str]] = mapped_column(String(20))  # 'uptrend', 'downtrend', 'sideways'
    
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
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
    date: Mapped[date] = mapped_column(nullable=False)
    
    # OHLCV data
    open: Mapped[Optional[Decimal]] = mapped_column()
    high: Mapped[Optional[Decimal]] = mapped_column()
    low: Mapped[Optional[Decimal]] = mapped_column()
    close: Mapped[Optional[Decimal]] = mapped_column()
    adj_close: Mapped[Optional[Decimal]] = mapped_column()
    volume: Mapped[Optional[int]] = mapped_column(BigInteger)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
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
    date: Mapped[date] = mapped_column(nullable=False)
    
    # OHLCV data
    open: Mapped[Optional[Decimal]] = mapped_column()
    high: Mapped[Optional[Decimal]] = mapped_column()
    low: Mapped[Optional[Decimal]] = mapped_column()
    close: Mapped[Optional[Decimal]] = mapped_column()
    adj_close: Mapped[Optional[Decimal]] = mapped_column()
    volume: Mapped[Optional[int]] = mapped_column(BigInteger)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<ETFPrice {self.symbol} {self.date}: {self.close}>"
