# ============================================================
#  CHAPTER 9 — DESIGN PATTERNS: CREATIONAL
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT ARE DESIGN PATTERNS?
# ------------------------------------------------------------
# Design patterns are proven, reusable solutions to common
# problems that come up repeatedly in software design.
#
# They are NOT code you copy-paste — they are TEMPLATES or
# BLUEPRINTS for how to structure your code.
#
# Three categories:
#   Creational  → how objects are CREATED
#   Structural  → how objects are COMPOSED / combined
#   Behavioral  → how objects COMMUNICATE / interact
#
# THIS FILE covers Creational patterns:
#   1. Singleton     → only ONE instance ever exists
#   2. Factory       → create objects without specifying exact class
#   3. Factory Method→ subclasses decide what to create
#   4. Abstract Factory→ families of related objects
#   5. Builder       → construct complex objects step by step
#   6. Prototype     → clone an existing object


# ------------------------------------------------------------
# 2. SINGLETON — only one instance ever exists
# ------------------------------------------------------------
# Problem:  You need exactly ONE instance of something —
#           a database connection, a config manager, a logger.
#           Creating multiple instances would waste resources
#           or cause inconsistency.
#
# Solution: Make the class control its own instantiation,
#           returning the SAME instance every time.

class Singleton:
    _instance = None    # class-level variable — shared by ALL instances
                        # stores the single instance once created

    def __new__(cls):
        # __new__ is called BEFORE __init__ — it creates the object
        # We override it to control how instances are created
        if cls._instance is None:
            # First call — no instance exists yet, create one
            cls._instance = super().__new__(cls)   # call the real __new__
            print("Creating the ONE instance")
        # Subsequent calls — instance already exists, return it
        return cls._instance    # always return the SAME object

    def __init__(self):
        # __init__ still runs every time you call Singleton()
        # Use a flag to prevent re-initialization
        if not hasattr(self, "_initialized"):
            self.value = 0
            self._initialized = True    # mark as initialized so we skip next time


# Test Singleton
s1 = Singleton()
s2 = Singleton()
s3 = Singleton()

print(s1 is s2)            # True  — same object!
print(s2 is s3)            # True  — all point to the same instance
print(id(s1) == id(s2))    # True  — same memory address

s1.value = 42
print(s2.value)    # 42  — because s1 and s2 are the SAME object


# Real-world Singleton: Configuration Manager
class ConfigManager:
    """Holds global application config — only ONE should ever exist."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}    # initialize config store
        return cls._instance

    def set(self, key, value):
        self._config[key] = value    # store config value

    def get(self, key, default=None):
        return self._config.get(key, default)    # retrieve config value

    def __repr__(self):
        return f"ConfigManager({self._config})"

config1 = ConfigManager()
config2 = ConfigManager()

config1.set("debug", True)
config1.set("host", "localhost")

print(config2.get("debug"))     # True  — same instance, sees config1's data
print(config1 is config2)       # True


# Thread-safe Singleton using a lock
import threading

class ThreadSafeSingleton:
    """Singleton safe for multi-threaded environments."""
    _instance = None
    _lock     = threading.Lock()    # lock prevents two threads creating instances simultaneously

    def __new__(cls):
        if cls._instance is None:           # first check (without lock — fast)
            with cls._lock:                 # acquire lock
                if cls._instance is None:   # second check (with lock — safe)
                    cls._instance = super().__new__(cls)
        return cls._instance
        # Double-checked locking: first check avoids locking every call (slow),
        # second check handles the race condition where two threads both passed first check


# ------------------------------------------------------------
# 3. FACTORY — create objects without specifying exact class
# ------------------------------------------------------------
# Problem:  Your code creates objects but doesn't always know
#           WHICH concrete class to instantiate — it depends
#           on config, user input, or runtime conditions.
#
# Solution: A factory function/class handles the "which class"
#           decision and returns the right object.

class Dog:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return f"{self.name} says: Woof!"

class Cat:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return f"{self.name} says: Meow!"

class Bird:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return f"{self.name} says: Tweet!"

# ❌ Without factory — caller must know and pick the class
dog  = Dog("Rex")
cat  = Cat("Whiskers")
bird = Bird("Tweety")

# ✅ With factory — caller just says WHAT they want
def animal_factory(animal_type, name):
    """Create and return the right animal based on type string.
    Caller doesn't need to import or know Dog/Cat/Bird classes."""

    animals = {
        "dog":  Dog,     # map string names to class objects
        "cat":  Cat,
        "bird": Bird,
    }
    cls = animals.get(animal_type.lower())    # look up the class
    if cls is None:
        raise ValueError(f"Unknown animal type: {animal_type}")
    return cls(name)    # instantiate and return

# Now caller only deals with the factory — not individual classes
pet1 = animal_factory("dog",  "Rex")
pet2 = animal_factory("cat",  "Whiskers")
pet3 = animal_factory("bird", "Tweety")

for pet in [pet1, pet2, pet3]:
    print(pet.speak())

# Real-world: database connection factory
class PostgreSQLConnection:
    def connect(self): return "Connected to PostgreSQL"
    def query(self, sql): return f"PG query: {sql}"

class MySQLConnection:
    def connect(self): return "Connected to MySQL"
    def query(self, sql): return f"MySQL query: {sql}"

class SQLiteConnection:
    def connect(self): return "Connected to SQLite"
    def query(self, sql): return f"SQLite query: {sql}"

def get_db_connection(db_type):
    """Return the right DB connection based on config."""
    connections = {
        "postgresql": PostgreSQLConnection,
        "mysql":      MySQLConnection,
        "sqlite":     SQLiteConnection,
    }
    cls = connections.get(db_type.lower())
    if not cls:
        raise ValueError(f"Unsupported database: {db_type}")
    return cls()    # create and return the connection object

# Just change the string to switch databases — no other code changes
db = get_db_connection("sqlite")
print(db.connect())
print(db.query("SELECT * FROM users"))


# ------------------------------------------------------------
# 4. FACTORY METHOD — subclasses decide what to create
# ------------------------------------------------------------
# Problem:  A base class needs to create objects, but the
#           EXACT type of object should be decided by subclasses.
#
# Solution: Define a "factory method" in the base class that
#           subclasses OVERRIDE to return their specific type.

from abc import ABC, abstractmethod

class Notification(ABC):
    """Base class — knows HOW to send, but not WHAT to create."""

    @abstractmethod
    def create_message(self, text):
        """Factory method — subclasses implement this to create their message type."""
        pass    # subclass decides what kind of message object to return

    def send(self, text):
        """Template method — uses create_message() to get the message."""
        message = self.create_message(text)   # calls the factory method
        print(f"Sending via {self.__class__.__name__}: {message.format()}")


class EmailMessage:
    def __init__(self, text):
        self.text = text
    def format(self):
        return f"[EMAIL] Subject: Notification | Body: {self.text}"

class SMSMessage:
    def __init__(self, text):
        self.text = text
    def format(self):
        return f"[SMS] {self.text[:160]}"    # SMS limited to 160 chars

class PushMessage:
    def __init__(self, text):
        self.text = text
    def format(self):
        return f"[PUSH] 🔔 {self.text}"


class EmailNotification(Notification):
    def create_message(self, text):
        return EmailMessage(text)    # factory method: creates EmailMessage

class SMSNotification(Notification):
    def create_message(self, text):
        return SMSMessage(text)      # factory method: creates SMSMessage

class PushNotification(Notification):
    def create_message(self, text):
        return PushMessage(text)     # factory method: creates PushMessage


# All use the same send() interface — each creates its own message type
notifiers = [EmailNotification(), SMSNotification(), PushNotification()]
for notifier in notifiers:
    notifier.send("Your order has shipped!")


# ------------------------------------------------------------
# 5. ABSTRACT FACTORY — families of related objects
# ------------------------------------------------------------
# Problem:  You need to create FAMILIES of related objects
#           that must work together. E.g., a UI toolkit where
#           all buttons and inputs must match the same theme.
#
# Solution: An abstract factory interface creates entire
#           families of objects without specifying concrete classes.

class Button(ABC):
    @abstractmethod
    def render(self): pass

class Input(ABC):
    @abstractmethod
    def render(self): pass

# Family 1: Light theme
class LightButton(Button):
    def render(self): return "[ Light Button ]"

class LightInput(Input):
    def render(self): return "[ Light Input ░░░ ]"

# Family 2: Dark theme
class DarkButton(Button):
    def render(self): return "█ Dark Button █"

class DarkInput(Input):
    def render(self): return "█ Dark Input ███ █"

# Family 3: Minimal theme
class MinimalButton(Button):
    def render(self): return "- Button -"

class MinimalInput(Input):
    def render(self): return "- Input -"


class UIFactory(ABC):
    """Abstract factory — declares methods to create a FAMILY of UI components."""

    @abstractmethod
    def create_button(self) -> Button: pass

    @abstractmethod
    def create_input(self) -> Input: pass


class LightThemeFactory(UIFactory):
    """Concrete factory — creates ALL light-themed components."""
    def create_button(self): return LightButton()
    def create_input(self):  return LightInput()

class DarkThemeFactory(UIFactory):
    """Concrete factory — creates ALL dark-themed components."""
    def create_button(self): return DarkButton()
    def create_input(self):  return DarkInput()

class MinimalThemeFactory(UIFactory):
    def create_button(self): return MinimalButton()
    def create_input(self):  return MinimalInput()


def build_ui(factory: UIFactory):
    """Build UI using whatever factory is passed — theme-agnostic."""
    button = factory.create_button()    # factory decides the exact class
    inp    = factory.create_input()
    print(f"UI: {button.render()}  |  {inp.render()}")

# Swap out the whole theme by passing a different factory
build_ui(LightThemeFactory())
build_ui(DarkThemeFactory())
build_ui(MinimalThemeFactory())


# ------------------------------------------------------------
# 6. BUILDER — construct complex objects step by step
# ------------------------------------------------------------
# Problem:  An object has many optional parts and complex
#           construction logic. A constructor with 10 parameters
#           is hard to use and easy to get wrong.
#
# Solution: Separate the construction from the representation.
#           A Builder constructs parts step by step,
#           and a final build() call assembles the whole object.

class Pizza:
    """The complex object being built — not created directly."""
    def __init__(self):
        # Initialize with defaults — builder sets these step by step
        self.size     = None
        self.crust    = None
        self.sauce    = None
        self.cheese   = None
        self.toppings = []

    def __str__(self):
        toppings = ", ".join(self.toppings) if self.toppings else "none"
        return (f"Pizza: {self.size} | {self.crust} crust | "
                f"{self.sauce} sauce | {self.cheese} cheese | "
                f"toppings: {toppings}")


class PizzaBuilder:
    """Builder — provides methods to configure each part of the pizza."""

    def __init__(self):
        self._pizza = Pizza()    # start with an empty pizza object

    def set_size(self, size):
        self._pizza.size = size
        return self              # return self to enable METHOD CHAINING

    def set_crust(self, crust):
        self._pizza.crust = crust
        return self

    def set_sauce(self, sauce):
        self._pizza.sauce = sauce
        return self

    def set_cheese(self, cheese):
        self._pizza.cheese = cheese
        return self

    def add_topping(self, topping):
        self._pizza.toppings.append(topping)
        return self              # returning self allows: .add_topping("x").add_topping("y")

    def build(self):
        """Validate and return the completed pizza."""
        if not self._pizza.size:
            raise ValueError("Pizza must have a size")
        if not self._pizza.crust:
            raise ValueError("Pizza must have a crust type")
        pizza = self._pizza          # grab the finished pizza
        self._pizza = Pizza()        # reset builder so it can build another pizza
        return pizza                 # return the assembled object


# Build different pizzas using the same builder — method chaining is clean
margherita = (PizzaBuilder()
              .set_size("large")
              .set_crust("thin")
              .set_sauce("tomato")
              .set_cheese("mozzarella")
              .build())

pepperoni = (PizzaBuilder()
             .set_size("medium")
             .set_crust("thick")
             .set_sauce("tomato")
             .set_cheese("cheddar")
             .add_topping("pepperoni")
             .add_topping("jalapeños")
             .build())

print(margherita)
print(pepperoni)


# Director — knows HOW to build common configurations
class PizzaDirector:
    """Knows the recipes — encapsulates common build sequences."""

    def __init__(self, builder: PizzaBuilder):
        self._builder = builder    # accepts any builder

    def make_cheese_pizza(self):
        return (self._builder
                .set_size("medium")
                .set_crust("regular")
                .set_sauce("tomato")
                .set_cheese("mozzarella")
                .build())

    def make_veggie_pizza(self):
        return (self._builder
                .set_size("large")
                .set_crust("thin")
                .set_sauce("pesto")
                .set_cheese("parmesan")
                .add_topping("mushrooms")
                .add_topping("bell peppers")
                .add_topping("olives")
                .build())

director = PizzaDirector(PizzaBuilder())
print(director.make_cheese_pizza())
print(director.make_veggie_pizza())


# ------------------------------------------------------------
# 7. PROTOTYPE — clone an existing object
# ------------------------------------------------------------
# Problem:  Creating a new object from scratch is expensive
#           or complex. You have an existing object that is
#           already configured and you want a copy of it.
#
# Solution: Clone (copy) an existing object instead of
#           creating a new one from scratch.

import copy

class ServerConfig:
    """A complex configuration object — expensive to build from scratch."""

    def __init__(self, host, port, db_url, settings=None):
        self.host     = host
        self.port     = port
        self.db_url   = db_url
        self.settings = settings or {}    # mutable dict — watch out when cloning!

    def clone(self):
        """Create a deep copy of this config — fully independent."""
        return copy.deepcopy(self)        # deepcopy copies nested objects too

    def __repr__(self):
        return (f"ServerConfig(host={self.host!r}, port={self.port}, "
                f"db={self.db_url!r}, settings={self.settings})")


# Base config — built once with all the complex setup
base_config = ServerConfig(
    host    = "localhost",
    port    = 8080,
    db_url  = "postgresql://localhost/mydb",
    settings= {"debug": False, "timeout": 30, "max_connections": 100}
)

# Clone and customize — much cheaper than building from scratch
dev_config  = base_config.clone()
dev_config.host               = "dev.example.com"
dev_config.settings["debug"]  = True    # only dev has debug on

prod_config = base_config.clone()
prod_config.host = "prod.example.com"
prod_config.port = 443
prod_config.settings["max_connections"] = 500

print(base_config)    # unchanged — deep copy means no shared references
print(dev_config)
print(prod_config)

# Verify independence — changing clone does NOT affect original
dev_config.settings["new_key"] = "new_value"
print("base_config still clean:", "new_key" not in base_config.settings)  # True


# Using Python's built-in copy protocol
class Blueprint:
    """Use __copy__ and __deepcopy__ to customize cloning behavior."""

    def __init__(self, name, components):
        self.name       = name
        self.components = components    # a list — shared if shallow copied!

    def __copy__(self):
        """Shallow copy — components list is SHARED."""
        return Blueprint(self.name, self.components)    # same list reference!

    def __deepcopy__(self, memo):
        """Deep copy — components list is INDEPENDENT."""
        return Blueprint(
            copy.deepcopy(self.name,       memo),
            copy.deepcopy(self.components, memo)   # fully independent list
        )

    def __repr__(self):
        return f"Blueprint({self.name!r}, {self.components})"

original = Blueprint("house", ["walls", "roof", "windows"])
shallow  = copy.copy(original)       # calls __copy__
deep     = copy.deepcopy(original)   # calls __deepcopy__

shallow.components.append("door")    # modifies original.components too! (shared)
print(original)    # has "door" — shallow copy shares the list!

deep.components.append("garage")     # does NOT affect original (independent)
print(original)    # unchanged — deep copy is fully independent


# ============================================================
# SUMMARY
# ============================================================
# Singleton       → one instance ever; __new__ controls creation
#                   use for: config, logging, DB connection pool
#
# Factory         → function/class returns right object based on input
#                   use for: when you need to pick class at runtime
#
# Factory Method  → base class defines abstract factory method,
#                   subclasses override it to return their type
#                   use for: frameworks, plugin systems
#
# Abstract Factory→ create FAMILIES of related objects together
#                   use for: UI themes, cross-platform toolkits
#
# Builder         → step-by-step construction, method chaining
#                   use for: complex objects with many optional parts
#                   key: return self from each method for chaining
#
# Prototype       → clone existing object instead of new creation
#                   use copy.deepcopy() for fully independent clones
#                   use for: expensive-to-create objects, config variants
# ============================================================