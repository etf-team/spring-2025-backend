from decimal import Decimal

from sqlalchemy.orm import Mapped

from sample_core.models.client_case import ClientCase
from sample_core.models.client_case_resolved import ClientCaseResolvedCategory

from .base import BasePriceCategory, IntegerPkBaseFk


class PriceCategoryFirst(BasePriceCategory):
    __tablename__ = "price_category_first"

    id: Mapped[IntegerPkBaseFk]

    middle_price: Mapped[float]
    electricity_price: Mapped[Decimal]

    __mapper_args__ = {
        "polymorphic_identity": "first",
    }

    def is_appropriate_for_case(
            self,
            case: ClientCase,
    ) -> bool:
        return case.volumes_info.max_power_capacity_kvt < 670

    def resolve_case(
            self,
            case: ClientCase,
    ) -> ClientCaseResolvedCategory:
        return ClientCaseResolvedCategory(
            category_name=self.name,
            total_cost=case.volumes_info.total_power_capacity_kvt
                       * self.general_price,
        )
