"""
SyncLog model for tracking data synchronization jobs.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SyncLog(Base):
    """Log entries for data synchronization jobs."""
    
    __tablename__ = "sync_log"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sync_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'quotes', 'prices', 'components'
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # 'started', 'completed', 'failed'
    records_processed: Mapped[int] = mapped_column(Integer, default=0)
    records_updated: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    started_at: Mapped[Optional[datetime]] = mapped_column()
    completed_at: Mapped[Optional[datetime]] = mapped_column()
    
    def __repr__(self) -> str:
        return f"<SyncLog {self.sync_type}: {self.status}>"
