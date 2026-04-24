# ============================================================
#  CHAPTER 5 — MODULES & IMPORTS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A MODULE?
# ------------------------------------------------------------
# A module is simply a .py file.
# It lets you organize code into reusable pieces.
#
# Three types of modules:
#   Built-in    → comes with Python (os, sys, math, random...)
#   Third-party → installed via pip (requests, pandas, flask...)
#   Your own    → .py files you write yourself


# ------------------------------------------------------------
# 2. IMPORTING MODULES
# ------------------------------------------------------------

# Import the whole module — access with dot notation
import math
print(math.pi)           # 3.141592653589793
print(math.sqrt(16))     # 4.0
print(math.ceil(4.3))    # 5
print(math.floor(4.9))   # 4

import random
print(random.randint(1, 10))        # random int between 1 and 10
print(random.choice(["a","b","c"])) # random item from list
print(random.random())              # float between 0.0 and 1.0

import os
print(os.getcwd())         # current working directory
print(os.path.exists(".")) # True

import sys
print(sys.version)         # Python version string
print(sys.platform)        # 'win32', 'linux', 'darwin'


# ------------------------------------------------------------
# 3. from ... import — import specific names
# ------------------------------------------------------------
# Brings names directly into your namespace.
# No need for module prefix.

from math import pi, sqrt, ceil, floor
print(pi)          # 3.14159...  (no math. prefix)
print(sqrt(25))    # 5.0

from random import randint, choice, shuffle
nums = [1, 2, 3, 4, 5]
shuffle(nums)
print(nums)


# ------------------------------------------------------------
# 4. ALIASES — rename on import
# ------------------------------------------------------------

import numpy as np           # industry standard alias
import pandas as pd          # industry standard alias
import matplotlib.pyplot as plt  # industry standard alias

# For built-ins too
import datetime as dt
from datetime import datetime as DateTime

# Long module names
from collections import defaultdict as dd


# ------------------------------------------------------------
# 5. import * — import everything (avoid this)
# ------------------------------------------------------------
# from math import *    ← imports ALL names from math
# Pollutes your namespace — hard to know where names come from
# Only acceptable in interactive REPL sessions


# ------------------------------------------------------------
# 6. THE STANDARD LIBRARY — most useful modules
# ------------------------------------------------------------

# --- os — operating system interface ---
import os

print(os.getcwd())                          # current directory
os.makedirs("temp_dir", exist_ok=True)      # create directory
print(os.listdir("."))                      # list files in dir
print(os.path.join("folder", "file.txt"))   # safe path joining
print(os.path.exists("temp_dir"))           # True
print(os.path.basename("/home/user/file.txt"))  # file.txt
print(os.path.dirname("/home/user/file.txt"))   # /home/user
print(os.path.splitext("report.pdf"))           # ('report', '.pdf')

# Environment variables
# os.environ.get("HOME", "/default")


# --- sys — system-specific parameters ---
import sys

print(sys.argv)          # command-line arguments list
print(sys.path)          # list of directories Python searches for modules
print(sys.version_info)  # (major, minor, micro, ...)
sys.exit(0)              # exit program with code 0 (comment this out!)


# --- math — mathematical functions ---
import math

print(math.pi)           # 3.14159...
print(math.e)            # 2.71828...
print(math.sqrt(144))    # 12.0
print(math.pow(2, 10))   # 1024.0
print(math.log(100, 10)) # 2.0  (log base 10)
print(math.log2(8))      # 3.0
print(math.sin(math.pi / 2))   # 1.0
print(math.factorial(5))       # 120
print(math.gcd(12, 8))         # 4
print(math.ceil(4.1))          # 5
print(math.floor(4.9))         # 4
print(math.inf)                # infinity
print(math.isfinite(math.inf)) # False


# --- random — random number generation ---
import random

random.seed(42)                      # reproducible results
print(random.randint(1, 100))        # int between 1 and 100 (inclusive)
print(random.uniform(0.0, 1.0))      # float between 0 and 1
print(random.choice([1,2,3,4,5]))    # random element
print(random.choices([1,2,3], k=5))  # k random elements WITH replacement
print(random.sample([1,2,3,4,5], 3)) # 3 unique random elements

deck = list(range(52))
random.shuffle(deck)   # shuffle in place


# --- datetime — dates and times ---
from datetime import datetime, date, timedelta

now  = datetime.now()
today = date.today()

print(now)               # 2024-01-15 14:30:00.123456
print(today)             # 2024-01-15
print(now.year)          # 2024
print(now.month)         # 1
print(now.day)           # 15
print(now.hour)          # 14
print(now.strftime("%Y-%m-%d %H:%M:%S"))   # formatted string
print(now.strftime("%B %d, %Y"))           # January 15, 2024

# Parsing a date string
dt = datetime.strptime("2024-01-15", "%Y-%m-%d")
print(dt)

# Arithmetic with timedelta
tomorrow   = today + timedelta(days=1)
next_week  = today + timedelta(weeks=1)
three_hours_later = now + timedelta(hours=3)

diff = datetime(2025, 1, 1) - now
print(f"Days until 2025: {diff.days}")


# --- collections — specialized data structures ---
from collections import Counter, defaultdict, deque, namedtuple, OrderedDict

# Counter
words = "the cat sat on the mat the cat".split()
c = Counter(words)
print(c)                    # Counter({'the': 3, 'cat': 2, ...})
print(c.most_common(2))     # [('the', 3), ('cat', 2)]

# defaultdict
graph = defaultdict(list)
graph["A"].append("B")      # no KeyError even though "A" didn't exist
graph["A"].append("C")
print(dict(graph))          # {'A': ['B', 'C']}

# deque — fast append/pop from BOTH ends
dq = deque([1, 2, 3])
dq.appendleft(0)    # O(1)
dq.append(4)        # O(1)
dq.popleft()        # O(1)
print(dq)           # deque([1, 2, 3, 4])

# deque as fixed-size sliding window
window = deque(maxlen=3)
for n in range(6):
    window.append(n)
    print(list(window))

# namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(p.x, p.y)     # 10 20


# --- itertools — powerful iteration tools ---
import itertools

# chain — combine multiple iterables
combined = list(itertools.chain([1,2,3], [4,5,6], [7,8]))
print(combined)    # [1,2,3,4,5,6,7,8]

# combinations — unique combinations
print(list(itertools.combinations([1,2,3,4], 2)))
# [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]

# permutations
print(list(itertools.permutations([1,2,3], 2)))

# product — cartesian product
print(list(itertools.product([0,1], repeat=3)))
# all 3-bit binary numbers

# groupby — group consecutive items
data = [("A",1),("A",2),("B",3),("B",4),("C",5)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))

# islice — lazy slice of any iterator
first5 = list(itertools.islice(itertools.count(0), 5))
print(first5)    # [0, 1, 2, 3, 4]


# --- functools — higher-order function utilities ---
import functools

# lru_cache — memoize expensive function calls
@functools.lru_cache(maxsize=128)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

print(fib(50))    # fast because results are cached
print(fib.cache_info())

# reduce — apply function cumulatively
product = functools.reduce(lambda x, y: x * y, [1,2,3,4,5])
print(product)    # 120

# partial — fix some arguments of a function
def power(base, exp):
    return base ** exp

square = functools.partial(power, exp=2)
cube   = functools.partial(power, exp=3)
print(square(5))   # 25
print(cube(3))     # 27


# --- json — encode/decode JSON ---
import json

# Python dict → JSON string
data = {"name": "Alice", "age": 30, "scores": [95, 87, 92]}
json_str = json.dumps(data)
print(json_str)             # '{"name": "Alice", "age": 30, ...}'

pretty = json.dumps(data, indent=2)
print(pretty)

# JSON string → Python dict
parsed = json.loads(json_str)
print(parsed["name"])    # Alice

# Write JSON to file
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Read JSON from file
with open("data.json", "r") as f:
    loaded = json.load(f)
print(loaded)


# --- re — regular expressions ---
import re

text = "My phone is 555-1234 and backup is 555-5678"

# Search for first match
match = re.search(r"\d{3}-\d{4}", text)
if match:
    print(match.group())    # 555-1234

# Find ALL matches
phones = re.findall(r"\d{3}-\d{4}", text)
print(phones)    # ['555-1234', '555-5678']

# Substitution
cleaned = re.sub(r"\d{3}-\d{4}", "XXX-XXXX", text)
print(cleaned)    # "My phone is XXX-XXXX and backup is XXX-XXXX"

# Split on pattern
parts = re.split(r"\s+", "hello   world  python")
print(parts)    # ['hello', 'world', 'python']

# Compile for reuse
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
emails = email_pattern.findall("Contact alice@example.com or bob@test.org")
print(emails)    # ['alice@example.com', 'bob@test.org']


# --- pathlib — modern file path handling ---
from pathlib import Path

p = Path(".")                          # current directory
print(p.resolve())                     # absolute path
print(list(p.iterdir()))               # list contents

# Build paths safely (works on Windows AND Linux/Mac)
config = Path.home() / ".config" / "myapp" / "settings.json"
print(config)

# File operations
p = Path("test.txt")
p.write_text("Hello, World!")          # write
content = p.read_text()                # read
print(content)
p.unlink()                             # delete

# Directory operations
d = Path("new_folder")
d.mkdir(exist_ok=True)
print(d.exists())     # True
print(d.is_dir())     # True

# Glob patterns
for py_file in Path(".").glob("*.py"):
    print(py_file.name)


# ------------------------------------------------------------
# 7. WRITING YOUR OWN MODULES
# ------------------------------------------------------------
# Any .py file is a module. Just import it.

# math_utils.py  (imagine this is a separate file)
# ------------------------------------------------
# def add(a, b):
#     return a + b
#
# def multiply(a, b):
#     return a * b
#
# PI = 3.14159
# ------------------------------------------------

# main.py
# import math_utils
# print(math_utils.add(2, 3))     # 5
# print(math_utils.PI)            # 3.14159

# from math_utils import add, PI
# print(add(2, 3))    # 5


# ------------------------------------------------------------
# 8. if __name__ == "__main__"
# ------------------------------------------------------------
# When Python runs a file directly:  __name__ == "__main__"
# When Python imports the file:      __name__ == "module_name"
#
# This lets you write code that runs ONLY when executed directly,
# not when imported.

def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

if __name__ == "__main__":
    # This block runs ONLY when you do: python 01_modules_and_imports.py
    # It does NOT run when another file does: import this_module
    print(greet("World"))
    print(add(2, 3))
    print("Running as main script!")


# ------------------------------------------------------------
# 9. PACKAGES — directories of modules
# ------------------------------------------------------------
# A package is a folder with an __init__.py file.
#
# my_package/
#   __init__.py         ← makes it a package (can be empty)
#   utils.py
#   models.py
#   helpers/
#     __init__.py
#     string_utils.py
#
# Importing from a package:
# import my_package.utils
# from my_package.utils import my_function
# from my_package.helpers.string_utils import clean


# ============================================================
# SUMMARY
# ============================================================
# import module              → full module, use module.name
# from module import name    → specific name, no prefix
# import module as alias     → shorter name
# Standard library           → no install needed
#   os        → filesystem, env vars
#   sys       → interpreter, args
#   math      → math functions
#   random    → random numbers
#   datetime  → dates and times
#   collections → Counter, defaultdict, deque
#   itertools → combinations, chain, product
#   functools → lru_cache, partial, reduce
#   json      → encode/decode JSON
#   re        → regular expressions
#   pathlib   → modern file paths
# if __name__ == "__main__"  → run only when executed directly
# package    → folder with __init__.py
# ============================================================