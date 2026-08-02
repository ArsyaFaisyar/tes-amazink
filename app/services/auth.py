from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import Token

class AuthService:
    @staticmethod
    def register(db: Session, user_in: UserCreate) -> User:
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        db_user = User(
            email=user_in.email,
            name=user_in.name,
            password_hash=get_password_hash(user_in.password),
            role=user_in.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User:
        user = db.query(User).filter(User.email == email, User.is_deleted == False).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    @staticmethod
    def create_token(user_id: int) -> Token:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(user_id, expires_delta=access_token_expires),
            token_type="bearer"
        )
