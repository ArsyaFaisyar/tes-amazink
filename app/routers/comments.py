from typing import Annotated,Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.comment import CommentService
from app.schemas.comment import CommentCreate, CommentOut, CommentUpdate
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CommentOut)
def create_comment(
    ticket_id: int,
    content: Annotated[str, Form(...)],                # Ambil teks dari Form-Data
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    image: Optional[UploadFile] = File(None)            # Upload file opsional
):
    return CommentService.create_comment(
        db=db,
        ticket_id=ticket_id,
        content=content,
        user=current_user,
        image=image
    )

@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int,
    content: Annotated[Optional[str], Form()] = None,
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    image: Optional[UploadFile] = File(None)
):
    return CommentService.update_comment(
        db=db,
        comment_id=comment_id,
        content=content,
        user=current_user,
        image=image
    )

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    CommentService.delete_comment(db, comment_id, current_user)
    return {"message": "Comment deleted successfully"}
