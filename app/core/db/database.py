import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import DATABASE_URI_ENV_KEY


load_dotenv(".env")

Base = declarative_base()

engine = create_engine(
    os.environ[DATABASE_URI_ENV_KEY],
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
