import asyncio
import random
import time

import uvicorn
from fastapi import Depends, FastAPI
from redis import asyncio as redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db import Session

app = FastAPI()


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


cache = {}


async def calc(foo: int) -> int:
    client = redis.Redis()
    if result := await client.get(str(foo)):
        return result

    time.sleep(1)
    result = foo * 2
    await client.set(str(foo), result)
    return result


@app.get('/')
async def root() -> int:
    return await calc(random.randint(1, 10))


if __name__ == '__main__':
    uvicorn.run('main:app', workers=1)
