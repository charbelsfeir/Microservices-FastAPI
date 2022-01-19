from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dal.models import user_model
from routers.models import models
from sqlalchemy.orm import Session
from hashlib import sha256
from passlib.context import CryptContext
from typing import Optional, MutableMapping, Union, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import os
from time import sleep

sleep(10)

PWD_CONTEXT = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://{}:{}@{}/{}".format(
    "root", os.environ["MYSQL_ROOT_PASSWORD"], os.environ["MYSQL_IP_ADDRESS"], os.environ["MYSQL_DATABASE"])
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def insert_default_roles(db: Session):
    role = user_model.DbUserRoleModel(name="buyer")
    db.add(role)
    role = user_model.DbUserRoleModel(name="seller")
    db.add(role)
    db.commit()


def create_user(db: Session, user: models.UserCreateModel):
    hashed_password = get_password_hash(user.password)
    # hashed_password = sha256(user.password.encode()).hexdigest()
    user = user_model.DbUserModel(first_name=user.first_name, last_name=user.last_name,
                                  email=user.email, hashed_password=hashed_password, role_id=user.role.role_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    user_role = models.UserRole(role_id=user.role_id, name=user.role.name)
    return models.User(id=user.id, is_active=user.is_active, is_deleted=user.is_deleted, first_name=user.first_name, last_name=user.last_name, email=user.email, role=user_role)


def get_user_by_id(db: Session, id: int):
    user = db.query(user_model.DbUserModel).filter(
        user_model.DbUserModel.id == id).first()
    user_role = models.UserRole(role_id=user.role_id, name=user.role.name)
    return models.User(id=user.id, is_active=user.is_active, is_deleted=user.is_deleted, first_name=user.first_name, last_name=user.last_name, email=user.email, role=user_role)


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.DbUserModel).filter(user_model.DbUserModel.email == email).first()


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[models.User]:
    user = db.query(user_model.DbUserModel).filter(
        user_model.DbUserModel.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):  # 1
        return None
    user_role = models.UserRole(role_id=user.role_id, name=user.role.name)
    return models.User(id=user.id, is_active=user.is_active, is_deleted=user.is_deleted, first_name=user.first_name, last_name=user.last_name, email=user.email, role=user_role)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def create_access_token(*, sub: str) -> str:  # 2
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=3),  # 3
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire  # 4
    payload["iat"] = datetime.utcnow()  # 5
    payload["sub"] = str(sub)  # 6

    # 8
    return jwt.encode(payload, "askjfafew124@41@&9%!asf)(", algorithm="HS256")
