# ============================================================
#  CHAPTER 7 — ASYNCIO
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS ASYNCIO?
# ------------------------------------------------------------
# Asyncio is Python's built-in library for writing CONCURRENT
# code using a single thread with cooperative multitasking.
#
# Threading: multiple threads, OS switches between them
# Asyncio:   single thread, YOU decide when to switch tasks
#            by using 'await' at natural pause points
#
# How it works:
#   → One EVENT LOOP runs in the background
#   → Tasks run until they hit an 'await' (a waiting point)
#   → While one task waits, the event loop runs another task
#   → When the wait is done, the first task resumes
#
# Threading vs Asyncio for I/O-bound work:
#   Threading  → OS switches threads (preemptive), more overhead
#   Asyncio    → you yield control with await (cooperative),
#                lower overhead, handles thousands of connections
#
# Best for:
#   → Web servers handling many simultaneous connections
#   → Fetching many URLs at once (aiohttp)
#   → Database queries (asyncpg, aiosqlite)
#   → WebSockets, chat servers, real-time apps
#
# NOT great for:
#   → CPU-bound tasks (still single thread — use multiprocessing)


# ------------------------------------------------------------
# 2. THE KEY KEYWORDS: async and await
# ------------------------------------------------------------
# async def  → defines a COROUTINE function
#              calling it returns a coroutine object (doesn't run yet!)
#
# await      → pause THIS coroutine until the awaited thing finishes
#              RELEASES control to the event loop while waiting
#              can ONLY be used inside async def functions
#
# Coroutine  → a function that can be paused and resumed

import asyncio
import time

# Regular function — runs to completion, blocks everything else
def regular_task():
    print("Regular: start")
    time.sleep(1)          # BLOCKS — nothing else can run during this second
    print("Regular: done")

# Coroutine — can pause and let other things run while waiting
async def async_task():
    print("Async: start")
    await asyncio.sleep(1)  # PAUSES this coroutine, lets others run
    print("Async: done")

# Calling an async function returns a coroutine object — doesn't run it
coro = async_task()
print(type(coro))    # <class 'coroutine'>
coro.close()         # must close it if we don't run it (avoids warning)

# To RUN a coroutine, use asyncio.run()
asyncio.run(async_task())    # creates an event loop, runs the coroutine, closes loop


# ------------------------------------------------------------
# 3. RUNNING MULTIPLE COROUTINES — asyncio.gather()
# ------------------------------------------------------------
# gather() runs multiple coroutines CONCURRENTLY.
# All start, all await their pauses together, all finish faster.

async def fetch(name, delay):
    """Simulate fetching data from a URL — takes 'delay' seconds."""
    print(f"  [{name}] Starting fetch...")
    await asyncio.sleep(delay)    # simulate network I/O — pause here
    print(f"  [{name}] Done!")
    return f"Data from {name}"    # return result when done

async def main_sequential():
    """Run tasks one after another — slow."""
    start = time.perf_counter()
    r1 = await fetch("API-1", 1)  # wait 1s, THEN start next
    r2 = await fetch("API-2", 1)  # wait 1s
    r3 = await fetch("API-3", 1)  # wait 1s
    print(f"Sequential: {time.perf_counter()-start:.2f}s")  # ~3.0s
    return [r1, r2, r3]

async def main_concurrent():
    """Run tasks concurrently — fast."""
    start = time.perf_counter()
    # gather() starts ALL coroutines, they all await their sleeps together
    results = await asyncio.gather(
        fetch("API-1", 1),    # all three start at the same time
        fetch("API-2", 1),    # all await their sleep simultaneously
        fetch("API-3", 1),    # all finish after ~1s total (not 3s)
    )
    print(f"Concurrent: {time.perf_counter()-start:.2f}s")  # ~1.0s
    return results

asyncio.run(main_sequential())
print()
asyncio.run(main_concurrent())


# ------------------------------------------------------------
# 4. async / await MECHANICS — step by step
# ------------------------------------------------------------

async def step_by_step():
    """Walk through exactly what happens with await."""

    print("1. Before first await")

    await asyncio.sleep(0)     # yield control to event loop for one cycle
                                # even sleep(0) lets other tasks run briefly

    print("2. After first await — resumed here")

    result = await asyncio.sleep(0.1)   # await returns the value sleep() returns
    # asyncio.sleep returns None — but other awaitables return useful values

    print("3. Done")

asyncio.run(step_by_step())


# ------------------------------------------------------------
# 5. TASKS — schedule coroutines to run concurrently
# ------------------------------------------------------------
# asyncio.create_task() schedules a coroutine to run on the
# event loop WITHOUT waiting for it immediately.
# Returns a Task object you can await later.

async def background_job(name, seconds):
    print(f"  {name}: started")
    await asyncio.sleep(seconds)
    print(f"  {name}: finished after {seconds}s")
    return f"{name}-result"

async def main_with_tasks():
    # create_task() schedules the coroutine to run — doesn't block here
    task1 = asyncio.create_task(background_job("Job-A", 2))
    task2 = asyncio.create_task(background_job("Job-B", 1))
    task3 = asyncio.create_task(background_job("Job-C", 3))
    # All three jobs are now SCHEDULED and running concurrently

    print("Tasks created — doing other work in main...")
    await asyncio.sleep(0.5)    # main does something else for 0.5s
    print("Main: back to waiting for tasks...")

    # await each task to get its result (waits if not done yet)
    result1 = await task1    # wait for Job-A to finish
    result2 = await task2    # wait for Job-B (likely already done)
    result3 = await task3    # wait for Job-C

    print(f"Results: {result1}, {result2}, {result3}")

asyncio.run(main_with_tasks())


# ------------------------------------------------------------
# 6. gather() vs create_task() — when to use which
# ------------------------------------------------------------
#
# asyncio.gather(*coros)
#   → run coroutines concurrently AND collect all results
#   → waits for ALL to finish
#   → results returned in the SAME ORDER as inputs
#   → if one raises exception, others are cancelled (by default)
#
# asyncio.create_task(coro)
#   → schedule a coroutine to run in background
#   → gives you a Task object for more control
#   → can cancel individual tasks: task.cancel()
#   → can check status: task.done(), task.result()
#
# Use gather() when you want to run a group and collect results.
# Use create_task() when you need fine-grained control.

async def gather_example():
    # gather — simple and clean for most use cases
    results = await asyncio.gather(
        fetch("Site-1", 0.5),
        fetch("Site-2", 1.0),
        fetch("Site-3", 0.3),
    )
    # results is a list matching the order of arguments
    print(results)    # ['Data from Site-1', 'Data from Site-2', 'Data from Site-3']

asyncio.run(gather_example())


# ------------------------------------------------------------
# 7. HANDLING EXCEPTIONS IN GATHER
# ------------------------------------------------------------

async def might_fail(name, should_fail):
    await asyncio.sleep(0.1)
    if should_fail:
        raise ValueError(f"{name} failed!")
    return f"{name} succeeded"

async def gather_with_errors():
    # return_exceptions=True → exceptions returned as values, not raised
    # Without this, ONE failure cancels the whole gather
    results = await asyncio.gather(
        might_fail("Task-A", False),    # will succeed
        might_fail("Task-B", True),     # will fail
        might_fail("Task-C", False),    # will succeed
        return_exceptions=True          # don't cancel others on failure
    )
    for r in results:
        if isinstance(r, Exception):    # check each result — might be an exception
            print(f"Error: {r}")
        else:
            print(f"OK: {r}")

asyncio.run(gather_with_errors())


# ------------------------------------------------------------
# 8. TIMEOUTS — don't wait forever
# ------------------------------------------------------------

async def slow_operation():
    print("Starting slow operation...")
    await asyncio.sleep(5)    # simulate something very slow
    return "finally done"

async def with_timeout():
    try:
        # asyncio.wait_for() cancels the coroutine if it takes too long
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=2.0    # cancel after 2 seconds
        )
        print(result)
    except asyncio.TimeoutError:
        print("Operation timed out after 2s!")    # coroutine was cancelled

asyncio.run(with_timeout())


# ------------------------------------------------------------
# 9. ASYNC CONTEXT MANAGERS — async with
# ------------------------------------------------------------
# Some resources need async setup/teardown (e.g., DB connections,
# HTTP sessions). These use 'async with' instead of plain 'with'.

class AsyncDatabaseConnection:
    """Simulate an async database connection."""

    async def __aenter__(self):
        """Async setup — called when entering 'async with' block."""
        print("Connecting to database...")
        await asyncio.sleep(0.1)    # simulate async connection time
        print("Connected!")
        return self                 # return self as the 'as' variable

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async cleanup — called when leaving 'async with' block."""
        print("Closing database connection...")
        await asyncio.sleep(0.05)   # simulate async cleanup
        print("Connection closed.")
        return False                # don't suppress exceptions

    async def query(self, sql):
        """Simulate an async database query."""
        await asyncio.sleep(0.1)    # simulate query time
        return f"Results for: {sql}"

async def use_database():
    async with AsyncDatabaseConnection() as db:    # async setup runs
        result = await db.query("SELECT * FROM users")
        print(result)
    # async cleanup runs here automatically

asyncio.run(use_database())


# ------------------------------------------------------------
# 10. ASYNC ITERATORS AND async for
# ------------------------------------------------------------
# Some iterables produce values asynchronously (e.g., reading
# from a websocket, streaming data). Use 'async for' for these.

class AsyncCounter:
    """An async iterator that yields numbers with a delay."""

    def __init__(self, start, stop):
        self.current = start
        self.stop    = stop

    def __aiter__(self):
        return self    # async iterator returns itself

    async def __anext__(self):
        """Called by 'async for' to get next value."""
        if self.current >= self.stop:
            raise StopAsyncIteration    # signals end of iteration
        await asyncio.sleep(0.1)        # simulate async delay between values
        value = self.current
        self.current += 1
        return value

async def use_async_iterator():
    async for num in AsyncCounter(0, 5):    # 'async for' handles __anext__
        print(f"Got: {num}")

asyncio.run(use_async_iterator())

# Async generator — simpler way to make async iterators using 'yield'
async def async_range(start, stop, delay=0.1):
    """Async generator: yield values with async delay between them."""
    for i in range(start, stop):
        await asyncio.sleep(delay)    # async pause between each value
        yield i                       # yield the value

async def use_async_generator():
    async for n in async_range(0, 5):
        print(f"Value: {n}")

asyncio.run(use_async_generator())


# ------------------------------------------------------------
# 11. ASYNCIO QUEUES — coordinate async tasks
# ------------------------------------------------------------
# asyncio.Queue is like queue.Queue but for async code.
# Use it to coordinate producers and consumers in async programs.

async def async_producer(queue, items):
    """Put items into the async queue."""
    for item in items:
        await queue.put(item)         # put item — suspends if queue is full
        print(f"Produced: {item}")
        await asyncio.sleep(0.1)      # simulate production delay
    await queue.put(None)             # sentinel — signals consumer to stop

async def async_consumer(queue, name):
    """Get items from the queue and process them."""
    while True:
        item = await queue.get()      # wait for item — suspends until one arrives
        if item is None:
            queue.task_done()
            break                     # exit on sentinel
        print(f"[{name}] Processing: {item} → {item**2}")
        await asyncio.sleep(0.2)      # simulate processing time
        queue.task_done()             # signal this item is done

async def producer_consumer():
    queue = asyncio.Queue(maxsize=3)  # buffer of max 3 items

    # Run producer and consumer concurrently
    await asyncio.gather(
        async_producer(queue, range(6)),
        async_consumer(queue, "Consumer-1"),
    )

asyncio.run(producer_consumer())


# ------------------------------------------------------------
# 12. REAL-WORLD PATTERN — fetch many URLs concurrently
# ------------------------------------------------------------
# This is the #1 real-world use case for asyncio.
# Use aiohttp for real HTTP requests (pip install aiohttp).
# Here we simulate it with asyncio.sleep.

import random

async def fetch_url(session_id, url):
    """Simulate fetching a URL asynchronously."""
    delay = random.uniform(0.1, 1.0)    # random response time
    await asyncio.sleep(delay)           # simulate network wait
    status = 200 if random.random() > 0.1 else 404   # 10% chance of 404
    return {"url": url, "status": status, "time": f"{delay:.2f}s"}

async def fetch_all(urls, concurrency=5):
    """Fetch all URLs with a concurrency limit."""
    semaphore = asyncio.Semaphore(concurrency)  # max 'concurrency' tasks at once
                                                # prevents overwhelming the server

    async def fetch_with_limit(url):
        async with semaphore:               # acquire semaphore (limits concurrency)
            return await fetch_url(0, url)  # fetch when slot is available

    results = await asyncio.gather(
        *[fetch_with_limit(url) for url in urls],   # * unpacks list as args
        return_exceptions=True
    )
    return results

async def main_fetch():
    urls = [f"https://api.example.com/item/{i}" for i in range(10)]

    start   = time.perf_counter()
    results = await fetch_all(urls, concurrency=3)
    elapsed = time.perf_counter() - start

    success = [r for r in results if isinstance(r, dict) and r["status"] == 200]
    print(f"Fetched {len(urls)} URLs in {elapsed:.2f}s")
    print(f"Success: {len(success)}, Failed: {len(results)-len(success)}")

asyncio.run(main_fetch())


# ------------------------------------------------------------
# 13. MIXING ASYNCIO WITH BLOCKING CODE
# ------------------------------------------------------------
# Problem: if you call a blocking function (time.sleep, file I/O,
# a slow library) inside async code, it BLOCKS the entire event loop.
# Solution: run blocking code in a thread pool using run_in_executor().

import asyncio
from concurrent.futures import ThreadPoolExecutor

def blocking_function(n):
    """This is a normal blocking function — can't use await inside."""
    time.sleep(1)           # blocks! would freeze the event loop if called directly
    return n * n

async def non_blocking_wrapper(n):
    """Run blocking code without freezing the event loop."""
    loop = asyncio.get_event_loop()    # get the current running event loop

    # run_in_executor runs the blocking function in a thread pool
    # → event loop is FREE to run other coroutines while thread runs
    result = await loop.run_in_executor(
        None,                   # None = use default ThreadPoolExecutor
        blocking_function,      # the blocking function to run
        n                       # argument to pass it
    )
    return result

async def main_mixed():
    # Run 3 blocking functions concurrently via thread pool
    results = await asyncio.gather(
        non_blocking_wrapper(3),
        non_blocking_wrapper(4),
        non_blocking_wrapper(5),
    )
    print(results)    # [9, 16, 25] — all ran concurrently in threads

asyncio.run(main_mixed())


# ============================================================
# SUMMARY
# ============================================================
# async def           → defines a coroutine function
# await               → pause coroutine, release control to event loop
# asyncio.run(coro)   → run a coroutine (entry point — call once)
# asyncio.sleep(n)    → async pause (use instead of time.sleep!)
# asyncio.gather()    → run multiple coroutines concurrently, collect results
# asyncio.create_task()→ schedule coroutine to run, get Task object back
# asyncio.wait_for()  → run with a timeout, raises TimeoutError
# async with          → async context manager (__aenter__/__aexit__)
# async for           → async iterator (__aiter__/__anext__)
# async generator     → async def with yield
# asyncio.Queue       → coordinate async producers and consumers
# Semaphore           → limit concurrency (e.g., max 5 requests at once)
# run_in_executor()   → run blocking code in thread pool without freezing loop
# return_exceptions   → gather() returns exceptions as values, not raises
# Best for            → many concurrent I/O operations (HTTP, DB, WebSocket)
# NOT for             → CPU-bound (still single thread — use multiprocessing)
# ============================================================