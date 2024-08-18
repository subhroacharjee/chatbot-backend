from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CurrentUser(UserBase):
    id: int


class AccessTokenBase(BaseModel):
    access_token: str
    user: UserBase
