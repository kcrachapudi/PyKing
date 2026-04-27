# ============================================================
#  CHAPTER 6 — CONTEXT MANAGERS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A CONTEXT MANAGER?
# ------------------------------------------------------------
# A context manager is an object that sets something UP
# before a block of code runs, and CLEANS IT UP afterwards —
# even if an error occurs inside the block.
#
# You already use one every time you open a file:
#   with open("file.txt") as f:
#       ...
#
# The 'with' statement IS the context manager protocol.
#
# Real-world analogy:
#   A hotel room:
#     - check in  (setup)   → room is ready
#     - stay      (block)   → do your work
#     - check out (cleanup) → room is cleaned, key returned
#
# Why does this matter?
#   Without context managers, if your code crashes mid-way,
#   the file stays open, the DB connection leaks, the lock
#   never releases. Context managers fix this automatically.


# ------------------------------------------------------------
# 2. THE with STATEMENT — how you USE context managers
# ------------------------------------------------------------

# Basic syntax:
#   with  <context_manager>  as  <variable>:
#       <block of code>
#   → setup runs before block
#   → cleanup runs after block (even if exception occurs)

# You've seen this with files:
with open("demo.txt", "w") as f:    # open() returns a context manager
    f.write("Hello\n")              # do work inside the block
    f.write("World\n")
# file is automatically closed here — even if an exception occurred above

# Without 'with' — you must close manually (easy to forget, dangerous)
f = open("demo.txt", "r")
content = f.read()
f.close()    # if an exception happens before this, file stays open!

# With 'with' — guaranteed cleanup, no matter what
with open("demo.txt", "r") as f:
    content = f.read()    # even if this raises an exception, file closes

print(content)


# ------------------------------------------------------------
# 3. HOW context managers WORK INTERNALLY
# ------------------------------------------------------------
# A context manager is any object that has two special methods:
#   __enter__  → runs when 'with' block starts (setup)
#   __exit__   → runs when 'with' block ends   (cleanup)

# Python translates:
#   with CM() as x:
#       body
#
# Into roughly:
#   cm = CM()
#   x = cm.__enter__()     ← setup, x gets the return value
#   try:
#       body
#   finally:
#       cm.__exit__(...)   ← cleanup, always runs


# ------------------------------------------------------------
# 4. BUILDING A CONTEXT MANAGER WITH A CLASS
# ------------------------------------------------------------
# Define __enter__ and __exit__ on any class.

class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename    # store args for later
        self.mode     = mode
        self.file     = None        # will hold the open file object

    def __enter__(self):
        print(f"Opening {self.filename}...")
        self.file = open(self.filename, self.mode)  # do the setup
        return self.file    # this becomes the 'as' variable in 'with ... as f'

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type  → type of exception (None if no exception)
        # exc_val   → exception value/message (None if no exception)
        # exc_tb    → traceback object (None if no exception)
        print(f"Closing {self.filename}...")
        if self.file:
            self.file.close()    # always close the file
        # Return False (or None) to let exceptions propagate normally
        # Return True to SUPPRESS the exception (rarely what you want)
        return False

with FileManager("demo.txt", "r") as f:
    content = f.read()
    print(content[:20])
# Opening demo.txt...
# Hello
# World
# Closing demo.txt...   ← always runs


# ------------------------------------------------------------
# 5. HANDLING EXCEPTIONS IN __exit__
# ------------------------------------------------------------
# __exit__ receives exception info so you can decide what to do.

class SuppressError:
    def __init__(self, *exception_types):
        self.exception_types = exception_types   # store which exceptions to suppress

    def __enter__(self):
        return self    # return self so you can use 'as' if needed

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False                    # no exception — nothing to do

        if issubclass(exc_type, self.exception_types):
            print(f"Suppressed: {exc_val}") # log it so it's not silent
            return True                     # return True = suppress the exception
                                            # the 'with' block ends quietly

        return False    # for all other exceptions, let them propagate normally


# Suppress only ZeroDivisionError
with SuppressError(ZeroDivisionError):
    result = 10 / 0          # this raises ZeroDivisionError
    print("This won't run")  # skipped because exception occurred above

print("But execution continues here!")  # runs because exception was suppressed

# Contrast — KeyError is NOT suppressed
# with SuppressError(ZeroDivisionError):
#     d = {}
#     d["missing"]    # KeyError — NOT suppressed, will propagate


# ------------------------------------------------------------
# 6. BUILDING A CONTEXT MANAGER WITH @contextmanager
# ------------------------------------------------------------
# The class approach works but is verbose.
# contextlib.contextmanager lets you write a context manager
# as a simple generator function — much cleaner.
#
# Structure:
#   - everything BEFORE yield  → setup    (__enter__)
#   - the yield value          → the 'as' variable
#   - everything AFTER yield   → cleanup  (__exit__)
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode):
    print(f"Opening {filename}")
    f = open(filename, mode)        # SETUP: open the file
    try:
        yield f                     # give the file to the 'with' block
                                    # code inside 'with' runs here
    finally:
        f.close()                   # CLEANUP: always close (finally = always runs)
        print(f"Closed {filename}")

with managed_file("demo.txt", "r") as f:
    print(f.read()[:10])
# Opening demo.txt
# Hello
# W
# Closed demo.txt


# --- Timer context manager ---
import time

@contextmanager
def timer(label=""):
    start = time.perf_counter()    # record start time before block runs
    try:
        yield                      # run the 'with' block (no 'as' value needed)
    finally:
        elapsed = time.perf_counter() - start    # calculate elapsed time
        print(f"{label} took {elapsed:.4f}s")    # always print, even on exception

with timer("List creation"):
    data = [x**2 for x in range(100_000)]    # code being timed
# List creation took 0.0123s


# --- Temporary directory context manager ---
import os
import shutil

@contextmanager
def temp_directory(name="temp"):
    """Create a temporary directory, clean it up when done."""
    os.makedirs(name, exist_ok=True)    # SETUP: create the directory
    print(f"Created temp dir: {name}")
    try:
        yield name                       # give the directory name to the block
    finally:
        shutil.rmtree(name)              # CLEANUP: delete directory and all contents
        print(f"Deleted temp dir: {name}")

with temp_directory("my_temp") as tmpdir:
    # write temporary files inside — they'll be gone after the block
    with open(f"{tmpdir}/temp.txt", "w") as f:
        f.write("temporary data")
    print(f"Working in {tmpdir}")
# Created temp dir: my_temp
# Working in my_temp
# Deleted temp dir: my_temp


# ------------------------------------------------------------
# 7. PRACTICAL CONTEXT MANAGERS
# ------------------------------------------------------------

# --- Database transaction context manager ---
@contextmanager
def transaction(connection):
    """Commit on success, rollback on failure."""
    try:
        yield connection        # let the block use the connection
        connection.commit()     # if block succeeded, commit changes
        print("Transaction committed")
    except Exception as e:
        connection.rollback()   # if block raised exception, undo all changes
        print(f"Transaction rolled back: {e}")
        raise                   # re-raise so caller knows something went wrong


# --- Redirect stdout context manager ---
import sys
from io import StringIO

@contextmanager
def capture_output():
    """Capture everything printed to stdout inside the block."""
    old_stdout = sys.stdout         # save the real stdout
    sys.stdout = StringIO()         # replace stdout with a string buffer
    try:
        yield sys.stdout            # give the buffer to the block
    finally:
        sys.stdout = old_stdout     # ALWAYS restore real stdout

with capture_output() as captured:
    print("This goes to the buffer, not the screen")
    print("So does this")

output = captured.getvalue()    # retrieve what was "printed"
print(f"Captured: {repr(output)}")
# Captured: 'This goes to the buffer, not the screen\nSo does this\n'


# --- Suppress specific exceptions (from contextlib) ---
from contextlib import suppress   # Python's built-in version of SuppressError

with suppress(FileNotFoundError):
    os.remove("file_that_does_not_exist.txt")   # would normally raise FileNotFoundError
    # suppress catches it and moves on silently

print("Continues normally")


# --- Change directory context manager ---
@contextmanager
def change_dir(path):
    """Temporarily change the working directory."""
    original = os.getcwd()          # remember where we are now
    os.chdir(path)                  # move to the new directory
    try:
        yield                       # run the block in the new directory
    finally:
        os.chdir(original)          # ALWAYS go back, even on exception

# with change_dir("/tmp"):
#     print(os.getcwd())    # /tmp
# print(os.getcwd())        # back to original directory


# --- Logging context manager ---
@contextmanager
def log_block(name):
    """Log the start and end of a block, and any errors."""
    print(f"[START] {name}")
    start = time.perf_counter()
    try:
        yield                        # run the block
        elapsed = time.perf_counter() - start
        print(f"[END]   {name} — {elapsed:.4f}s")
    except Exception as e:
        elapsed = time.perf_counter() - start
        print(f"[ERROR] {name} — {e} (after {elapsed:.4f}s)")
        raise                        # re-raise so the program still sees the error

with log_block("data processing"):
    data = [x**2 for x in range(10_000)]
# [START] data processing
# [END]   data processing — 0.0010s


# ------------------------------------------------------------
# 8. MULTIPLE CONTEXT MANAGERS IN ONE with STATEMENT
# ------------------------------------------------------------

# Open two files at once — both are guaranteed to close
with open("demo.txt", "r") as src, open("copy.txt", "w") as dst:
    for line in src:        # read each line from source
        dst.write(line)     # write it to destination
# both files close here automatically

# This is equivalent to nested with statements:
# with open("demo.txt", "r") as src:
#     with open("copy.txt", "w") as dst:
#         ...


# ------------------------------------------------------------
# 9. contextlib UTILITIES — useful tools from the standard library
# ------------------------------------------------------------
from contextlib import (
    contextmanager,    # already covered — turn generator into context manager
    suppress,          # already covered — suppress specific exceptions
    ExitStack,         # manage dynamic number of context managers
    nullcontext,       # a no-op context manager (useful for optional CMs)
)

# --- ExitStack — when you don't know how many CMs you need ---
# Useful when the number of files/connections is determined at runtime

filenames = ["demo.txt", "copy.txt"]    # could be any number of files

with ExitStack() as stack:
    # open each file and register it with the stack
    files = [stack.enter_context(open(f, "r")) for f in filenames]
    # ALL files are guaranteed to close when the block ends
    for f in files:
        print(f.readline().strip())


# --- nullcontext — a context manager that does nothing ---
# Useful when a context manager is optional

def process(data, lock=None):
    # If a lock was provided, use it. If not, use nullcontext (does nothing).
    # This avoids writing if/else around every with statement.
    from contextlib import nullcontext
    with (lock if lock is not None else nullcontext()):
        return [x * 2 for x in data]    # safe whether lock exists or not

print(process([1, 2, 3]))           # no lock — nullcontext used
# print(process([1, 2, 3], some_lock))  # with lock — lock used


# ------------------------------------------------------------
# 10. CLEANUP — remove files created in this script
# ------------------------------------------------------------
import os
for fname in ["demo.txt", "copy.txt"]:
    try:
        os.remove(fname)    # delete each temp file created during this script
    except FileNotFoundError:
        pass                # if it doesn't exist, skip quietly


# ============================================================
# SUMMARY
# ============================================================
# with CM() as x        → use a context manager
# __enter__             → runs on block entry (setup), return value = 'as' var
# __exit__(t, v, tb)    → runs on block exit (cleanup), return True to suppress
# @contextmanager       → turn a generator function into a context manager
#                         code before yield = setup
#                         yield value       = 'as' variable
#                         code after yield  = cleanup (put in finally!)
# suppress(Err)         → silently swallow specific exceptions
# ExitStack             → manage dynamic/variable number of CMs
# nullcontext           → no-op CM for optional context managers
# Multiple CMs          → with A() as a, B() as b:
# Key guarantee         → cleanup ALWAYS runs, even on exceptions
# ============================================================