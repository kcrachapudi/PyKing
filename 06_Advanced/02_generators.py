# ============================================================
#  CHAPTER 6 — GENERATORS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A GENERATOR?
# ------------------------------------------------------------
# A generator is a function that produces values ONE AT A TIME
# instead of computing and storing all values at once.
#
# Normal function:  computes everything → stores in memory → returns all
# Generator:        computes one value → gives it to you → PAUSES → waits
#                   for you to ask for the next one
#
# Real-world analogy:
#   Normal list  = buying an entire book upfront
#   Generator    = a librarian who reads you one page at a time
#                  and only turns to the next page when you ask
#
# Why use generators?
#   → Memory efficient — only ONE value in memory at a time
#   → Great for large files, infinite sequences, streaming data
#   → Faster start — don't wait for all values to be computed


# ------------------------------------------------------------
# 2. THE yield KEYWORD — what makes a generator
# ------------------------------------------------------------
# A function becomes a generator the moment it uses 'yield'.
# 'yield' is like 'return' BUT:
#   → it pauses the function (doesn't destroy it)
#   → saves the function's state (all local variables)
#   → resumes from that exact point next time you ask

def simple_generator():
    print("About to yield 1")
    yield 1                     # pause here, give 1 to caller
    print("About to yield 2")
    yield 2                     # pause here, give 2 to caller
    print("About to yield 3")
    yield 3                     # pause here, give 3 to caller
    print("Generator finished") # runs after last yield

gen = simple_generator()        # calling the function does NOT run it yet!
                                 # it just creates a generator object
print(type(gen))                 # <class 'generator'>

# next() asks the generator to run until the next yield
print(next(gen))    # "About to yield 1"  then  1
print(next(gen))    # "About to yield 2"  then  2
print(next(gen))    # "About to yield 3"  then  3
# next(gen)         # "Generator finished" then StopIteration exception
                    # because there are no more yields


# ------------------------------------------------------------
# 3. LOOPING OVER A GENERATOR
# ------------------------------------------------------------
# A for loop automatically calls next() and handles StopIteration

def count_up(n):
    i = 0
    while i < n:
        yield i      # pause and give current value of i
        i += 1       # this runs AFTER the caller processes the value

# for loop handles next() and StopIteration automatically
for num in count_up(5):
    print(num)       # 0  1  2  3  4

# You can also convert to list (but this loads everything into memory)
values = list(count_up(5))
print(values)    # [0, 1, 2, 3, 4]


# ------------------------------------------------------------
# 4. GENERATORS vs LISTS — memory comparison
# ------------------------------------------------------------
import sys

# List — stores ALL values in memory right now
numbers_list = [x * 2 for x in range(1_000_000)]   # list comprehension
print(f"List size:      {sys.getsizeof(numbers_list):,} bytes")   # ~8 MB

# Generator — stores NOTHING, computes on demand
numbers_gen = (x * 2 for x in range(1_000_000))    # generator expression (note: parentheses not brackets)
print(f"Generator size: {sys.getsizeof(numbers_gen):,} bytes")    # ~200 bytes

# Both give you the same values — but generator uses almost no memory
# Use a generator when you only need to loop through once


# ------------------------------------------------------------
# 5. GENERATOR EXPRESSIONS — one-liner generators
# ------------------------------------------------------------
# Same syntax as list comprehension but with () instead of []
# They are LAZY — values computed only when requested

# List comprehension  → [expr for x in iter]   — eager, all at once
# Generator expression→ (expr for x in iter)   — lazy, one at a time

squares_list = [x**2 for x in range(10)]     # creates list immediately
squares_gen  = (x**2 for x in range(10))     # creates generator object

# Both can be iterated
for val in squares_gen:
    print(val, end=" ")    # 0 1 4 9 16 25 36 49 64 81
print()

# Very useful inside function calls — no extra () needed
total = sum(x**2 for x in range(10))    # sum of squares without creating a list
print(total)    # 285

biggest = max(len(word) for word in ["apple", "banana", "fig"])
print(biggest)  # 6

any_negative = any(x < 0 for x in [1, 2, -3, 4])   # stops as soon as it finds one
print(any_negative)    # True


# ------------------------------------------------------------
# 6. PRACTICAL GENERATORS — real use cases
# ------------------------------------------------------------

# --- Read a huge file line by line (memory efficient) ---
def read_large_file(filepath):
    """Yields one line at a time — never loads whole file into memory."""
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:              # file objects are themselves iterators
            yield line.strip()      # strip whitespace, yield one line

# Usage — processes each line without loading the whole file
# for line in read_large_file("huge_log.txt"):
#     process(line)    # only one line is in memory at a time


# --- Infinite sequence generator ---
def infinite_counter(start=0, step=1):
    """Counts forever — only use with break or islice."""
    current = start
    while True:             # infinite loop is fine in a generator
        yield current       # pause and give current value
        current += step     # advance for next time

# Take only what you need using itertools.islice
import itertools
first_10_evens = list(itertools.islice(infinite_counter(0, 2), 10))
print(first_10_evens)    # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Or use break
counter = infinite_counter()
for n in counter:
    if n > 5:
        break       # stop the infinite generator
    print(n)        # 0 1 2 3 4 5


# --- Fibonacci generator ---
def fibonacci():
    """Infinite Fibonacci sequence."""
    a, b = 0, 1              # start with first two Fibonacci numbers
    while True:
        yield a              # give the current number
        a, b = b, a + b      # advance: new a = old b, new b = old a+b

fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]    # pull 10 values one at a time
print(first_10)    # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# --- Data pipeline with generators ---
# Generators chain together beautifully — each step is lazy

def read_numbers(numbers):
    """First stage: yield each number."""
    for n in numbers:
        yield n

def filter_evens(numbers):
    """Second stage: only pass through even numbers."""
    for n in numbers:
        if n % 2 == 0:      # only yield if even
            yield n

def square_them(numbers):
    """Third stage: square each number."""
    for n in numbers:
        yield n ** 2        # yield the square

# Chain the stages — nothing runs until you iterate!
raw      = read_numbers(range(20))      # stage 1
evens    = filter_evens(raw)            # stage 2 — wraps stage 1
squared  = square_them(evens)           # stage 3 — wraps stage 2

# Only NOW does data flow through the pipeline, one item at a time
result = list(squared)
print(result)    # [0, 4, 16, 36, 64, 100, 144, 196, 256, 324]


# --- Batch/chunk generator ---
def chunked(iterable, size):
    """Split an iterable into chunks of 'size'."""
    iterable = list(iterable)              # convert to list so we can slice
    for i in range(0, len(iterable), size):# step through by 'size'
        yield iterable[i : i + size]       # yield one chunk (slice) at a time

for batch in chunked(range(10), 3):
    print(list(batch))    # [0,1,2]  [3,4,5]  [6,7,8]  [9]


# ------------------------------------------------------------
# 7. yield FROM — delegate to another generator
# ------------------------------------------------------------
# 'yield from' lets a generator yield ALL values from another iterable.
# Cleaner than a for loop with yield inside.

def gen_a():
    yield 1
    yield 2
    yield 3

def gen_b():
    yield 4
    yield 5

# Without yield from — verbose
def combined_verbose():
    for val in gen_a():     # loop through gen_a and yield each item
        yield val
    for val in gen_b():     # loop through gen_b and yield each item
        yield val

# With yield from — clean
def combined():
    yield from gen_a()      # delegate all yielding to gen_a
    yield from gen_b()      # then delegate all yielding to gen_b

print(list(combined()))    # [1, 2, 3, 4, 5]

# yield from also works with any iterable
def flatten(nested):
    """Flatten a nested list of any depth."""
    for item in nested:
        if isinstance(item, list):      # if this item is itself a list
            yield from flatten(item)    # recursively flatten it
        else:
            yield item                  # it's a plain value, yield it

nested = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(nested)))    # [1, 2, 3, 4, 5, 6, 7]


# ------------------------------------------------------------
# 8. GENERATOR STATE — how pause and resume works
# ------------------------------------------------------------
# When a generator yields, Python saves:
#   - current line of execution
#   - all local variables
#   - the entire call stack for that function
# When next() is called, Python restores all of that and continues.

def stateful_gen():
    total = 0                    # local variable — preserved between yields
    for i in range(1, 6):
        total += i               # accumulate
        print(f"  i={i}, total so far={total}")
        yield total              # pause, give total to caller

gen = stateful_gen()
print(next(gen))    # i=1, total=1  → yields 1
print(next(gen))    # i=2, total=3  → yields 3
print(next(gen))    # i=3, total=6  → yields 6
# total is PRESERVED between calls — that's the magic


# ------------------------------------------------------------
# 9. send() — passing values INTO a generator
# ------------------------------------------------------------
# next() pulls values OUT of a generator.
# send() pushes a value IN and also advances the generator.
# The sent value becomes the result of the yield expression.

def accumulator():
    total = 0
    while True:
        value = yield total     # yield current total AND receive incoming value
                                # yield pauses AND returns 'total' to caller
                                # send() resumes AND puts sent value into 'value'
        if value is None:
            break
        total += value          # add the received value to total

gen = accumulator()
next(gen)            # must call next() first to advance to first yield
                     # returns 0 (initial total)

print(gen.send(10))  # sends 10 into generator → total becomes 10 → yields 10
print(gen.send(20))  # sends 20 → total becomes 30 → yields 30
print(gen.send(5))   # sends 5  → total becomes 35 → yields 35


# ------------------------------------------------------------
# 10. COMMON PATTERNS
# ------------------------------------------------------------

# Pattern 1: Generate unique IDs
def id_generator(prefix="ID"):
    """Generate sequential unique IDs."""
    n = 1
    while True:
        yield f"{prefix}-{n:04d}"    # format: ID-0001, ID-0002, ...
        n += 1

gen = id_generator("USR")
print(next(gen))    # USR-0001
print(next(gen))    # USR-0002
print(next(gen))    # USR-0003

# Pattern 2: Sliding window over a sequence
def sliding_window(seq, n):
    """Yield overlapping windows of size n."""
    seq = list(seq)                          # ensure indexable
    for i in range(len(seq) - n + 1):       # stop when window would go past end
        yield seq[i : i + n]                # yield current window slice

for window in sliding_window([1,2,3,4,5], 3):
    print(window)    # [1,2,3]  [2,3,4]  [3,4,5]

# Pattern 3: Round-robin between multiple iterables
def round_robin(*iterables):
    """Cycle through multiple iterables one item at a time."""
    iterators = [iter(it) for it in iterables]   # convert all to iterators
    while iterators:
        for it in list(iterators):
            try:
                yield next(it)               # get next item from this iterator
            except StopIteration:
                iterators.remove(it)         # remove exhausted iterators

result = list(round_robin([1,2,3], ["a","b"], [True]))
print(result)    # [1, 'a', True, 2, 'b', 3]

# Pattern 4: Paginate a large list
def paginate(items, page_size):
    """Yield one page at a time."""
    for i in range(0, len(items), page_size):
        yield items[i : i + page_size]    # yield one page (slice) at a time

data = list(range(25))
for page_num, page in enumerate(paginate(data, 10), 1):
    print(f"Page {page_num}: {page}")
# Page 1: [0..9]   Page 2: [10..19]   Page 3: [20..24]


# ============================================================
# SUMMARY
# ============================================================
# yield             → pauses function, gives value to caller, resumes on next()
# generator func    → any function containing yield
# next(gen)         → advance generator to next yield
# StopIteration     → raised when generator is exhausted (no more yields)
# for loop          → handles next() and StopIteration automatically
# Generator expr    → (x for x in iter)  lazy, memory-efficient
# vs list comp      → [x for x in iter]  eager, all in memory
# yield from        → delegate to another iterable/generator
# send(val)         → push a value into a generator
# Memory            → generators use ~200 bytes regardless of size
# Best for          → large files, infinite sequences, pipelines, streaming
# ============================================================