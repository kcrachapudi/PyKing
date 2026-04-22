# ============================================================
#  CHAPTER 1 — STRINGS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. CREATING STRINGS
# ------------------------------------------------------------

s1 = "Hello"                  # double quotes
s2 = 'World'                  # single quotes — same thing
s3 = "It's a great day"       # single quote inside double → fine
s4 = 'He said "wow"'          # double inside single → fine
s5 = "She said \"hello\""     # escape with backslash

# Multi-line strings
poem = """
Roses are red,
Violets are blue,
Python is awesome,
And so are you.
"""
print(poem)

# Raw strings — backslashes are NOT escape characters
# Useful for file paths and regex
path = r"C:\Users\Alice\Documents"
print(path)    # C:\Users\Alice\Documents  (no weird characters)

# ------------------------------------------------------------
# 2. ESCAPE CHARACTERS
# ------------------------------------------------------------

print("Line 1\nLine 2")     # \n = newline
print("Col1\tCol2")         # \t = tab
print("She said \"hi\"")    # \" = literal quote
print("Back\\slash")        # \\ = literal backslash


# ------------------------------------------------------------
# 3. INDEXING — accessing one character
# ------------------------------------------------------------
#
#  String:   P  y  t  h  o  n
#  Index:    0  1  2  3  4  5
#  Negative:-6 -5 -4 -3 -2 -1

word = "Python"

print(word[0])     # P   (first character)
print(word[5])     # n   (last character)
print(word[-1])    # n   (last character, negative index)
print(word[-2])    # o   (second from last)

# Strings are immutable — you cannot change a character
# word[0] = "J"   ← TypeError!  You must create a new string.


# ------------------------------------------------------------
# 4. SLICING — extracting a substring
# ------------------------------------------------------------
# Syntax: string[start : stop : step]
# start  → index to begin (included)
# stop   → index to end   (NOT included)
# step   → how many to jump (default 1)

s = "Hello, World!"

print(s[0:5])      # Hello        (index 0 up to but not including 5)
print(s[7:])       # World!       (from 7 to end)
print(s[:5])       # Hello        (from start to 5)
print(s[-6:])      # World!       (last 6 characters)
print(s[::2])      # Hlo ol!      (every other character)
print(s[::-1])     # !dlroW ,olleH  (reversed)

# Practical: get file extension
filename = "report.pdf"
ext = filename[-3:]          # pdf
name = filename[:-4]         # report


# ------------------------------------------------------------
# 5. STRING METHODS — the big ones
# ------------------------------------------------------------

text = "  Hello, Python World!  "

# Case
print(text.upper())          # "  HELLO, PYTHON WORLD!  "
print(text.lower())          # "  hello, python world!  "
print(text.title())          # "  Hello, Python World!  "
print(text.capitalize())     # "  hello, python world!  " (first char only)
print(text.swapcase())       # flips upper↔lower

# Whitespace
print(text.strip())          # "Hello, Python World!"  (both ends)
print(text.lstrip())         # removes leading spaces only
print(text.rstrip())         # removes trailing spaces only

# Search
print(text.find("Python"))   # 9  (index where it starts, -1 if not found)
print(text.index("Python"))  # 9  (same but raises error if not found)
print(text.count("l"))       # 3  (how many times "l" appears)
print("Python" in text)      # True  (membership test — use this most often)

# Replace
print(text.replace("Python", "Java"))  # replaces all occurrences
print(text.replace("l", "L", 1))       # replace only first occurrence

# Split & Join
sentence = "one two three four"
words = sentence.split(" ")            # ['one', 'two', 'three', 'four']
words2 = sentence.split(" ", 2)        # ['one', 'two', 'three four']  (max 2 splits)

csv_line = "Alice,30,Engineer"
parts = csv_line.split(",")            # ['Alice', '30', 'Engineer']

# join — opposite of split
print(", ".join(["a", "b", "c"]))      # a, b, c
print("-".join(words))                 # one-two-three-four
print("".join(["H","i","!"])  )        # Hi!

# Check content
print("hello".isalpha())    # True  (only letters)
print("123".isdigit())      # True  (only digits)
print("abc123".isalnum())   # True  (letters and/or digits)
print("  ".isspace())       # True  (only whitespace)

# Starts / ends with
url = "https://example.com"
print(url.startswith("https"))   # True
print(url.endswith(".com"))      # True

# Strip specific characters
print("###hello###".strip("#"))  # hello


# ------------------------------------------------------------
# 6. F-STRINGS (formatted string literals) — use these always
# ------------------------------------------------------------

name = "Alice"
age = 30
score = 95.678

# Basic embedding
print(f"Name: {name}, Age: {age}")

# Expressions inside {}
print(f"Next year: {age + 1}")
print(f"Upper: {name.upper()}")

# Number formatting
print(f"{score:.2f}")        # 95.68   (2 decimal places)
print(f"{score:.0f}")        # 96      (0 decimal places = rounded)
print(f"{1000000:,}")        # 1,000,000  (thousands separator)
print(f"{0.25:.0%}")         # 25%     (as percentage)
print(f"{42:05d}")           # 00042   (zero-padded to width 5)

# Alignment
print(f"{'left':<10}|")      # "left      |"  (left align in 10 chars)
print(f"{'right':>10}|")     # "     right|"  (right align)
print(f"{'center':^10}|")    # "  center  |"  (center)


# ------------------------------------------------------------
# 7. STRING CONCATENATION & REPETITION
# ------------------------------------------------------------

first = "Hello"
second = "World"

# Concatenation with +
print(first + " " + second)    # Hello World

# Repetition with *
print("ha" * 3)                # hahaha
print("-" * 40)                # ----------------------------------------

# DON'T concatenate inside loops — slow!
# ❌ Bad
result = ""
for i in range(5):
    result += str(i)          # creates a new string every time

# ✅ Good — collect then join
parts = []
for i in range(5):
    parts.append(str(i))
result = "".join(parts)        # "01234"


# ------------------------------------------------------------
# 8. STRING IMMUTABILITY
# ------------------------------------------------------------

# Strings CANNOT be changed after creation
s = "hello"
# s[0] = "H"   ← TypeError: 'str' object does not support item assignment

# You must create a NEW string
s = "H" + s[1:]    # "Hello"
print(s)

# Or use replace
s = "hello".replace("h", "H")
print(s)    # Hello


# ------------------------------------------------------------
# 9. USEFUL BUILT-IN FUNCTIONS WITH STRINGS
# ------------------------------------------------------------

print(len("Python"))         # 6
print(min("python"))         # h  (alphabetically smallest)
print(max("python"))         # y  (alphabetically largest)
print(sorted("python"))      # ['h', 'n', 'o', 'p', 't', 'y']
print(list("abc"))           # ['a', 'b', 'c']
print(ord("A"))              # 65  (ASCII code)
print(chr(65))               # A   (character from ASCII code)


# ------------------------------------------------------------
# 10. COMMON PATTERNS YOU WILL USE EVERYWHERE
# ------------------------------------------------------------

# Reverse a string
s = "hello"
print(s[::-1])               # olleh

# Check if palindrome
word = "racecar"
print(word == word[::-1])    # True

# Count vowels
sentence = "Hello World"
vowels = sum(1 for c in sentence if c.lower() in "aeiou")
print(vowels)    # 3

# Remove all spaces
print("h e l l o".replace(" ", ""))    # hello

# Check if a string is a number
print("123".isdigit())       # True
print("12.3".isdigit())      # False  ← floats need try/except

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

print(is_number("12.3"))     # True
print(is_number("abc"))      # False

# Title-case a name safely
name = "alice bob"
print(name.title())          # Alice Bob


# ============================================================
# SUMMARY
# ============================================================
# Creation    → "text", 'text', """multiline""", r"raw"
# Indexing    → s[0], s[-1]
# Slicing     → s[start:stop:step], s[::-1] to reverse
# Methods     → .upper() .lower() .strip() .replace()
#               .split() .join() .find() .startswith()
# f-strings   → f"{var:.2f}"  always prefer these
# Immutable   → can't change in place, must create new string
# ============================================================