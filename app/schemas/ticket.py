from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.ticket import TicketType, TicketPriority, TicketStatus
from app.schemas.user import UserOut

class TicketBase(BaseModel):
    ticket_type: TicketType
    title: str
    description: str
    app_module: str
    priority: TicketPriority = TicketPriority.LOW

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    app_module: str | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None
    pic_id: int | None = None

class TicketStatusUpdate(BaseModel):
    status: TicketStatus

class TicketAssign(BaseModel):
    pic_id: int
    priority: TicketPriority | None = None

class TicketOut(TicketBase):
    id: int
    ticket_number: str
    status: TicketStatus
    reporter_id: int
    pic_id: int | None = None
    created_at: datetime
    updated_at: datetime
    
    reporter: UserOut
    pic: UserOut | None = None
    
    model_config = ConfigDict(from_attributes=True)

class TicketHistoryOut(BaseModel):
    id: int
    field_changed: str
    old_value: str | None
    new_value: str | None
    created_at: datetime
    changed_by: UserOut
    
    model_config = ConfigDict(from_attributes=True)

class TicketDetailOut(TicketOut):
    # We will add comments and attachments in subsequent schemas or here
    pass
