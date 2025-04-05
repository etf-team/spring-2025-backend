from decimal import Decimal

from pydantic import BaseModel


class ResolvedCategoryInfo(BaseModel):
    category_name: str
    total_cost: Decimal


class ResolvedVolumesInfo(BaseModel):
    categories: list[ResolvedCategoryInfo]
