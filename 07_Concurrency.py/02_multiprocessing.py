# ============================================================
#  CHAPTER 7 — MULTIPROCESSING
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHY MULTIPROCESSING?
# ------------------------------------------------------------
# Threading is limited by the GIL — only ONE thread runs
# Python code at a time, even on a multi-core machine.
#
# Multiprocessing bypasses the GIL entirely by spawning
# SEPARATE PROCESSES — each gets its own Python interpreter,
# its own GIL, and its own memory space.
#
# Each process runs on a SEPARATE CPU CORE → true parallelism.
#
# Threading vs Multiprocessing:
#
#   Threading
#     → Shared memory (all threads see same variables)
#     → One GIL → not truly parallel for CPU work
#     → Low overhead (cheap to create threads)
#     → Best for: I/O-bound tasks (network, file, DB)
#
#   Multiprocessing
#     → Separate memory (processes don't share variables)
#     → No GIL → truly parallel on multiple cores
#     → Higher overhead (spawning a process is expensive)
#     → Best for: CPU-bound tasks (math, image processing, ML)
#
# Rule of thumb:
#   Waiting for I/O?      → Threading or Asyncio
#   Heavy computation?    → Multiprocessing


# ------------------------------------------------------------
# 2. IMPORTANT: if __name__ == "__main__" GUARD
# ------------------------------------------------------------
# On Windows (and when using 'spawn' start method), Python
# IMPORTS the script when spawning child processes.
# Without the guard, child processes would try to spawn MORE
# children → infinite loop of process creation → crash.
#
# ALWAYS wrap multiprocessing code in:
#   if __name__ == "__main__":
#       ...your code...
#
# We'll show it in examples below.


# ------------------------------------------------------------
# 3. CREATING A PROCESS — basic usage
# ------------------------------------------------------------
import multiprocessing
import time
import os

def cpu_task(name, n):
    """A CPU-bound task — counts up to n (simulates real computation)."""
    print(f"[{name}] PID={os.getpid()} starting...")   # os.getpid() = this process's ID
    total = sum(range(n))                               # actual CPU work
    print(f"[{name}] Done. Sum={total}")
    return total

if __name__ == "__main__":

    # Without multiprocessing — sequential, uses ONE core
    start = time.perf_counter()
    cpu_task("Task-1", 10_000_000)
    cpu_task("Task-2", 10_000_000)
    print(f"Sequential: {time.perf_counter() - start:.2f}s\n")

    # With multiprocessing — parallel, uses MULTIPLE cores
    start = time.perf_counter()

    p1 = multiprocessing.Process(target=cpu_task, args=("Task-1", 10_000_000))
    p2 = multiprocessing.Process(target=cpu_task, args=("Task-2", 10_000_000))

    p1.start()    # spawn child process — runs cpu_task in a new process
    p2.start()    # spawn another child process — runs concurrently

    p1.join()     # wait for p1 to finish before continuing
    p2.join()     # wait for p2 to finish before continuing

    print(f"Parallel: {time.perf_counter() - start:.2f}s\n")
    # On a multi-core machine, parallel will be roughly 2x faster


# ------------------------------------------------------------
# 4. PROCESS PROPERTIES
# ------------------------------------------------------------
if __name__ == "__main__":
    def show_info(label):
        print(f"{label}: PID={os.getpid()}, parent PID={os.getppid()}")

    show_info("Main process")    # main program's process ID

    p = multiprocessing.Process(target=show_info, args=("Child",))
    p.start()
    p.join()

    # Process attributes
    p2 = multiprocessing.Process(target=time.sleep, args=(2,))
    p2.start()
    print(f"PID:     {p2.pid}")         # child process ID
    print(f"alive:   {p2.is_alive()}")  # True while running
    print(f"name:    {p2.name}")        # auto-assigned name
    p2.terminate()                       # forcefully kill the process
    p2.join()                            # reap it (clean up)
    print(f"alive:   {p2.is_alive()}")  # False after terminate


# ------------------------------------------------------------
# 5. SHARING DATA — the challenge with multiprocessing
# ------------------------------------------------------------
# Processes have SEPARATE memory — changes in one process
# are NOT visible in another. This is the key difference
# from threading.

# ❌ This does NOT work — each process has its own 'shared_list'
shared_list = []

def add_to_list(value):
    shared_list.append(value)    # modifies THAT PROCESS's copy, not the main one
    print(f"Inside process: {shared_list}")

if __name__ == "__main__":
    p = multiprocessing.Process(target=add_to_list, args=(42,))
    p.start()
    p.join()
    print(f"Main process: {shared_list}")    # [] — main's list is unchanged!


# ------------------------------------------------------------
# 6. SHARED MEMORY — Value and Array
# ------------------------------------------------------------
# multiprocessing.Value and multiprocessing.Array live in
# shared memory — ALL processes can read and write them.

from multiprocessing import Process, Value, Array
import ctypes   # ctypes provides C-type declarations (i=int, d=double, etc.)

def increment(counter, lock):
    """Increment a shared counter safely using a lock."""
    for _ in range(100_000):
        with lock:              # protect the read-modify-write
            counter.value += 1  # .value accesses the shared integer

if __name__ == "__main__":
    # Value('i', 0) = shared integer initialized to 0
    # 'i' = C int type, 'd' = C double, 'f' = C float
    counter = Value('i', 0)
    lock    = multiprocessing.Lock()    # lock to prevent race conditions

    processes = [Process(target=increment, args=(counter, lock))
                 for _ in range(4)]

    for p in processes: p.start()
    for p in processes: p.join()

    print(f"Counter: {counter.value}")    # 400000 ✅

    # Array — shared array of a fixed type and size
    shared_arr = Array('i', [0, 0, 0, 0, 0])   # shared array of 5 ints

    def fill_array(arr, index, value):
        arr[index] = value    # write to shared array

    procs = [Process(target=fill_array, args=(shared_arr, i, i*10))
             for i in range(5)]
    for p in procs: p.start()
    for p in procs: p.join()

    print(list(shared_arr))    # [0, 10, 20, 30, 40]


# ------------------------------------------------------------
# 7. MANAGER — share complex Python objects
# ------------------------------------------------------------
# Value/Array only support simple C types.
# Manager lets you share Python lists, dicts, and more.
# Manager objects are accessed through a PROXY — slower but flexible.

from multiprocessing import Manager

def worker_append(shared_list, shared_dict, i):
    """Worker that appends to a shared list and updates a shared dict."""
    shared_list.append(i * i)           # append to shared list
    shared_dict[f"key_{i}"] = i * 2    # update shared dict

if __name__ == "__main__":
    with Manager() as manager:
        # Create managed (shared) objects
        m_list = manager.list()      # shared list — all processes can modify it
        m_dict = manager.dict()      # shared dict — all processes can modify it

        processes = [Process(target=worker_append, args=(m_list, m_dict, i))
                     for i in range(5)]

        for p in processes: p.start()
        for p in processes: p.join()

        print(sorted(m_list))          # [0, 1, 4, 9, 16]
        print(dict(m_dict))            # {'key_0':0, 'key_1':2, ...}


# ------------------------------------------------------------
# 8. QUEUE — safe communication between processes
# ------------------------------------------------------------
# multiprocessing.Queue is process-safe (unlike queue.Queue
# which is only thread-safe). Use it to pass data between processes.

from multiprocessing import Process, Queue

def producer(q, items):
    """Put items into the queue."""
    for item in items:
        print(f"Producing: {item}")
        q.put(item)             # put item — blocks if queue is full
    q.put(None)                 # None = sentinel value to signal "done"

def consumer(q, results):
    """Get items from queue and process them."""
    while True:
        item = q.get()          # get item — blocks until one is available
        if item is None:        # check for sentinel "done" signal
            break
        result = item ** 2      # process the item
        print(f"Consumed: {item} → {result}")
        results.put(result)     # put result in results queue

if __name__ == "__main__":
    task_queue   = Queue()
    result_queue = Queue()

    p1 = Process(target=producer, args=(task_queue, range(5)))
    p2 = Process(target=consumer, args=(task_queue, result_queue))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Drain the results queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    print(f"Results: {sorted(results)}")    # [0, 1, 4, 9, 16]


# ------------------------------------------------------------
# 9. PIPE — direct two-way communication
# ------------------------------------------------------------
# Pipe() returns two Connection objects (conn1, conn2).
# What you send on conn1 arrives at conn2, and vice versa.
# Faster than Queue for two-process communication.

from multiprocessing import Process, Pipe

def sender(conn):
    """Send messages through the pipe."""
    messages = ["hello", "world", "done"]
    for msg in messages:
        print(f"Sending: {msg}")
        conn.send(msg)       # send a Python object through the pipe
    conn.close()             # close this end when done

def receiver(conn):
    """Receive messages from the pipe."""
    while True:
        try:
            msg = conn.recv()         # receive next message — blocks until one arrives
            print(f"Received: {msg}")
            if msg == "done":
                break
        except EOFError:
            break    # raised when sender closes its end of the pipe

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()    # create two connected endpoints

    p1 = Process(target=sender,   args=(parent_conn,))
    p2 = Process(target=receiver, args=(child_conn,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()


# ------------------------------------------------------------
# 10. POOL — the workhorse for parallel computation
# ------------------------------------------------------------
# Pool manages a pool of worker processes.
# You submit tasks, it distributes them across workers automatically.
# This is the MOST COMMON way to use multiprocessing.

from multiprocessing import Pool

def square(n):
    """CPU work: square a number."""
    return n * n

def slow_square(n):
    """Simulate slow CPU work."""
    time.sleep(0.1)
    return n * n

if __name__ == "__main__":
    numbers = list(range(12))

    # map() — apply function to each item, returns results IN ORDER
    # Blocks until ALL results are ready
    with Pool(processes=4) as pool:     # 4 worker processes
        results = pool.map(square, numbers)
    print(results)    # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121]

    # starmap() — like map() but unpacks tuples as multiple arguments
    pairs = [(2, 3), (4, 5), (6, 7)]
    with Pool() as pool:                # processes=None → uses os.cpu_count()
        results = pool.starmap(pow, pairs)   # pow(2,3), pow(4,5), pow(6,7)
    print(results)    # [8, 1024, 279936]

    # map_async() — non-blocking, returns AsyncResult immediately
    with Pool(4) as pool:
        async_result = pool.map_async(slow_square, numbers)
        print("Doing other work while pool runs...")   # runs while pool works
        results = async_result.get()    # block here until results are ready
    print(results)

    # apply() — run ONE function call in a worker (blocking)
    with Pool(4) as pool:
        result = pool.apply(square, args=(7,))
    print(result)    # 49

    # apply_async() — run ONE function call in a worker (non-blocking)
    with Pool(4) as pool:
        future = pool.apply_async(square, args=(7,))
        result = future.get(timeout=5)    # wait up to 5s for result
    print(result)    # 49


# ------------------------------------------------------------
# 11. ProcessPoolExecutor — modern high-level API
# ------------------------------------------------------------
# Like ThreadPoolExecutor but for processes.
# Part of concurrent.futures — cleaner API than Pool.

from concurrent.futures import ProcessPoolExecutor, as_completed

def process_item(n):
    """Simulate CPU-bound work."""
    return sum(range(n))    # compute sum of 0..n

if __name__ == "__main__":
    items = [1_000_000, 2_000_000, 500_000, 1_500_000]

    # map() — returns results in submission order
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_item, items))
    print(results)

    # submit() + as_completed() — process results as they finish
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_item, n): n for n in items}

        for future in as_completed(futures):     # fires as each finishes
            n      = futures[future]             # which input was this?
            result = future.result()             # get the result
            print(f"sum(0..{n}) = {result}")


# ------------------------------------------------------------
# 12. WHEN TO USE WHAT — decision guide
# ------------------------------------------------------------
#
# Your task is...         Use...
# ─────────────────────── ──────────────────────────────
# I/O-bound (1-100 ops)   threading.Thread
# I/O-bound (many ops)    asyncio
# CPU-bound (easy API)    ProcessPoolExecutor
# CPU-bound (more ctrl)   multiprocessing.Pool
# Share simple data       multiprocessing.Value / Array
# Share complex data      multiprocessing.Manager
# Two-process comms       multiprocessing.Pipe
# Multi-process comms     multiprocessing.Queue


# ------------------------------------------------------------
# 13. COMMON PATTERNS
# ------------------------------------------------------------

# Pattern 1: Parallel map — process a list using all CPU cores
def parallel_map(func, items, workers=None):
    """Apply func to every item in parallel, return results in order."""
    workers = workers or os.cpu_count()    # default to number of CPU cores
    with Pool(workers) as pool:
        return pool.map(func, items)       # distribute work across pool

# Pattern 2: Chunk large work into batches
def chunked(lst, n):
    """Split list into chunks of size n."""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]    # yield each chunk

def process_chunk(chunk):
    """Process one chunk of data."""
    return [x ** 2 for x in chunk]    # do work on the chunk

if __name__ == "__main__":
    big_data = list(range(1000))
    chunks   = list(chunked(big_data, 100))   # split into 10 chunks of 100

    with Pool() as pool:
        results = pool.map(process_chunk, chunks)    # process chunks in parallel

    flat = [item for chunk in results for item in chunk]   # flatten results
    print(f"Processed {len(flat)} items")

# Pattern 3: CPU-bound with progress tracking
from multiprocessing import Pool, Value, Lock as MpLock
import ctypes

def heavy_work_with_progress(args):
    """Unpack args tuple and do work, updating shared counter."""
    n, counter, lock = args
    result = sum(range(n))         # the actual CPU work
    with lock:
        counter.value += 1         # increment shared progress counter
    return result

if __name__ == "__main__":
    counter = Value(ctypes.c_int, 0)    # shared counter across processes
    lock    = MpLock()
    tasks   = [(100_000, counter, lock) for _ in range(20)]

    with Pool(4) as pool:
        results = pool.map(heavy_work_with_progress, tasks)

    print(f"Completed: {counter.value}/20 tasks")


# ============================================================
# SUMMARY
# ============================================================
# Process              → separate program instance, own memory, own GIL
# Process(target, args)→ create a process
# p.start()            → spawn the process
# p.join()             → wait for process to finish
# p.terminate()        → forcefully kill the process
# os.getpid()          → get current process ID
# Value('i', 0)        → shared integer in shared memory
# Array('i', [...])    → shared array in shared memory
# Manager()            → share Python lists, dicts, etc.
# Queue()              → process-safe message passing
# Pipe()               → direct two-process communication
# Pool(n)              → n worker processes, distributes tasks
# pool.map()           → parallel map, results in order
# pool.starmap()       → map with multi-arg functions
# pool.map_async()     → non-blocking map
# ProcessPoolExecutor  → modern high-level API (recommended)
# if __name__=="__main__" → REQUIRED guard on Windows
# Best for             → CPU-bound: math, image/video, ML, compression
# NOT for              → I/O-bound (overhead too high — use threading/asyncio)
# ============================================================