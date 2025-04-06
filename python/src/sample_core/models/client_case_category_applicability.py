from pydantic import BaseModel


class ClientCaseCategoryApplicability(BaseModel):
    is_applicable_power_capacity: bool
    power_capacity_change_recommendation: float
