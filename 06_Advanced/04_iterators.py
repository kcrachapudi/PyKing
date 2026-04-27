# ============================================================
#  CHAPTER 6 — ITERATORS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS AN ITERATOR?
# ------------------------------------------------------------
# An ITERABLE  is anything you can loop over (list, str, dict, file...)
# An ITERATOR  is an object that does the actual looping — it keeps
#              track of WHERE you are and knows how to get the NEXT item.
#
# Think of it like a book:
#   Iterable  = the book itself (contains all the pages)
#   Iterator  = a bookmark    (remembers which page you're on,
#                              can turn to the next page on demand)
#
# Two special methods make something an iterator:
#   __iter__()  → returns the iterator object itself
#   __next__()  → returns the next value, raises StopIteration when done
#
# Every iterator is also an iterable (it returns itself from __iter__)
# But not every iterable is an iterator (a list has __iter__ but no __next__)


# ------------------------------------------------------------
# 2. iter() AND next() — the two built-in functions
# ------------------------------------------------------------

# iter(obj)   → calls obj.__iter__() and returns the iterator
# next(iter)  → calls iter.__next__() and returns the next value

numbers = [10, 20, 30]         # list is an ITERABLE (not an iterator)

it = iter(numbers)             # iter() creates an ITERATOR from the list
print(type(numbers))           # <class 'list'>      — iterable
print(type(it))                # <class 'list_iterator'> — iterator

print(next(it))    # 10  → advances iterator, returns first item
print(next(it))    # 20  → advances iterator, returns second item
print(next(it))    # 30  → advances iterator, returns third item
# next(it)         # StopIteration! — no more items left

# A for loop does this AUTOMATICALLY under the hood:
#   1. calls iter() on the iterable
#   2. calls next() repeatedly
#   3. catches StopIteration and stops the loop

# This for loop:
for n in [10, 20, 30]:
    print(n)

# Is EXACTLY equivalent to:
it = iter([10, 20, 30])
while True:
    try:
        n = next(it)    # get next item
        print(n)        # do the loop body
    except StopIteration:
        break           # stop when exhausted


# ------------------------------------------------------------
# 3. CHECKING IF SOMETHING IS ITERABLE / AN ITERATOR
# ------------------------------------------------------------
from collections.abc import Iterable, Iterator

# Check if something is iterable (has __iter__)
print(isinstance([1,2,3],   Iterable))   # True  — list
print(isinstance("hello",   Iterable))   # True  — string
print(isinstance(42,        Iterable))   # False — int has no __iter__
print(isinstance({"a": 1},  Iterable))   # True  — dict

# Check if something is an iterator (has both __iter__ and __next__)
my_list = [1, 2, 3]
my_iter = iter(my_list)

print(isinstance(my_list, Iterator))    # False — list has no __next__
print(isinstance(my_iter, Iterator))    # True  — list_iterator has both

# Strings are iterable but NOT iterators
print(isinstance("hello", Iterator))    # False — no __next__
print(isinstance(iter("hello"), Iterator))  # True — str_iterator has both


# ------------------------------------------------------------
# 4. BUILDING A CUSTOM ITERATOR WITH A CLASS
# ------------------------------------------------------------
# Implement __iter__ and __next__ on any class.

class CountUp:
    """Iterator that counts from 'start' up to 'stop' (exclusive)."""

    def __init__(self, start, stop):
        self.current = start    # track current position
        self.stop    = stop     # track when to stop

    def __iter__(self):
        return self             # an iterator returns itself from __iter__

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration     # signal that iteration is complete
        value = self.current        # save current value to return
        self.current += 1           # advance position for next call
        return value                # return the saved value

# Use it in a for loop — for loop calls __iter__ then __next__ repeatedly
for n in CountUp(1, 6):
    print(n, end=" ")    # 1 2 3 4 5
print()

# Use it with next() manually
counter = CountUp(10, 13)
print(next(counter))    # 10
print(next(counter))    # 11
print(next(counter))    # 12
# next(counter)         # StopIteration

# Can also convert to list/tuple
print(list(CountUp(0, 5)))     # [0, 1, 2, 3, 4]
print(tuple(CountUp(5, 10)))   # (5, 6, 7, 8, 9)


# ------------------------------------------------------------
# 5. ITERABLE vs ITERATOR — an important distinction
# ------------------------------------------------------------
# An ITERABLE can be looped over MULTIPLE times (fresh iterator each time)
# An ITERATOR can only be looped over ONCE (it gets exhausted)

# Iterable — can loop multiple times
my_list = [1, 2, 3]
for x in my_list: print(x, end=" ")    # 1 2 3
print()
for x in my_list: print(x, end=" ")    # 1 2 3  ← works again!
print()

# Iterator — can only loop ONCE
my_iter = iter([1, 2, 3])
for x in my_iter: print(x, end=" ")    # 1 2 3
print()
for x in my_iter: print(x, end=" ")    # (nothing! — iterator is exhausted)
print()

# ⚠️  This is a common bug — saving an iterator and reusing it
it = iter(range(5))
print(list(it))    # [0, 1, 2, 3, 4]
print(list(it))    # []  ← exhausted! people expect [0,1,2,3,4] again


# ------------------------------------------------------------
# 6. MAKING A CLASS BOTH ITERABLE AND REUSABLE
# ------------------------------------------------------------
# Separate the iterable (data container) from the iterator (cursor)
# so the data can be iterated multiple times independently.

class NumberRange:
    """Iterable container — can be looped over multiple times."""

    def __init__(self, start, stop):
        self.start = start
        self.stop  = stop

    def __iter__(self):
        # Return a NEW iterator object each time — fresh start every loop
        return NumberRangeIterator(self.start, self.stop)


class NumberRangeIterator:
    """The actual iterator — keeps track of position."""

    def __init__(self, start, stop):
        self.current = start
        self.stop    = stop

    def __iter__(self):
        return self         # iterator returns itself

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        val = self.current
        self.current += 1
        return val

r = NumberRange(1, 4)

# Can loop multiple times — each loop gets a fresh iterator
for x in r: print(x, end=" ")    # 1 2 3
print()
for x in r: print(x, end=" ")    # 1 2 3  ← works again! fresh iterator
print()


# ------------------------------------------------------------
# 7. REAL-WORLD CUSTOM ITERATORS
# ------------------------------------------------------------

# --- Linked List Iterator ---
class Node:
    """A single node in a linked list."""
    def __init__(self, value, next_node=None):
        self.value     = value       # the data stored in this node
        self.next_node = next_node   # pointer to the next node (or None)

class LinkedList:
    """A simple linked list that supports iteration."""

    def __init__(self):
        self.head = None    # start with empty list

    def append(self, value):
        new_node = Node(value)              # create new node
        if not self.head:
            self.head = new_node            # first node becomes the head
            return
        current = self.head
        while current.next_node:            # walk to the end of the list
            current = current.next_node
        current.next_node = new_node        # attach new node at the end

    def __iter__(self):
        current = self.head                 # start from the beginning
        while current:                      # keep going while there's a node
            yield current.value             # yield this node's value
            current = current.next_node     # move to next node
        # using yield makes this a GENERATOR — Python handles __next__ for us!

ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)

for val in ll:
    print(val, end=" ")    # 10 20 30
print()


# --- File Line Iterator ---
class CSVReader:
    """Iterate over a CSV file row by row as dicts."""

    def __init__(self, filepath):
        self.filepath = filepath

    def __iter__(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            headers = f.readline().strip().split(",")  # first line = column names
            for line in f:                             # each remaining line = a row
                values = line.strip().split(",")       # split by comma
                # zip headers with values to make a dict
                yield dict(zip(headers, values))       # yield one row as a dict


# --- Infinite Cycling Iterator ---
class Cycle:
    """Cycle through a sequence forever."""

    def __init__(self, sequence):
        self.sequence = list(sequence)    # store as list for indexing
        self.index    = 0                 # current position

    def __iter__(self):
        return self

    def __next__(self):
        if not self.sequence:
            raise StopIteration           # empty sequence — nothing to cycle
        value = self.sequence[self.index % len(self.sequence)]  # wrap around using modulo
        self.index += 1                   # advance (keeps going past end — that's the point)
        return value

colors = Cycle(["red", "green", "blue"])
for i, color in zip(range(7), colors):   # zip limits to 7 items (stops Cycle from going forever)
    print(f"{i}: {color}")
# 0:red  1:green  2:blue  3:red  4:green  5:blue  6:red


# ------------------------------------------------------------
# 8. itertools — the iterator toolbox
# ------------------------------------------------------------
# itertools is Python's built-in module for working with iterators.
# All functions return ITERATORS (lazy — no memory wasted).

import itertools

# --- count(start, step) — infinite counter ---
counter = itertools.count(10, 5)          # start at 10, step by 5
first5  = list(itertools.islice(counter, 5))  # take only first 5
print(first5)    # [10, 15, 20, 25, 30]

# --- cycle(iterable) — repeat an iterable forever ---
colors  = itertools.cycle(["R", "G", "B"])
pattern = list(itertools.islice(colors, 7))   # take 7 items from infinite cycle
print(pattern)    # ['R', 'G', 'B', 'R', 'G', 'B', 'R']

# --- repeat(val, n) — repeat a value n times (or forever if n omitted) ---
print(list(itertools.repeat(0, 5)))    # [0, 0, 0, 0, 0]

# --- islice(iter, stop) — lazy slice of an iterator ---
# Unlike list slicing, islice works on ANY iterator (including infinite ones)
gen = (x**2 for x in itertools.count())   # infinite squares
print(list(itertools.islice(gen, 6)))      # [0, 1, 4, 9, 16, 25]

# --- chain(*iterables) — join multiple iterables into one ---
combined = itertools.chain([1,2,3], [4,5,6], [7,8])
print(list(combined))    # [1, 2, 3, 4, 5, 6, 7, 8]

# chain.from_iterable — when you have a list of iterables
nested = [[1,2], [3,4], [5,6]]
flat   = itertools.chain.from_iterable(nested)
print(list(flat))    # [1, 2, 3, 4, 5, 6]

# --- zip_longest — like zip but pads shorter iterables ---
a = [1, 2, 3, 4, 5]
b = ["a", "b", "c"]
print(list(itertools.zip_longest(a, b, fillvalue="?")))
# [(1,'a'), (2,'b'), (3,'c'), (4,'?'), (5,'?')]

# --- takewhile(pred, iter) — take items while condition is True ---
nums = [1, 3, 5, 2, 7, 9]
taken = list(itertools.takewhile(lambda x: x % 2 != 0, nums))
print(taken)    # [1, 3, 5]  — stops as soon as 2 (even) is seen

# --- dropwhile(pred, iter) — skip items while condition is True ---
dropped = list(itertools.dropwhile(lambda x: x % 2 != 0, nums))
print(dropped)    # [2, 7, 9]  — starts from first item that fails condition

# --- groupby — group consecutive items by a key ---
data = [
    {"name": "Alice", "dept": "Eng"},
    {"name": "Bob",   "dept": "Eng"},
    {"name": "Carol", "dept": "HR"},
    {"name": "Dave",  "dept": "HR"},
    {"name": "Eve",   "dept": "Eng"},
]
# ⚠️  groupby requires data to be SORTED by key first
data.sort(key=lambda x: x["dept"])
for dept, members in itertools.groupby(data, key=lambda x: x["dept"]):
    names = [m["name"] for m in members]
    print(f"{dept}: {names}")

# --- combinations and permutations ---
items = [1, 2, 3, 4]
print(list(itertools.combinations(items, 2)))     # order doesn't matter
# [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]

print(list(itertools.permutations(items, 2)))     # order DOES matter
# [(1,2),(1,3),(1,4),(2,1),(2,3)...]

print(list(itertools.combinations_with_replacement([1,2,3], 2)))
# [(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]

# --- product — cartesian product ---
print(list(itertools.product([0,1], repeat=3)))   # all 3-bit binary numbers
# [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)]


# ------------------------------------------------------------
# 9. COMMON PATTERNS
# ------------------------------------------------------------

# Pattern 1: Enumerate with custom start using itertools
import itertools

for i, val in zip(itertools.count(1), ["a","b","c"]):
    print(f"{i}: {val}")    # 1:a  2:b  3:c

# Pattern 2: Pairwise sliding window
def pairwise(iterable):
    """Return successive overlapping pairs."""
    it = iter(iterable)                 # create ONE iterator from the iterable
    a  = next(it)                       # prime with first value
    for b in it:                        # walk the rest of the values
        yield a, b                      # yield current pair
        a = b                           # slide the window forward

for pair in pairwise([1,2,3,4,5]):
    print(pair)    # (1,2) (2,3) (3,4) (4,5)

# Pattern 3: Consume an iterator completely (fast)
import collections
def consume(iterator):
    """Exhaust an iterator in the fastest way possible."""
    collections.deque(iterator, maxlen=0)   # deque with maxlen=0 discards immediately

# Pattern 4: nth item from an iterable
def nth(iterable, n, default=None):
    """Return the nth item, or a default if out of range."""
    return next(itertools.islice(iterable, n, None), default)

print(nth([10,20,30,40], 2))    # 30  (0-indexed)
print(nth([10,20,30], 9, -1))   # -1  (out of range, returns default)

# Pattern 5: Flatten one level
nested = [[1,2,3],[4,5],[6,7,8,9]]
flat = list(itertools.chain.from_iterable(nested))
print(flat)    # [1,2,3,4,5,6,7,8,9]


# ============================================================
# SUMMARY
# ============================================================
# Iterable        → has __iter__, can be looped over (list, str, dict...)
# Iterator        → has __iter__ + __next__, tracks position, one-use
# iter(obj)       → get an iterator from an iterable
# next(it)        → get next value, raises StopIteration when done
# for loop        → calls iter() + next() + catches StopIteration for you
# Custom iterator → implement __iter__ and __next__ on a class
# yield in class  → shortcut — Python auto-creates __next__ for you
# One-use         → iterators exhaust; iterables can make fresh iterators
# itertools       → count, cycle, repeat, islice, chain, zip_longest,
#                   takewhile, dropwhile, groupby, combinations,
#                   permutations, product — all lazy/memory-efficient
# ============================================================