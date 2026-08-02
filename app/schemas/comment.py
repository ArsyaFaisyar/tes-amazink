from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.user import UserOut

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    ticket_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserOut
    
    model_config = ConfigDict(from_attributes=True)
