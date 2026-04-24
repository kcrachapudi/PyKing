# ============================================================
#  CHAPTER 3 — CLASSES AND OBJECTS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS OOP?
# ------------------------------------------------------------
# Object-Oriented Programming is a way to model real-world
# things as "objects" that have:
#   - Attributes → data / properties  (what it HAS)
#   - Methods    → functions          (what it DOES)
#
# A CLASS is the blueprint.
# An OBJECT (instance) is the thing built from that blueprint.
#
# Blueprint: Car
#   → attributes: color, brand, speed
#   → methods:    accelerate(), brake(), honk()
#
# Object 1: my_car = Car("red", "Toyota")
# Object 2: your_car = Car("blue", "Honda")


# ------------------------------------------------------------
# 2. DEFINING A CLASS
# ------------------------------------------------------------

class Dog:
    pass    # empty class — valid Python

# Create an instance (object)
my_dog = Dog()
print(type(my_dog))    # <class '__main__.Dog'>


# ------------------------------------------------------------
# 3. __init__ — the constructor
# ------------------------------------------------------------
# __init__ runs automatically when you create an instance.
# 'self' refers to the object being created.
# Always the first parameter — Python passes it automatically.

class Dog:
    def __init__(self, name, breed, age):
        self.name  = name     # instance attribute
        self.breed = breed    # instance attribute
        self.age   = age      # instance attribute

# Creating instances
rex   = Dog("Rex",   "Labrador", 3)
buddy = Dog("Buddy", "Poodle",   5)

# Accessing attributes
print(rex.name)     # Rex
print(buddy.age)    # 5
print(rex.breed)    # Labrador


# ------------------------------------------------------------
# 4. INSTANCE METHODS
# ------------------------------------------------------------
# Functions defined inside a class.
# First parameter is always 'self' — the instance itself.

class Dog:
    def __init__(self, name, breed, age):
        self.name  = name
        self.breed = breed
        self.age   = age

    def bark(self):
        print(f"{self.name} says: Woof!")

    def describe(self):
        print(f"{self.name} is a {self.age}-year-old {self.breed}.")

    def birthday(self):
        self.age += 1    # modify the instance's own data
        print(f"Happy birthday {self.name}! Now {self.age} years old.")

rex = Dog("Rex", "Labrador", 3)
rex.bark()        # Rex says: Woof!
rex.describe()    # Rex is a 3-year-old Labrador.
rex.birthday()    # Happy birthday Rex! Now 4 years old.
rex.describe()    # Rex is a 4-year-old Labrador.


# ------------------------------------------------------------
# 5. CLASS ATTRIBUTES vs INSTANCE ATTRIBUTES
# ------------------------------------------------------------
# Instance attribute → belongs to ONE object  (self.x)
# Class attribute    → shared by ALL objects  (defined in class body)

class Dog:
    species = "Canis familiaris"    # class attribute — shared by all

    def __init__(self, name, age):
        self.name = name    # instance attribute — unique per object
        self.age  = age

rex   = Dog("Rex", 3)
buddy = Dog("Buddy", 5)

# All instances share the class attribute
print(rex.species)      # Canis familiaris
print(buddy.species)    # Canis familiaris
print(Dog.species)      # Canis familiaris  ← access via class too

# Instance attributes are unique
print(rex.name)     # Rex
print(buddy.name)   # Buddy

# Changing class attribute affects ALL instances
Dog.species = "Canis lupus familiaris"
print(rex.species)      # Canis lupus familiaris
print(buddy.species)    # Canis lupus familiaris

# ⚠️  Setting on instance creates a NEW instance attribute — doesn't change class attr
rex.species = "special"
print(rex.species)      # special   ← rex's own copy
print(buddy.species)    # Canis lupus familiaris  ← unchanged


# ------------------------------------------------------------
# 6. DUNDER (MAGIC) METHODS
# ------------------------------------------------------------
# Special methods with double underscores.
# Python calls them automatically in certain situations.

class Book:
    def __init__(self, title, author, pages):
        self.title  = title
        self.author = author
        self.pages  = pages

    def __str__(self):
        # Called by print() and str() — human-readable
        return f'"{self.title}" by {self.author}'

    def __repr__(self):
        # Called in the REPL and repr() — developer-readable
        return f'Book(title={self.title!r}, author={self.author!r}, pages={self.pages})'

    def __len__(self):
        # Called by len()
        return self.pages

    def __eq__(self, other):
        # Called by ==
        if not isinstance(other, Book):
            return False
        return self.title == other.title and self.author == other.author

    def __lt__(self, other):
        # Called by < (less than)
        return self.pages < other.pages

    def __add__(self, other):
        # Called by + — combine page counts
        return self.pages + other.pages


book1 = Book("Python Crash Course", "Eric Matthes", 544)
book2 = Book("Fluent Python", "Luciano Ramalho", 792)
book3 = Book("Python Crash Course", "Eric Matthes", 544)

print(book1)              # "Python Crash Course" by Eric Matthes
print(repr(book1))        # Book(title='Python Crash Course', ...)
print(len(book1))         # 544
print(book1 == book3)     # True   (same title + author)
print(book1 == book2)     # False
print(book1 < book2)      # True   (544 < 792)
print(book1 + book2)      # 1336   (total pages)


# ------------------------------------------------------------
# 7. @property — controlled attribute access
# ------------------------------------------------------------
# Lets you access a method LIKE an attribute (no parentheses).
# Also lets you add validation when setting values.

class Circle:
    def __init__(self, radius):
        self._radius = radius    # _ means "intended as private"

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2

    @property
    def diameter(self):
        return self._radius * 2


c = Circle(5)
print(c.radius)      # 5       ← looks like attribute, not method
print(c.area)        # 78.53...
print(c.diameter)    # 10

c.radius = 10        # calls the setter
print(c.area)        # 314.15...

# c.radius = -1      # ValueError: Radius cannot be negative
# c.area = 50        # AttributeError: can't set attribute (no setter)


# ------------------------------------------------------------
# 8. @classmethod and @staticmethod
# ------------------------------------------------------------

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        # Alternative constructor — creates instance from Fahrenheit
        # cls = the class itself (like self but for the class)
        return cls((fahrenheit - 32) * 5 / 9)

    @classmethod
    def from_kelvin(cls, kelvin):
        return cls(kelvin - 273.15)

    @staticmethod
    def is_valid(celsius):
        # Doesn't need self or cls — just a utility function
        # that lives here because it's related to Temperature
        return celsius >= -273.15

    def __str__(self):
        return f"{self.celsius:.1f}°C"


t1 = Temperature(100)
t2 = Temperature.from_fahrenheit(212)   # alternative constructor
t3 = Temperature.from_kelvin(373.15)

print(t1)    # 100.0°C
print(t2)    # 100.0°C
print(t3)    # 100.0°C

print(Temperature.is_valid(-300))    # False
print(Temperature.is_valid(25))      # True


# ------------------------------------------------------------
# 9. PUTTING IT ALL TOGETHER — a complete class
# ------------------------------------------------------------

class BankAccount:
    bank_name = "Python Bank"    # class attribute

    def __init__(self, owner, balance=0):
        self.owner    = owner
        self._balance = balance      # _ = intended as private
        self._history = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self._history.append(f"Deposited ${amount:,.2f}")
        return self

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._history.append(f"Withdrew ${amount:,.2f}")
        return self    # return self enables method chaining

    def get_history(self):
        for entry in self._history:
            print(f"  {entry}")

    def __str__(self):
        return f"Account({self.owner}, ${self._balance:,.2f})"

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"


# Using the class
acc = BankAccount("Alice", 1000)
print(acc)             # Account(Alice, $1,000.00)
print(acc.balance)     # 1000

# Method chaining — deposit and withdraw in one line
acc.deposit(500).withdraw(200).deposit(100)

print(acc)             # Account(Alice, $1,400.00)
acc.get_history()
#   Deposited $500.00
#   Withdrew $200.00
#   Deposited $100.00

print(BankAccount.bank_name)   # Python Bank


# ============================================================
# SUMMARY
# ============================================================
# class Name:           → define a class
# __init__(self, ...)   → constructor, runs on creation
# self                  → refers to the current instance
# instance attribute    → self.x = val  (unique per object)
# class attribute       → defined in class body (shared)
# instance method       → def method(self):
# __str__               → called by print()
# __repr__              → called in REPL / repr()
# __len__               → called by len()
# __eq__                → called by ==
# @property             → access method like an attribute
# @property.setter      → validate on assignment
# @classmethod          → alternative constructors, gets cls
# @staticmethod         → utility function, no self/cls
# ============================================================