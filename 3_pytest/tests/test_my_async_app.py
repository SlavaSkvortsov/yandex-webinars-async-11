from unittest.mock import AsyncMock, patch

import pytest
import respx
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from my_async_app.db_models import MyTable
from my_async_app.some_functions import (
    NiceClass, fetch_important_data_from_async_function,
    fetch_important_data_from_database, fetch_important_data_from_internet,
)


@pytest.mark.asyncio()
@patch('my_async_app.some_functions.mock_me')
async def test_fetch_from_async_function(mocked_function: AsyncMock) -> None:
    mocked_function.return_value = 1
    assert await fetch_important_data_from_async_function() == 1
    mocked_function.assert_awaited_once()


@pytest.mark.asyncio()
@patch.object(NiceClass, '_mock_me_too', return_value=1)
async def test_fetch_from_a_nice_class(mocked_function: AsyncMock) -> None:
    nice_class = NiceClass()

    assert await nice_class.get_nice_number() == 1

    mocked_function.assert_awaited_once()


@respx.mock
@pytest.mark.asyncio()
async def test_fetch_from_internet() -> None:
    respx.get('https://httpbin.org/get').respond(json={'test': 'test'})
    result = await fetch_important_data_from_internet()

    assert result == {'test': 'test'}
    assert respx.calls.call_count == 1


@pytest.mark.asyncio()
@patch('my_async_app.fastapi_app.mock_me')
async def test_fastapi_app(mocked_function: AsyncMock, client: AsyncClient) -> None:
    mocked_function.return_value = 1

    response = await client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.text == '1'


@pytest.mark.asyncio()
async def test_fetch_from_db(session: AsyncSession) -> None:
    session.add(MyTable(text_field='test'))
    await session.commit()

    result = await fetch_important_data_from_database()

    assert result == ['test']
