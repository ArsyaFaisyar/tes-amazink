from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from fastapi import HTTPException, status
from app.models.ticket import Ticket, TicketStatus, TicketPriority, TicketType
from app.models.user import User, UserRole
from app.models.history import TicketHistory, HistoryField
from app.models.activity import ActivityLog
from app.models.notification import Notification
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketStatusUpdate, TicketAssign

class TicketService:
    @staticmethod
    def generate_ticket_number(db: Session) -> str:
        year = datetime.utcnow().year
        count = db.query(Ticket).filter(Ticket.ticket_number.like(f"TCK-{year}-%")).count()
        return f"TCK-{year}-{str(count + 1).zfill(3)}"

    @staticmethod
    def create_ticket(db: Session, ticket_in: TicketCreate, reporter: User) -> Ticket:
        ticket = Ticket(
            **ticket_in.model_dump(),
            ticket_number=TicketService.generate_ticket_number(db),
            reporter_id=reporter.id,
            status=TicketStatus.OPEN
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        
        # Log activity
        TicketService.log_activity(db, reporter.id, "CREATE_TICKET", f"Created ticket {ticket.ticket_number}")
        return ticket

    @staticmethod
    def get_tickets(
        db: Session, 
        user: User,
        skip: int = 0, 
        limit: int = 10,
        search: str | None = None,
        status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
        ticket_type: TicketType | None = None,
        pic_id: int | None = None
    ):
        query = db.query(Ticket).filter(Ticket.is_deleted == False)
        
        # RBAC Filtering
        if user.role == UserRole.USER:
            query = query.filter(Ticket.reporter_id == user.id)
        elif user.role == UserRole.STAFF_IT:
            query = query.filter(Ticket.pic_id == user.id)
        
        # Search
        if search:
            query = query.join(Ticket.reporter).filter(
                or_(
                    Ticket.ticket_number.ilike(f"%{search}%"),
                    Ticket.title.ilike(f"%{search}%"),
                    User.name.ilike(f"%{search}%")
                )
            )
            
        # Multi-filter
        if status:
            query = query.filter(Ticket.status == status)
        if priority:
            query = query.filter(Ticket.priority == priority)
        if ticket_type:
            query = query.filter(Ticket.ticket_type == ticket_type)
        if pic_id:
            query = query.filter(Ticket.pic_id == pic_id)
            
        total = query.count()
        tickets = query.offset(skip).limit(limit).all()
        return tickets, total

    @staticmethod
    def update_status(db: Session, ticket_id: int, status_in: TicketStatusUpdate, current_user: User) -> Ticket:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.is_deleted == False).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        if ticket.status == TicketStatus.DONE:
            raise HTTPException(status_code=400, detail="Ticket is locked and cannot be updated")

        # State Machine Logic
        valid_transitions = {
            TicketStatus.OPEN: [TicketStatus.ASSIGNED],
            TicketStatus.ASSIGNED: [TicketStatus.IN_PROGRESS],
            TicketStatus.IN_PROGRESS: [TicketStatus.QA],
            TicketStatus.QA: [TicketStatus.DONE, TicketStatus.IN_PROGRESS], # Can go back to IN_PROGRESS if QA fails
        }
        
        new_status = status_in.status
        if new_status not in valid_transitions.get(ticket.status, []):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid status transition from {ticket.status} to {new_status}"
            )
            
        old_status = ticket.status
        ticket.status = new_status
        
        # side effects
        TicketService.add_history(db, ticket.id, current_user.id, HistoryField.STATUS, old_status, new_status)
        TicketService.log_activity(db, current_user.id, "UPDATE_STATUS", f"Updated {ticket.ticket_number} status to {new_status}")
        TicketService.notify(db, ticket.reporter_id, f"Ticket {ticket.ticket_number} status updated to {new_status}")
        if ticket.pic_id:
            TicketService.notify(db, ticket.pic_id, f"Ticket {ticket.ticket_number} status updated to {new_status}")
            
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def assign_ticket(db: Session, ticket_id: int, assign_in: TicketAssign, current_user: User) -> Ticket:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.is_deleted == False).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Only PM_IT can assign
        if current_user.role != UserRole.PM_IT:
            raise HTTPException(status_code=403, detail="Only PM IT can assign tickets")

        old_pic = ticket.pic_id
        ticket.pic_id = assign_in.pic_id
        
        # Automatically move to ASSIGNED if currently OPEN
        if ticket.status == TicketStatus.OPEN:
            ticket.status = TicketStatus.ASSIGNED
            TicketService.add_history(db, ticket.id, current_user.id, HistoryField.STATUS, TicketStatus.OPEN, TicketStatus.ASSIGNED)
        
        TicketService.add_history(db, ticket.id, current_user.id, HistoryField.PIC, str(old_pic), str(assign_in.pic_id))
        
        if assign_in.priority:
            old_prio = ticket.priority
            ticket.priority = assign_in.priority
            TicketService.add_history(db, ticket.id, current_user.id, HistoryField.PRIORITY, old_prio, assign_in.priority)

        TicketService.log_activity(db, current_user.id, "ASSIGN_TICKET", f"Assigned {ticket.ticket_number} to PIC ID {assign_in.pic_id}")
        TicketService.notify(db, assign_in.pic_id, f"You have been assigned to ticket {ticket.ticket_number}")
        
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def add_history(db: Session, ticket_id: int, user_id: int, field: HistoryField, old_val: str, new_val: str):
        history = TicketHistory(
            ticket_id=ticket_id,
            changed_by_id=user_id,
            field_changed=field,
            old_value=str(old_val),
            new_value=str(new_val)
        )
        db.add(history)

    @staticmethod
    def log_activity(db: Session, user_id: int, action: str, details: str):
        log = ActivityLog(user_id=user_id, action=action, details=details)
        db.add(log)

    @staticmethod
    def notify(db: Session, user_id: int, message: str):
        notification = Notification(user_id=user_id, message=message)
        db.add(notification)
