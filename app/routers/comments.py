from typing import Annotated
from fastapi import APIRouter, Depends
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
    comment_in: CommentCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    return CommentService.create_comment(db, ticket_id, comment_in, current_user)

@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    return CommentService.update_comment(db, comment_id, comment_in, current_user)

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    CommentService.delete_comment(db, comment_id, current_user)
    return {"message": "Comment deleted successfully"}
