from datetime import datetime

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, IntegerPk


class PowerHoursNet(Base):
    __tablename__ = "power_hours_net"

    id: Mapped[IntegerPk]

    include_hours: Mapped[list[str]] = mapped_column(ARRAY(String))

    comes_info_force_from: Mapped[datetime]
