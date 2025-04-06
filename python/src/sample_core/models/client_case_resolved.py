from decimal import Decimal

from pydantic import BaseModel

from sample_core.models.client_case_category_applicability import (
    ClientCaseCategoryApplicability,
)
from sample_core.services.docs_parser import PriceCategoryTypeEnum


class ClientCaseResolvedCategory(BaseModel):
    applicability: ClientCaseCategoryApplicability
    category_type: PriceCategoryTypeEnum
    total_cost: Decimal


class ClientCaseResolved(BaseModel):
    categories: list[ClientCaseResolvedCategory]
