from sqladmin import ModelView

from sample_core.models.user import (
    User,
)


class UserAdmin(ModelView, model=User):
    column_list = [
        "id",
        "email",
        "phone_number",
        "full_name",
        "description",
        "created_at",
    ]
