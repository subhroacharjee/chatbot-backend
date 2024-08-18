from sqlalchemy.orm import Session

from app.core.config import throw_error
from app.core.security import create_access_token, hash_password, verify_password
from app.internal.auth import model, schemas


def create_access_token_for_user(user: schemas.User):
    user_dict = user.model_dump()
    if user_dict.get("created_at"):
        user_dict.pop("created_at")
    access_token = create_access_token(user_dict)
    return schemas.AccessTokenBase(access_token=access_token, user=user)


def create_user(db: Session, data: schemas.UserCreate):
    hashed_password = hash_password(data.password)
    db_user = model.Users(username=data.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.User.model_validate(db_user)


def get_user(db: Session, username: str):
    return db.query(model.Users).filter(model.Users.username == username).first()


def login(db: Session, data: schemas.UserCreate):
    user = get_user(db, data.username)
    if user is not None:
        if verify_password(data.password, user.password):
            return create_access_token_for_user(schemas.User.model_validate(user))
    return throw_error(400, "invalid username or password")


def register(db: Session, data: schemas.UserCreate):
    user = get_user(db, data.username)
    if user is None:
        return create_access_token_for_user(create_user(db, data))

    return throw_error(400, "username already exists")
