from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_token, hash_password, verify_password
from app.db import get_db
from app.models import User
from app.schemas import LoginRequest, TokenResponse, UserCreate, UserProfile

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email già registrata")
    
    user = User(
        nome=payload.username,  # Map username to nome
        email=payload.email,
        password_hash=hash_password(payload.password),
        telefono=getattr(payload, 'telefono', None),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create token and return with user info
    access_token = create_token(str(user.ID), timedelta(minutes=settings.access_token_exp_minutes))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "ID": user.ID,
            "nome": user.nome,
            "email": user.email,
        }
    }


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenziali non valide")
    
    access_token = create_token(str(user.ID), timedelta(minutes=settings.access_token_exp_minutes))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "ID": user.ID,
            "nome": user.nome,
            "email": user.email,
        }
    }
