from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, IntegerPk


class ApplicationConfig(Base):
    __tablename__ = "application_config"

    id: Mapped[IntegerPk]

    power_price: Mapped[Decimal]
    power_price_net: Mapped[Decimal]
    comes_into_force_from: Mapped[datetime]
