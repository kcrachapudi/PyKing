# ============================================================
#  CHAPTER 1 — LOOPS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. THE for LOOP — iterate over a sequence
# ------------------------------------------------------------
# Use when you know WHAT you are iterating over.

fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
# apple
# banana
# cherry

# Loop over a string — character by character
for char in "Python":
    print(char)

# Loop over a dictionary
person = {"name": "Alice", "age": 30, "city": "NYC"}

for key in person:              # loops over keys by default
    print(key)

for value in person.values():   # loop over values
    print(value)

for key, value in person.items():  # loop over both
    print(f"{key}: {value}")


# ------------------------------------------------------------
# 2. range() — generate a sequence of numbers
# ------------------------------------------------------------
# range(stop)
# range(start, stop)
# range(start, stop, step)
# ⚠️  stop is NOT included

for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):       # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8  (step 2)
    print(i)

for i in range(10, 0, -1):  # 10, 9, 8 ... 1  (countdown)
    print(i)

# Useful: repeat something N times
for _ in range(3):          # _ means "I don't need the variable"
    print("Hello!")


# ------------------------------------------------------------
# 3. enumerate() — loop with index AND value
# ------------------------------------------------------------
# Don't do:  for i in range(len(fruits)) — that's unpythonic.
# Do this instead:

fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Start index from 1
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
# 1. apple
# 2. banana
# 3. cherry


# ------------------------------------------------------------
# 4. zip() — loop over two lists in parallel
# ------------------------------------------------------------

names  = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]

for name, score in zip(names, scores):
    print(f"{name} scored {score}")
# Alice scored 95
# Bob scored 87
# Charlie scored 92

# zip stops at the shortest list
a = [1, 2, 3]
b = [10, 20]
for x, y in zip(a, b):
    print(x, y)    # (1,10)  (2,20)  — 3 is ignored


# ------------------------------------------------------------
# 5. THE while LOOP — repeat while condition is True
# ------------------------------------------------------------
# Use when you DON'T know how many iterations you need.

count = 0
while count < 5:
    print(count)
    count += 1      # ⚠️  always move toward the exit condition!
# 0 1 2 3 4

# Classic: ask user until valid input
# (run this interactively to see it in action)
# while True:
#     answer = input("Type 'yes' to continue: ")
#     if answer == "yes":
#         break

# Count down
n = 5
while n > 0:
    print(n)
    n -= 1
print("Liftoff!")


# ------------------------------------------------------------
# 6. break — exit the loop immediately
# ------------------------------------------------------------

# Stop as soon as we find what we want
numbers = [3, 7, 1, 9, 4, 6]
target = 9

for num in numbers:
    if num == target:
        print(f"Found {target}!")
        break           # stops the loop right here
    print(f"Checking {num}...")
# Checking 3...
# Checking 7...
# Checking 1...
# Found 9!

# break in while loop
count = 0
while True:             # infinite loop — only exits via break
    print(count)
    count += 1
    if count >= 3:
        break
# 0 1 2


# ------------------------------------------------------------
# 7. continue — skip to the next iteration
# ------------------------------------------------------------

# Skip even numbers
for i in range(10):
    if i % 2 == 0:
        continue        # skip the rest of this iteration
    print(i)
# 1 3 5 7 9

# Skip empty strings
words = ["hello", "", "world", "", "python"]
for word in words:
    if not word:        # empty string is falsy
        continue
    print(word)
# hello  world  python


# ------------------------------------------------------------
# 8. else on a loop — runs if loop completed without break
# ------------------------------------------------------------
# Unusual but useful — the else block runs only if
# the loop was NOT exited via break.

# Searching example
numbers = [1, 3, 5, 7, 9]
target = 6

for num in numbers:
    if num == target:
        print("Found it!")
        break
else:
    print("Not found.")    # runs because break was never hit
# Not found.

# Contrast — when break IS hit:
target = 5
for num in numbers:
    if num == target:
        print("Found it!")
        break
else:
    print("Not found.")    # does NOT run
# Found it!


# ------------------------------------------------------------
# 9. NESTED LOOPS — loop inside a loop
# ------------------------------------------------------------

# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}")
    print("---")

# ⚠️  break only breaks the INNER loop
for i in range(3):
    for j in range(3):
        if j == 1:
            break           # breaks inner loop only
        print(f"i={i}, j={j}")


# ------------------------------------------------------------
# 10. LIST COMPREHENSIONS — compact for loops
# ------------------------------------------------------------
# Syntax: [expression  for  item  in  iterable  if  condition]
# Creates a new list in one line. Very Pythonic.

# Basic
squares = [x**2 for x in range(6)]
print(squares)    # [0, 1, 4, 9, 16, 25]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
print(evens)      # [0, 2, 4, 6, 8]

# Transform strings
fruits = ["apple", "banana", "cherry"]
upper = [f.upper() for f in fruits]
print(upper)      # ['APPLE', 'BANANA', 'CHERRY']

# Filter and transform together
long_fruits = [f.title() for f in fruits if len(f) > 5]
print(long_fruits)    # ['Banana', 'Cherry']

# Nested comprehension — flatten a 2D list
# The order might be confusing at first — read it inside out:
# imagine you are writing a nested loop, you would strt with for row in matrix, then for num in row, then append num to flat.
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)    # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ⚠️  Keep comprehensions readable.
# If it's hard to read on one line, use a regular for loop.


# ------------------------------------------------------------
# 11. COMMON LOOP PATTERNS
# ------------------------------------------------------------

# Pattern 1: accumulate a total
numbers = [10, 20, 30, 40, 50]
total = 0
for n in numbers:
    total += n
print(total)    # 150  (or just use sum(numbers))

# Pattern 2: collect matching items
scores = [45, 78, 92, 61, 88, 34]
passing = [s for s in scores if s >= 60]
print(passing)    # [78, 92, 61, 88]

# Pattern 3: find first match
def find_first(items, condition):
    for item in items:
        if condition(item):
            return item
    return None

first_even = find_first([1, 3, 4, 7, 8], lambda x: x % 2 == 0)
print(first_even)    # 4

# Pattern 4: build a dict from two lists
keys   = ["a", "b", "c"]
values = [1, 2, 3]
d = dict(zip(keys, values))
print(d)    # {'a': 1, 'b': 2, 'c': 3}

# Pattern 5: remove duplicates while preserving order
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
seen = set()
unique = []
for item in items:
    if item not in seen:
        unique.append(item)
        seen.add(item)
print(unique)    # [3, 1, 4, 5, 9, 2, 6]

# List of Functions: 
#the concept of a list of functions (or a "registry" of functions) is actually used all the 
# time in professional software engineering. Here are three real-world scenarios:
#1. Data Validation Pipelines
#Imagine you are processing a user’s signup form. You might have a list of "checkers" that every piece of data must pass through.
# A list of functions (rules)
validators = [
    lambda s: len(s) > 8,             # Rule: long enough
    lambda s: any(c.isdigit() for c in s), # Rule: has a number
    lambda s: any(c.isupper() for c in s)  # Rule: has a capital
]
password = "MyPassword123"
# Real-world use: List of Validators_valid = all(rule(password) for rule in validators)
#Instead of one massive if-else block, you have a clean list of functions you can 
# easily add to or remove from.

#2. Custom "Plugins" or Toolsets
#Think of a photo editor. You might have a list of "filters" (functions) that the 
# user wants to apply to an image in a specific order:
# Each function takes an image and returns a modified version
#filters = [add_brightness, convert_to_grayscale, add_border]
#for process in filters:
#    image = process(image)
#Storing them in a list allows the user to reorder them, toggle them on/off, or undo the last step easily.
#3. Task Schedulers (The "To-Do" List)
#In web servers or game engines, you often have a "queue" of things that need to happen at the end of a frame or a request.
#You don't want to run the code now (it might slow things down).
#So, you "wrap" the action in a lambda and throw it into a list (a queue).
#Later, a single "worker" loop goes through the list and runs every function inside it.
#Why not just use def?
#You usually would use def for these! The only reason people use lambdas in these lists 
# is when the operation is so tiny (like x > 5) that writing a full def feels like overkill.


# ============================================================
# SUMMARY
# ============================================================
# for loop       → iterate over any sequence
# range()        → generate numbers  range(start, stop, step)
# enumerate()    → index + value together
# zip()          → two lists in parallel
# while loop     → repeat while condition is True
# break          → exit loop immediately
# continue       → skip to next iteration
# else on loop   → runs only if no break occurred
# nested loops   → loop inside a loop
# comprehension  → [expr for x in iter if cond]
# ============================================================