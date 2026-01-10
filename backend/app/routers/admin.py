"""
Admin endpoints for database management.
"""
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.config import get_settings
from app.services.data_seeder import run_all_seeds

router = APIRouter(tags=["admin"])


@router.post("/seed")
async def seed_database(
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
    db: AsyncSession = Depends(get_db)
):
    """Seed the database with initial data.
    
    Requires X-Admin-Key header matching ADMIN_API_KEY env var.
    """
    settings = get_settings()
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    
    await run_all_seeds(db)
    
    return {
        "success": True,
        "message": "Database seeded successfully",
        "seeded": ["indices", "stocks", "etfs", "index_components"]
    }
