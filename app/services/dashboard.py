from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.ticket import Ticket, TicketStatus, TicketPriority
from app.schemas.dashboard import DashboardSummary, StatusBreakdown, PriorityBreakdown

class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> DashboardSummary:
        total_tickets = db.query(Ticket).filter(Ticket.is_deleted == False).count()
        
        status_counts = (
            db.query(Ticket.status, func.count(Ticket.id))
            .filter(Ticket.is_deleted == False)
            .group_by(Ticket.status)
            .all()
        )
        
        priority_counts = (
            db.query(Ticket.priority, func.count(Ticket.id))
            .filter(Ticket.is_deleted == False)
            .group_by(Ticket.priority)
            .all()
        )
        
        return DashboardSummary(
            total_tickets=total_tickets,
            status_breakdown=[StatusBreakdown(status=s.value, count=c) for s, c in status_counts],
            priority_breakdown=[PriorityBreakdown(priority=p.value, count=c) for p, c in priority_counts]
        )
