# ============================================================
#  CHAPTER 2 — SETS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A SET?
# ------------------------------------------------------------
# A set is an unordered collection of UNIQUE items.
# - Unordered  → no index, no guaranteed order
# - Unique     → duplicates are automatically removed
# - Mutable    → you can add/remove items
# - Hashable   → items must be immutable (str, int, tuple)
#
# Best used for:
#   → removing duplicates
#   → fast membership testing  O(1)
#   → mathematical set operations (union, intersection...)

fruits  = {"apple", "banana", "cherry"}
numbers = {1, 2, 3, 4, 5}
mixed   = {1, "hello", 3.14, (1, 2)}   # items must be hashable
empty   = set()     # ⚠️  NOT {}  — that creates an empty DICT!

print(type(fruits))   # <class 'set'>
print(type({}))       # <class 'dict'>  ← gotcha!
print(type(set()))    # <class 'set'>   ← correct empty set


# ------------------------------------------------------------
# 2. SETS ARE UNORDERED — no indexing
# ------------------------------------------------------------

s = {"banana", "apple", "cherry"}
print(s)         # order is NOT guaranteed — could be anything
# print(s[0])    ← TypeError: 'set' object is not subscriptable

# Duplicates are silently removed
s = {1, 2, 2, 3, 3, 3, 4}
print(s)    # {1, 2, 3, 4}


# ------------------------------------------------------------
# 3. CREATING SETS
# ------------------------------------------------------------

# From a list — great for removing duplicates
nums_with_dupes = [1, 2, 2, 3, 3, 3, 4]
unique = set(nums_with_dupes)
print(unique)    # {1, 2, 3, 4}

# From a string — unique characters
chars = set("hello")
print(chars)    # {'h', 'e', 'l', 'o'}  (one 'l', not two)

# From a tuple
s = set((1, 2, 3, 2, 1))
print(s)    # {1, 2, 3}

# Set comprehension
squares = {x**2 for x in range(1, 6)}
print(squares)    # {1, 4, 9, 16, 25}

evens = {x for x in range(20) if x % 2 == 0}
print(evens)    # {0, 2, 4, 6, 8, 10, 12, 14, 16, 18}


# ------------------------------------------------------------
# 4. ADDING & REMOVING ITEMS
# ------------------------------------------------------------

fruits = {"apple", "banana"}

# add() — add one item
fruits.add("cherry")
print(fruits)    # {'apple', 'banana', 'cherry'}

# add() is safe — adding a duplicate does nothing
fruits.add("apple")
print(fruits)    # still {'apple', 'banana', 'cherry'}

# update() — add multiple items from any iterable
fruits.update(["date", "elderberry"])
fruits.update({"fig", "grape"})
print(fruits)

# remove() — raises KeyError if item not found
fruits.remove("banana")
# fruits.remove("mango")   ← KeyError!

# discard() — safe remove, no error if not found  ✅ prefer this
fruits.discard("mango")    # no error
fruits.discard("apple")    # removes it silently
print(fruits)

# pop() — removes and returns an ARBITRARY item (unpredictable)
item = fruits.pop()
print(f"Removed: {item}")

# clear() — remove all items
s = {1, 2, 3}
s.clear()
print(s)    # set()


# ------------------------------------------------------------
# 5. MEMBERSHIP TESTING — the #1 reason to use sets
# ------------------------------------------------------------
# Sets use a hash table → O(1) average lookup
# Lists scan every element → O(n) lookup

fruits_set  = {"apple", "banana", "cherry", "date", "elderberry"}
fruits_list = ["apple", "banana", "cherry", "date", "elderberry"]

# Both work, but set is MUCH faster with large data
print("apple" in fruits_set)     # True  O(1)
print("apple" in fruits_list)    # True  O(n)
print("mango" not in fruits_set) # True

# Real-world example: seen items tracker
def has_duplicate(items):
    seen = set()
    for item in items:
        if item in seen:    # O(1) check
            return True
        seen.add(item)
    return False

print(has_duplicate([1, 2, 3, 4]))     # False
print(has_duplicate([1, 2, 3, 1]))     # True


# ------------------------------------------------------------
# 6. SET OPERATIONS — math-style
# ------------------------------------------------------------

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

# Union — all items from BOTH sets  (| or .union())
print(a | b)            # {1, 2, 3, 4, 5, 6, 7, 8}
print(a.union(b))       # same

# Intersection — items in BOTH sets  (& or .intersection())
print(a & b)                   # {4, 5}
print(a.intersection(b))       # same

# Difference — items in a but NOT in b  (- or .difference())
print(a - b)                   # {1, 2, 3}
print(a.difference(b))         # same
print(b - a)                   # {6, 7, 8}  ← order matters!

# Symmetric difference — items in EITHER but NOT BOTH  (^ or .symmetric_difference())
print(a ^ b)                           # {1, 2, 3, 6, 7, 8}
print(a.symmetric_difference(b))       # same


# ------------------------------------------------------------
# 7. SET COMPARISON OPERATORS
# ------------------------------------------------------------

a = {1, 2, 3}
b = {1, 2, 3, 4, 5}
c = {1, 2, 3}

# Subset — is a inside b?
print(a <= b)              # True   a is a subset of b
print(a.issubset(b))       # True

# Proper subset — subset but not equal
print(a < b)               # True   (a != b)
print(a < c)               # False  (a == c)

# Superset — does b contain all of a?
print(b >= a)              # True   b is a superset of a
print(b.issuperset(a))     # True

# Equality
print(a == c)              # True   same items
print(a == b)              # False

# Disjoint — no items in common
print(a.isdisjoint({6, 7, 8}))    # True
print(a.isdisjoint({3, 4, 5}))    # False  (3 is shared)


# ------------------------------------------------------------
# 8. IN-PLACE SET OPERATIONS
# ------------------------------------------------------------

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# |= update with union
a |= b
print(a)    # {1, 2, 3, 4, 5, 6}

a = {1, 2, 3, 4}

# &= update with intersection
a &= b
print(a)    # {3, 4}

a = {1, 2, 3, 4}

# -= update with difference
a -= b
print(a)    # {1, 2}

a = {1, 2, 3, 4}

# ^= update with symmetric difference
a ^= b
print(a)    # {1, 2, 5, 6}


# ------------------------------------------------------------
# 9. FROZENSET — immutable set
# ------------------------------------------------------------
# Like a set but cannot be changed after creation.
# Can be used as dict keys or stored inside other sets.

fs = frozenset([1, 2, 3, 4])
print(fs)           # frozenset({1, 2, 3, 4})
print(2 in fs)      # True
# fs.add(5)         ← AttributeError: no add on frozenset

# Use as dict key
permissions = {
    frozenset(["read"]):            "basic",
    frozenset(["read", "write"]):   "editor",
    frozenset(["read", "write", "admin"]): "admin",
}
user_perms = frozenset(["read", "write"])
print(permissions[user_perms])    # editor


# ------------------------------------------------------------
# 10. COMMON PATTERNS
# ------------------------------------------------------------

# Pattern 1: Remove duplicates from a list
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
unique = list(set(items))
print(unique)    # order not guaranteed

# Preserve order while removing duplicates
seen, unique_ordered = set(), []
for item in items:
    if item not in seen:
        unique_ordered.append(item)
        seen.add(item)
print(unique_ordered)    # [3, 1, 4, 5, 9, 2, 6]

# Pattern 2: Find common items between two lists
list1 = [1, 2, 3, 4, 5]
list2 = [3, 4, 5, 6, 7]
common = list(set(list1) & set(list2))
print(common)    # [3, 4, 5]

# Pattern 3: Find items in one list but not the other
only_in_1 = list(set(list1) - set(list2))
only_in_2 = list(set(list2) - set(list1))
print(only_in_1)    # [1, 2]
print(only_in_2)    # [6, 7]

# Pattern 4: Fast lookup table
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def is_valid_image(filename):
    ext = filename[filename.rfind("."):].lower()
    return ext in VALID_EXTENSIONS    # O(1)

print(is_valid_image("photo.jpg"))    # True
print(is_valid_image("doc.pdf"))      # False

# Pattern 5: Track visited states (e.g. in graph traversal)
def count_unique_chars(s):
    return len(set(s))

print(count_unique_chars("hello"))        # 4
print(count_unique_chars("aabbccddee"))   # 5

# Pattern 6: Check if two strings are anagrams
def is_anagram(s1, s2):
    # character sets alone aren't enough — also need counts
    from collections import Counter
    return Counter(s1) == Counter(s2)

print(is_anagram("listen", "silent"))    # True
print(is_anagram("hello", "world"))      # False


# ------------------------------------------------------------
# 11. TIME COMPLEXITY — know this for interviews
# ------------------------------------------------------------
#
# Operation           | Average | Worst
# ------------------- | ------- | -----
# Add    .add()       |  O(1)   | O(n)
# Remove .remove()    |  O(1)   | O(n)
# Membership  in      |  O(1)   | O(n)
# Union    |          |  O(m+n) |
# Intersection  &     |  O(min) |
# Difference   -      |  O(m)   |
#
# Worst case O(n) only in pathological hash collision scenarios.
# In practice, treat all basic operations as O(1).


# ============================================================
# SUMMARY
# ============================================================
# Create        → {1,2,3}  set()  set(list)  {x for x in ...}
# Empty set     → set()  NOT {}  (that's a dict!)
# Unordered     → no indexing, no slicing
# Unique        → duplicates silently removed
# Add           → .add()  .update()
# Remove        → .discard() safe,  .remove() raises KeyError
# Membership    → in / not in  →  O(1) average
# Union         → a | b   or  a.union(b)
# Intersection  → a & b   or  a.intersection(b)
# Difference    → a - b   or  a.difference(b)
# Sym. diff     → a ^ b   or  a.symmetric_difference(b)
# Subset        → a <= b  or  a.issubset(b)
# Frozenset     → immutable set, can be used as dict key
# ============================================================