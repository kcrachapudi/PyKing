# ============================================================
#  CHAPTER 2 — LISTS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A LIST?
# ------------------------------------------------------------
# A list is an ordered, mutable collection of items.
# - Ordered    → items stay in the order you put them
# - Mutable    → you can change, add, remove items
# - Any type   → items can be anything, even mixed types

numbers = [1, 2, 3, 4, 5]
names   = ["Alice", "Bob", "Charlie"]
mixed   = [1, "hello", 3.14, True, None]   # mixed types allowed
empty   = []                                # empty list
nested  = [[1, 2], [3, 4], [5, 6]]          # list of lists


# ------------------------------------------------------------
# 2. INDEXING — access one item
# ------------------------------------------------------------
#
#  List:     a    p    p    l    e
#  Index:    0    1    2    3    4
#  Negative:-5   -4   -3   -2   -1

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print(fruits[0])     # apple       (first)
print(fruits[2])     # cherry
print(fruits[-1])    # elderberry  (last)
print(fruits[-2])    # date        (second from last)

# Modify by index
fruits[1] = "blueberry"
print(fruits)    # ['apple', 'blueberry', 'cherry', 'date', 'elderberry']

# IndexError — going out of range
# print(fruits[10])   ← IndexError: list index out of range


# ------------------------------------------------------------
# 3. SLICING — extract a portion of the list
# ------------------------------------------------------------
# Syntax: list[start : stop : step]
# start → included, stop → NOT included

nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(nums[2:5])      # [2, 3, 4]        start=2, stop=5
print(nums[:4])       # [0, 1, 2, 3]     from beginning to 4
print(nums[6:])       # [6, 7, 8, 9]     from 6 to end
print(nums[:])        # full copy        entire list
print(nums[::2])      # [0, 2, 4, 6, 8]  every other item
print(nums[1::2])     # [1, 3, 5, 7, 9]  odd indices
print(nums[::-1])     # [9,8,7,6,5,4,3,2,1,0]  reversed
print(nums[7:2:-1])   # [7, 6, 5, 4, 3]  reverse slice

# Slicing never raises IndexError — it just gives what it can
print(nums[0:100])    # [0,1,2,...,9]  safe even if 100 > length


# ------------------------------------------------------------
# 4. ADDING ITEMS
# ------------------------------------------------------------

fruits = ["apple", "banana"]

# append() — add ONE item to the END  O(1)
fruits.append("cherry")
print(fruits)    # ['apple', 'banana', 'cherry']

# insert() — add at a specific index  O(n)
fruits.insert(1, "avocado")
print(fruits)    # ['apple', 'avocado', 'banana', 'cherry']

# extend() — add ALL items from another iterable  O(k)
fruits.extend(["date", "elderberry"])
print(fruits)    # ['apple', 'avocado', 'banana', 'cherry', 'date', 'elderberry']

# + operator — combine two lists into a NEW list
a = [1, 2, 3]
b = [4, 5, 6]
c = a + b
print(c)    # [1, 2, 3, 4, 5, 6]
print(a)    # [1, 2, 3]  ← unchanged

# * operator — repeat a list
print([0] * 5)        # [0, 0, 0, 0, 0]
print(["hi"] * 3)     # ['hi', 'hi', 'hi']


# ------------------------------------------------------------
# 5. REMOVING ITEMS
# ------------------------------------------------------------

fruits = ["apple", "banana", "cherry", "banana", "date"]

# remove() — removes FIRST occurrence of a value  O(n)
fruits.remove("banana")
print(fruits)    # ['apple', 'cherry', 'banana', 'date']

# pop() — removes and RETURNS item at index  O(1) for last, O(n) for others
last = fruits.pop()       # removes last item
print(last)               # date
print(fruits)             # ['apple', 'cherry', 'banana']

item = fruits.pop(0)      # removes item at index 0
print(item)               # apple
print(fruits)             # ['cherry', 'banana']

# del — delete by index or slice
nums = [10, 20, 30, 40, 50]
del nums[1]
print(nums)    # [10, 30, 40, 50]

del nums[1:3]
print(nums)    # [10, 50]

# clear() — remove ALL items
nums.clear()
print(nums)    # []


# ------------------------------------------------------------
# 6. SEARCHING & CHECKING
# ------------------------------------------------------------

fruits = ["apple", "banana", "cherry", "apple"]

# in / not in — membership test  O(n)
print("apple" in fruits)        # True
print("mango" in fruits)        # False
print("mango" not in fruits)    # True

# index() — find position of first occurrence  O(n)
print(fruits.index("apple"))    # 0
print(fruits.index("cherry"))   # 2
# fruits.index("mango")  ← ValueError if not found

# Safe search with in check first
item = "mango"
if item in fruits:
    print(fruits.index(item))
else:
    print(f"{item} not in list")

# count() — count occurrences
print(fruits.count("apple"))    # 2
print(fruits.count("mango"))    # 0


# ------------------------------------------------------------
# 7. SORTING
# ------------------------------------------------------------

nums = [3, 1, 4, 1, 5, 9, 2, 6, 5]

# sort() — sorts IN PLACE, returns None  O(n log n)
nums.sort()
print(nums)    # [1, 1, 2, 3, 4, 5, 5, 6, 9]

nums.sort(reverse=True)
print(nums)    # [9, 6, 5, 5, 4, 3, 2, 1, 1]

# sorted() — returns a NEW sorted list, original unchanged
original = [3, 1, 4, 1, 5]
new_sorted = sorted(original)
print(new_sorted)    # [1, 1, 3, 4, 5]
print(original)      # [3, 1, 4, 1, 5]  ← unchanged

# Sort by key function
words = ["banana", "apple", "fig", "cherry", "date"]
words.sort(key=len)                          # sort by length
print(words)    # ['fig', 'date', 'apple', 'banana', 'cherry']

words.sort(key=str.lower)                    # case-insensitive sort

students = [("Alice", 92), ("Bob", 85), ("Charlie", 95)]
students.sort(key=lambda s: s[1])            # sort by score
print(students)    # [('Bob', 85), ('Alice', 92), ('Charlie', 95)]

students.sort(key=lambda s: s[1], reverse=True)  # highest first

# reverse() — reverses IN PLACE
nums = [1, 2, 3, 4, 5]
nums.reverse()
print(nums)    # [5, 4, 3, 2, 1]


# ------------------------------------------------------------
# 8. LIST COMPREHENSIONS
# ------------------------------------------------------------
# [expression  for  item  in  iterable  if  condition]

# Basic
squares = [x**2 for x in range(1, 6)]
print(squares)    # [1, 4, 9, 16, 25]

# With condition
evens = [x for x in range(20) if x % 2 == 0]
print(evens)    # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Transform
fruits = ["apple", "banana", "cherry"]
upper = [f.upper() for f in fruits]
lengths = [len(f) for f in fruits]
print(upper)     # ['APPLE', 'BANANA', 'CHERRY']
print(lengths)   # [5, 6, 6]

# Nested comprehension
matrix = [[1,2,3],[4,5,6],[7,8,9]]
flat   = [n for row in matrix for n in row]
print(flat)    # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Conditional expression inside comprehension
nums = [1, -2, 3, -4, 5]
abs_vals = [x if x >= 0 else -x for x in nums]
print(abs_vals)    # [1, 2, 3, 4, 5]


# ------------------------------------------------------------
# 9. USEFUL BUILT-IN FUNCTIONS WITH LISTS
# ------------------------------------------------------------

nums = [3, 1, 4, 1, 5, 9, 2, 6]

print(len(nums))      # 8       number of items
print(sum(nums))      # 31      total
print(min(nums))      # 1       smallest
print(max(nums))      # 9       largest
print(sorted(nums))   # sorted copy
print(list(reversed(nums)))   # reversed copy

# enumerate — index + value
for i, val in enumerate(nums):
    print(f"{i}: {val}")

# zip — pair up two lists
names  = ["Alice", "Bob", "Charlie"]
scores = [92, 85, 95]
paired = list(zip(names, scores))
print(paired)    # [('Alice', 92), ('Bob', 85), ('Charlie', 95)]

# any() and all()
nums = [2, 4, 6, 7, 8]
print(any(x % 2 != 0 for x in nums))   # True  (7 is odd)
print(all(x > 0 for x in nums))         # True  (all positive)


# ------------------------------------------------------------
# 10. COPYING LISTS
# ------------------------------------------------------------

original = [1, 2, 3, 4, 5]

# ❌ This is NOT a copy — both variables point to same list
alias = original
alias.append(99)
print(original)    # [1, 2, 3, 4, 5, 99]  ← original changed!

# ✅ Shallow copy — three equivalent ways
copy1 = original.copy()
copy2 = original[:]
copy3 = list(original)

copy1.append(100)
print(original)    # unchanged
print(copy1)       # has 100

# ⚠️  Shallow copy caveat — nested lists are still shared
nested = [[1, 2], [3, 4]]
shallow = nested.copy()
shallow[0].append(99)
print(nested)    # [[1, 2, 99], [3, 4]]  ← inner list was shared!

# ✅ Deep copy — fully independent copy of everything
import copy
deep = copy.deepcopy(nested)
deep[0].append(100)
print(nested)    # [[1, 2, 99], [3, 4]]  ← unchanged this time


# ------------------------------------------------------------
# 11. NESTED LISTS (2D lists / matrices)
# ------------------------------------------------------------

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access: matrix[row][col]
print(matrix[0][0])    # 1   top-left
print(matrix[1][2])    # 6   row 1, col 2
print(matrix[2][2])    # 9   bottom-right

# Loop through
for row in matrix:
    for val in row:
        print(val, end=" ")
    print()

# Create with comprehension
rows, cols = 3, 4
grid = [[0] * cols for _ in range(rows)]
print(grid)    # [[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# ⚠️  Don't create nested lists like this — rows are SHARED:
bad_grid = [[0] * 3] * 3
bad_grid[0][0] = 9
print(bad_grid)    # [[9,0,0],[9,0,0],[9,0,0]]  ← bug!


# ------------------------------------------------------------
# 12. COMMON LIST PATTERNS
# ------------------------------------------------------------

# Pattern 1: Remove duplicates (preserving order)
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
seen, unique = set(), []
for item in items:
    if item not in seen:
        unique.append(item)
        seen.add(item)
print(unique)    # [3, 1, 4, 5, 9, 2, 6]

# Pattern 2: Flatten a nested list
nested = [[1, 2], [3, 4], [5, 6]]
flat = [x for sublist in nested for x in sublist]
print(flat)    # [1, 2, 3, 4, 5, 6]

# Pattern 3: Chunk a list into groups of n
def chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

print(chunk([1,2,3,4,5,6,7], 3))    # [[1,2,3],[4,5,6],[7]]

# Pattern 4: Rotate a list
def rotate(lst, k):
    k = k % len(lst)
    return lst[-k:] + lst[:-k]

print(rotate([1,2,3,4,5], 2))    # [4, 5, 1, 2, 3]

# Pattern 5: Find most frequent item
from collections import Counter
items = [1, 3, 2, 1, 4, 1, 3, 2, 1]
most_common = Counter(items).most_common(1)[0]
print(most_common)    # (1, 4) — value 1 appears 4 times

# Pattern 6: Zip two lists into a dict
keys   = ["name", "age", "city"]
values = ["Alice", 30, "NYC"]
d = dict(zip(keys, values))
print(d)    # {'name': 'Alice', 'age': 30, 'city': 'NYC'}


# ------------------------------------------------------------
# 13. TIME COMPLEXITY — know this for interviews
# ------------------------------------------------------------
#
# Operation               | Time
# ----------------------- | -------
# Access by index  lst[i] | O(1)
# Append to end           | O(1) amortized
# Pop from end            | O(1)
# Insert at index         | O(n)
# Delete at index         | O(n)
# Search (in)             | O(n)
# Sort                    | O(n log n)
# Length  len()           | O(1)
# Slice                   | O(k) where k = slice size
#
# Key insight: lists are fast at the END, slow in the MIDDLE/START.
# If you need fast inserts/deletes at both ends → use collections.deque

from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0)      # O(1) — fast!
dq.popleft()          # O(1) — fast!
print(dq)             # deque([1, 2, 3])


# ============================================================
# SUMMARY
# ============================================================
# Create         → [], list(), [x]*n
# Index          → lst[0], lst[-1]
# Slice          → lst[start:stop:step], lst[::-1]
# Add            → .append(), .insert(), .extend(), +
# Remove         → .remove(), .pop(), del, .clear()
# Search         → in, .index(), .count()
# Sort           → .sort() in-place, sorted() new list
# Comprehension  → [expr for x in iter if cond]
# Built-ins      → len, sum, min, max, sorted, reversed
# Copy           → .copy() / [:] shallow, copy.deepcopy() full
# Nested         → matrix[row][col]
# Complexity     → O(1) access/append, O(n) search/insert
# ============================================================