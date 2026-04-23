# ============================================================
#  CHAPTER 2 — TUPLES
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A TUPLE?
# ------------------------------------------------------------
# A tuple is an ordered, IMMUTABLE collection of items.
# - Ordered    → items stay in the order you put them
# - Immutable  → cannot be changed after creation
# - Any type   → items can be anything, even mixed types
#
# Think of a tuple as a "sealed list" — use it when the
# data should NOT change: coordinates, RGB colors, DB records.

point       = (10, 20)
rgb         = (255, 128, 0)
person      = ("Alice", 30, "NYC")
mixed       = (1, "hello", 3.14, True)
empty       = ()
single      = (42,)      # ⚠️  trailing comma makes it a tuple!
not_a_tuple = (42)       # this is just an int in parentheses
nested      = ((1, 2), (3, 4), (5, 6))

print(type(single))      # <class 'tuple'>
print(type(not_a_tuple)) # <class 'int'>  ← gotcha!

# You can also create without parentheses — packing
coords = 10, 20
print(type(coords))      # <class 'tuple'>


# ------------------------------------------------------------
# 2. INDEXING & SLICING — same as lists
# ------------------------------------------------------------

person = ("Alice", 30, "NYC", "Engineer")

# Indexing
print(person[0])     # Alice
print(person[-1])    # Engineer
print(person[1])     # 30

# Slicing — returns a new tuple
print(person[1:3])   # (30, 'NYC')
print(person[:2])    # ('Alice', 30)
print(person[::-1])  # ('Engineer', 'NYC', 30, 'Alice')

# ⚠️  Cannot modify by index
# person[0] = "Bob"   ← TypeError: 'tuple' object does not support item assignment


# ------------------------------------------------------------
# 3. TUPLE UNPACKING — the most used tuple feature
# ------------------------------------------------------------
# Assign each item to a separate variable in one line.

point = (10, 20)
x, y = point
print(x)    # 10
print(y)    # 20

# Unpack any number of items
name, age, city = ("Alice", 30, "NYC")
print(name, age, city)

# Swap variables — uses tuple packing/unpacking under the hood
a, b = 1, 2
a, b = b, a
print(a, b)    # 2 1

# Extended unpacking with * — capture the "rest"
first, *rest = (1, 2, 3, 4, 5)
print(first)    # 1
print(rest)     # [2, 3, 4, 5]  ← rest becomes a list

*start, last = (1, 2, 3, 4, 5)
print(start)    # [1, 2, 3, 4]
print(last)     # 5

first, *middle, last = (1, 2, 3, 4, 5)
print(first)     # 1
print(middle)    # [2, 3, 4]
print(last)      # 5

# Ignore values with _ (convention for "don't care")
name, _, city = ("Alice", 30, "NYC")   # ignore age
print(name, city)    # Alice NYC

# Unpack nested tuples
point_3d = ((1, 2), 3)
(x, y), z = point_3d
print(x, y, z)    # 1 2 3


# ------------------------------------------------------------
# 4. TUPLE METHODS — only two
# ------------------------------------------------------------
# Tuples are immutable so there are only two methods.

t = (1, 3, 2, 1, 4, 1, 5)

# count() — how many times a value appears
print(t.count(1))    # 3

# index() — position of first occurrence
print(t.index(4))    # 4
# t.index(99)  ← ValueError if not found


# ------------------------------------------------------------
# 5. SEARCHING & CHECKING
# ------------------------------------------------------------

person = ("Alice", 30, "NYC")

print("Alice" in person)      # True
print("Bob" in person)        # False
print("Bob" not in person)    # True
print(len(person))            # 3
print(min((3, 1, 4, 1, 5)))   # 1
print(max((3, 1, 4, 1, 5)))   # 5
print(sum((1, 2, 3, 4)))      # 10


# ------------------------------------------------------------
# 6. TUPLES ARE HASHABLE — can be used as dict keys
# ------------------------------------------------------------
# Lists CANNOT be dict keys (mutable = unhashable).
# Tuples CAN because they are immutable.

# ✅ Tuple as dict key
grid = {}
grid[(0, 0)] = "start"
grid[(3, 4)] = "checkpoint"
grid[(9, 9)] = "end"
print(grid[(3, 4)])    # checkpoint

# ✅ Tuples in a set
visited = set()
visited.add((0, 0))
visited.add((1, 2))
visited.add((0, 0))    # duplicate — ignored
print(visited)    # {(0, 0), (1, 2)}

# ❌ List as dict key — TypeError
# d = {}
# d[[1, 2]] = "value"   ← TypeError: unhashable type: 'list'


# ------------------------------------------------------------
# 7. TUPLE vs LIST — when to use which
# ------------------------------------------------------------
#
# Use TUPLE when:
#   ✅ Data is fixed and should not change
#   ✅ You need it as a dict key or in a set
#   ✅ Returning multiple values from a function
#   ✅ Representing a record (name, age, city)
#   ✅ Slightly more memory-efficient than a list
#
# Use LIST when:
#   ✅ Data will change (append, remove, sort)
#   ✅ You're building up a collection over time
#   ✅ You need list-specific methods

import sys
lst = [1, 2, 3, 4, 5]
tpl = (1, 2, 3, 4, 5)
print(sys.getsizeof(lst))    # 104 bytes (may vary)
print(sys.getsizeof(tpl))    # 80 bytes  ← tuples are smaller


# ------------------------------------------------------------
# 8. RETURNING MULTIPLE VALUES FROM A FUNCTION
# ------------------------------------------------------------
# Python functions can "return multiple values" —
# they actually return a tuple.

def min_max(numbers):
    return min(numbers), max(numbers)    # returns a tuple

result = min_max([3, 1, 9, 2, 7])
print(result)         # (1, 9)
print(type(result))   # <class 'tuple'>

# Unpack directly
lo, hi = min_max([3, 1, 9, 2, 7])
print(lo, hi)    # 1 9

def divide(a, b):
    if b == 0:
        return None, "Division by zero"
    return a / b, None    # (result, error)

value, error = divide(10, 2)
print(value, error)    # 5.0 None

value, error = divide(10, 0)
print(value, error)    # None Division by zero


# ------------------------------------------------------------
# 9. CONVERTING BETWEEN TUPLE AND LIST
# ------------------------------------------------------------

# tuple → list (to modify it)
t = (1, 2, 3)
lst = list(t)
lst.append(4)
t = tuple(lst)
print(t)    # (1, 2, 3, 4)

# list → tuple (to make it hashable)
lst = [1, 2, 3]
t = tuple(lst)
print(t)    # (1, 2, 3)

# String → tuple of characters
t = tuple("hello")
print(t)    # ('h', 'e', 'l', 'l', 'o')


# ------------------------------------------------------------
# 10. NAMED TUPLES — tuples with named fields
# ------------------------------------------------------------
# A great way to make tuples readable without full classes.

from collections import namedtuple

# Define the structure
Point   = namedtuple("Point", ["x", "y"])
Person  = namedtuple("Person", ["name", "age", "city"])
Card    = namedtuple("Card", ["rank", "suit"])

# Create instances
p = Point(10, 20)
print(p.x, p.y)      # 10 20   ← access by name
print(p[0], p[1])    # 10 20   ← also works by index

alice = Person("Alice", 30, "NYC")
print(alice.name)    # Alice
print(alice.age)     # 30

# Still immutable
# alice.age = 31   ← AttributeError

# Useful for database rows, CSV records
Row = namedtuple("Row", ["id", "name", "score"])
rows = [
    Row(1, "Alice", 92),
    Row(2, "Bob", 85),
    Row(3, "Charlie", 95),
]
for row in rows:
    print(f"{row.name}: {row.score}")


# ------------------------------------------------------------
# 11. COMMON PATTERNS
# ------------------------------------------------------------

# Pattern 1: Swap two variables
a, b = 10, 20
a, b = b, a
print(a, b)    # 20 10

# Pattern 2: Iterate list of tuples
students = [("Alice", 92), ("Bob", 85), ("Charlie", 95)]
for name, score in students:        # tuple unpacking in for loop
    print(f"{name}: {score}")

# Important note: if you do for name in students, 
# name will be the whole tuple ('Alice', 92) — not what you want! 
# Always unpack in the loop header when iterating tuples.
for name in students:        # wrong tuple unpacking in for loop
    print(f"{name}: {score}") # name is the whole tuple, 
# EVEN WORSE:  score is from previous for loop iteration (last value 95)
# This is because for loop leak variables into the surrounding scope. 
# Always unpack in the loop header to avoid this issue.

# Pattern 3: Sort list of tuples
students.sort(key=lambda s: s[1], reverse=True)
print(students)    # Charlie first (95)

# Pattern 4: Use tuple as compound dict key
scores = {}
scores[("Alice", "Math")] = 92
scores[("Alice", "Science")] = 88
scores[("Bob", "Math")] = 79
print(scores[("Alice", "Math")])    # 92

# Pattern 5: Enumerate with unpacking
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, 1):    # enumerate returns tuples
    print(f"{i}. {fruit}")

# Pattern 6: zip returns tuples
names  = ["Alice", "Bob"]
scores = [92, 85]
for pair in zip(names, scores):     # pair is a tuple
    print(pair)    # ('Alice', 92)  ('Bob', 85)


# ============================================================
# SUMMARY
# ============================================================
# Create        → (1,2,3)  (x,)  for single item
# Immutable     → cannot change after creation
# Indexing      → t[0], t[-1]
# Slicing       → t[start:stop:step]
# Unpacking     → a, b = (1, 2)
# Extended      → first, *rest = t
# Methods       → .count(), .index()  (only two!)
# Hashable      → can be dict key or in a set
# vs List       → tuple=fixed/hashable, list=mutable/flexible
# Multi-return  → return a, b  →  actually returns a tuple
# namedtuple    → readable field access by name
# ============================================================