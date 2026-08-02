import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class UserRole(str, enum.Enum):
    USER = "USER"
    PM_IT = "PM_IT"
    STAFF_IT = "STAFF_IT"

class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)

    # Relationships
    reported_tickets = relationship("Ticket", back_populates="reporter", foreign_keys="[Ticket.reporter_id]")
    assigned_tickets = relationship("Ticket", back_populates="pic", foreign_keys="[Ticket.pic_id]")
    comments = relationship("Comment", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user")
