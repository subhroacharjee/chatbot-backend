from sqlalchemy import Column, DateTime, Integer, String, func
from app.core.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, autoincrement=True, index=True, nullable=False
    )
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    created_at = Column(DateTime(True), nullable=False, default=func.now())
