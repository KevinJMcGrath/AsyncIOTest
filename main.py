import asyncio
import random



async def one_sec():
    while True:
        await asyncio.sleep(1)
        print('beep')


async def five_sec(async_queue):
    while True:
        await asyncio.sleep(5)
        print('\tboop')

        for _ in range(3):
            p = {
                "name": "five_sec",
                "timer": random.randint(1, 5)
            }
            async_queue.put_nowait(p)


async def ten_sec(async_queue):
    while True:
        await asyncio.sleep(10)
        print('\t\tbzzzt')

        for _ in range(3):
            p = {
                "name": "ten_sec",
                "timer": random.randint(5, 10)
            }
            async_queue.put_nowait(p)


async def gather_coroutines(async_queue):
    await asyncio.gather(
        one_sec(),
        five_sec(async_queue),
        ten_sec(async_queue),
        queue_consumer(async_queue)
        #*queue_task_generator(async_queue)
    )


async def queue_consumer(async_queue):
    while True:
        sleep_obj = await async_queue.get()

        sleep_name = sleep_obj['name']
        sleep_timer = sleep_obj['timer']

        await asyncio.sleep(sleep_timer)

        async_queue.task_done()

        # sec = random.randint(1, 15)

        print(f'*** Queued process {sleep_name} slept for: {sleep_timer} ***')


# def queue_task_generator(async_queue):
#     tasks = []
#     for i in range(3):
#         task = asyncio.create_task(queue_worker(async_queue))
#         tasks.append(task)
#
#     return tasks

def run_main():
    background_queue = asyncio.Queue()

    #queue_task_generator(background_queue)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather_coroutines(background_queue))

if __name__ == '__main__':
    run_main()