from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from mail.send_mail import send_simple_message
from utils.colorText import colorText
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from typing import Optional
from datetime import timedelta
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime
from core.config import settings
from database import get_db
from models.models import User as DBUser
from auth.authentication import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    pwd_context
)
from auth.schemas import UserCreate, Token, UserSchema as AuthUserSchema, ForgotPasswordRequest, ResetPasswordRequest, UserResponse

router = APIRouter(
    prefix="/auth", # All paths in this router will start with /auth
    tags=["Authentication"],
)

@router.post("/register", response_model=AuthUserSchema)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user_by_username = db.query(DBUser).filter(DBUser.username == user.username).first()
    if db_user_by_username:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Username already registered")

    db_user_by_email = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(user.password)

    new_user = DBUser(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
    ):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=AuthUserSchema)
async def read_users_me(current_user: DBUser = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.email == request.email).first()

    # Security: not reveal if email exists or not
    if user:
        expires = datetime.now() + timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)
        reset_token_data = {"sub": user.email, "exp": expires, "purpose": "password_reset" }
        reset_token = jwt.encode(reset_token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        user.reset_password_token = reset_token
        user.reset_password_expires_at = expires
        db.add(user)
        db.commit()

        reset_link = f"{settings.FRONTEND_URL}/auth/reset-password?token={reset_token}"
        background_tasks.add_task(send_simple_message, user.email, "Réinitialisation de votre mot de passe", f"Cliquez sur ce lien pour réinitialiser votre mot de passe: {reset_link}")

    return print(colorText("Si l'email est enregistré, un lien de réinitialisation a été envoyé.", "vert_fonce"))

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        email: Optional[str] = payload.get("sub")
        purpose: Optional[str] = payload.get("purpose")

        if email is None or purpose != "password_reset":
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Jeton invalide")
        
        expires_at = datetime.fromtimestamp(payload["exp"])
        if expires_at < datetime.now():
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Jeton expiré")

    except jwt.JWTError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Jeton invalide")

    user = db.query(DBUser).filter(DBUser.email == email).first()

    # check the token in db matches
    if not user or user.reset_password_token != request.token or user.reset_password_expires_at < datetime.now():
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Jeton invalide ou expiré")
    
    user.hashed_password = get_password_hash(request.new_password)
    user.reset_password_token = None
    user.reset_password_expires_at = None
    db.add(user)
    db.commit()

    return print(colorText("Mot de passe réinitialisé avec succès.", "vert_fonce"))


def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> UserResponse | None:
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        return None
    return UserResponse.model_validate(db_user)

