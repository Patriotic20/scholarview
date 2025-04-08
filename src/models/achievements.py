from sqlalchemy import String, Integer, Date, func 
from sqlalchemy.orm import Mapped, mapped_column
from src.core.base import Base 
from datetime import date

class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type_of_achievement: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_award_of_achievement: Mapped[date] = mapped_column(Date, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False) 
    file_path: Mapped[str] = mapped_column(String(255), nullable=False) 

    def __repr__(self) -> str:
        return (f"Achievement(id={self.id!r}, name={self.name!r}, "
                f"type_of_achievement={self.type_of_achievement!r}, "
                f"date_of_award_of_achievement={self.date_of_award_of_achievement!r}, "
                f"file_path={self.file_path!r})") 