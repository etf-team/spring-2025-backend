from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sample_core.models.application_config import ApplicationConfig


class ServiceApplicationConfig:
    def __init__(
            self,
            orm_session: AsyncSession,
    ):
        self.orm_session = orm_session

    async def get_config(self):
        config = select(ApplicationConfig)
