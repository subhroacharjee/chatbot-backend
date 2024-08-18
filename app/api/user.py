from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import response
from app.core.db.database import get_db
from app.internal.auth import auth, schemas


user_router = APIRouter(prefix="/auth")


@user_router.post("/signup")
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return response(auth.register(db, user))


@user_router.post("/login")
async def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return response(auth.login(db, user))


@user_router.post("/token")
async def oauth2_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = schemas.UserCreate(username=form_data.username, password=form_data.password)
    login_data = auth.login(db, user)
    return {"access_token": login_data.access_token, "token_type": "bearer"}
