from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ticket import TicketService
from app.schemas.ticket import TicketCreate, TicketOut, TicketStatusUpdate, TicketAssign
from app.dependencies import get_current_user, RoleChecker
from app.models.user import User, UserRole
from app.models.ticket import TicketStatus, TicketPriority, TicketType

router = APIRouter()

@router.post("/", response_model=TicketOut)
def create_ticket(
    ticket_in: TicketCreate, 
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    return TicketService.create_ticket(db, ticket_in, current_user)

@router.get("/")
def list_tickets(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    status: TicketStatus | None = None,
    priority: TicketPriority | None = None,
    ticket_type: TicketType | None = None,
    pic_id: int | None = None
):
    tickets, total = TicketService.get_tickets(
        db, current_user, skip, limit, search, status, priority, ticket_type, pic_id
    )
    return {"data": tickets, "total": total}

@router.patch("/{id}/status", response_model=TicketOut)
def update_ticket_status(
    id: int,
    status_in: TicketStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    return TicketService.update_status(db, id, status_in, current_user)

@router.patch("/{id}/assign", response_model=TicketOut)
def assign_ticket(
    id: int,
    assign_in: TicketAssign,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(RoleChecker([UserRole.PM_IT]))]
):
    return TicketService.assign_ticket(db, id, assign_in, current_user)
