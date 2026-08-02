from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.dashboard import DashboardService
from app.schemas.dashboard import DashboardSummary
from app.dependencies import RoleChecker
from app.models.user import UserRole

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
def get_summary(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[None, Depends(RoleChecker([UserRole.PM_IT]))]
):
    return DashboardService.get_summary(db)
