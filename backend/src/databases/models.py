from datetime import datetime
from uuid import uuid4, UUID
from typing import List, Optional

from pydantic import EmailStr

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import ForeignKey
from sqlmodel import SQLModel, Field, Column, Relationship


class User(SQLModel, table=True):
    __tablename__ = 'users'

    uid: UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), default=uuid4, unique=True, primary_key=True, index=True))
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    middle_name: str | None = Field(default=None)
    full_name: str | None = Field(default=None)
    role: str = Field(default='user')
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str = Field(exclude=True)
    user_name: str = Field(unique=True, nullable=False)
    is_verified: bool = Field(default=False)

    # Relationships
    challenges: List["Challenge"] = Relationship(back_populates="creator")
    quota: Optional["ChallengeQuota"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})


class Challenge(SQLModel, table=True):
    __tablename__ = 'challenges'

    id: int = Field(primary_key=True)
    difficulty: str = Field(nullable=False)
    date_created: datetime = Field(default=datetime.now)
    created_by: UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("users.uid")),)
    title: str = Field(nullable=False)
    options: str = Field(nullable=False)
    correct_answer_id: str = Field(nullable=False)
    explanation: str = Field(nullable=False)

    # Relationship to the user who created the challenge
    creator: Optional[User] = Relationship(back_populates="challenges")


class ChallengeQuota(SQLModel, table=True):
    __tablename__ = 'challenge_quotas'

    id: int = Field(primary_key=True)
    user_id: UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("users.uid"), unique=True,) )
    quota_remaining: int = Field(nullable=False, default=5)
    last_reset_date: datetime = Field(default=datetime.now)

    # Relationship back to user (one-to-one)
    user: Optional[User] = Relationship(back_populates="quota")
