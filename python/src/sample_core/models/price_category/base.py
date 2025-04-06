from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import TypeAlias, Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from sample_core.models.client_case import ClientCase
from sample_core.models.client_case_resolved import ClientCaseResolvedCategory

from ..base import Base, IntegerPk


class BasePriceCategory(Base):
    __tablename__ = "base_price_category"

    id: Mapped[IntegerPk]
    type: Mapped[str]
    name: Mapped[str]
    accepted_at: Mapped[datetime]

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "base_price_category",
    }

    @abstractmethod
    def is_appropriate_for_case(self, case: ClientCase) -> bool:
        pass

    @abstractmethod
    def resolve_case(self, case: ClientCase) -> ClientCaseResolvedCategory:
        pass


IntegerPkBaseFk: TypeAlias = Annotated[
    int,
    mapped_column(ForeignKey("base_price_category.id"), primary_key=True, autoincrement=True),
]
RubblesAmount: TypeAlias = Annotated[
    Decimal,
    mapped_column()
]
