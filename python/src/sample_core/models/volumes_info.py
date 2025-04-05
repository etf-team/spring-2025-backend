from datetime import datetime
from io import BytesIO
from typing import Self

import pandas as pd
from dataclasses import dataclass

import datetime


@dataclass
class VolumeInfoEntry:
    datetime: datetime


@dataclass
class VolumesInfo:
    entries: list[VolumeInfoEntry]

    @classmethod
    def from_xlsx(cls, data: bytes) -> Self:
        result = pd.read_excel(data)
        # todo:
        return None
