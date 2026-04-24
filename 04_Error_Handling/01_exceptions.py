# ============================================================
#  CHAPTER 4 — ERROR HANDLING & EXCEPTIONS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT ARE EXCEPTIONS?
# ------------------------------------------------------------
# An exception is an error that happens at RUNTIME.
# Without handling it, your program crashes.
# With handling it, your program recovers gracefully.
#
# Two types of errors:
#   Syntax Error   → code won't even run  (typo, bad indentation)
#   Exception      → code runs but hits a problem

# Common built-in exceptions:
#   TypeError        → wrong type  ("2" + 2)
#   ValueError       → right type, wrong value  (int("abc"))
#   IndexError       → list index out of range
#   KeyError         → dict key doesn't exist
#   AttributeError   → object has no such attribute
#   ZeroDivisionError→ dividing by zero
#   FileNotFoundError→ file doesn't exist
#   NameError        → variable not defined
#   ImportError      → module not found
#   StopIteration    → iterator exhausted
#   OverflowError    → number too large
#   MemoryError      → out of memory
#   RecursionError   → max recursion depth exceeded


# ------------------------------------------------------------
# 2. try / except — catching exceptions
# ------------------------------------------------------------
# Code in try block runs.
# If an exception occurs, execution jumps to except block.

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

print("Program continues...")    # this still runs


# Without try/except — program would crash here:
# result = 10 / 0   ← ZeroDivisionError: division by zero


# ------------------------------------------------------------
# 3. CATCHING THE EXCEPTION OBJECT
# ------------------------------------------------------------
# Use 'as e' to capture the exception and inspect it.

try:
    number = int("abc")
except ValueError as e:
    print(f"Error: {e}")           # invalid literal for int()...
    print(f"Type: {type(e)}")      # <class 'ValueError'>
    print(f"Args: {e.args}")       # ('invalid literal...',)


# ------------------------------------------------------------
# 4. MULTIPLE except BLOCKS
# ------------------------------------------------------------
# Handle different exceptions differently.
# Python checks them in order — first match wins.

def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
    except TypeError:
        print("Error: Both arguments must be numbers")

print(divide(10, 2))    # 5.0
print(divide(10, 0))    # Error: Cannot divide by zero
print(divide(10, "x"))  # Error: Both arguments must be numbers


# ------------------------------------------------------------
# 5. CATCHING MULTIPLE EXCEPTIONS IN ONE LINE
# ------------------------------------------------------------

def parse_input(value):
    try:
        return int(value)
    except (ValueError, TypeError) as e:
        print(f"Could not parse: {e}")
        return None

print(parse_input("42"))     # 42
print(parse_input("abc"))    # Could not parse...
print(parse_input(None))     # Could not parse...


# ------------------------------------------------------------
# 6. else — runs if NO exception was raised
# ------------------------------------------------------------

def read_number(s):
    try:
        n = int(s)
    except ValueError:
        print(f"'{s}' is not a valid integer")
    else:
        # Only runs if try block succeeded — no exception
        print(f"Successfully parsed: {n}")
        return n

read_number("42")     # Successfully parsed: 42
read_number("abc")    # 'abc' is not a valid integer


# ------------------------------------------------------------
# 7. finally — ALWAYS runs no matter what
# ------------------------------------------------------------
# Use for cleanup: close files, release connections, etc.

def open_file(path):
    file = None
    try:
        file = open(path, "r")
        content = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except PermissionError:
        print("No permission to read this file")
        return None
    finally:
        if file:
            file.close()          # ALWAYS closes the file
        print("Cleanup done.")    # ALWAYS runs


# The 'with' statement does this automatically (Chapter 5)
# but finally is important to understand.


# ------------------------------------------------------------
# 8. FULL try / except / else / finally
# ------------------------------------------------------------

def process(data):
    try:
        result = int(data) * 2      # might raise ValueError
        print(f"Processing: {result}")
    except ValueError as e:
        print(f"Bad input: {e}")    # runs if ValueError
    else:
        print("Processing complete!")  # runs if NO exception
    finally:
        print("Always runs.\n")        # runs no matter what

process("10")    # Processing: 20 → complete → always
process("abc")   # Bad input   →             → always


# ------------------------------------------------------------
# 9. raise — throw an exception intentionally
# ------------------------------------------------------------

def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"Age must be int, got {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValueError(f"Age {age} is out of valid range (0-150)")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(f"Caught: {e}")

try:
    set_age("thirty")
except TypeError as e:
    print(f"Caught: {e}")

# Re-raise — catch, log, then re-raise for caller to handle
def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        print(f"Config file missing: {path}")
        raise    # re-raises the same exception


# ------------------------------------------------------------
# 10. CUSTOM EXCEPTIONS
# ------------------------------------------------------------
# Create your own exception classes for meaningful errors.
# Always inherit from Exception (or a subclass of it).

class AppError(Exception):
    """Base exception for this application."""
    pass


class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(self, field, message):
        self.field   = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")


class InsufficientFundsError(AppError):
    """Raised when account balance is too low."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount  = amount
        super().__init__(
            f"Cannot withdraw ${amount:.2f}. Balance: ${balance:.2f}"
        )


class DatabaseError(AppError):
    """Raised on database failures."""
    pass


# Using custom exceptions
def create_user(name, age):
    if not name or not name.strip():
        raise ValidationError("name", "Name cannot be empty")
    if not isinstance(age, int) or age < 0:
        raise ValidationError("age", "Age must be a non-negative integer")
    return {"name": name, "age": age}


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


# Catching custom exceptions
try:
    user = create_user("", 25)
except ValidationError as e:
    print(f"[{e.field}] {e.message}")

try:
    new_balance = withdraw(100, 200)
except InsufficientFundsError as e:
    print(e)
    print(f"Short by: ${e.amount - e.balance:.2f}")

# Catch base class catches all subclasses
try:
    create_user("Alice", -1)
except AppError as e:
    print(f"App error: {e}")


# ------------------------------------------------------------
# 11. EXCEPTION HIERARCHY
# ------------------------------------------------------------
# All exceptions inherit from BaseException.
# Most user exceptions inherit from Exception.
#
# BaseException
#   ├── SystemExit
#   ├── KeyboardInterrupt
#   └── Exception
#         ├── ArithmeticError
#         │     ├── ZeroDivisionError
#         │     └── OverflowError
#         ├── LookupError
#         │     ├── IndexError
#         │     └── KeyError
#         ├── ValueError
#         ├── TypeError
#         ├── AttributeError
#         ├── NameError
#         ├── IOError / OSError
#         │     └── FileNotFoundError
#         └── RuntimeError
#               └── RecursionError
#
# Catching a parent catches ALL its children:
# except Exception  → catches almost everything
# except LookupError → catches both IndexError and KeyError

data = {"key": "value"}
try:
    print(data["missing"])
except LookupError:          # catches KeyError (child of LookupError)
    print("Key or index not found")


# ------------------------------------------------------------
# 12. BEST PRACTICES
# ------------------------------------------------------------

# ✅ 1. Catch SPECIFIC exceptions — not bare except
try:
    x = int("abc")
except ValueError:      # specific
    print("Not a number")

# ❌ Never do this — hides ALL errors including bugs
# try:
#     x = int("abc")
# except:               # catches everything including KeyboardInterrupt!
#     pass

# ✅ 2. Don't silence exceptions without logging
import logging
try:
    result = 1 / 0
except ZeroDivisionError as e:
    logging.error(f"Division error: {e}")   # at least log it
    result = 0

# ✅ 3. Use finally or 'with' for cleanup
# (covered in Modules chapter with file I/O)

# ✅ 4. Raise early, handle late
# Validate at the edge of your system (input), raise immediately.
# Handle exceptions at the level that can do something about it.

# ✅ 5. Use custom exceptions for your app's error types
# Makes it clear what went wrong and where.

# ✅ 6. Keep try blocks SMALL — only the risky line(s)
# ❌ Bad — too much in try
try:
    data = []
    for i in range(10):
        data.append(i)
    result = data[20]         # only THIS can raise IndexError
    print(result)
except IndexError:
    print("Index out of range")

# ✅ Good — minimal try block
data = list(range(10))
try:
    result = data[20]
except IndexError:
    result = None
print(result)


# ------------------------------------------------------------
# 13. COMMON PATTERNS
# ------------------------------------------------------------

# Pattern 1: Safe type conversion
def to_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

print(to_int("42"))       # 42
print(to_int("abc"))      # 0
print(to_int(None, -1))   # -1

# Pattern 2: Safe dict access with custom error
def get_required(d, key):
    try:
        return d[key]
    except KeyError:
        raise ValidationError(key, f"Required field '{key}' is missing")

# Pattern 3: Retry logic
import time

def retry(func, times=3, delay=1):
    for attempt in range(1, times + 1):
        try:
            return func()
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < times:
                time.sleep(delay)
    raise RuntimeError(f"All {times} attempts failed")

# Pattern 4: Context-specific error wrapping
def fetch_user(user_id):
    try:
        # imagine DB call here
        users = {1: "Alice", 2: "Bob"}
        return users[user_id]
    except KeyError:
        raise ValidationError("user_id", f"No user with id {user_id}")

try:
    print(fetch_user(1))    # Alice
    print(fetch_user(99))   # raises ValidationError
except ValidationError as e:
    print(e)


# ============================================================
# SUMMARY
# ============================================================
# try / except         → catch and handle exceptions
# except Type as e     → capture the exception object
# Multiple excepts     → handle different errors differently
# except (A, B)        → catch multiple types at once
# else                 → runs only if NO exception occurred
# finally              → ALWAYS runs — use for cleanup
# raise                → throw an exception intentionally
# raise (bare)         → re-raise the current exception
# Custom exceptions    → class MyError(Exception): ...
# Specific catch       → always prefer over bare except:
# ============================================================