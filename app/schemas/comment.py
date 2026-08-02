from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
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
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user: UserOut
    
    model_config = ConfigDict(from_attributes=True)
