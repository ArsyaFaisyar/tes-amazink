from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.comment import Comment
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate

class CommentService:
    @staticmethod
    def create_comment(db: Session, ticket_id: int, comment_in: CommentCreate, user: User) -> Comment:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.is_deleted == False).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        comment = Comment(
            ticket_id=ticket_id,
            user_id=user.id,
            content=comment_in.content
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def update_comment(db: Session, comment_id: int, comment_in: CommentUpdate, user: User) -> Comment:
        comment = db.query(Comment).filter(Comment.id == comment_id, Comment.is_deleted == False).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        
        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
            
        comment.content = comment_in.content
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def delete_comment(db: Session, comment_id: int, user: User):
        comment = db.query(Comment).filter(Comment.id == comment_id, Comment.is_deleted == False).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        
        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
            
        comment.soft_delete()
        db.commit()
