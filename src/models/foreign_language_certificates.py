from sqlalchemy import String , Integer , Date
from sqlalchemy.orm  import Mapped , mapped_column
from src.core.base import Base
from datetime import date

class ForeignLanguageCertificate(Base):

    __tablename__ = "foreign_language_certificate"


    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    certificate_type: Mapped[str] = mapped_column(String(50), nullable=False)
    level: Mapped[str] = mapped_column(String(10), nullable=False)
    series_and_number: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_issue: Mapped[date] = mapped_column(Date, nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, language={self.language}, certificate_type={self.certificate_type}, date_of_issue={self.date_of_issue})>"