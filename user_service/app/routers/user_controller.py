import sys
import os
import pathlib
import shutil
from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from routers.models.models import UserCreateModel, User
from datetime import datetime
from dal.db_helper import SessionLocal
from sqlalchemy.orm import Session
from dal import db_helper
from jose import jwt, JWTError


router = APIRouter()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/api/create_roles', tags=["User"])
def create_roles(db: Session = Depends(get_db)):
    db_helper.insert_default_roles(db)


@router.post('/api/create', tags=["User"])
def create_user(user: UserCreateModel, db: Session = Depends(get_db)):
    db_user = db_helper.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_helper.create_user(db=db, user=user)
    # result = "Hello and welcome to microservices course"
    # return result


@router.get('/api/profile', tags=["User"])
def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(db_helper.oauth2_scheme)
) -> User:
    # skipping for simplicity...
    try:
        payload = jwt.decode(
            token,
            "askjfafew124@41@&9%!asf)(",
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
        user_id: int = int(payload.get("sub").split(":")[0])
    except JWTError:
        raise credentials_exception
    user = db_helper.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


@router.post("/api/v1/auth/login", tags=["User"])
def login(
    # 1
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = db_helper.authenticate(
        email=form_data.username, password=form_data.password, db=db)  # 2
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")  # 3

    return {
        # 4
        "access_token": db_helper.create_access_token(sub="{0}:{1}".format(user.id, user.role.role_id)),
        "token_type": "bearer",
    }
