from enum import StrEnum


class VoltageCategoryEnum(StrEnum):
    BH = "BH"
    CH1 = "CH1"
    CH11 = "CH11"
    HH = "HH"

    @classmethod
    def from_any_lang(cls, val: str):
        ru_to_en = {
            "Н": "H",
            "В": "B",
            "С": "C",
        }
        res = ""
        for i in val:
            res += ru_to_en.get(i, i)
        return cls(res)
