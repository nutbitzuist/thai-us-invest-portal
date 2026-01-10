"""
Index and IndexComponent models.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Text, ForeignKey, UniqueConstraint, Index as SQLIndex
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Index(Base):
    """Stock market index (e.g., S&P 500, Nasdaq 100)."""
    
    __tablename__ = "indices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_th: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    description_th: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    components: Mapped[list["IndexComponent"]] = relationship(
        back_populates="index",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<Index {self.symbol}: {self.name}>"


class IndexComponent(Base):
    """Stock that belongs to an index."""
    
    __tablename__ = "index_components"
    __table_args__ = (
        UniqueConstraint("index_symbol", "stock_symbol", name="uq_index_stock"),
        SQLIndex("idx_index_components_index", "index_symbol"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    index_symbol: Mapped[str] = mapped_column(
        String(20), 
        ForeignKey("indices.symbol", ondelete="CASCADE"),
        nullable=False
    )
    stock_symbol: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("stocks.symbol", ondelete="CASCADE"),
        nullable=False
    )
    weight: Mapped[Optional[Decimal]] = mapped_column()
    added_date: Mapped[Optional[date]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    index: Mapped["Index"] = relationship(back_populates="components")
    stock: Mapped["Stock"] = relationship(back_populates="index_memberships")
    
    def __repr__(self) -> str:
        return f"<IndexComponent {self.index_symbol}/{self.stock_symbol}>"


# Import Stock here to avoid circular imports
from app.models.stock import Stock
