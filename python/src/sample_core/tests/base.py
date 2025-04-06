from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock

import pytest
import pytest_asyncio
from dishka import make_async_container
from sqlalchemy.ext.asyncio import AsyncSession

from sample_core.models import (
    User,
)
from sample_rest_server.dishka import ProviderSampleRestServer


@pytest_asyncio.fixture
async def app_container():
    async_container = make_async_container(ProviderSampleRestServer())
    async with async_container() as container:
        yield container


@pytest_asyncio.fixture
async def session_container(
        app_container
):
    async with app_container() as container:
        yield container


@pytest_asyncio.fixture
async def request_container(
        session_container,
):
    async with session_container() as container:
        yield container


@pytest_asyncio.fixture
async def session(
        request_container,
):
    async with await request_container.get(AsyncSession) as session:
        session.commit = Mock(side_effect=NotImplementedError)
        yield session
        await session.rollback()


@pytest.mark.asyncio
async def test_sample(
        request_container,
        session: AsyncSession,
):
    pass
