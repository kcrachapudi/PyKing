# ============================================================
#  CHAPTER 2 — DICTIONARIES
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A DICTIONARY?
# ------------------------------------------------------------
# A dictionary stores data as KEY : VALUE pairs.
# - Keys must be unique and hashable (str, int, tuple)
# - Values can be anything — any type, any structure
# - Ordered (Python 3.7+) → insertion order is preserved
# - Mutable → you can add, change, remove pairs
#
# Think of it as a real dictionary:
#   word (key) → definition (value)

person = {
    "name": "Alice",
    "age": 30,
    "city": "NYC"
}

empty = {}
empty = dict()    # same thing

# Different key types
mixed_keys = {
    1:       "integer key",
    "name":  "string key",
    (0, 1):  "tuple key",    # tuples are hashable ✅
    # [1,2]: "list key"      # ← TypeError: lists are NOT hashable
}


# ------------------------------------------------------------
# 2. ACCESSING VALUES
# ------------------------------------------------------------

person = {"name": "Alice", "age": 30, "city": "NYC"}

# Direct access — raises KeyError if key doesn't exist
print(person["name"])    # Alice
print(person["age"])     # 30
# print(person["email"]) ← KeyError!

# .get() — safe access, returns None (or default) if missing
print(person.get("name"))           # Alice
print(person.get("email"))          # None   ← no error
print(person.get("email", "N/A"))   # N/A    ← custom default

# Always prefer .get() when the key might not exist
email = person.get("email", "no email provided")
print(email)    # no email provided


# ------------------------------------------------------------
# 3. ADDING & UPDATING ITEMS
# ------------------------------------------------------------

person = {"name": "Alice", "age": 30}

# Add a new key
person["city"] = "NYC"
print(person)    # {'name': 'Alice', 'age': 30, 'city': 'NYC'}

# Update an existing key
person["age"] = 31
print(person["age"])    # 31

# update() — add/overwrite multiple keys at once
person.update({"email": "alice@example.com", "age": 32})
print(person)

# update() also accepts keyword arguments
person.update(phone="555-1234", country="USA")
print(person)

# setdefault() — set a value ONLY if key doesn't exist yet
person.setdefault("city", "Unknown")    # city already exists → no change
person.setdefault("nickname", "Ali")    # doesn't exist → sets it
print(person["city"])       # NYC     ← unchanged
print(person["nickname"])   # Ali     ← newly set


# ------------------------------------------------------------
# 4. REMOVING ITEMS
# ------------------------------------------------------------

person = {"name": "Alice", "age": 30, "city": "NYC", "email": "a@b.com"}

# pop() — remove by key and RETURN the value
age = person.pop("age")
print(age)       # 30
print(person)    # age is gone

# pop() with default — no KeyError if missing
val = person.pop("phone", "not found")
print(val)    # not found

# del — remove by key, no return value
del person["email"]
print(person)

# popitem() — removes and returns the LAST inserted (key, value) pair
last = person.popitem()
print(last)     # ('city', 'NYC')  — last inserted pair

# clear() — remove everything
d = {"a": 1, "b": 2}
d.clear()
print(d)    # {}


# ------------------------------------------------------------
# 5. LOOPING THROUGH A DICTIONARY
# ------------------------------------------------------------

scores = {"Alice": 92, "Bob": 85, "Charlie": 95, "Diana": 88}

# Loop over keys (default)
for name in scores:
    print(name)

# Loop over values
for score in scores.values():
    print(score)

# Loop over key-value pairs — use this most often
for name, score in scores.items():
    print(f"{name}: {score}")

# Loop with index
for i, (name, score) in enumerate(scores.items(), 1):
    print(f"{i}. {name}: {score}")


# ------------------------------------------------------------
# 6. CHECKING KEYS & VALUES
# ------------------------------------------------------------

person = {"name": "Alice", "age": 30}

# Check if key exists
print("name" in person)      # True
print("email" in person)     # False
print("email" not in person) # True

# ⚠️  'in' checks KEYS only by default
print(30 in person)          # False  (30 is a value, not a key)
print(30 in person.values()) # True   (check values explicitly)

# Get all keys, values, items
print(list(person.keys()))    # ['name', 'age']
print(list(person.values()))  # ['Alice', 30]
print(list(person.items()))   # [('name', 'Alice'), ('age', 30)]

# Length
print(len(person))    # 2


# ------------------------------------------------------------
# 7. DICTIONARY COMPREHENSIONS
# ------------------------------------------------------------
# { key_expr : value_expr  for  item  in  iterable  if  cond }

# Basic
squares = {x: x**2 for x in range(1, 6)}
print(squares)    # {1:1, 2:4, 3:9, 4:16, 5:25}

# With condition
even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(even_squares)    # {2:4, 4:16, 6:36, 8:64, 10:100}

# Transform existing dict
scores = {"Alice": 92, "Bob": 85, "Charlie": 95}
grades = {name: "A" if score >= 90 else "B"
          for name, score in scores.items()}
print(grades)    # {'Alice': 'A', 'Bob': 'B', 'Charlie': 'A'}

# Invert a dictionary (swap keys and values)
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)    # {1: 'a', 2: 'b', 3: 'c'}

# Filter a dictionary
scores = {"Alice": 92, "Bob": 55, "Charlie": 95, "Diana": 48}
passing = {name: score for name, score in scores.items() if score >= 60}
print(passing)    # {'Alice': 92, 'Charlie': 95}


# ------------------------------------------------------------
# 8. MERGING DICTIONARIES
# ------------------------------------------------------------

defaults = {"color": "blue", "size": 10, "visible": True}
custom   = {"color": "red", "size": 20}

# Python 3.9+  — | operator (cleanest)
merged = defaults | custom
print(merged)    # {'color': 'red', 'size': 20, 'visible': True}

# Python 3.5+  — ** unpacking
merged = {**defaults, **custom}
print(merged)    # same result

# update() — modifies in place
result = defaults.copy()
result.update(custom)
print(result)

# ⚠️  Later dict wins on duplicate keys in all methods above


# ------------------------------------------------------------
# 9. NESTED DICTIONARIES
# ------------------------------------------------------------

company = {
    "name": "TechCorp",
    "employees": {
        "alice": {"age": 30, "role": "Engineer", "salary": 95000},
        "bob":   {"age": 25, "role": "Designer",  "salary": 80000},
    },
    "offices": ["NYC", "LA", "Chicago"]
}

# Accessing nested values
print(company["name"])                          # TechCorp
print(company["employees"]["alice"]["role"])    # Engineer
print(company["offices"][0])                   # NYC

# Safe nested access with .get()
salary = company["employees"].get("charlie", {}).get("salary", 0)
print(salary)    # 0  ← no error even though charlie doesn't exist

# Modifying nested values
company["employees"]["alice"]["salary"] = 100000

# Loop through nested
for emp_name, emp_data in company["employees"].items():
    print(f"{emp_name}: {emp_data['role']}, ${emp_data['salary']:,}")


# ------------------------------------------------------------
# 10. SPECIAL DICTIONARIES FROM collections
# ------------------------------------------------------------

from collections import defaultdict, Counter, OrderedDict

# --- defaultdict — auto-creates missing keys ---
# No more KeyError when a key is missing!

# Group items by first letter
words = ["apple", "banana", "avocado", "blueberry", "cherry"]
grouped = defaultdict(list)   # missing keys default to empty list

for word in words:
    grouped[word[0]].append(word)

print(dict(grouped))
# {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}

# Count with defaultdict
text = "hello world"
freq = defaultdict(int)    # missing keys default to 0
for char in text:
    freq[char] += 1        # no KeyError on first occurrence

# --- Counter — count occurrences ---
from collections import Counter

text = "banana"
c = Counter(text)
print(c)    # Counter({'a': 3, 'n': 2, 'b': 1})

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
print(c)                        # Counter({'apple': 3, ...})
print(c.most_common(2))         # [('apple', 3), ('banana', 2)]
print(c["apple"])               # 3
print(c["mango"])               # 0  ← no KeyError!

# Counter arithmetic
a = Counter("aabbc")
b = Counter("abcd")
print(a + b)    # combine counts
print(a - b)    # subtract counts
print(a & b)    # min of counts
print(a | b)    # max of counts


# ------------------------------------------------------------
# 11. COMMON PATTERNS
# ------------------------------------------------------------

# Pattern 1: Frequency counter (very common in interviews)
def char_frequency(s):
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq

print(char_frequency("hello"))    # {'h':1, 'e':1, 'l':2, 'o':1}

# Pattern 2: Group by property
people = [
    {"name": "Alice", "city": "NYC"},
    {"name": "Bob",   "city": "LA"},
    {"name": "Carol", "city": "NYC"},
    {"name": "Dave",  "city": "LA"},
]
by_city = defaultdict(list)
for p in people:
    by_city[p["city"]].append(p["name"])
print(dict(by_city))
# {'NYC': ['Alice', 'Carol'], 'LA': ['Bob', 'Dave']}

# Pattern 3: Caching / memoization
cache = {}
def expensive_compute(n):
    if n in cache:
        return cache[n]
    result = n ** 2    # imagine this is slow
    cache[n] = result
    return result

# Pattern 4: Two-sum using dict (classic interview)
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i

print(two_sum([2, 7, 11, 15], 9))    # [0, 1]

# Pattern 5: Count and find most common
from collections import Counter
words = "the quick brown fox jumps over the lazy dog the".split()
c = Counter(words)
print(c.most_common(3))    # top 3 most common words

# Pattern 6: Dict as a switch/dispatch table
def add(a, b):      return a + b
def sub(a, b):      return a - b
def mul(a, b):      return a * b
def div(a, b):      return a / b if b != 0 else "Error"

operations = {"+": add, "-": sub, "*": mul, "/": div}
op = "+"
print(operations[op](10, 5))    # 15  — cleaner than if/elif chain


# ------------------------------------------------------------
# 12. TIME COMPLEXITY — know this for interviews
# ------------------------------------------------------------
#
# Operation              | Average | Notes
# ---------------------- | ------- | ----------------------
# Access   d[key]        |  O(1)   |
# Insert   d[key] = val  |  O(1)   |
# Delete   del d[key]    |  O(1)   |
# Membership  key in d   |  O(1)   | checks keys only
# Iteration              |  O(n)   |
# .keys() .values()      |  O(1)   | returns a view, not a list
# .items()               |  O(1)   | returns a view
# Copy                   |  O(n)   |
#
# Dicts are O(1) for get/set — that's the superpower.
# Use a dict whenever you need fast lookup by a key.


# ============================================================
# SUMMARY
# ============================================================
# Create        → {}  dict()  {k:v for ...}
# Access        → d[key]  d.get(key, default)
# Add/Update    → d[key]=val  d.update()  d.setdefault()
# Remove        → d.pop(key)  del d[key]  d.popitem()  d.clear()
# Loop          → for k in d  /  .values()  /  .items()
# Check         → key in d  (checks keys only)
# Comprehension → {k:v for k,v in d.items() if cond}
# Merge         → d1 | d2  (3.9+)  or  {**d1, **d2}
# Nested        → d["a"]["b"]["c"]
# defaultdict   → auto-creates missing keys
# Counter       → count occurrences, .most_common()
# Complexity    → O(1) get/set/delete — the superpower
# ============================================================