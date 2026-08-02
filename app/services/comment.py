from sqlalchemy.orm import Session
import os
import uuid
from fastapi import HTTPException, UploadFile, status
from app.models.comment import Comment
from app.models.ticket import Ticket
from app.models.user import User
from typing import Optional
from app.schemas.comment import CommentCreate, CommentUpdate

class CommentService:
    @staticmethod
    def create_comment(db: Session,content : str, ticket_id: int, user: User,image: Optional[UploadFile] = None,) -> Comment:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.is_deleted == False).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        image_url = None

        if image:
            # Validasi ekstensi/tipe file
            allowed_types = ["image/jpeg", "image/png", "image/webp"]
            if image.content_type not in allowed_types:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Format file harus JPEG, PNG, atau WEBP"
                )
            
            # Buat folder penyimpanan jika belum ada
            upload_dir = "uploads/comments"
            os.makedirs(upload_dir, exist_ok=True)

            # Buat nama unik file agar tidak bentrok
            file_extension = os.path.splitext(image.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)

            # Simpan file ke server
            with open(file_path, "wb") as buffer:
                buffer.write(image.file.read())

            # URL path statis yang nanti bisa diakses dari browser/client
            image_url = f"/static/comments/{unique_filename}"
        
        comment = Comment(
            ticket_id=ticket_id,
            user_id=user.id,
            content=content,
            image_url=image_url
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def update_comment(db: Session, comment_id: int, content: Optional[str], user: User,image: Optional[UploadFile] = None) -> Comment:
        comment = db.query(Comment).filter(Comment.id == comment_id, Comment.is_deleted == False).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        
        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
        
        
        if content is not None:
            comment.content = content

        # 4. Jika user mengunggah gambar baru
        if image:
            # Validasi tipe file
            allowed_types = ["image/jpeg", "image/png", "image/webp"]
            if image.content_type not in allowed_types:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Format file harus JPEG, PNG, atau WEBP"
                )

            # Hapus gambar lama dari penyimpanan lokal jika ada
            if comment.image_url:
                old_filename = os.path.basename(comment.image_url)
                old_file_path = os.path.join("uploads/comments", old_filename)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Simpan gambar baru ke folder uploads/comments
            upload_dir = "uploads/comments"
            os.makedirs(upload_dir, exist_ok=True)

            file_extension = os.path.splitext(image.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)

            with open(file_path, "wb") as buffer:
                buffer.write(image.file.read())

            # Update path image_url di DB
            comment.image_url = f"/static/comments/{unique_filename}"
            
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
