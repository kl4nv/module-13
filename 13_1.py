import asyncio
import time


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    await asyncio.sleep(1)
    for i in range(1, 6):
        print(f'Силач {name} поднял {i} шар')
        await asyncio.sleep(1 / power)
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Artem', 3))
    task2 = asyncio.create_task(start_strongman('Bob', 4))
    task3 = asyncio.create_task(start_strongman('Karl', 5))
    await task1
    await task2
    await task3

asyncio.run(start_tournament())

