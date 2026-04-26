"""
3. Asynchronous Programming (async / await)
This paradigm is essential for I/O-bound tasks where your program would otherwise sit idle waiting for a response. 
The Event Loop: Instead of using multiple threads, asyncio uses a single thread that switches between tasks whenever one is "waiting".
Benefit: Massive efficiency for web scraping, database queries, or handling thousands of network connections. 
"""

"""
Think of Asynchronous Programming as a busy chef in a kitchen. 
A "Synchronous" chef would start the pasta, stand still and watch the water boil for 10 minutes,
and only then start the sauce. An "Asynchronous" chef starts the water, sets a timer, 
and immediately starts chopping onions while the water heats up.
In Python, we use asyncio to handle these "waiting" periods efficiently.
"""
"""
Core Concepts
The Event Loop: This is the "manager." It keeps track of all tasks. 
When one task is waiting (e.g., for a database response), the loop pauses it and works on another task.
Coroutines: Functions defined with async def. They don't run immediately when called; 
they return a "coroutine object" that needs to be scheduled on the loop.
Await: The await keyword is used to pause the coroutine. It tells the event loop: 
"I'm waiting for this to finish; go do something else in the meantime."
Tasks: A way to run coroutines concurrently. When you wrap a coroutine in a Task, 
Python starts running it in the background as soon as the loop is free.
"""

"""5 Real-World Examples
1. Web Scraping (Multiple Pages)
Instead of waiting for Page A to download before starting Page B, you trigger requests for all of them at once.
"""
import asyncio

async def fetch_page(url):
    print(f"Starting download: {url}")
    await asyncio.sleep(2)  # Simulates network delay
    return f"Data from {url}"

async def main():
    urls = ["site1.com", "site2.com", "site3.com"]
    # Run all fetches concurrently
    results = await asyncio.gather(*(fetch_page(u) for u in urls))
    print(results)

asyncio.run(main())
