# ============================================================
#  CHAPTER 3 — ENCAPSULATION
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS ENCAPSULATION?
# ------------------------------------------------------------
# Encapsulation = bundling data + methods that operate on it
# into one unit (a class), AND controlling access to that data.
#
# The idea: hide internal details, expose only what's needed.
#
# Think of a TV remote:
#   - You press buttons (public interface)
#   - You don't touch the circuit board inside (private internals)
#
# Why it matters:
#   → Prevents accidental data corruption
#   → Makes code easier to change without breaking other parts
#   → Hides complexity


# ------------------------------------------------------------
# 2. PUBLIC, PROTECTED, PRIVATE — Python's conventions
# ------------------------------------------------------------
# Python doesn't have true access modifiers like Java/C++.
# Instead it uses NAMING CONVENTIONS:
#
#   name      → public     (anyone can access)
#   _name     → protected  (convention: internal use / subclasses)
#   __name    → private    (name-mangled — hard to access from outside)

class Person:
    def __init__(self, name, age, ssn):
        self.name   = name       # public    — free to access
        self._age   = age        # protected — "please don't touch directly"
        self.__ssn  = ssn        # private   — really don't touch this

p = Person("Alice", 30, "123-45-6789")

print(p.name)      # Alice       ✅ public — fine
print(p._age)      # 30          ⚠️  works but violates convention
# print(p.__ssn)   # AttributeError ← name mangled, can't access directly

# Python mangles __name to _ClassName__name internally
print(p._Person__ssn)   # 123-45-6789  (exists but don't do this!)


# ------------------------------------------------------------
# 3. WHY NAME MANGLING EXISTS
# ------------------------------------------------------------
# It prevents accidental override in subclasses — not true security.

class Base:
    def __init__(self):
        self.__secret = "base secret"

    def get_secret(self):
        return self.__secret     # works inside the class


class Child(Base):
    def __init__(self):
        super().__init__()
        self.__secret = "child secret"    # this is _Child__secret
                                           # does NOT overwrite _Base__secret

b = Base()
c = Child()
print(b.get_secret())    # base secret   ← Base's __secret unchanged
print(c.get_secret())    # base secret   ← still reads Base's version


# ------------------------------------------------------------
# 4. @property — the right way to control access
# ------------------------------------------------------------
# Instead of direct attribute access, use properties to:
#   - validate input before setting
#   - compute values on the fly
#   - make attributes read-only

class BankAccount:
    def __init__(self, owner, balance):
        self.owner    = owner
        self.__balance = balance    # private

    @property
    def balance(self):              # getter — read access
        return self.__balance

    @balance.setter
    def balance(self, amount):      # setter — with validation
        if not isinstance(amount, (int, float)):
            raise TypeError("Balance must be a number")
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = amount

    @balance.deleter
    def balance(self):              # deleter — control deletion
        raise AttributeError("Cannot delete balance")


acc = BankAccount("Alice", 1000)

print(acc.balance)      # 1000        ← calls getter
acc.balance = 1500      # calls setter with validation
print(acc.balance)      # 1500

# acc.balance = -500    # ValueError: Balance cannot be negative
# del acc.balance       # AttributeError: Cannot delete balance


# ------------------------------------------------------------
# 5. READ-ONLY PROPERTIES
# ------------------------------------------------------------
# Define @property with NO setter → attribute is read-only.

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value

    @property
    def area(self):             # computed on the fly — NO setter
        import math
        return round(math.pi * self._radius ** 2, 4)

    @property
    def diameter(self):         # read-only — NO setter
        return self._radius * 2


c = Circle(5)
print(c.radius)      # 5
print(c.area)        # 78.5398
print(c.diameter)    # 10

c.radius = 10        # ✅ allowed — has a setter
print(c.area)        # 314.1593

# c.area = 100       # AttributeError: can't set attribute — no setter


# ------------------------------------------------------------
# 6. GETTERS AND SETTERS — full validation example
# ------------------------------------------------------------

class Student:
    VALID_GRADES = {"A", "B", "C", "D", "F"}

    def __init__(self, name, age, grade):
        self.name  = name      # public — no restriction
        self.age   = age       # goes through setter
        self.grade = grade     # goes through setter

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if not (5 <= value <= 100):
            raise ValueError(f"Age {value} is out of range (5-100)")
        self.__age = value

    @property
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self, value):
        if value not in self.VALID_GRADES:
            raise ValueError(f"Grade must be one of {self.VALID_GRADES}")
        self.__grade = value

    def __str__(self):
        return f"Student({self.name}, age={self.age}, grade={self.grade})"


s = Student("Alice", 20, "A")
print(s)              # Student(Alice, age=20, grade=A)

s.age   = 21          # ✅
s.grade = "B"         # ✅
print(s)              # Student(Alice, age=21, grade=B)

# s.age = -5          # ValueError: Age -5 is out of range
# s.grade = "Z"       # ValueError: Grade must be one of {...}


# ------------------------------------------------------------
# 7. ENCAPSULATION WITH METHODS — hiding internal logic
# ------------------------------------------------------------
# Private methods (__ prefix) hide implementation details.
# Only the class itself should call them.

class PasswordManager:
    def __init__(self):
        self.__passwords = {}    # private dict

    def __hash_password(self, password):     # private method
        # Simplified — real code uses bcrypt/hashlib
        return hash(password)

    def __is_strong(self, password):         # private method
        return (len(password) >= 8 and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password))

    def save(self, site, password):          # public method
        if not self.__is_strong(password):
            raise ValueError("Password too weak. Need 8+ chars, uppercase, digit.")
        self.__passwords[site] = self.__hash_password(password)
        print(f"Password saved for {site}")

    def verify(self, site, password):        # public method
        if site not in self.__passwords:
            return False
        return self.__passwords[site] == self.__hash_password(password)

    def sites(self):
        return list(self.__passwords.keys())


pm = PasswordManager()
pm.save("github.com", "MyPass123")
pm.save("gmail.com",  "SecureP4ss")

print(pm.verify("github.com", "MyPass123"))    # True
print(pm.verify("github.com", "wrongpass"))    # False
print(pm.sites())     # ['github.com', 'gmail.com']

# pm.__hash_password("test")   # AttributeError — private
# pm.__passwords               # AttributeError — private


# ------------------------------------------------------------
# 8. SLOTS — restrict attributes & save memory
# ------------------------------------------------------------
# __slots__ prevents adding arbitrary attributes and
# reduces memory usage (no __dict__ per instance).
# Good for classes with many instances.

class Point:
    __slots__ = ["x", "y"]    # only these attributes allowed

    def __init__(self, x, y):
        self.x = x
        self.y = y


p = Point(1, 2)
print(p.x, p.y)    # 1 2

# p.z = 3          # AttributeError — z not in __slots__
# p.__dict__       # AttributeError — no __dict__ with __slots__

import sys
class PointNormal:
    def __init__(self, x, y): self.x = x; self.y = y

class PointSlots:
    __slots__ = ["x", "y"]
    def __init__(self, x, y): self.x = x; self.y = y

print(sys.getsizeof(PointNormal(1, 2)))   # ~48 bytes + dict overhead
print(sys.getsizeof(PointSlots(1, 2)))    # ~56 bytes but NO dict overhead


# ------------------------------------------------------------
# 9. COMPLETE EXAMPLE — a well-encapsulated class
# ------------------------------------------------------------

class Inventory:
    def __init__(self):
        self.__items = {}        # private: {name: (price, qty)}
        self.__total_value = 0   # private: cached value

    def __recalculate(self):     # private helper
        self.__total_value = sum(
            p * q for p, q in self.__items.values()
        )

    def add_item(self, name, price, quantity):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.__items[name] = (price, quantity)
        self.__recalculate()

    def remove_item(self, name):
        if name not in self.__items:
            raise KeyError(f"{name} not in inventory")
        del self.__items[name]
        self.__recalculate()

    def sell(self, name, qty):
        if name not in self.__items:
            raise KeyError(f"{name} not found")
        price, current_qty = self.__items[name]
        if qty > current_qty:
            raise ValueError(f"Only {current_qty} in stock")
        self.__items[name] = (price, current_qty - qty)
        self.__recalculate()
        return price * qty    # return revenue

    @property
    def total_value(self):     # read-only
        return self.__total_value

    @property
    def item_count(self):      # read-only
        return len(self.__items)

    def report(self):
        print(f"{'Item':<15} {'Price':>8} {'Qty':>6} {'Value':>10}")
        print("-" * 42)
        for name, (price, qty) in self.__items.items():
            print(f"{name:<15} ${price:>7,.2f} {qty:>6} ${price*qty:>9,.2f}")
        print("-" * 42)
        print(f"{'TOTAL':<15} {'':>8} {'':>6} ${self.__total_value:>9,.2f}")


inv = Inventory()
inv.add_item("Laptop",  999.99, 10)
inv.add_item("Mouse",    29.99, 50)
inv.add_item("Keyboard", 79.99, 30)

inv.report()

revenue = inv.sell("Laptop", 3)
print(f"\nSold 3 laptops, revenue: ${revenue:,.2f}")
print(f"Total inventory value: ${inv.total_value:,.2f}")


# ============================================================
# SUMMARY
# ============================================================
# Public    name      → accessible everywhere
# Protected _name     → convention: internal/subclass use only
# Private   __name    → name-mangled, hard to access outside
# @property           → getter — access method as attribute
# @x.setter           → setter — validate on assignment
# @x.deleter          → deleter — control deletion
# Read-only           → @property with no setter
# Private methods     → __method() hides implementation
# __slots__           → restrict attributes, save memory
# Goal                → hide internals, expose clean interface
# ============================================================