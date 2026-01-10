"""
Common schemas for API responses.
"""
from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

DataT = TypeVar("DataT")


class ErrorDetail(BaseModel):
    """Error detail for API responses."""
    code: str
    message: str


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: ErrorDetail


class SuccessResponse(BaseModel, Generic[DataT]):
    """Standard success response."""
    success: bool = True
    data: DataT


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    total: int
    page: int
    per_page: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Paginated response with metadata."""
    success: bool = True
    data: list[DataT]
    meta: PaginationMeta


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
