from __future__ import annotations

from datetime import datetime

from sample_rest_api.dtos.base import BaseDTO


class UserDTO(BaseDTO):
    id: int
    full_name: str
    email: str


class UserFullDTO(UserDTO):
    pass
