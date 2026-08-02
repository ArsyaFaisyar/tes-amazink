from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.user import UserOut

class AttachmentOut(BaseModel):
    id: int
    file_name: str
    file_type: str
    file_size: int
    uploaded_by_id: int
    created_at: datetime
    uploaded_by: UserOut
    
    model_config = ConfigDict(from_attributes=True)
