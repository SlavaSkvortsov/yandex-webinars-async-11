from typing import Any

from httpx import AsyncClient
from sqlalchemy import select

from my_async_app.db_models import MyTable
from my_async_app.more_functions import mock_me
from my_async_app.db import Session


async def fetch_important_data_from_database() -> list[str]:
    async with Session() as session:
        query_result = await session.execute(select(MyTable.text_field))

    return query_result.scalars().all()


async def fetch_important_data_from_internet() -> Any:
    async with AsyncClient() as client:
        response = await client.get('https://httpbin.org/get')
        return response.json()


async def fetch_important_data_from_async_function() -> int:
    return await mock_me()


class NiceClass:

    async def get_nice_number(self) -> int:
        return await self._mock_me_too()

    async def _mock_me_too(self) -> int:
        return 42
