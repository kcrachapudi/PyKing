# ============================================================
#  CHAPTER 1 — FUNCTIONS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A FUNCTION?
# ------------------------------------------------------------
# A function is a reusable block of code with a name.
# Define once, call many times.
# Keeps code DRY — Don't Repeat Yourself.

def greet():
    print("Hello, World!")

greet()    # call it
greet()    # call it again


# ------------------------------------------------------------
# 2. PARAMETERS AND ARGUMENTS
# ------------------------------------------------------------
# Parameter → the variable in the function definition
# Argument  → the actual value you pass when calling

def greet(name):           # 'name' is the parameter
    print(f"Hello, {name}!")

greet("Alice")             # "Alice" is the argument
greet("Bob")


# Multiple parameters
def add(a, b):
    return a + b

result = add(3, 5)
print(result)    # 8


# ------------------------------------------------------------
# 3. RETURN VALUES
# ------------------------------------------------------------
# return sends a value back to the caller.
# Without return (or bare return), the function returns None.

def square(n):
    return n ** 2

x = square(4)
print(x)    # 16

# Return multiple values — actually returns a tuple
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 9, 2, 7])
print(lo, hi)    # 1 9

# Function without return → returns None
def say_hi():
    print("Hi!")

result = say_hi()
print(result)    # None


# ------------------------------------------------------------
# 4. DEFAULT ARGUMENTS
# ------------------------------------------------------------
# Give a parameter a default value — caller can omit it.
# ⚠️  Parameters WITH defaults must come AFTER those without.

def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Good morning") # Good morning, Bob!
greet("Carol", greeting="Hey") # Hey, Carol!


# ------------------------------------------------------------
# 5. KEYWORD ARGUMENTS
# ------------------------------------------------------------
# Pass arguments by name — order doesn't matter.

def describe(name, age, city):
    print(f"{name}, {age}, from {city}")

describe("Alice", 30, "NYC")              # positional
describe(age=30, city="NYC", name="Alice") # keyword — any order
describe("Alice", city="NYC", age=30)     # mix: positional first


# ------------------------------------------------------------
# 6. *args — variable number of positional arguments
# ------------------------------------------------------------
# * collects extra positional args into a TUPLE.
# Name 'args' is convention — the * is what matters.

def total(*numbers):
    print(type(numbers))    # <class 'tuple'>
    return sum(numbers)

print(total(1, 2, 3))        # 6
print(total(10, 20, 30, 40)) # 100
print(total())               # 0

# Mixing regular and *args
def first_and_rest(first, *rest):
    print(f"First: {first}")
    print(f"Rest: {rest}")

first_and_rest(1, 2, 3, 4)
# First: 1
# Rest: (2, 3, 4)


# ------------------------------------------------------------
# 7. **kwargs — variable number of keyword arguments
# ------------------------------------------------------------
# ** collects extra keyword args into a DICT.

def describe(**info):
    print(type(info))    # <class 'dict'>
    for key, value in info.items():
        print(f"  {key}: {value}")

describe(name="Alice", age=30, city="NYC")
# name: Alice
# age: 30
# city: NYC

# Full signature order: normal, *args, **kwargs
def everything(a, b, *args, **kwargs):
    print(a, b)
    print(args)
    print(kwargs)

everything(1, 2, 3, 4, x=10, y=20)
# 1 2
# (3, 4)
# {'x': 10, 'y': 20}


# ------------------------------------------------------------
# 8. TYPE HINTS — document what goes in and out
# ------------------------------------------------------------
# Python doesn't enforce these at runtime, but they
# make code readable and IDEs can catch mistakes.

def add(a: int, b: int) -> int:
    return a + b

def greet(name: str, times: int = 1) -> None:
    for _ in range(times):
        print(f"Hello, {name}!")

def first_item(items: list) -> object:
    return items[0] if items else None


# ------------------------------------------------------------
# 9. DOCSTRINGS — document what your function does
# ------------------------------------------------------------
# Triple-quoted string right after def line.
# Shows up in help() and IDEs.

def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert a temperature from Celsius to Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit.

    Example:
        >>> celsius_to_fahrenheit(100)
        212.0
    """
    return (celsius * 9/5) + 32

print(celsius_to_fahrenheit(100))    # 212.0
help(celsius_to_fahrenheit)          # shows the docstring


# ------------------------------------------------------------
# 10. SCOPE — where variables live
# ------------------------------------------------------------
# Local scope  → variable created inside a function
# Global scope → variable created outside all functions

x = 10    # global

def show():
    y = 20       # local — only exists inside show()
    print(x)     # can READ global variables
    print(y)

show()
# print(y)   ← NameError — y doesn't exist out here

# global keyword — modify a global variable from inside a function
# ⚠️  Avoid this pattern — it makes code hard to follow.
count = 0

def increment():
    global count
    count += 1

increment()
increment()
print(count)    # 2

# Better approach — return the new value instead
def increment(count):
    return count + 1

count = 0
count = increment(count)
count = increment(count)
print(count)    # 2


# ------------------------------------------------------------
# 11. LAMBDA — anonymous one-line functions
# ------------------------------------------------------------
# Syntax: lambda parameters: expression
# Used for short, throwaway functions.

square = lambda x: x ** 2
print(square(5))    # 25

add = lambda a, b: a + b
print(add(3, 4))    # 7

# Most common use — as a key function for sorting
names = ["Charlie", "Alice", "Bob"]
names.sort(key=lambda x: x.lower())
print(names)    # ['Alice', 'Bob', 'Charlie']

students = [("Alice", 92), ("Bob", 85), ("Charlie", 95)]
students.sort(key=lambda s: s[1], reverse=True)
print(students)    # [('Charlie', 95), ('Alice', 92), ('Bob', 85)]

# With map() and filter()
numbers = [1, 2, 3, 4, 5]
doubled  = list(map(lambda x: x * 2, numbers))
evens    = list(filter(lambda x: x % 2 == 0, numbers))
print(doubled)    # [2, 4, 6, 8, 10]
print(evens)      # [2, 4]


# ------------------------------------------------------------
# 12. FUNCTIONS ARE FIRST-CLASS OBJECTS
# ------------------------------------------------------------
# In Python, functions are values — you can:
# - assign them to variables
# - pass them as arguments
# - return them from other functions

def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

def speak(func, message):   # takes a function as argument
    print(func(message))

speak(shout, "hello")     # HELLO
speak(whisper, "HELLO")   # hello

# Store functions in a list or dict
operations = {
    "double": lambda x: x * 2,
    "triple": lambda x: x * 3,
    "square": lambda x: x ** 2,
}

print(operations["double"](5))    # 10
print(operations["square"](4))    # 16


# ------------------------------------------------------------
# 13. RECURSION — a function that calls itself
# ------------------------------------------------------------
# Every recursive function needs:
# 1. Base case  — when to stop
# 2. Recursive case — call itself with a simpler input

def factorial(n: int) -> int:
    """Return n! (n factorial)"""
    if n <= 1:          # base case
        return 1
    return n * factorial(n - 1)   # recursive case

print(factorial(5))    # 120  (5 * 4 * 3 * 2 * 1)
print(factorial(0))    # 1

# How it works for factorial(4):
# factorial(4) = 4 * factorial(3)
#                    3 * factorial(2)
#                        2 * factorial(1)
#                            1   ← base case
# = 4 * 3 * 2 * 1 = 24

# Another classic: fibonacci
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(8)])    # [0, 1, 1, 2, 3, 5, 8, 13]

def fib_loop(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fib_loop(10))  # Output: 55

"""Why this is usually preferred:
Memory Efficient: It only ever tracks two numbers (a and b) in memory. It doesn't create a massive "tree" of functions or a list of tuples.
No "Recursion Depth" Error: If you try to run a recursive fib(2000), Python will crash because the stack is too deep. This loop can handle fib(10000) without breaking a sweat.
Readability: Most developers can look at a, b = b, a + b and immediately understand that the values are "shifting" forward.
Comparison of the 3 Methods
Method	Style	Best For...
Recursion	Mathematical	Teaching the concept of Fibonacci.
Reduce	Functional	When you want to avoid side effects or "flex" your FP skills.
For Loop	Imperative	Production code. It's fast, safe, and readable.
Now that you've seen the "big three" ways to handle logic (Recursion, Functional/Reduce, and Loops), do you want to dive deeper into tuple unpacking (the a, b = b, a + b part), or should we look at something else?
"""

# ⚠️  Recursion without a base case = infinite loop → crash.
# ⚠️  Python's default recursion limit is 1000 calls.


# ------------------------------------------------------------
# 14. COMMON FUNCTION PATTERNS
# ------------------------------------------------------------

# Pattern 1: Guard clause — exit early, reduce nesting
def process_age(age):
    if not isinstance(age, int):
        return "Error: age must be an integer"
    if age < 0:
        return "Error: age cannot be negative"
    if age > 150:
        return "Error: unrealistic age"
    return f"Valid age: {age}"

# Pattern 2: Default mutable argument trap — common bug!
# ❌ WRONG — list is shared across all calls
def add_item_bad(item, lst=[]):
    lst.append(item)
    return lst

print(add_item_bad(1))    # [1]
print(add_item_bad(2))    # [1, 2]  ← bug! expected [2]

# ✅ CORRECT — use None as default, create new list inside
def add_item_good(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(add_item_good(1))    # [1]
print(add_item_good(2))    # [2]  ✅
#The Golden Rule: Never use a mutable object (list, dict, set) as a 
# default argument in a function. Always use None.

# Pattern 3: Unpacking arguments with * and **
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))       # unpacks list into positional args → 6

info = {"a": 1, "b": 2, "c": 3}
print(add(**info))      # unpacks dict into keyword args → 6

from functools import reduce
#You have a list of tuples representing students and their grades:
#Write a sorted() function using a lambda as the key that sorts the students primarily by grade 
# (highest to lowest), and secondarily by name (alphabetically) if the grades are tied.
#students = [("Alice", 88), ("Bob", 95), ("Charlie", 88), ("David", 92)]
#sorted_students = sorted(students, lambda s: )


#Write a lambda function called check_val that takes a number x.
#If x is greater than 10, return "High".
#If x is between 5 and 10 (inclusive), return "Medium". Otherwise, return "Low".
#Constraint: You must do this in a single lambda line using nested ternary operators.
check_val = lambda x: "High" if x>10 else "Medium" if 5<=x<=10 else "Low"
print(check_val(4))

#Question 4: Dictionary Mapping
#Given a list of dictionaries:
data = [{"id": 1, "val": 10}, {"id": 2, "val": 20}, {"id": 3, "val": 30}]
#Use the map() function and a lambda to return a list of just the "val" numbers, 
# but multiply each value by 2 only if the "id" is an odd number.
#new_data = list(map(lambda x: list(x.items())[1]*2 if list(x.items())[0]%2==0 else list(x.items())[1], data))
#print(new_data)
#Question 5: The "Self-Executing" Challenge
#Write a single line of code using a lambda that calculates the factorial of 5 
# without using the math module or defining a standard def function.
#Hint: You’ll need to pass the lambda into itself or use a functional tool like reduce.
#Take your time—I'm ready when you are! Which one do you want to tackle first?

print(list(range(5, 0, -1)))
factorial = reduce(lambda x, y: x*y, list(range(5, 1, -1)))
print(factorial)



# ============================================================
# SUMMARY
# ============================================================
# def name(params): → define a function
# return            → send value back (None if omitted)
# default args      → def f(x, y=10)
# keyword args      → f(y=5, x=3)
# *args             → extra positional args as tuple
# **kwargs          → extra keyword args as dict
# type hints        → def f(x: int) -> str
# docstrings        → """explain here"""
# scope             → local vs global, avoid global keyword
# lambda            → lambda x: x*2  (short anonymous function)
# first-class       → functions are values, pass them around
# recursion         → function calls itself (needs base case)
# ============================================================