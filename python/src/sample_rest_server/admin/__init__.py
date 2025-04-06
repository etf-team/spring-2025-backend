from datetime import timedelta

from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine

from dishka import AsyncContainer
from fastapi import FastAPI

from sample_rest_server.admin.auth_backend import AdminAuthBackend
from sample_rest_server.admin import views
from sample_rest_server.dishka import RestAPIAdminConfig


async def setup_admin(container: AsyncContainer, app: FastAPI) -> Admin:
    engine = await container.get(AsyncEngine)
    config: RestAPIAdminConfig = await container.get(RestAPIAdminConfig)

    admin = Admin(
        app,
        engine=engine,
        authentication_backend=AdminAuthBackend(
            secret_key=config.secret_key,
            username=config.username,
            password=config.password,
            login_duration=timedelta(days=3),
        )
    )

    # admin.add_view(views.UserAdmin)
    admin.add_view(views.ApplicationConfigAdmin)
    admin.add_view(views.CategoryPriceInfoFileAdmin)
    admin.add_view(views.PowerHoursNetAdmin)
    admin.add_view(views.PowerHoursAtsRecordAdmin)

    return admin
