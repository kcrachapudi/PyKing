# ============================================================
#  CHAPTER 1 — CONTROL FLOW
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. THE if STATEMENT
# ------------------------------------------------------------
# Python runs the block only if the condition is True.
# Indentation (4 spaces) defines the block — NOT curly braces.

age = 20

if age >= 18:
    print("You are an adult.")

# Nothing happens if condition is False and there is no else
if age < 10:
    print("This will NOT print.")


# ------------------------------------------------------------
# 2. if / else
# ------------------------------------------------------------

score = 55

if score >= 60:
    print("Pass")
else:
    print("Fail")    # prints this


# ------------------------------------------------------------
# 3. if / elif / else
# ------------------------------------------------------------
# elif = "else if" — check multiple conditions in order.
# Python stops at the FIRST True condition.

score = 82

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"     # ← this one matches, stops here
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(grade)    # B


# ------------------------------------------------------------
# 4. COMPARISON OPERATORS
# ------------------------------------------------------------

x = 10

print(x == 10)    # True   equal to
print(x != 5)     # True   not equal to
print(x > 8)      # True   greater than
print(x < 8)      # False  less than
print(x >= 10)    # True   greater than or equal
print(x <= 9)     # False  less than or equal

# ⚠️  = is assignment.  == is comparison. Common beginner mistake.
x = 5      # assigns 5 to x
x == 5     # checks if x equals 5 (but doesn't print anything)
print(x == 5)    # True


# ------------------------------------------------------------
# 5. LOGICAL OPERATORS — and, or, not
# ------------------------------------------------------------

age = 25
has_ticket = True
is_vip = False

# and → BOTH must be True
if age >= 18 and has_ticket:
    print("You can enter.")

# or → AT LEAST ONE must be True
if has_ticket or is_vip:
    print("Access granted.")

# not → flips True to False and vice versa
if not is_vip:
    print("Not a VIP.")

# Combining them — use parentheses to be clear
if (age >= 18 and has_ticket) or is_vip:
    print("Welcome!")


# ------------------------------------------------------------
# 6. TRUTHY AND FALSY VALUES
# ------------------------------------------------------------
# In Python, every value has a truth value — not just True/False.

# FALSY — treated as False in conditions:
#   False, None, 0, 0.0, "", [], {}, set(), ()

# TRUTHY — everything else is treated as True

# Examples
if 0:
    print("won't print")    # 0 is falsy

if 1:
    print("prints!")        # any non-zero number is truthy

if "":
    print("won't print")    # empty string is falsy

if "hello":
    print("prints!")        # non-empty string is truthy

if []:
    print("won't print")    # empty list is falsy

if [1, 2, 3]:
    print("prints!")        # non-empty list is truthy

if None:
    print("won't print")    # None is falsy

# Practical use — check if a list has items
names = ["Alice", "Bob"]
if names:                   # cleaner than: if len(names) > 0
    print("We have names!")


# ------------------------------------------------------------
# 7. NESTED if STATEMENTS
# ------------------------------------------------------------

logged_in = True
is_admin = False

if logged_in:
    print("Welcome back!")
    if is_admin:
        print("Admin panel available.")
    else:
        print("Regular user view.")
else:
    print("Please log in.")

# ⚠️  Don't nest too deep — if you're 4+ levels in, refactor.


# ------------------------------------------------------------
# 8. TERNARY OPERATOR (one-line if/else)
# ------------------------------------------------------------
# Syntax:  value_if_true  if  condition  else  value_if_false

age = 20
status = "adult" if age >= 18 else "minor"
print(status)    # adult

# Assigning a default
name = ""
display_name = name if name else "Guest"
print(display_name)    # Guest

# Can be used inline
print("Even" if 4 % 2 == 0 else "Odd")    # Even

# ⚠️  Keep it simple. If it's hard to read, use a regular if/else.


# ------------------------------------------------------------
# 9. MEMBERSHIP OPERATORS — in, not in
# ------------------------------------------------------------

fruits = ["apple", "banana", "cherry"]

print("apple" in fruits)        # True
print("mango" in fruits)        # False
print("mango" not in fruits)    # True

# Works on strings too
print("py" in "python")         # True
print("z" not in "python")      # True

# Works on dicts (checks keys)
person = {"name": "Alice", "age": 30}
print("name" in person)         # True
print("email" in person)        # False


# ------------------------------------------------------------
# 10. IDENTITY OPERATORS — is, is not
# ------------------------------------------------------------
# is checks if two variables point to the SAME object in memory.
# == checks if two variables have the SAME VALUE.

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)     # True   — same value
print(a is b)     # False  — different objects in memory
print(a is c)     # True   — c points to the SAME object as a

# Use 'is' ONLY for None checks — that's the standard practice
value = None
if value is None:
    print("No value set.")

if value is not None:
    print("Value exists.")


# ------------------------------------------------------------
# 11. CHAINED COMPARISONS
# ------------------------------------------------------------
# Python lets you chain comparisons naturally — very readable.

age = 25

# Instead of: if age >= 18 and age <= 65
if 18 <= age <= 65:
    print("Working age")    # prints

x = 5
print(1 < x < 10)    # True
print(1 < x < 4)     # False


# ------------------------------------------------------------
# 12. PASS — placeholder for empty blocks
# ------------------------------------------------------------
# Python doesn't allow empty blocks. Use pass as a placeholder.

age = 15

if age >= 18:
    pass    # TODO: implement adult logic later
else:
    print("Minor")


# ------------------------------------------------------------
# 13. REAL-WORLD EXAMPLES
# ------------------------------------------------------------

# Example 1: Login check
username = "alice"
password = "secret123"

if username == "alice" and password == "secret123":
    print("Login successful!")
else:
    print("Invalid credentials.")

# Example 2: Grade classifier
def classify_grade(score):
    if not isinstance(score, (int, float)):
        return "Invalid input"
    if score < 0 or score > 100:
        return "Score out of range"
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"

print(classify_grade(85))    # B
print(classify_grade(101))   # Score out of range

# Example 3: Fizzbuzz (classic interview question)
for n in range(1, 21):
    if n % 15 == 0:       # divisible by both 3 and 5 — check FIRST
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)


# ============================================================
# SUMMARY
# ============================================================
# if / elif / else   → make decisions
# ==  !=  >  <  >=  <=  → compare values
# and  or  not        → combine conditions
# Truthy / Falsy      → every value has a truth value
# Ternary             → x = a if condition else b
# in / not in         → membership test
# is / is not         → identity test (use for None only)
# Chained comparisons → 18 <= age <= 65
# pass                → empty block placeholder
# ============================================================