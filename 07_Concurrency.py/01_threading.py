# ============================================================
#  CHAPTER 7 — THREADING
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS CONCURRENCY AND WHY DO WE NEED IT?
# ------------------------------------------------------------
# By default Python runs ONE thing at a time — line by line.
# This is fine for simple scripts but real programs often need to:
#   → Download multiple files at the same time
#   → Handle multiple users simultaneously
#   → Do work while waiting for a database response
#
# Concurrency = making progress on multiple tasks at once.
# There are three tools in Python for this:
#
#   Threading        → multiple threads share one CPU core
#                      best for I/O-bound tasks (waiting for network/disk)
#
#   Multiprocessing  → multiple CPU cores run truly in parallel
#                      best for CPU-bound tasks (math, image processing)
#
#   Asyncio          → single thread, cooperative multitasking
#                      best for I/O-bound tasks with many connections
#
# THIS FILE covers Threading.


# ------------------------------------------------------------
# 2. THE GIL — Global Interpreter Lock
# ------------------------------------------------------------
# Python has a GIL — a lock that allows only ONE thread to
# execute Python bytecode at a time.
#
# This means:
#   → Threads do NOT run truly in parallel for CPU work
#   → BUT for I/O tasks (waiting for network, file, user input),
#     the GIL is RELEASED while waiting — so other threads run
#
# Rule of thumb:
#   I/O-bound  → use threading (GIL released during waiting)
#   CPU-bound  → use multiprocessing (bypasses GIL entirely)


# ------------------------------------------------------------
# 3. CREATING A THREAD — basic usage
# ------------------------------------------------------------
import threading
import time

def task(name, seconds):
    """A simple task that simulates work by sleeping."""
    print(f"[{name}] Starting...")
    time.sleep(seconds)              # simulate waiting (I/O, network, etc.)
    print(f"[{name}] Done after {seconds}s")

# Without threading — tasks run ONE AFTER ANOTHER (sequential)
start = time.perf_counter()
task("Task-1", 2)    # runs, finishes, THEN task 2 starts
task("Task-2", 2)    # total: ~4 seconds
end = time.perf_counter()
print(f"Sequential: {end - start:.2f}s\n")    # ~4.0s

# With threading — tasks run CONCURRENTLY (overlapping)
start = time.perf_counter()

# threading.Thread(target=func, args=(arg1, arg2))
t1 = threading.Thread(target=task, args=("Task-1", 2))
t2 = threading.Thread(target=task, args=("Task-2", 2))

t1.start()    # start thread 1 — begins running task() in background
t2.start()    # start thread 2 — begins running task() WHILE thread 1 runs

t1.join()     # wait for thread 1 to finish before continuing
t2.join()     # wait for thread 2 to finish before continuing

end = time.perf_counter()
print(f"Concurrent: {end - start:.2f}s\n")    # ~2.0s  (both ran at same time)


# ------------------------------------------------------------
# 4. Thread ARGUMENTS — passing data to threads
# ------------------------------------------------------------

def download(url, result_list, index):
    """Simulate downloading a URL and storing result."""
    print(f"Downloading {url}...")
    time.sleep(1)                         # simulate network delay
    result = f"Data from {url}"           # simulate received data
    result_list[index] = result           # store in shared list by index
    print(f"Finished {url}")

# Create a shared list to collect results from all threads
results = [None] * 3    # pre-allocate slots: [None, None, None]

urls = ["https://api.site1.com", "https://api.site2.com", "https://api.site3.com"]

threads = []
for i, url in enumerate(urls):
    # Create a thread for each URL, passing index so each thread writes to its own slot
    t = threading.Thread(target=download, args=(url, results, i))
    threads.append(t)    # keep reference so we can join later
    t.start()            # start the thread

for t in threads:
    t.join()    # wait for ALL threads to finish

print(results)    # ['Data from site1', 'Data from site2', 'Data from site3']


# ------------------------------------------------------------
# 5. Thread KWARGS — using keyword arguments
# ------------------------------------------------------------

def greet(name, greeting="Hello", times=1):
    for _ in range(times):
        print(f"{greeting}, {name}!")
        time.sleep(0.1)

# Pass keyword arguments with kwargs= dict
t = threading.Thread(
    target=greet,
    kwargs={"name": "Alice", "greeting": "Hi", "times": 3}
)
t.start()
t.join()


# ------------------------------------------------------------
# 6. THREAD SUBCLASSING — OOP approach
# ------------------------------------------------------------
# Instead of passing a function to Thread, subclass Thread
# and override the run() method. Useful for more complex threads.

class WorkerThread(threading.Thread):
    def __init__(self, task_id, duration):
        super().__init__()                  # MUST call Thread's __init__
        self.task_id  = task_id             # store our custom data
        self.duration = duration
        self.result   = None                # will hold the result when done

    def run(self):
        """This method runs when thread.start() is called."""
        print(f"Worker {self.task_id} started")
        time.sleep(self.duration)           # simulate work
        self.result = f"Result-{self.task_id}"   # store result in instance
        print(f"Worker {self.task_id} finished → {self.result}")

# Create and start worker threads
workers = [WorkerThread(i, duration=1) for i in range(3)]

for w in workers:
    w.start()      # calls run() in a new thread

for w in workers:
    w.join()       # wait for each to finish

# Access results stored on each thread instance
for w in workers:
    print(f"Thread {w.task_id} result: {w.result}")


# ------------------------------------------------------------
# 7. DAEMON THREADS — background threads that auto-exit
# ------------------------------------------------------------
# A daemon thread runs in the background and is automatically
# KILLED when the main program exits (no join needed).
# Use for background tasks like logging, monitoring, heartbeats.

def background_monitor():
    """Runs forever in background — logs every second."""
    while True:
        print("[Monitor] System is running...")
        time.sleep(1)

monitor = threading.Thread(target=background_monitor)
monitor.daemon = True    # mark as daemon BEFORE starting
monitor.start()          # starts running in background

# Main program does its work
print("Main: doing important work...")
time.sleep(2)            # main sleeps 2s — monitor prints twice
print("Main: done!")
# When main program exits here, the daemon thread is killed automatically
# No need to call monitor.join() — it just stops


# ------------------------------------------------------------
# 8. RACE CONDITIONS — the danger of shared state
# ------------------------------------------------------------
# A race condition happens when multiple threads read/write
# shared data at the same time, causing unpredictable results.

# ❌ UNSAFE — race condition on shared counter
counter = 0    # shared between threads

def increment_unsafe():
    global counter
    for _ in range(100_000):
        counter += 1    # NOT atomic! read → add 1 → write (3 separate steps)
                        # another thread can interfere between these steps

threads = [threading.Thread(target=increment_unsafe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Unsafe counter (expected 500000): {counter}")
# You'll likely get something LESS than 500000 — lost updates!


# ------------------------------------------------------------
# 9. LOCKS — protecting shared state
# ------------------------------------------------------------
# A Lock ensures only ONE thread can execute a block at a time.
# Other threads must WAIT until the lock is released.

lock    = threading.Lock()   # create one lock per shared resource
counter = 0

def increment_safe():
    global counter
    for _ in range(100_000):
        with lock:           # acquire lock → only one thread in here at a time
            counter += 1     # now this read-add-write is protected
                             # lock is released automatically when 'with' block ends

counter = 0    # reset
threads = [threading.Thread(target=increment_safe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Safe counter (expected 500000): {counter}")    # 500000 ✅

# Manual lock usage (equivalent to 'with lock:')
def increment_manual():
    global counter
    lock.acquire()    # block until lock is available, then acquire it
    try:
        counter += 1
    finally:
        lock.release()    # ALWAYS release in finally — even if exception occurs
# 'with lock:' does acquire/release automatically — always prefer it


# ------------------------------------------------------------
# 10. OTHER SYNCHRONIZATION PRIMITIVES
# ------------------------------------------------------------

# --- RLock (Reentrant Lock) --- same thread can acquire it multiple times ---
rlock = threading.RLock()    # re-entrant: same thread can lock it again without deadlock

def recursive_task(n):
    with rlock:          # first acquisition
        if n > 0:
            with rlock:  # second acquisition by SAME thread — OK with RLock
                recursive_task(n - 1)


# --- Semaphore --- limits how many threads can run at once ---
# Like a ticket system — only N tickets available at once

semaphore = threading.Semaphore(3)   # allow max 3 threads to run concurrently

def limited_task(n):
    with semaphore:          # acquire one of the 3 "tickets"
        print(f"Task {n} running (max 3 at a time)")
        time.sleep(0.5)      # do work
        print(f"Task {n} done")
                             # ticket released when 'with' block ends

threads = [threading.Thread(target=limited_task, args=(i,)) for i in range(8)]
for t in threads: t.start()
for t in threads: t.join()


# --- Event --- signal between threads (one thread waits for another) ---
event = threading.Event()   # starts in "not set" state

def waiter():
    print("Waiter: waiting for signal...")
    event.wait()             # BLOCK here until event is set
    print("Waiter: received signal! Continuing...")

def signaler():
    print("Signaler: doing work for 1 second...")
    time.sleep(1)
    print("Signaler: signaling now!")
    event.set()              # unblock all threads waiting on this event

t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=signaler)
t1.start()
t2.start()
t1.join()
t2.join()


# --- Condition --- more advanced coordination ---
condition = threading.Condition()   # combines a lock with wait/notify

items = []   # shared buffer

def producer():
    for i in range(5):
        with condition:              # acquire the condition's lock
            items.append(i)
            print(f"Produced: {i}")
            condition.notify()       # wake up one waiting consumer
        time.sleep(0.1)

def consumer():
    for _ in range(5):
        with condition:
            while not items:         # while buffer is empty
                condition.wait()     # release lock and wait for notify
            item = items.pop(0)      # get item from buffer
            print(f"Consumed: {item}")

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start(); t2.start()
t1.join();  t2.join()


# ------------------------------------------------------------
# 11. THREAD-SAFE QUEUE — the preferred way to share data
# ------------------------------------------------------------
# queue.Queue is thread-safe by design — no locks needed!
# Producer threads PUT items in, consumer threads GET items out.
# This is the RECOMMENDED pattern for thread communication.

import queue

task_queue   = queue.Queue()      # unlimited size queue
result_queue = queue.Queue()      # to collect results

def worker(task_q, result_q):
    """Worker thread: get tasks, process them, put results."""
    while True:
        try:
            task = task_q.get(timeout=1)    # wait up to 1s for a task
                                             # raises queue.Empty if nothing arrives
            result = task * 2               # process the task (double it)
            result_q.put(result)            # put result in result queue
            task_q.task_done()              # signal this task is complete
        except queue.Empty:
            break    # no more tasks after timeout — exit worker

# Put tasks into the queue
for i in range(10):
    task_queue.put(i)    # add tasks: 0, 1, 2, ..., 9

# Start worker threads
workers = [threading.Thread(target=worker, args=(task_queue, result_queue))
           for _ in range(3)]          # 3 workers share the task queue

for w in workers: w.start()

task_queue.join()    # block until ALL tasks have been marked task_done()

for w in workers: w.join()

# Collect all results
results = []
while not result_queue.empty():
    results.append(result_queue.get())

print(sorted(results))    # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]


# ------------------------------------------------------------
# 12. ThreadPoolExecutor — high-level thread management
# ------------------------------------------------------------
# concurrent.futures.ThreadPoolExecutor manages a pool of threads
# so you don't have to create/join them manually.
# This is the MODERN recommended approach for threading.

from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_data(url):
    """Simulate fetching data from a URL."""
    time.sleep(0.5)                      # simulate network delay
    return f"Data from {url}"            # return the result

urls = [f"https://api.example.com/{i}" for i in range(6)]

# Submit all tasks to the pool — returns Future objects
with ThreadPoolExecutor(max_workers=3) as executor:    # max 3 threads at once
    # map() — like built-in map() but runs in threads, returns results in ORDER
    results = list(executor.map(fetch_data, urls))
    print(results)

# submit() — for more control, returns a Future for each task
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(fetch_data, url): url   # submit each task
               for url in urls}                        # dict: future → url

    for future in as_completed(futures):      # process results AS THEY FINISH
        url    = futures[future]              # look up which URL this future was for
        result = future.result()              # get the result (blocks until ready)
        print(f"Completed {url}: {result}")


# ------------------------------------------------------------
# 13. COMMON PATTERNS
# ------------------------------------------------------------

# Pattern 1: Download multiple URLs concurrently
def download_all(urls, max_workers=5):
    """Download all URLs concurrently, return list of results."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(fetch_data, urls))

results = download_all(urls)
print(f"Downloaded {len(results)} items")

# Pattern 2: Thread-safe counter using Lock
class SafeCounter:
    def __init__(self):
        self._count = 0
        self._lock  = threading.Lock()    # one lock per counter

    def increment(self):
        with self._lock:          # protect the read-modify-write
            self._count += 1

    def get(self):
        with self._lock:          # even reads should be protected
            return self._count

c = SafeCounter()
threads = [threading.Thread(target=c.increment) for _ in range(1000)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Counter: {c.get()}")    # 1000 ✅

# Pattern 3: Run something on a timer in background
class RepeatingTimer:
    def __init__(self, interval, func):
        self.interval = interval
        self.func     = func
        self._timer   = None
        self._running = False

    def _run(self):
        self.func()                                      # call the function
        if self._running:
            self._timer = threading.Timer(self.interval, self._run)  # schedule next call
            self._timer.start()

    def start(self):
        self._running = True
        self._timer   = threading.Timer(self.interval, self._run)
        self._timer.start()

    def stop(self):
        self._running = False
        if self._timer:
            self._timer.cancel()    # cancel the scheduled call

count = 0
def tick():
    global count
    count += 1
    print(f"Tick {count}")

timer = RepeatingTimer(0.3, tick)
timer.start()
time.sleep(1)       # let it run for 1 second
timer.stop()


# ============================================================
# SUMMARY
# ============================================================
# Thread              → unit of concurrent execution
# threading.Thread    → Thread(target=func, args=(), kwargs={})
# t.start()           → begin running thread
# t.join()            → wait for thread to finish
# t.daemon = True     → thread dies when main program exits
# Race condition      → multiple threads corrupting shared data
# Lock                → threading.Lock() — only one thread at a time
# with lock:          → acquire on enter, release on exit (always use this)
# RLock               → reentrant lock — same thread can acquire multiple times
# Semaphore           → limit N threads running concurrently
# Event               → signal between threads (wait/set)
# Condition           → wait/notify pattern for producer-consumer
# queue.Queue         → thread-safe data sharing (preferred over raw locks)
# ThreadPoolExecutor  → high-level pool, use map() or submit()/as_completed()
# GIL                 → only one thread runs Python bytecode at a time
# Best for            → I/O-bound tasks (network, file, database, user input)
# NOT for             → CPU-bound tasks (use multiprocessing instead)
# ============================================================