from datetime import timedelta
from typing import AsyncIterable, Iterable, TypeAlias

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from authx import AuthX, AuthXConfig, TokenPayload
from dishka import Provider, provide, Scope, from_context
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from starlette.requests import Request

from sample_core.models.user import User


AccessTokenPayload: TypeAlias = TokenPayload


openapi_auth_dep = Depends(OAuth2PasswordBearer(tokenUrl="token"))


class RestAPIAdminConfig(BaseModel):
    secret_key: str
    username: str
    password: str


class ConfigSampleRestServer(BaseSettings):
    jwt_secret: str
    jwt_expire_hours: int = 24*2
    admin: RestAPIAdminConfig | None = None

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_prefix="SAMPLE__REST_SERVER__",
        extra="ignore",
    )


class ProviderSampleRestServer(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> ConfigSampleRestServer:
        return ConfigSampleRestServer()

    @provide(scope=Scope.APP)
    def get_admin_config(
            self,
            config: ConfigSampleRestServer,
    ) -> RestAPIAdminConfig:
        if config.admin is None:
            raise RuntimeError("Admin panel configuration not found")

        return config.admin

    @provide(scope=Scope.APP)
    def get_authx(
            self,
            rest_server_config: ConfigSampleRestServer,
    ) -> AuthX:
        authx_config = AuthXConfig(
            JWT_ALGORITHM="HS256",
            JWT_SECRET_KEY=rest_server_config.jwt_secret,
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(
                hours=rest_server_config.jwt_expire_hours,
            ),
        )
        return AuthX(
            config=authx_config,
        )

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_access_token_payload(
            self,
            request: Request,
            security: AuthX,
    ) -> AccessTokenPayload:
        return await security.access_token_required(request)

    @provide(scope=Scope.REQUEST)
    async def get_user(
            self,
            access_token_payload: AccessTokenPayload,
            session: AsyncSession,
    ) -> User:
        user: User = await session.get(User, int(access_token_payload.sub))
        if user is None:
            raise HTTPException(
                401,
                detail="Current user does not exists.",
            )
        return user
