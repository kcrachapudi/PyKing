# ============================================================
#  CHAPTER 1 — VARIABLES & DATA TYPES
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS A VARIABLE?
# ------------------------------------------------------------
# A variable is a name that points to a value in memory.
# Python figures out the type automatically — no need to declare it.

name = "Alice"
age = 30
height = 5.7
is_student = True

print(name)       # Alice
print(age)        # 30
print(height)     # 5.7
print(is_student) # True


# ------------------------------------------------------------
# 2. THE CORE DATA TYPES
# ------------------------------------------------------------

# --- int (whole numbers) ---
x = 10
y = -5
big = 1_000_000     # underscores make big numbers readable

# --- float (decimal numbers) ---
pi = 3.14159
temp = -12.5
sci = 1.5e3         # scientific notation → 1500.0

# --- str (text) ---
greeting = "Hello"
name = 'World'      # single or double quotes, both fine
multiline = """
This spans
multiple lines.
"""

# --- bool (True or False) ---
raining = False
sunny = True

# --- NoneType (absence of a value) ---
result = None       # like null in other languages


# ------------------------------------------------------------
# 3. CHECKING THE TYPE
# ------------------------------------------------------------

print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
print(type("hi"))      # <class 'str'>
print(type(True))      # <class 'bool'>
print(type(None))      # <class 'NoneType'>


# ------------------------------------------------------------
# 4. TYPE CONVERSION (CASTING)
# ------------------------------------------------------------

# str → int
num_str = "42"
num_int = int(num_str)     # 42
print(type(num_int))       # <class 'int'>

# int → float
print(float(10))           # 10.0

# int → str
print(str(100))            # "100"

# float → int (truncates, does NOT round)
print(int(9.9))            # 9   ← watch out!

# bool ← anything
print(bool(0))             # False
print(bool(1))             # True
print(bool(""))            # False  (empty string is falsy)
print(bool("hi"))          # True
print(bool(None))          # False


# ------------------------------------------------------------
# 5. BASIC ARITHMETIC OPERATORS
# ------------------------------------------------------------

print(10 + 3)    # 13   addition
print(10 - 3)    # 7    subtraction
print(10 * 3)    # 30   multiplication
print(10 / 3)    # 3.333...  division (always returns float)
print(10 // 3)   # 3    floor division (whole number only)
print(10 % 3)    # 1    modulus (remainder)
print(10 ** 3)   # 1000 exponentiation (10 to the power of 3)


# ------------------------------------------------------------
# 6. STRINGS IN DEPTH
# ------------------------------------------------------------

name = "Python King"

# Length
print(len(name))          # 11

# Indexing (starts at 0)
print(name[0])            # P
print(name[-1])           # g  (negative = from the end)

# Slicing [start:stop:step]
print(name[0:6])          # Python
print(name[7:])           # King
print(name[:6])           # Python

#Reverse slicing
print(name[::-1])         # gniK nohtyP  (reversed)
#The Shift: Since you're moving backward, Python assumes you want to start at the end of the string and finish at the beginning.
#The Starting Line: It places the "pointer" at the very last character (g) instead of 0.
#The Movement: It then steps backward through the indices: 10, 9, 8... all the way to 0.
#To reverse only the word "King" (which occupies indices 7 through 10) and stop there, you would use:
print(name[:6:-1])
#To print "nohtyP", you can combine slicing:
print(name[5::-1]) #This handles the reversal.

# Common string methods
print(name.upper())       # PYTHON KING
print(name.lower())       # python king
print(name.replace("King", "Master"))  # Python Master
print(name.split(" "))    # ['Python', 'King']
print("  hello  ".strip())  # "hello"  removes whitespace
print(name.startswith("Py")) # True
print(name.endswith("ng"))   # True
print("King" in name)     # True  (membership test)

# f-strings — the modern way to embed variables in strings
age = 30
print(f"My name is {name} and I am {age} years old.")
print(f"Next year I will be {age + 1}.")   # expressions work too
print(f"{3.14159:.2f}")    # 3.14  (format to 2 decimal places)


# ------------------------------------------------------------
# 7. MULTIPLE ASSIGNMENT & SWAPPING
# ------------------------------------------------------------

# Assign multiple variables in one line
a, b, c = 1, 2, 3

# Swap without a temp variable (very Pythonic)
a, b = b, a
print(a, b)    # 2 1

#Python swap can work with any data type and mixing types
# Python will not raise a runtime error when you swap variables of different types.
# Even in Object-Oriented Python, the same rules apply: 
# Python remains dynamic, even inside classes.

#The tools like mypy are designed to catch type errors,
#  but they are not perfect and can be bypassed.

# Assign same value to many variables
x = y = z = 0


# ------------------------------------------------------------
# 8. COMPARISON OPERATORS (return True or False)
# ------------------------------------------------------------

print(5 == 5)    # True   equal to
print(5 != 4)    # True   not equal to
print(5 > 3)     # True   greater than
print(5 < 3)     # False  less than
print(5 >= 5)    # True   greater than or equal
print(5 <= 4)    # False  less than or equal


# ------------------------------------------------------------
# 9. LOGICAL OPERATORS
# ------------------------------------------------------------

print(True and False)   # False  (both must be True)
print(True or False)    # True   (at least one must be True)
print(not True)         # False  (flips it)

# Practical example
age = 20
has_id = True
can_enter = age >= 18 and has_id
print(can_enter)    # True

# ------------------------------------------------------------
# 10. COMMON BEGINNER MISTAKES TO AVOID
# ------------------------------------------------------------

# ❌ Mistake 1: int division looks like float
print(7 / 2)     # 3.5  (not 3!)  use // for integer division
print(7 // 2)    # 3

# ❌ Mistake 2: string + number doesn't work
# print("Age: " + 30)   → TypeError!
print("Age: " + str(30))   # ✅ convert first

# ❌ Mistake 3: = is assignment, == is comparison
x = 5          # assigns 5 to x
print(x == 5)  # checks if x equals 5 → True

# ❌ Mistake 4: int("3.14") fails — convert via float first
print(int(float("3.14")))   # 3  ✅


# ============================================================
# SUMMARY
# ============================================================
# int      → whole numbers           42, -7, 1_000
# float    → decimals                3.14, -0.5
# str      → text                    "hello", 'world'
# bool     → True / False
# None     → no value / absence
#
# type()   → check the type
# int()  float()  str()  bool()  → convert between types
# ============================================================