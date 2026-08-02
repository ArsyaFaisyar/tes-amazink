import enum
from datetime import datetime
from sqlalchemy import String, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class HistoryField(str, enum.Enum):
    STATUS = "STATUS"
    PIC = "PIC"
    PRIORITY = "PRIORITY"

class TicketHistory(Base):
    __tablename__ = "ticket_histories"

    # Override id to not have it from Base if needed, but Base has it.
    # We'll just use Base.id
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    changed_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    field_changed: Mapped[HistoryField] = mapped_column(Enum(HistoryField))
    old_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    new_value: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    ticket = relationship("Ticket", back_populates="histories")
    changed_by = relationship("User")
