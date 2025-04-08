from sqlalchemy import Integer , String 
from sqlalchemy.orm import Mapped , mapped_column
from src.core.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, username={self.username})>"
