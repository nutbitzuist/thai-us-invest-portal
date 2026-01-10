"""
Stock model.
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, Boolean, Index as SQLIndex
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.index import IndexComponent


class Stock(Base):
    """US stock information."""
    
    __tablename__ = "stocks"
    __table_args__ = (
        SQLIndex("idx_stocks_symbol", "symbol"),
        SQLIndex("idx_stocks_sector", "sector"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_th: Mapped[Optional[str]] = mapped_column(String(255))
    sector: Mapped[Optional[str]] = mapped_column(String(100))
    industry: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    description_th: Mapped[Optional[str]] = mapped_column(Text)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500))
    website: Mapped[Optional[str]] = mapped_column(String(500))
    ceo: Mapped[Optional[str]] = mapped_column(String(255))
    employees: Mapped[Optional[int]] = mapped_column()
    headquarters: Mapped[Optional[str]] = mapped_column(String(255))
    founded_year: Mapped[Optional[int]] = mapped_column()
    analysis_data: Mapped[Optional[str]] = mapped_column(Text)  # JSON string
    country: Mapped[str] = mapped_column(String(50), default="USA")
    exchange: Mapped[Optional[str]] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    index_memberships: Mapped[list["IndexComponent"]] = relationship(
        back_populates="stock",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<Stock {self.symbol}: {self.name}>"
