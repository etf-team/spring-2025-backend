from datetime import date

from sqlalchemy import Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, IntegerPk


class PowerHoursAtsRecord(Base):
    __tablename__ = "power_hours_ats_record"

    id: Mapped[IntegerPk]

    date: Mapped[date]
    hour: Mapped[int]

    __table_args__ = (
        UniqueConstraint("date"),
    )

    def __str__(self):
        return f"{self.date} <{self.hour}>"
