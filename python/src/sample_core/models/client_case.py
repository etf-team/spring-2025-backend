from datetime import datetime, timedelta, date, time

from pydantic import BaseModel, computed_field

from sample_core.models.voltage_category import VoltageCategoryEnum


class PowerConsumptionEntry(BaseModel):
    date: date | None
    day: int
    time: time
    duration: timedelta
    amount_kwt: float

    @computed_field
    @property
    def amount_mwt(self) -> float:
        return self.amount_kwt / 1000


class ClientCase(BaseModel):
    is_transmission_included: bool
    max_power_capacity_kwt: float
    voltage_category: VoltageCategoryEnum
    power_consumption_entries: list[PowerConsumptionEntry]

    @computed_field
    @property
    def total_power_capacity_mwt(self) -> float:
        return (sum(i.amount_kwt for i in self.power_consumption_entries)
                / 1000)
