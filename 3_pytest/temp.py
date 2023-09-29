import asyncio

number = 0


async def increment(lock: asyncio.Lock):
    global number
    async with lock:
        if number == 0:
            await asyncio.sleep(1)
            number += 1
    await asyncio.sleep(1)


async def temp():
    lock = asyncio.Lock()
    await asyncio.gather(increment(lock), increment(lock), increment(lock))


if __name__ == '__main__':
    asyncio.run(temp())
    print(number)
