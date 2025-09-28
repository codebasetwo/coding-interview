from uuid import uuid4, UUID
from pydantic import EmailStr
from typing import Literal

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column


class User(SQLModel, table = True):
    __tablename__ = 'users'

    uid: UUID = Field(sa_column=Column(pg.UUID, default=uuid4, unique=True, primary_key=True, nullable=False, index=True))
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    middle_name: str = Field(nullable=True)
    full_name: str 
    role: Literal['user', 'admin'] = Field(default='user')
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str = Field(exclude=True)
    user_name: str = Field(unique=True, nullable=False)
    is_verified: bool = Field(default=False)
