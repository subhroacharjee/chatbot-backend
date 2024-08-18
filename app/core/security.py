from datetime import datetime, timedelta
import os
from passlib.context import CryptContext
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain: str, hash):
    return pwd_context.verify(plain, hash)


def create_access_token(data: dict, expires_data: timedelta | None = None):
    to_encode = data.copy()

    if expires_data:
        expire = datetime.now() + expires_data
    else:
        expire = datetime.now() + timedelta(minutes=90)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, os.environ["SECRET_KEY"], os.environ["JWT_ALGORITHM"])


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token, os.environ["SECRET_KEY"], algorithms=[os.environ["JWT_ALGORITHM"]]
    )
