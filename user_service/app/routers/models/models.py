from pydantic import BaseModel
from typing import List

class UserRole(BaseModel):
    role_id: int
    name: str
    class Config:
        orm_mode: True

class UserCreateModel(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: UserRole
    class Config:
        orm_mode: True

class User(BaseModel):
    id: int
    is_active: bool
    is_deleted: bool
    first_name: str
    last_name: str
    email: str
    role: UserRole
