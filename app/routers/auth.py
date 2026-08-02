from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.auth import AuthService
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import Token,UserLogin
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Annotated[Session, Depends(get_db)]):
    return AuthService.register(db, user_in)

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Annotated[Session, Depends(get_db)]):  # Menggunakan UserLogin JSON
    user = AuthService.authenticate(db, user_in.email, user_in.password)
    return AuthService.create_token(user.id)

@router.get("/me", response_model=UserOut)
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
