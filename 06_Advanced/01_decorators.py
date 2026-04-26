# ============================================================
#  CHAPTER 6 — DECORATORS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A DECORATOR?
# ------------------------------------------------------------
# A decorator is a function that WRAPS another function
# to add behaviour without changing its source code.
#
# Real-world analogy:
#   A coffee cup sleeve — it wraps the cup, adds grip and
#   insulation, but the cup (function) is unchanged inside.
#
# You've already seen decorators:
#   @property, @classmethod, @staticmethod
#
# Common uses:
#   → logging, timing, caching, authentication, retry logic


# ------------------------------------------------------------
# 2. FUNCTIONS ARE FIRST-CLASS OBJECTS
# ------------------------------------------------------------
# Before decorators, understand this foundation:
# In Python, functions are values — just like integers or strings.
# You can assign them to variables, pass them around, return them.

def greet():
    print("Hello!")

# Assign a function to a new variable — no () means no call yet
say_hello = greet      # say_hello now points to the same function
say_hello()            # NOW we call it → Hello!

# Pass a function as an argument to another function
def run(func):         # 'func' receives a function as its value
    func()             # call whatever function was passed in

run(greet)             # passing greet (not greet()) → Hello!

# Return a function FROM another function
def get_greeter():
    def inner_greet():          # define a function INSIDE a function
        print("Hi there!")
    return inner_greet          # return the function itself (no parentheses!)

greeter = get_greeter()         # greeter now holds the inner_greet function
greeter()                       # call it → Hi there!


# ------------------------------------------------------------
# 3. CLOSURES — the foundation of decorators
# ------------------------------------------------------------
# A closure is an inner function that REMEMBERS variables
# from its outer (enclosing) function's scope, even after
# the outer function has finished running.

def make_multiplier(factor):    # outer function — 'factor' lives here
    def multiply(n):            # inner function — 'factor' is remembered
        return n * factor       # uses 'factor' from the outer scope
    return multiply             # return the inner function

double = make_multiplier(2)     # factor=2 is "locked in" to double
triple = make_multiplier(3)     # factor=3 is "locked in" to triple

print(double(5))    # 10  →  5 * 2  (remembers factor=2)
print(triple(5))    # 15  →  5 * 3  (remembers factor=3)
print(double(9))    # 18  →  9 * 2


# ------------------------------------------------------------
# 4. BUILDING A DECORATOR FROM SCRATCH
# ------------------------------------------------------------
# A decorator is just a function that:
#   1. Takes a function as input
#   2. Defines a wrapper function around it
#   3. Returns the wrapper

# Step 1 — manually wrap a function
def my_decorator(func):         # receives the original function
    def wrapper():              # the new function that replaces it
        print("Before the function runs")
        func()                  # call the ORIGINAL function
        print("After the function runs")
    return wrapper              # return the wrapper, not the result

def say_hi():
    print("Hi!")

# Manually decorate — replace say_hi with the wrapped version
say_hi = my_decorator(say_hi)
say_hi()
# Before the function runs
# Hi!
# After the function runs

# Step 2 — use @ syntax (does exactly the same thing, cleaner)
def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

@my_decorator           # Python translates this to: greet = my_decorator(greet)
def greet():
    print("Hello!")

greet()
# Before
# Hello!
# After


# ------------------------------------------------------------
# 5. DECORATORS WITH ARGUMENTS — *args and **kwargs
# ------------------------------------------------------------
# The problem: what if the function we decorate has arguments?
# The wrapper must accept AND pass through ALL arguments.

def my_decorator(func):
    def wrapper(*args, **kwargs):    # * catches all positional args as tuple
                                     # ** catches all keyword args as dict
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)   # unpack and pass them to original
        print(f"Done")
        return result                    # MUST return the result or it's lost!
    return wrapper

@my_decorator
def add(a, b):          # has positional args
    return a + b

@my_decorator
def greet(name, greeting="Hello"):   # has a default arg too
    return f"{greeting}, {name}!"

print(add(3, 5))              # Calling add → Done → 8
print(greet("Alice"))         # Calling greet → Done → Hello, Alice!
print(greet("Bob", "Hey"))    # Calling greet → Done → Hey, Bob!


# ------------------------------------------------------------
# 6. functools.wraps — preserve function metadata
# ------------------------------------------------------------
# Problem: after wrapping, the function "looks like" the wrapper,
# not the original. It loses its name and docstring.
# @functools.wraps fixes this by copying metadata from original to wrapper.

import functools

# ❌ Without @wraps — metadata is lost
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_func():
    """This is my function's docstring."""
    pass

print(my_func.__name__)    # wrapper  ← WRONG, should be 'my_func'
print(my_func.__doc__)     # None     ← WRONG, docstring is gone

# ✅ With @wraps — metadata is preserved
def good_decorator(func):
    @functools.wraps(func)       # copies __name__, __doc__, etc. from func
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_func():
    """This is my function's docstring."""
    pass

print(my_func.__name__)    # my_func  ✅  correct name preserved
print(my_func.__doc__)     # This is my function's docstring. ✅


# ------------------------------------------------------------
# 7. PRACTICAL DECORATORS — ones you'll actually use
# ------------------------------------------------------------

import time
import functools

# --- Timer decorator --- measures how long a function takes ---
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()         # high-resolution clock — record start time
        result = func(*args, **kwargs)       # run the actual function
        end    = time.perf_counter()         # record end time
        print(f"{func.__name__} took {end - start:.4f}s")   # print elapsed time
        return result                        # return the function's result unchanged
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))    # add all numbers from 0 to n

print(slow_sum(1_000_000))    # slow_sum took 0.03s  →  499999500000


# --- Logger decorator --- prints what was called and what was returned ---
def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Build a readable string of all the arguments passed in
        args_repr   = [repr(a) for a in args]                      # positional args as strings
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]    # keyword args as "k=v"
        signature   = ", ".join(args_repr + kwargs_repr)           # combine them
        print(f"Calling {func.__name__}({signature})")             # log the call
        result = func(*args, **kwargs)                             # run the function
        print(f"{func.__name__} returned {result!r}")              # log the result
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

add(3, 5)
# Calling add(3, 5)
# add returned 8


# --- Retry decorator --- re-runs a function if it fails ---
def retry(times=3, delay=1, exceptions=(Exception,)):
    # This outer function receives the decorator's arguments
    def decorator(func):                        # this is the actual decorator
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):     # try up to 'times' attempts
                try:
                    return func(*args, **kwargs)     # if it succeeds, return immediately
                except exceptions as e:              # if it raises one of our exceptions
                    print(f"Attempt {attempt}/{times} failed: {e}")
                    if attempt < times:
                        time.sleep(delay)            # wait before retrying
            # if all attempts failed, raise an error
            raise RuntimeError(f"{func.__name__} failed after {times} attempts")
        return wrapper
    return decorator    # return the decorator (not wrapper — that's the job of decorator)

@retry(times=3, delay=0, exceptions=(ValueError,))
def unstable():
    import random
    if random.random() < 0.7:        # 70% chance to fail
        raise ValueError("Random failure!")
    return "Success!"


# --- Memoize decorator --- caches results so same inputs aren't recomputed ---
def memoize(func):
    cache = {}                           # dict to store already-computed results
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:            # if we haven't seen these args before
            cache[args] = func(*args)    # compute and store the result
        return cache[args]               # return stored result (skip recomputation)
    return wrapper

@memoize
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)    # without memoize this would be exponentially slow

print(fib(40))    # fast because intermediate results are cached in the dict


# ------------------------------------------------------------
# 8. PARAMETRIZED DECORATORS — decorators that take arguments
# ------------------------------------------------------------
# When your decorator needs its own arguments, you need
# THREE levels of nesting:
#   Level 1 — decorator factory    (receives decorator args)
#   Level 2 — decorator            (receives the function)
#   Level 3 — wrapper              (receives function args, does the work)

def repeat(n):                          # Level 1: takes decorator argument 'n'
    def decorator(func):                # Level 2: takes the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):   # Level 3: called when function is invoked
            for _ in range(n):          # repeat the function call n times
                result = func(*args, **kwargs)
            return result               # return result of last call
        return wrapper
    return decorator    # return the decorator so @repeat(3) gives a decorator

@repeat(3)              # repeat(3) runs first → returns decorator → applied to say()
def say(message):
    print(message)

say("Hello!")
# Hello!
# Hello!
# Hello!


# ------------------------------------------------------------
# 9. STACKING DECORATORS
# ------------------------------------------------------------
# You can apply multiple decorators to one function.
# They apply from BOTTOM to TOP (closest to function first).

@timer          # applied second (outer layer)
@logger         # applied first  (inner layer)
def multiply(a, b):
    return a * b

multiply(4, 5)
# logger runs first:  Calling multiply(4, 5) → multiply returned 20
# timer runs second:  multiply took 0.0001s

# This is equivalent to: multiply = timer(logger(multiply))
# Read it as: timer wraps (logger wraps (multiply))


# ------------------------------------------------------------
# 10. CLASS-BASED DECORATORS
# ------------------------------------------------------------
# Instead of nested functions, use a class with __call__.
# Useful when your decorator needs to maintain STATE between calls.

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)  # like @functools.wraps but for classes
        self.func  = func    # store the original function
        self.count = 0       # initialize call counter — this persists between calls!

    def __call__(self, *args, **kwargs):
        # __call__ is invoked when the instance is called like a function
        self.count += 1      # increment counter each time the function is called
        print(f"{self.func.__name__} has been called {self.count} time(s)")
        return self.func(*args, **kwargs)    # run the original function

@CountCalls                  # CountCalls(say_hello) is called → returns an instance
def say_hello():
    print("Hello!")

say_hello()    # say_hello has been called 1 time(s) → Hello!
say_hello()    # say_hello has been called 2 time(s) → Hello!
say_hello()    # say_hello has been called 3 time(s) → Hello!
print(say_hello.count)    # 3  ← state is preserved in the instance


# ------------------------------------------------------------
# 11. BUILT-IN DECORATORS Python gives you for free
# ------------------------------------------------------------

# @functools.lru_cache — memoization with automatic LRU eviction
# LRU = Least Recently Used — evicts oldest cached result when maxsize is reached
@functools.lru_cache(maxsize=128)   # cache up to 128 unique argument combinations
def expensive(n):
    return n ** 2

print(expensive(10))            # computed fresh
print(expensive(10))            # served from cache (no recompute)
print(expensive.cache_info())   # CacheInfo(hits=1, misses=1, maxsize=128, currsize=1)
expensive.cache_clear()         # clear all cached results

# @functools.cached_property — like @property but computed only ONCE then stored
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @functools.cached_property
    def area(self):
        import math
        print("Computing area...")      # this only prints the FIRST time
        return math.pi * self.radius ** 2

c = Circle(5)
print(c.area)    # Computing area... → 78.53...  (computed)
print(c.area)    # 78.53...  (returned from cache, no recompute, no print)

#################################
#QnA Session
"""
Q1: Why do we have to return the wrapper function in a decorator?
This is the "aha!" moment for decorators. The reason you must return the wrapper is 
because of how Python handles the @ symbol.
The Secret Swap
When you write @my_decorator above the add function, Python internally performs a 
permanent name swap. It immediately executes this line behind the scenes:
add = my_decorator(add)
Look closely at what happens:
my_decorator runs and returns the wrapper function.
The name add is now assigned to that wrapper.
The original add function is now "trapped" inside the wrapper’s closure 
(the backpack we discussed).
Why the return matters
If you didn't return the wrapper, look at what would happen to the swap:
# If my_decorator returned nothing (None)
add = my_decorator(add) 
# Now 'add' is equal to None!
add(3, 5) # ERROR: 'NoneType' object is not callable
"No one cares for it" — Actually, everyone is using it!
When you later call add(3, 5), you aren't actually calling your original add function. 
You are calling the wrapper. You only think you're calling the original because the name 
is the same. It’s like a "body snatcher" situation: The name on the outside says add.
The code on the inside is the wrapper. The wrapper then goes and fetches the original add 
from its backpack to get the actual math done.
Summary
You return the wrapper so that the variable name (add) has a function to point to. 
If you don't return it, the name add becomes empty (None), and your function effectively 
disappears from the program.
"""
"""
Q2: The only reason everything works well is even when you pass parameters they all 
get sent to the wrapped function as if nothing happened. 
So a caller would not know what they are calling the wrapper or the wrapped 
as they don't need to know (do they?) and wouldn't know if they wanted to (is this true?). 
The function definition and name are the same so it should work is what a caller would assume. 
Am I right in all these assumptions
Ans: Spot on. You’ve just described the "Principle of Least Astonishment"—
a good decorator should be a perfect imposter. Here’s a breakdown of your assumptions:
1. "They don't need to know" (True)
The caller shouldn't care. Whether they are calling a raw function or a decorated one, 
the contract remains the same: "I give you two numbers, you give me a sum." 
If the decorator adds logging or timing in the background, the caller’s life doesn't change. 
This is the heart of Encapsulation.
2. "They wouldn't know if they wanted to" (Mostly True)
To a casual user, it is invisible. However, as we discussed with the __closure__ backpack, 
a "detective" could find out. Without @wraps: It’s obvious. 
If they check add.__name__, it returns "wrapper". The secret is out.
With @wraps: It’s very hard to tell. Python copies the name, docstring, and signature. 
It looks and smells like the original. The "Undo" Button: Most decorators "hide" the original 
function in an attribute called __wrapped__. A suspicious caller could actually bypass your 
decorator by calling add.__wrapped__(3, 5).
3. "The function definition and name are the same" (Exactly!)
Because *args and **kwargs act like a universal funnel, the signature 
(what arguments the function accepts) stays compatible. This is why decorators are so 
powerful for things like: Authentication: "I'll check if you're logged in, 
then pass the arguments through." Caching: "I'll check if I already have the answer for these 
arguments; if not, I'll pass them through." The "Leaky Abstraction" Exception
There is one case where the caller might find out: Performance.
If a decorator is poorly written and adds 2 seconds of delay to every call, 
the caller will definitely notice something is "wrong," even if the results are correct.

"""
##################################
# ============================================================
# SUMMARY
# ============================================================
# Decorator          → function that wraps another function
# @syntax            → shorthand for: func = decorator(func)
# *args/**kwargs     → always use in wrapper to handle any function signature
# @functools.wraps   → always use to preserve __name__ and __doc__
# Parametrized       → factory(args) → decorator(func) → wrapper(*args)
# Stacking           → applies bottom-up, closest decorator first
# Class decorator    → use __call__, good when you need persistent state
# Common uses        → @timer @logger @retry @memoize @repeat
# Built-in           → @lru_cache @cached_property
#                      @property @classmethod @staticmethod
# ============================================================