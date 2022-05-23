import asyncio
import queue
import threading
import time


async def network_call(wait_for: int):
    await asyncio.sleep(wait_for)
    return wait_for


async def main():
    tasks = []
    for i in range(5):
        tasks.append(asyncio.create_task(network_call(wait_for=i)))

    await asyncio.wait(tasks)

    for task in tasks:
        print(task.result())


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f"Completed at {time.time() - start_time}")
