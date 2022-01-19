from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from dal.models import Base

class DbUserRoleModel(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    users = relationship("DbUserModel", back_populates="role")

class DbUserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("role.id"))

    role = relationship("DbUserRoleModel", back_populates="users")
