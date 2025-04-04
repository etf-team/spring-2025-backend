from __future__ import annotations

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sample_core.models.base import Base, CreatedAt, IntegerPk


class User(Base):
    __tablename__ = "user"

    id: Mapped[IntegerPk]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    full_name: Mapped[str]
    created_at: Mapped[CreatedAt]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"
