from sqlalchemy import String , Integer , Date
from sqlalchemy.orm import Mapped , mapped_column
from src.core.base import Base
from datetime import date

class ScientificResearchWork(Base):

    __tablename__ = "scientific_research_works"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    scientific_research_form: Mapped[str] = mapped_column(String, nullable=False)
    date_of_publication: Mapped[date] = mapped_column(Date, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, name={self.name}, date_of_publication={self.date_of_publication})>"