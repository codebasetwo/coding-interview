from datetime import datetime
from uuid import uuid4, UUID
from pydantic import EmailStr

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column


class User(SQLModel, table = True):
    __tablename__ = 'users'

    uid: UUID = Field(sa_column=Column(pg.UUID, default=uuid4, unique=True, primary_key=True, nullable=False, index=True))
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    middle_name: str = Field(nullable=True)
    full_name: str 
    role: str = Field(default='user')
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str = Field(exclude=True)
    user_name: str = Field(unique=True, nullable=False)
    is_verified: bool = Field(default=False)


class Challenge(SQLModel, table = True):
    __tablename__ = 'challenges'

    id: int =  Field(primary_key=True)
    difficulty: str = Field(nullable=False)
    date_created: datetime =  Field(default=datetime.now)
    created_by: str = Field(nullable=False)
    title: str = Field(nullable=False)
    options: str =  Field(nullable=False)
    correct_answer_id: str =  Field(nullable=False)
    explanation: str =  Field(nullable=False)


class ChallengeQuota(SQLModel, table = True):
    __tablename__ = 'challenge_quotas'

    id: int =  Field(primary_key=True)
    user_id: str =  Field(nullable=False, unique=True)
    quota_remaining: int=  Field(nullable=False, default=50)
    last_reset_date:datetime =  Field(default=datetime.now)
