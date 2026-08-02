import enum
from datetime import datetime
from sqlalchemy import String, Enum, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class TicketType(str, enum.Enum):
    BUG = "BUG"
    FEATURE_REQUEST = "FEATURE_REQUEST"

class TicketPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class TicketStatus(str, enum.Enum):
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    QA = "QA"
    DONE = "DONE"

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    ticket_type: Mapped[TicketType] = mapped_column(Enum(TicketType))
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    app_module: Mapped[str] = mapped_column(String(100))
    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority), default=TicketPriority.LOW)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.OPEN)
    pic_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    # Relationships
    reporter = relationship("User", back_populates="reported_tickets", foreign_keys=[reporter_id])
    pic = relationship("User", back_populates="assigned_tickets", foreign_keys=[pic_id])
    histories = relationship("TicketHistory", back_populates="ticket")
    comments = relationship("Comment", back_populates="ticket")
    attachments = relationship("Attachment", back_populates="ticket")
