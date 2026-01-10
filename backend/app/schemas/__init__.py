"""
Schemas package initialization.
"""
from app.schemas.common import (
    SuccessResponse,
    ErrorResponse,
    ErrorDetail,
    PaginationMeta,
    PaginatedResponse,
)
from app.schemas.index import (
    IndexBase,
    IndexResponse,
    IndexComponentResponse,
)
from app.schemas.stock import (
    StockBase,
    StockResponse,
    StockQuoteResponse,
)
from app.schemas.etf import (
    ETFBase,
    ETFResponse,
    ETFHoldingResponse,
)
from app.schemas.analysis import (
    AnalysisBase,
    AnalysisCreate,
    AnalysisUpdate,
    AnalysisResponse,
)

__all__ = [
    # Common
    "SuccessResponse",
    "ErrorResponse", 
    "ErrorDetail",
    "PaginationMeta",
    "PaginatedResponse",
    # Index
    "IndexBase",
    "IndexResponse",
    "IndexComponentResponse",
    # Stock
    "StockBase",
    "StockResponse",
    "StockQuoteResponse",
    # ETF
    "ETFBase",
    "ETFResponse",
    "ETFHoldingResponse",
    # Analysis
    "AnalysisBase",
    "AnalysisCreate",
    "AnalysisUpdate",
    "AnalysisResponse",
]
