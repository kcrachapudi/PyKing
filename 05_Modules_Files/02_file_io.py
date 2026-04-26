# ============================================================
#  CHAPTER 5 — FILE I/O (Input / Output)
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS FILE I/O?
# ------------------------------------------------------------
# File I/O = reading from and writing to files on disk.
# Every real program does this — configs, logs, data, reports.
#
# File modes:
#   "r"   → read       (default) — file must exist
#   "w"   → write      — creates file, OVERWRITES if exists
#   "a"   → append     — adds to end, creates if not exists
#   "x"   → exclusive  — creates new file, fails if exists
#   "r+"  → read+write — file must exist
#   "b"   → binary mode (add to above: "rb", "wb")
#   "t"   → text mode  (default, can omit)


# ------------------------------------------------------------
# 2. OPENING AND CLOSING FILES — the basic way
# ------------------------------------------------------------

# Always close files after using them to free resources.
# Without closing: data may not be written, resources leak.

file = open("sample.txt", "w")
file.write("Hello, World!\n")
file.write("Python File I/O\n")
file.close()    # must close manually — easy to forget!


# ------------------------------------------------------------
# 3. THE with STATEMENT — always use this
# ------------------------------------------------------------
# 'with' automatically closes the file when the block ends,
# even if an exception occurs. This is the correct way.

# Writing
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3\n")
# file is automatically closed here

# Reading entire file at once
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)
# Line 1
# Line 2
# Line 3


# ------------------------------------------------------------
# 4. READING FILES — all the ways
# ------------------------------------------------------------

# First, create a sample file to read
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("Alice,30,Engineer\n")
    f.write("Bob,25,Designer\n")
    f.write("Charlie,35,Manager\n")
    f.write("Diana,28,Developer\n")

# --- read() — entire file as one string ---
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(repr(content))    # 'Alice,30...\nBob,25...\n...'

# --- read(n) — read n characters ---
with open("data.txt", "r", encoding="utf-8") as f:
    first10 = f.read(10)
print(first10)    # 'Alice,30,E'

# --- readline() — one line at a time ---
with open("data.txt", "r", encoding="utf-8") as f:
    line1 = f.readline()    # 'Alice,30,Engineer\n'
    line2 = f.readline()    # 'Bob,25,Designer\n'
print(line1.strip())
print(line2.strip())

# --- readlines() — all lines as a list ---
with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print(lines)
# ['Alice,30,Engineer\n', 'Bob,25,Designer\n', ...]

# Strip newlines
lines = [line.strip() for line in lines]
print(lines)

# --- Iterate line by line — BEST for large files ---
# Memory efficient — doesn't load whole file at once
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:              # f itself is an iterator
        print(line.strip())


# ------------------------------------------------------------
# 5. WRITING FILES
# ------------------------------------------------------------

# --- write() --- writes a string (no newline added automatically)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("First line\n")
    f.write("Second line\n")

# --- writelines() --- writes a list of strings
lines = ["one\n", "two\n", "three\n"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

# Using print() with file argument
with open("output.txt", "w", encoding="utf-8") as f:
    print("Hello from print!", file=f)
    print("Another line", file=f)

# "w" mode overwrites. "a" mode appends:
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")    # adds to end without erasing


# ------------------------------------------------------------
# 6. FILE POSITION — seek() and tell()
# ------------------------------------------------------------

with open("sample.txt", "r", encoding="utf-8") as f:
    print(f.tell())       # 0 — at the start

    content = f.read(6)   # read 6 chars
    print(content)        # "Line 1"
    print(f.tell())       # 6 — current position

    f.seek(0)             # go back to start
    print(f.tell())       # 0

    f.seek(0, 2)          # seek to END (0 bytes from end)
    print(f.tell())       # file size in bytes


# ------------------------------------------------------------
# 7. WORKING WITH CSV FILES
# ------------------------------------------------------------
import csv

# Writing CSV
employees = [
    ["Name",    "Age", "Role"],
    ["Alice",   30,    "Engineer"],
    ["Bob",     25,    "Designer"],
    ["Charlie", 35,    "Manager"],
]

with open("employees.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(employees)    # write all rows at once
    # or row by row: writer.writerow(["Dave", 28, "Dev"])

# Reading CSV
with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)    # ['Name', 'Age', 'Role'], ['Alice', '30', ...]

# DictReader — rows as dicts (column name → value)
with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['Name']} is {row['Age']} years old")

# DictWriter — write dicts to CSV
employees_data = [
    {"Name": "Alice", "Age": 30, "Role": "Engineer"},
    {"Name": "Bob",   "Age": 25, "Role": "Designer"},
]

with open("employees2.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["Name", "Age", "Role"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()         # writes column names
    writer.writerows(employees_data)


# ------------------------------------------------------------
# 8. WORKING WITH JSON FILES
# ------------------------------------------------------------
import json

# Writing JSON
data = {
    "users": [
        {"id": 1, "name": "Alice", "scores": [95, 87, 92]},
        {"id": 2, "name": "Bob",   "scores": [78, 85, 88]},
    ],
    "total": 2
}

with open("users.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)    # indent=2 for pretty printing

# Reading JSON
with open("users.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded["total"])                    # 2
print(loaded["users"][0]["name"])         # Alice
print(loaded["users"][1]["scores"])       # [78, 85, 88]

# JSON with custom types — default serializer handles: dict, list,
# str, int, float, bool, None
# For custom objects, use a custom encoder:

class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)


# ------------------------------------------------------------
# 9. pathlib — modern, recommended approach
# ------------------------------------------------------------
from pathlib import Path

# pathlib.Path makes file operations cleaner than os.path

# Write and read text
p = Path("notes.txt")
p.write_text("Hello from pathlib!\nLine 2\n", encoding="utf-8")
content = p.read_text(encoding="utf-8")
print(content)

# Check existence
print(p.exists())     # True
print(p.is_file())    # True
print(p.is_dir())     # False

# File info
print(p.name)         # notes.txt
print(p.stem)         # notes
print(p.suffix)       # .txt
print(p.stat().st_size)  # file size in bytes

# Safe path building (cross-platform)
base = Path(".")
data_file = base / "data" / "users.json"   # . / data / users.json
print(data_file)

# Create directories safely
output_dir = Path("output") / "reports" / "2024"
output_dir.mkdir(parents=True, exist_ok=True)

# Glob — find files matching a pattern
for txt_file in Path(".").glob("*.txt"):
    print(txt_file.name)

for py_file in Path(".").rglob("*.py"):    # recursive glob
    print(py_file)

# Rename and delete
p.rename("notes_renamed.txt")
Path("notes_renamed.txt").unlink()    # delete file


# ------------------------------------------------------------
# 10. BINARY FILES
# ------------------------------------------------------------

# Write binary data
with open("binary.bin", "wb") as f:
    f.write(b"\x00\x01\x02\x03\xFF\xFE")   # raw bytes

# Read binary data
with open("binary.bin", "rb") as f:
    data = f.read()
print(data)           # b'\x00\x01\x02\x03\xff\xfe'
print(list(data))     # [0, 1, 2, 3, 255, 254]

# Copy a file (binary-safe)
def copy_file(src, dst):
    with open(src, "rb") as f_in:
        with open(dst, "wb") as f_out:
            f_out.write(f_in.read())

# Or use shutil (cleaner)
import shutil
shutil.copy("data.txt", "data_backup.txt")
shutil.copy2("data.txt", "data_backup2.txt")   # preserves metadata


# ------------------------------------------------------------
# 11. COMMON PATTERNS
# ------------------------------------------------------------

# Pattern 1: Safe file read with error handling
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except PermissionError:
        print(f"No permission to read: {path}")
        return None

# Pattern 2: Read and process line by line
def count_lines(path):
    count = 0
    with open(path, "r", encoding="utf-8") as f:
        for _ in f:
            count += 1
    return count

# Pattern 3: Append to a log file
def log(message, log_file="app.log"):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

log("Application started")
log("User logged in: Alice")

# Pattern 4: Read config from JSON
def load_config(path="config.json"):
    default = {"debug": False, "port": 8080, "host": "localhost"}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default

# Pattern 5: Write all results to CSV
def save_results(results, path="results.csv"):
    if not results:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

results = [
    {"name": "Alice", "score": 92},
    {"name": "Bob",   "score": 85},
]
save_results(results)

# Pattern 6: Temp file for safe writes (write to temp, then rename)
import tempfile
import os

def safe_write(path, content):
    """Write atomically — file is never partially written."""
    dir_name = os.path.dirname(path) or "."
    with tempfile.NamedTemporaryFile(mode="w", dir=dir_name,
                                      delete=False, encoding="utf-8") as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    os.replace(tmp_path, path)   # atomic on most OS


# ------------------------------------------------------------
# 12. CLEANUP — remove files created during this script
# ------------------------------------------------------------
import os

# This is CLEANUP CODE — it runs at the END of the script to delete
# all the temporary files and folders that were created DURING the script.
# Think of it as tidying up after yourself so your folder stays clean.

# Loop through a list of filenames that were created earlier in the script
for fname in ["sample.txt", "data.txt", "output.txt", ...]:
    try:
        os.remove(fname)          # os.remove() deletes a single FILE
    except FileNotFoundError:
        pass                      # if the file doesn't exist (maybe it was
                                  # never created), just skip it silently
                                  # instead of crashing

# Loop through folder names created during the script
for dname in ["output", "new_folder"]:
    try:
        shutil.rmtree(dname)      # shutil.rmtree() deletes a FOLDER and
                                  # everything inside it (rm = remove, tree = folder tree)
    except FileNotFoundError:
        pass                      # same idea — skip if folder doesn't exist

# ============================================================
# SUMMARY
# ============================================================
# open(path, mode)      → open a file
# modes: r w a x rb wb → read write append exclusive binary
# with open(...) as f   → ALWAYS use this (auto-closes)
# f.read()              → entire file as string
# f.readline()          → one line
# f.readlines()         → all lines as list
# for line in f         → iterate line by line (memory efficient)
# f.write(str)          → write string
# f.writelines(list)    → write list of strings
# f.seek(n)             → move to position n
# f.tell()              → current position
# csv.reader/writer     → read/write CSV
# csv.DictReader/Writer → CSV rows as dicts
# json.load/dump        → read/write JSON from/to file
# json.loads/dumps      → JSON from/to string
# pathlib.Path          → modern path handling
# shutil.copy           → copy files
# ============================================================