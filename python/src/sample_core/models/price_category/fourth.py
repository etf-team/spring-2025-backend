from sqlalchemy.orm import Mapped

from .base import BasePriceCategory, IntegerPkBaseFk
from ..client_case import ClientCase


class PriceCategoryFourth(BasePriceCategory):
    __tablename__ = "price_category_forth"

    id: Mapped[IntegerPkBaseFk]

    def is_appropriate_for_case(self, case: ClientCase) -> bool:
        return False

    __mapper_args__ = {
        "polymorphic_identity": "forth",
    }
