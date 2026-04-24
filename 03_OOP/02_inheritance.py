# ============================================================
#  CHAPTER 3 — INHERITANCE
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT IS INHERITANCE?
# ------------------------------------------------------------
# Inheritance lets a class REUSE and EXTEND another class.
#
# Parent class (Base class)   → the original class
# Child class (Derived class) → inherits from the parent
#
# Child gets ALL attributes and methods of the parent.
# Child can ADD new ones and OVERRIDE existing ones.
#
# Real-world analogy:
#   Animal (parent)  →  Dog, Cat, Bird (children)
#   Vehicle (parent) →  Car, Truck, Motorcycle (children)


# ------------------------------------------------------------
# 2. BASIC INHERITANCE
# ------------------------------------------------------------

class Animal:                          # Parent class
    def __init__(self, name, age):
        self.name = name
        self.age  = age

    def eat(self):
        print(f"{self.name} is eating.")

    def sleep(self):
        print(f"{self.name} is sleeping.")

    def __str__(self):
        return f"{self.name} (age {self.age})"


class Dog(Animal):                     # Child class — inherits Animal
    pass                               # nothing extra yet


rex = Dog("Rex", 3)
print(rex)           # Rex (age 3)    ← from Animal.__str__
rex.eat()            # Rex is eating. ← from Animal.eat
rex.sleep()          # Rex is sleeping.

print(isinstance(rex, Dog))      # True
print(isinstance(rex, Animal))   # True  ← Dog IS an Animal


# ------------------------------------------------------------
# 3. EXTENDING THE CHILD — adding new attributes and methods
# ------------------------------------------------------------

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)    # call parent __init__ first!
        self.breed = breed             # add new attribute

    def bark(self):                    # new method
        print(f"{self.name} says: Woof!")

    def fetch(self, item):             # new method
        print(f"{self.name} fetches the {item}!")


class Cat(Animal):
    def __init__(self, name, age, indoor):
        super().__init__(name, age)
        self.indoor = indoor

    def meow(self):
        print(f"{self.name} says: Meow!")

    def purr(self):
        print(f"{self.name} purrs...")


rex   = Dog("Rex", 3, "Labrador")
kitty = Cat("Kitty", 2, indoor=True)

rex.eat()          # from Animal
rex.bark()         # from Dog
rex.fetch("ball")  # from Dog

kitty.sleep()      # from Animal
kitty.meow()       # from Cat


# ------------------------------------------------------------
# 4. super() — calling the parent's methods
# ------------------------------------------------------------
# super() gives you access to the parent class.
# Most common use: calling parent __init__ to set up parent attrs.

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age  = age

    def describe(self):
        print(f"I am {self.name}, age {self.age}.")


class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)    # runs Animal.__init__
        self.breed = breed

    def describe(self):
        super().describe()             # call parent's describe first
        print(f"I am a {self.breed}.")  # then add more


rex = Dog("Rex", 3, "Labrador")
rex.describe()
# I am Rex, age 3.
# I am a Labrador.


# ------------------------------------------------------------
# 5. METHOD OVERRIDING — redefining a parent method
# ------------------------------------------------------------
# Child defines a method with the SAME NAME as the parent.
# Python uses the child's version — the parent's is "overridden".

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")


class Dog(Animal):
    def speak(self):                        # overrides Animal.speak
        print(f"{self.name} says: Woof!")


class Cat(Animal):
    def speak(self):                        # overrides Animal.speak
        print(f"{self.name} says: Meow!")


class Duck(Animal):
    def speak(self):
        print(f"{self.name} says: Quack!")


class Fish(Animal):
    pass                                    # uses Animal.speak unchanged


animals = [
    Dog("Rex"),
    Cat("Kitty"),
    Duck("Donald"),
    Fish("Nemo"),
]

for animal in animals:
    animal.speak()   # each calls its OWN version — this is POLYMORPHISM
# Rex says: Woof!
# Kitty says: Meow!
# Donald says: Quack!
# Nemo makes a sound.


# ------------------------------------------------------------
# 6. POLYMORPHISM — same interface, different behavior
# ------------------------------------------------------------
# Polymorphism = "many forms"
# Same method name, different behavior per class.
# Lets you write code that works with ANY subclass.

class Shape:
    def area(self):
        raise NotImplementedError("Subclass must implement area()")

    def perimeter(self):
        raise NotImplementedError("Subclass must implement perimeter()")

    def describe(self):
        print(f"{type(self).__name__}: area={self.area():.2f}, "
              f"perimeter={self.perimeter():.2f}")


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width  = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def area(self):
        s = (self.a + self.b + self.c) / 2
        return (s*(s-self.a)*(s-self.b)*(s-self.c)) ** 0.5

    def perimeter(self):
        return self.a + self.b + self.c


shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]

# Same code works for ALL shapes — polymorphism in action
for shape in shapes:
    shape.describe()

total_area = sum(s.area() for s in shapes)
print(f"Total area: {total_area:.2f}")


# ------------------------------------------------------------
# 7. MULTI-LEVEL INHERITANCE
# ------------------------------------------------------------
# A → B → C  (chain of inheritance)

class Animal:
    def __init__(self, name):
        self.name = name

    def breathe(self):
        print(f"{self.name} breathes.")


class Mammal(Animal):
    def feed_young(self):
        print(f"{self.name} feeds young with milk.")


class Dog(Mammal):
    def bark(self):
        print(f"{self.name} barks!")


rex = Dog("Rex")
rex.breathe()      # from Animal
rex.feed_young()   # from Mammal
rex.bark()         # from Dog

# Check the inheritance chain
print(Dog.__mro__)
# (<class 'Dog'>, <class 'Mammal'>, <class 'Animal'>, <class 'object'>)


# ------------------------------------------------------------
# 8. MULTIPLE INHERITANCE
# ------------------------------------------------------------
# A class can inherit from MORE THAN ONE parent.
# Python resolves method lookup using MRO (Method Resolution Order).

class Flyable:
    def fly(self):
        print(f"{self.name} is flying!")

    def describe(self):
        print("I can fly.")


class Swimmable:
    def swim(self):
        print(f"{self.name} is swimming!")

    def describe(self):
        print("I can swim.")


class Duck(Animal, Flyable, Swimmable):
    def quack(self):
        print(f"{self.name} quacks!")


donald = Duck("Donald")
donald.fly()       # from Flyable
donald.swim()      # from Swimmable
donald.quack()     # from Duck
donald.breathe()   # from Animal

# Which describe() gets called? → first parent wins (MRO order)
donald.describe()    # "I can fly."  ← Flyable comes first

print(Duck.__mro__)  # shows the full resolution order


# ------------------------------------------------------------
# 9. isinstance() and issubclass()
# ------------------------------------------------------------

class Animal: pass
class Dog(Animal): pass
class Cat(Animal): pass

rex = Dog()

# isinstance — check if object is an instance of a class
print(isinstance(rex, Dog))      # True
print(isinstance(rex, Animal))   # True  ← Dog IS an Animal
print(isinstance(rex, Cat))      # False

# issubclass — check if class is a subclass of another
print(issubclass(Dog, Animal))   # True
print(issubclass(Cat, Animal))   # True
print(issubclass(Dog, Cat))      # False
print(issubclass(Animal, object))# True  ← everything inherits object


# ------------------------------------------------------------
# 10. ABSTRACT BASE CLASSES — enforcing a contract
# ------------------------------------------------------------
# Force child classes to implement specific methods.
# Can't instantiate an abstract class directly.

from abc import ABC, abstractmethod

class Shape(ABC):             # inherit from ABC
    @abstractmethod
    def area(self):           # child MUST implement this
        pass

    @abstractmethod
    def perimeter(self):      # child MUST implement this
        pass

    def describe(self):       # NOT abstract — optional to override
        print(f"Area: {self.area():.2f}")


# shape = Shape()   ← TypeError: Can't instantiate abstract class

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):           # must implement
        return self.side ** 2

    def perimeter(self):      # must implement
        return 4 * self.side

s = Square(5)
s.describe()    # Area: 25.00
print(s.perimeter())    # 20


# ------------------------------------------------------------
# 11. REAL-WORLD EXAMPLE — Employee hierarchy
# ------------------------------------------------------------

class Employee:
    def __init__(self, name, emp_id, base_salary):
        self.name        = name
        self.emp_id      = emp_id
        self.base_salary = base_salary

    def get_pay(self):
        return self.base_salary

    def __str__(self):
        return f"{self.name} (ID: {self.emp_id})"


class Manager(Employee):
    def __init__(self, name, emp_id, base_salary, bonus):
        super().__init__(name, emp_id, base_salary)
        self.bonus = bonus
        self.reports = []        # list of employees they manage

    def add_report(self, employee):
        self.reports.append(employee)

    def get_pay(self):           # override
        return self.base_salary + self.bonus

    def describe_team(self):
        print(f"{self.name} manages:")
        for emp in self.reports:
            print(f"  - {emp.name}: ${emp.get_pay():,}")


class ContractEmployee(Employee):
    def __init__(self, name, emp_id, hourly_rate, hours):
        super().__init__(name, emp_id, base_salary=0)
        self.hourly_rate = hourly_rate
        self.hours       = hours

    def get_pay(self):           # override
        return self.hourly_rate * self.hours


alice = Manager("Alice", "M001", 90000, bonus=15000)
bob   = Employee("Bob",   "E001", 75000)
carol = ContractEmployee("Carol", "C001", hourly_rate=80, hours=160)

alice.add_report(bob)
alice.add_report(carol)

alice.describe_team()
print(f"\nPayroll:")
for person in [alice, bob, carol]:
    print(f"  {person}: ${person.get_pay():,}")


# ============================================================
# SUMMARY
# ============================================================
# class Child(Parent):    → inherit from Parent
# super().__init__(...)   → call parent constructor
# Override method         → define same name in child
# Polymorphism            → same method, different behavior
# Multi-level             → A → B → C
# Multiple inheritance    → class C(A, B):
# MRO                     → order Python looks up methods
# isinstance(obj, Class)  → check object type
# issubclass(Sub, Base)   → check class relationship
# ABC + @abstractmethod   → force child to implement methods
# ============================================================