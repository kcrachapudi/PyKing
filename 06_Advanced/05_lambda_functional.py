# ============================================================
#  CHAPTER 6 — LAMBDA & FUNCTIONAL PROGRAMMING
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS FUNCTIONAL PROGRAMMING?
# ------------------------------------------------------------
# Functional programming (FP) is a style of writing code where:
#   → You build programs by composing FUNCTIONS together
#   → Functions are treated as VALUES (pass them, return them)
#   → You avoid changing state / mutating data
#   → You prefer expressions over statements
#
# Python is NOT a purely functional language, but it borrows
# many FP ideas that make code shorter and more expressive.
#
# Key FP tools in Python:
#   lambda, map(), filter(), reduce(), zip(), sorted() with key,
#   functools.partial, functools.reduce, closures


# ------------------------------------------------------------
# 2. LAMBDA — anonymous one-line functions
# ------------------------------------------------------------
# Syntax:  lambda  parameters  :  expression
#
# Lambda is just a shorthand way to write a simple function.
# It has NO name, NO return statement (expression IS the return),
# and can only contain a SINGLE EXPRESSION (no if/else blocks,
# no multiple lines, no assignments).

# Regular function
def square(x):
    return x ** 2

# Equivalent lambda
square = lambda x: x ** 2      # lambda x  →  takes one arg called x
                                # : x ** 2  →  evaluates and returns this

print(square(5))    # 25

# Multiple parameters
add   = lambda a, b: a + b
power = lambda base, exp: base ** exp
clamp = lambda val, lo, hi: max(lo, min(hi, val))  # keep val between lo and hi

print(add(3, 4))          # 7
print(power(2, 10))       # 1024
print(clamp(15, 0, 10))   # 10  (15 is clamped down to max of 10)

# Default parameter
greet = lambda name, greeting="Hello": f"{greeting}, {name}!"
print(greet("Alice"))           # Hello, Alice!
print(greet("Bob", "Hi"))       # Hi, Bob!

# No parameters
get_pi = lambda: 3.14159
print(get_pi())    # 3.14159

# ⚠️  When NOT to use lambda:
#   - If you need more than one expression → use def
#   - If you assign it to a name and reuse it → use def (more readable)
#   - If it needs a docstring → use def
# Lambda shines when used INLINE and thrown away after one use.


# ------------------------------------------------------------
# 3. WHERE LAMBDA IS MOST USEFUL — as a key function
# ------------------------------------------------------------
# The most common real use of lambda is as the 'key=' argument
# in sort(), sorted(), min(), max(), groupby(), etc.

# Sort a list of strings by LENGTH
words = ["banana", "apple", "fig", "cherry", "date"]
words.sort(key=lambda w: len(w))          # sort by length of each word
print(words)    # ['fig', 'date', 'apple', 'banana', 'cherry']

# Sort in reverse (longest first)
words.sort(key=lambda w: len(w), reverse=True)
print(words)    # ['banana', 'cherry', 'apple', 'date', 'fig']

# Sort a list of dicts by a specific field
students = [
    {"name": "Charlie", "grade": 88},
    {"name": "Alice",   "grade": 95},
    {"name": "Bob",     "grade": 72},
]
students.sort(key=lambda s: s["grade"])           # sort by grade, low to high
print([s["name"] for s in students])              # ['Bob', 'Charlie', 'Alice']

students.sort(key=lambda s: s["grade"], reverse=True)  # high to low
print([s["name"] for s in students])              # ['Alice', 'Charlie', 'Bob']

# Sort by multiple fields — return a tuple as the key
people = [
    ("Alice", 30), ("Bob", 25), ("Charlie", 30), ("Diana", 25)
]
# Sort by age first, then alphabetically by name within same age
people.sort(key=lambda p: (p[1], p[0]))   # tuple: (age, name)
print(people)    # [('Bob', 25), ('Diana', 25), ('Alice', 30), ('Charlie', 30)]

# Find min/max with a custom key
scores = [("Alice", 92), ("Bob", 85), ("Charlie", 95)]
best  = max(scores, key=lambda s: s[1])    # person with highest score
worst = min(scores, key=lambda s: s[1])    # person with lowest score
print(best)     # ('Charlie', 95)
print(worst)    # ('Bob', 85)


# ------------------------------------------------------------
# 4. map() — apply a function to every item
# ------------------------------------------------------------
# map(function, iterable)
# Returns a MAP OBJECT (lazy iterator) — use list() to see results.
# Applies 'function' to each item in 'iterable'.

numbers = [1, 2, 3, 4, 5]

# Apply a function to every element
squares = list(map(lambda x: x**2, numbers))
print(squares)    # [1, 4, 9, 16, 25]

# map with a regular function (not just lambda)
def double(x):
    return x * 2

doubled = list(map(double, numbers))
print(doubled)    # [2, 4, 6, 8, 10]

# map with built-in functions
words = ["  hello  ", "  world  ", "  python  "]
stripped = list(map(str.strip, words))    # apply str.strip to each word
print(stripped)    # ['hello', 'world', 'python']

strings = ["1", "2", "3", "4"]
integers = list(map(int, strings))       # convert each string to int
print(integers)    # [1, 2, 3, 4]

# map with two iterables — function receives one item from each
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))   # 1+10, 2+20, 3+30
print(sums)    # [11, 22, 33]

# ⚠️  In modern Python, list comprehensions are usually preferred over map:
# map:            list(map(lambda x: x**2, numbers))
# comprehension:  [x**2 for x in numbers]           ← more readable
# Both are valid — know both for interviews


# ------------------------------------------------------------
# 5. filter() — keep only items that pass a test
# ------------------------------------------------------------
# filter(function, iterable)
# Returns a FILTER OBJECT (lazy iterator).
# Keeps items where function(item) returns True.

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)    # [2, 4, 6, 8, 10]

# Keep only positive numbers
mixed = [-3, -1, 0, 2, 5, -2, 8]
positives = list(filter(lambda x: x > 0, mixed))
print(positives)    # [2, 5, 8]

# Filter with a regular function
def is_long(word):
    return len(word) > 4    # True if word has more than 4 characters

words = ["hi", "hello", "cat", "python", "go", "world"]
long_words = list(filter(is_long, words))
print(long_words)    # ['hello', 'python', 'world']

# filter with None — removes all falsy values
data = [0, 1, "", "hello", None, [], [1,2], False, True]
truthy = list(filter(None, data))    # None as function = keep truthy items
print(truthy)    # [1, 'hello', [1, 2], True]

# Again — comprehension equivalent (often clearer):
# filter:        list(filter(lambda x: x % 2 == 0, numbers))
# comprehension: [x for x in numbers if x % 2 == 0]


# ------------------------------------------------------------
# 6. reduce() — collapse an iterable to a single value
# ------------------------------------------------------------
# reduce(function, iterable, initial?)
# Applies function cumulatively: result = f(f(f(a,b),c),d)...
# Must import from functools — not a built-in anymore.

from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum — apply addition cumulatively
# Step 1: f(1, 2) = 3
# Step 2: f(3, 3) = 6
# Step 3: f(6, 4) = 10
# Step 4: f(10,5) = 15
total = reduce(lambda acc, x: acc + x, numbers)
print(total)    # 15   (same as sum(numbers) but shows the concept)

# Product — multiply all numbers together
product = reduce(lambda acc, x: acc * x, numbers)
print(product)    # 120  (1*2*3*4*5)

# Find maximum manually using reduce
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)    # 5

# Flatten a list of lists using reduce
nested = [[1,2], [3,4], [5,6]]
flat = reduce(lambda acc, lst: acc + lst, nested, [])
# initial [] + [1,2] = [1,2]
# [1,2] + [3,4]      = [1,2,3,4]
# [1,2,3,4] + [5,6]  = [1,2,3,4,5,6]
print(flat)    # [1, 2, 3, 4, 5, 6]

# With initial value
total = reduce(lambda acc, x: acc + x, numbers, 100)  # start from 100
print(total)    # 115   (100 + 1+2+3+4+5)

# ⚠️  For most common cases, prefer built-ins:
# sum(), max(), min(), any(), all() — clearer than reduce


# ------------------------------------------------------------
# 7. zip() — combine multiple iterables
# ------------------------------------------------------------
# zip(iter1, iter2, ...) pairs up items at matching positions.
# Returns a ZIP OBJECT (lazy iterator).
# Stops at the SHORTEST iterable.

names  = ["Alice", "Bob", "Charlie"]
scores = [92, 85, 95]
grades = ["A",  "B",  "A"]

# Pair up three lists
for name, score, grade in zip(names, scores, grades):
    print(f"{name}: {score} ({grade})")

# Convert to list of tuples
pairs = list(zip(names, scores))
print(pairs)    # [('Alice', 92), ('Bob', 85), ('Charlie', 95)]

# Build a dict from two lists — very common pattern
student_dict = dict(zip(names, scores))
print(student_dict)    # {'Alice': 92, 'Bob': 85, 'Charlie': 95}

# Unzip — transpose a list of pairs back into two separate lists
pairs = [("Alice", 92), ("Bob", 85), ("Charlie", 95)]
names_out, scores_out = zip(*pairs)    # * unpacks the list into arguments
print(list(names_out))     # ['Alice', 'Bob', 'Charlie']
print(list(scores_out))    # [92, 85, 95]

# Transpose a matrix (rows become columns, columns become rows)
matrix = [[1,2,3],
          [4,5,6],
          [7,8,9]]
transposed = list(zip(*matrix))        # * unpacks rows as arguments to zip
print(transposed)    # [(1,4,7), (2,5,8), (3,6,9)]


# ------------------------------------------------------------
# 8. CLOSURES — functions that capture their environment
# ------------------------------------------------------------
# A closure is an inner function that REMEMBERS variables
# from its outer scope even after the outer function has returned.

def make_adder(n):
    """Returns a function that adds n to its argument."""
    def adder(x):
        return x + n    # 'n' is captured from the outer scope
    return adder        # return the inner function (not its result)

add5  = make_adder(5)    # n=5 is "locked in" to add5
add10 = make_adder(10)   # n=10 is "locked in" to add10

print(add5(3))    # 8   (3 + 5)
print(add10(3))   # 13  (3 + 10)
print(add5(7))    # 12  (7 + 5)

# Inspect what a closure has captured
print(add5.__closure__[0].cell_contents)    # 5  ← the captured value

# Closures for creating configurable functions
def make_validator(min_val, max_val):
    def validate(x):
        return min_val <= x <= max_val    # captures min_val and max_val
    return validate

is_valid_age   = make_validator(0, 150)
is_valid_score = make_validator(0, 100)
is_valid_temp  = make_validator(-273.15, 1e6)

print(is_valid_age(25))       # True
print(is_valid_score(105))    # False
print(is_valid_temp(-300))    # False

# ⚠️  Classic closure gotcha in loops
# All closures share the SAME variable, not a copy of its value
funcs_bad = []
for i in range(5):
    funcs_bad.append(lambda: i)    # all capture 'i' by REFERENCE

print([f() for f in funcs_bad])    # [4, 4, 4, 4, 4]  ← all see final i=4!

# Fix: capture the value using a default argument
funcs_good = []
for i in range(5):
    funcs_good.append(lambda x=i: x)    # x=i captures current VALUE of i

print([f() for f in funcs_good])    # [0, 1, 2, 3, 4]  ✅


# ------------------------------------------------------------
# 9. functools.partial — pre-fill function arguments
# ------------------------------------------------------------
# partial(func, *args, **kwargs) creates a new function with
# some arguments already filled in (partial application).

from functools import partial

def power(base, exponent):
    return base ** exponent

# Create specialized versions with one argument fixed
square = partial(power, exponent=2)    # exponent is always 2
cube   = partial(power, exponent=3)    # exponent is always 3

print(square(5))     # 25
print(cube(3))       # 27
print(square(10))    # 100

# partial with positional arg
def log(level, message):
    print(f"[{level}] {message}")

info    = partial(log, "INFO")     # level is always "INFO"
warning = partial(log, "WARNING")  # level is always "WARNING"
error   = partial(log, "ERROR")    # level is always "ERROR"

info("Server started")           # [INFO] Server started
warning("Low disk space")        # [WARNING] Low disk space
error("Connection failed")       # [ERROR] Connection failed

# partial is great for callbacks and event handlers
import functools

def process(data, multiplier, offset):
    return [x * multiplier + offset for x in data]

# Create a specialized processor for a specific use case
normalize = partial(process, multiplier=1/255, offset=0)  # scale to 0-1
print(normalize([0, 128, 255]))    # [0.0, 0.502, 1.0]


# ------------------------------------------------------------
# 10. COMPOSING FUNCTIONS
# ------------------------------------------------------------
# Function composition: apply one function, then pass result to another.
# compose(f, g)(x) = f(g(x))

def compose(*funcs):
    """Compose multiple functions right-to-left: compose(f,g,h)(x) = f(g(h(x)))"""
    def composed(x):
        result = x
        for func in reversed(funcs):    # apply from right to left
            result = func(result)        # each function's output is next function's input
        return result
    return composed

# Build a text processing pipeline by composing functions
strip   = str.strip                         # remove whitespace
lower   = str.lower                         # lowercase
def remove_punct(s):
    return s.replace(".", "").replace(",", "").replace("!", "")

clean_text = compose(lower, strip, remove_punct)  # applied right to left
print(clean_text("  Hello, World!  "))    # "hello world"


# ------------------------------------------------------------
# 11. COMMON FUNCTIONAL PATTERNS
# ------------------------------------------------------------

# Pattern 1: Transform and filter in one pass
data = [1, -2, 3, -4, 5, -6]
positive_squares = [x**2 for x in data if x > 0]   # filter then transform
print(positive_squares)    # [1, 9, 25]

# Pattern 2: Group items using a key function
from itertools import groupby

words = ["ant","bear","cat","deer","emu","fox"]
words.sort(key=lambda w: len(w))   # must sort first for groupby to work
for length, group in groupby(words, key=lambda w: len(w)):
    print(f"Length {length}: {list(group)}")

# Pattern 3: Apply different functions based on a condition
def process_value(x):
    transform = (lambda v: v * 2) if x > 0 else (lambda v: abs(v))
    return transform(x)    # apply the chosen function

print([process_value(x) for x in [-3, 0, 4, -1, 5]])  # [3, 0, 8, 1, 10]

# Pattern 4: Build a pipeline of transformations
pipeline = [
    lambda x: x * 2,      # step 1: double
    lambda x: x + 10,     # step 2: add 10
    lambda x: x ** 2,     # step 3: square
]

def run_pipeline(value, steps):
    """Apply each transformation in order."""
    result = value
    for step in steps:         # apply each function one by one
        result = step(result)  # output of one step is input to the next
    return result

print(run_pipeline(3, pipeline))    # ((3*2)+10)^2 = 16^2 = 256

# Pattern 5: Memoize with a dict (manual caching)
def memoized(func):
    cache = {}
    return lambda *args: cache.setdefault(args, func(*args))
    # setdefault(key, default): if key exists return its value,
    # if not, set it to default and return default


# ============================================================
# SUMMARY
# ============================================================
# lambda              → lambda params: expression  (one-liner function)
# Best for            → key= argument in sort/min/max, inline callbacks
# map(f, iter)        → apply f to every item → lazy iterator
# filter(f, iter)     → keep items where f(item) is True → lazy iterator
# reduce(f, iter)     → fold iterable to one value (import from functools)
# zip(a, b)           → pair up items from multiple iterables
# dict(zip(k,v))      → build dict from two lists
# zip(*pairs)         → unzip / transpose
# Closure             → inner function that captures outer scope variables
# Closure gotcha      → loop variable captured by reference, use default arg
# partial(f, **kw)    → pre-fill some arguments of a function
# Composition         → chain functions: output of one → input of next
# ============================================================