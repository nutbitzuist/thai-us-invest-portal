"""
FastAPI application entry point.
"""
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import close_db
from app.routers import health, indices, stocks, etfs, search, analysis, admin

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    print(f"Starting Thai U.S. Investment Portal API...")
    print(f"Environment: {settings.environment}")
    
    # Auto-migration for schema updates
    try:
        from app.database import engine
        from sqlalchemy import text
        
        columns = [
            "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS ceo VARCHAR(255)",
            "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS employees INTEGER",
            "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS headquarters VARCHAR(255)",
            "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS founded_year INTEGER",
            "ALTER TABLE stocks ADD COLUMN IF NOT EXISTS analysis_data TEXT",
        ]
        
        async with engine.begin() as conn:
            for col_sql in columns:
                try:
                    await conn.execute(text(col_sql))
                except Exception as e:
                    # Ignore if column exists or other minor error
                    print(f"Migration note: {e}")
                    
        print("Schema migration checked.")
    except Exception as e:
        print(f"Schema migration warning: {e}")
    
    yield
    
    # Shutdown
    print("Shutting down...")
    await close_db()


# Create FastAPI application
app = FastAPI(
    title="Thai U.S. Investment Portal API",
    description="API สำหรับข้อมูลการลงทุนหุ้นสหรัฐสำหรับนักลงทุนไทย",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(indices.router, prefix=settings.api_prefix)
app.include_router(stocks.router, prefix=settings.api_prefix)
app.include_router(etfs.router, prefix=settings.api_prefix)
app.include_router(search.router, prefix=settings.api_prefix)
app.include_router(analysis.router, prefix=settings.api_prefix)
app.include_router(admin.router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Thai U.S. Investment Portal API",
        "name_th": "API ศูนย์ข้อมูลลงทุนหุ้นสหรัฐ",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
