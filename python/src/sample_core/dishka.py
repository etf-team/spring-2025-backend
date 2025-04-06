from typing import AsyncIterable, Iterable

from dishka import Provider, provide, Scope
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import Session


class ConfigPostgres(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str

    def get_sqlalchemy_url(self, driver: str):
        return "postgresql+{}://{}:{}@{}:{}/{}".format(
            driver,
            self.user,
            self.password,
            self.host,
            self.port,
            self.database,
        )


class ConfigSampleCoreProduction(BaseSettings):
    postgres: ConfigPostgres = None

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_prefix="SAMPLE__CORE__",
        extra="ignore",
    )


class ProviderSampleCore(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> ConfigSampleCoreProduction:
        return ConfigSampleCoreProduction()

    @provide(scope=Scope.APP)
    def get_postgres_config(
            self,
            config: ConfigSampleCoreProduction,
    ) -> ConfigPostgres:
        if config.postgres is None:
            raise RuntimeError("Postgres configuration not found")

        return config.postgres

    @provide(scope=Scope.APP)
    async def get_async_engine(
            self,
            postgres_config: ConfigPostgres,
    ) -> AsyncEngine:
        return create_async_engine(
            postgres_config.get_sqlalchemy_url("asyncpg"),
        )

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
            self,
            engine: AsyncEngine,
    ) -> AsyncIterable[AsyncSession]:
        async with AsyncSession(
            bind=engine,
            expire_on_commit=False,
        ) as session:
            yield session

    @provide(scope=Scope.APP)
    def get_sync_engine(
            self,
            postgres_config: ConfigPostgres,
    ) -> Engine:
        return create_engine(
            postgres_config.get_sqlalchemy_url("psycopg"),
        )

    @provide(scope=Scope.REQUEST)
    def get_sync_session(
            self,
            engine: Engine
    ) -> Iterable[Session]:
        with Session(
                bind=engine,
                expire_on_commit=False,
        ) as session:
            yield session
