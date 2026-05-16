# ============================================================
#  CHAPTER 9 — DESIGN PATTERNS: STRUCTURAL
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT ARE STRUCTURAL PATTERNS?
# ------------------------------------------------------------
# Structural patterns deal with how classes and objects are
# COMPOSED together to form larger structures.
#
# They help you:
#   → Make incompatible interfaces work together (Adapter)
#   → Add responsibilities to objects dynamically (Decorator)
#   → Simplify complex subsystems (Facade)
#   → Share data efficiently between many objects (Flyweight)
#   → Separate abstraction from implementation (Bridge)
#   → Compose objects into tree structures (Composite)
#   → Control access to another object (Proxy)
#
# THIS FILE covers:
#   1. Adapter    → make incompatible interfaces compatible
#   2. Decorator  → add behaviour without changing the class
#   3. Facade     → simple interface over a complex system
#   4. Proxy      → control access to another object
#   5. Composite  → treat individual objects and groups the same
#   6. Bridge     → separate abstraction from implementation
#   7. Flyweight  → share data to support many small objects


# ------------------------------------------------------------
# 2. ADAPTER — make incompatible interfaces work together
# ------------------------------------------------------------
# Problem:  You have two classes that do similar things but
#           have different interfaces (method names/signatures).
#           You can't change either class (e.g., third-party lib).
#
# Solution: Create an Adapter class that wraps one interface
#           and translates calls to the other.
#
# Real-world analogy: a power plug adapter — your device's plug
# doesn't fit the wall socket, so you use an adapter in between.

# Existing class — works fine, can't change it
class EuropeanSocket:
    """Provides 230V power via European interface."""
    def voltage(self):
        return 230    # European voltage

    def live(self):
        return 1      # live wire signal

    def neutral(self):
        return -1     # neutral wire signal


# New interface — what our code EXPECTS
class USASocketInterface:
    """Interface our code is written against — 120V USA standard."""
    def voltage(self): pass
    def live(self):    pass
    def neutral(self): pass


# Adapter — wraps EuropeanSocket to look like USASocketInterface
class Adapter(USASocketInterface):
    def __init__(self, socket):
        self._socket = socket    # hold a reference to the adaptee (European socket)

    def voltage(self):
        # translate: convert 230V European to 120V USA equivalent
        return self._socket.voltage() / 2    # simplified conversion

    def live(self):
        return self._socket.live()       # pass through unchanged

    def neutral(self):
        return self._socket.neutral()    # pass through unchanged


# Our code only knows about USASocketInterface — works with adapter transparently
def charge_device(socket: USASocketInterface):
    """Charges a device — expects USA socket interface."""
    print(f"Voltage: {socket.voltage()}V")
    print(f"Live: {socket.live()}, Neutral: {socket.neutral()}")
    print("Device charging!")

european_socket = EuropeanSocket()
adapter         = Adapter(european_socket)   # wrap the European socket

charge_device(adapter)    # works! adapter translates the interface


# Real-world: adapt a third-party payment processor
class StripeAPI:
    """Third-party payment API — can't change this."""
    def create_charge(self, amount_cents, currency, source):
        return {"id": "ch_123", "amount": amount_cents, "status": "succeeded"}

class PayPalAPI:
    """Another third-party API — different interface entirely."""
    def make_payment(self, amount_dollars, payer_email):
        return {"transaction_id": "pp_456", "success": True}


class PaymentProcessor:
    """What OUR code expects — a unified payment interface."""
    def pay(self, amount, currency="USD"):
        raise NotImplementedError


class StripeAdapter(PaymentProcessor):
    """Adapts StripeAPI to our PaymentProcessor interface."""
    def __init__(self):
        self._stripe = StripeAPI()    # hold the real Stripe client

    def pay(self, amount, currency="USD"):
        # translate our interface to Stripe's interface
        amount_cents = int(amount * 100)    # Stripe uses cents, we use dollars
        result = self._stripe.create_charge(amount_cents, currency, "tok_visa")
        return result["status"] == "succeeded"    # translate result too

class PayPalAdapter(PaymentProcessor):
    """Adapts PayPalAPI to our PaymentProcessor interface."""
    def __init__(self, email):
        self._paypal = PayPalAPI()
        self._email  = email

    def pay(self, amount, currency="USD"):
        result = self._paypal.make_payment(amount, self._email)
        return result["success"]

# Our checkout code doesn't know or care which payment provider is used
def checkout(processor: PaymentProcessor, amount):
    success = processor.pay(amount)
    print(f"Payment {'succeeded' if success else 'failed'}: ${amount}")

checkout(StripeAdapter(),              99.99)
checkout(PayPalAdapter("bob@x.com"),  49.99)


# ------------------------------------------------------------
# 3. DECORATOR — add behaviour without changing the class
# ------------------------------------------------------------
# Problem:  You want to add features to an object dynamically
#           without modifying its class or using inheritance.
#           Inheritance is static — you can't add/remove at runtime.
#
# Solution: Wrap the object in a Decorator that adds behaviour
#           before/after delegating to the wrapped object.
#
# Note: This is the OOP Decorator pattern — similar idea to
# Python's @decorator syntax but different implementation.

from abc import ABC, abstractmethod

class Coffee(ABC):
    """Base component interface."""
    @abstractmethod
    def cost(self) -> float: pass

    @abstractmethod
    def description(self) -> str: pass


class SimpleCoffee(Coffee):
    """Concrete component — the base object being decorated."""
    def cost(self):        return 1.00
    def description(self): return "Simple coffee"


class CoffeeDecorator(Coffee):
    """Base decorator — wraps a Coffee object and delegates to it."""
    def __init__(self, coffee: Coffee):
        self._coffee = coffee    # hold reference to the wrapped object

    def cost(self):
        return self._coffee.cost()    # delegate to wrapped object by default

    def description(self):
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    """Adds milk — wraps any Coffee and adds milk's cost and description."""
    def cost(self):
        return self._coffee.cost() + 0.25    # add milk cost on top

    def description(self):
        return self._coffee.description() + ", milk"    # extend description


class SugarDecorator(CoffeeDecorator):
    """Adds sugar."""
    def cost(self):        return self._coffee.cost() + 0.10
    def description(self): return self._coffee.description() + ", sugar"


class WhipDecorator(CoffeeDecorator):
    """Adds whipped cream."""
    def cost(self):        return self._coffee.cost() + 0.50
    def description(self): return self._coffee.description() + ", whip"


class VanillaDecorator(CoffeeDecorator):
    """Adds vanilla syrup."""
    def cost(self):        return self._coffee.cost() + 0.75
    def description(self): return self._coffee.description() + ", vanilla"


# Compose decorators dynamically at runtime — any combination!
coffee = SimpleCoffee()
print(f"{coffee.description()}: ${coffee.cost():.2f}")    # $1.00

# Wrap with milk
coffee = MilkDecorator(coffee)
print(f"{coffee.description()}: ${coffee.cost():.2f}")    # $1.25

# Wrap again with sugar
coffee = SugarDecorator(coffee)
print(f"{coffee.description()}: ${coffee.cost():.2f}")    # $1.35

# Wrap again with whip
coffee = WhipDecorator(coffee)
print(f"{coffee.description()}: ${coffee.cost():.2f}")    # $1.85

# Or build a fancy drink all at once
fancy = VanillaDecorator(WhipDecorator(MilkDecorator(SimpleCoffee())))
print(f"{fancy.description()}: ${fancy.cost():.2f}")      # $2.50


# Real-world: HTTP request decorator (add headers, logging, retry)
class HTTPRequest:
    """Base HTTP request handler."""
    def get(self, url):
        return f"GET {url} → 200 OK"    # simulate HTTP response


class AuthDecorator:
    """Adds authentication header to every request."""
    def __init__(self, request, token):
        self._request = request    # wrapped request object
        self._token   = token      # auth token to inject

    def get(self, url):
        # Add auth header before delegating to the real request
        print(f"  Adding Authorization: Bearer {self._token[:8]}...")
        return self._request.get(url)    # delegate to wrapped object


class LoggingDecorator:
    """Logs every request."""
    def __init__(self, request):
        self._request = request

    def get(self, url):
        print(f"  [LOG] GET {url}")
        response = self._request.get(url)    # delegate
        print(f"  [LOG] Response: {response}")
        return response


class RetryDecorator:
    """Retries failed requests up to N times."""
    def __init__(self, request, retries=3):
        self._request = request
        self._retries = retries

    def get(self, url):
        for attempt in range(1, self._retries + 1):
            try:
                return self._request.get(url)    # try the request
            except Exception as e:
                print(f"  [RETRY] Attempt {attempt} failed: {e}")
        raise RuntimeError("All retries exhausted")


# Compose decorators — each adds a layer of behaviour
request = HTTPRequest()
request = AuthDecorator(request, token="secret_token_abc123")
request = LoggingDecorator(request)
request = RetryDecorator(request, retries=3)

response = request.get("https://api.example.com/users")
print(response)


# ------------------------------------------------------------
# 4. FACADE — simple interface over a complex system
# ------------------------------------------------------------
# Problem:  A subsystem has many complex classes and steps.
#           Client code has to know all the details and call
#           things in the right order — fragile and complex.
#
# Solution: A Facade provides ONE simple interface that hides
#           all the complexity. Client only calls the facade.
#
# Real-world analogy: a TV remote — you press "watch movie"
# and it turns on the TV, receiver, switches input, dims lights.
# You don't do each step manually.

# Complex subsystem — many classes, each doing one thing
class DVDPlayer:
    def on(self):     print("DVD Player: ON")
    def off(self):    print("DVD Player: OFF")
    def play(self, movie): print(f"DVD Player: Playing '{movie}'")
    def stop(self):   print("DVD Player: Stopped")

class Projector:
    def on(self):          print("Projector: ON")
    def off(self):         print("Projector: OFF")
    def wide_screen(self): print("Projector: Wide screen mode")

class SurroundSound:
    def on(self):         print("Sound: ON")
    def off(self):        print("Sound: OFF")
    def set_volume(self, v): print(f"Sound: Volume set to {v}")

class Lights:
    def dim(self, level): print(f"Lights: Dimmed to {level}%")
    def on(self):         print("Lights: ON")

class PopcornMaker:
    def on(self):  print("Popcorn Maker: ON")
    def off(self): print("Popcorn Maker: OFF")
    def pop(self): print("Popcorn Maker: Popping!")


class HomeTheaterFacade:
    """Facade — ONE simple interface over the whole home theater system."""

    def __init__(self):
        # Create all subsystem objects — client never sees these directly
        self._dvd      = DVDPlayer()
        self._proj     = Projector()
        self._sound    = SurroundSound()
        self._lights   = Lights()
        self._popcorn  = PopcornMaker()

    def watch_movie(self, movie):
        """One call sets up EVERYTHING for movie night."""
        print(f"\n=== Preparing to watch '{movie}' ===")
        self._popcorn.on()
        self._popcorn.pop()
        self._lights.dim(10)       # dim lights to 10%
        self._proj.on()
        self._proj.wide_screen()
        self._sound.on()
        self._sound.set_volume(8)
        self._dvd.on()
        self._dvd.play(movie)

    def end_movie(self):
        """One call shuts EVERYTHING down."""
        print("\n=== Shutting down home theater ===")
        self._dvd.stop()
        self._dvd.off()
        self._sound.off()
        self._proj.off()
        self._lights.on()
        self._popcorn.off()


# Client code is simple — just one object, two methods
theater = HomeTheaterFacade()
theater.watch_movie("Interstellar")
theater.end_movie()


# Real-world: Order processing facade
class InventoryService:
    def check_stock(self, item, qty): return qty <= 10    # simulate

class PaymentService:
    def charge(self, amount): return {"status": "ok", "id": "pay_123"}

class ShippingService:
    def create_shipment(self, address): return "SHIP-789"

class NotificationService:
    def send_email(self, email, msg): print(f"Email to {email}: {msg}")

class OrderFacade:
    """Hides the complexity of placing an order."""
    def __init__(self):
        self._inventory = InventoryService()
        self._payment   = PaymentService()
        self._shipping  = ShippingService()
        self._notify    = NotificationService()

    def place_order(self, item, qty, price, address, email):
        """Client calls this ONE method — facade handles everything."""
        if not self._inventory.check_stock(item, qty):
            raise ValueError("Item out of stock")
        payment = self._payment.charge(price * qty)
        if payment["status"] != "ok":
            raise RuntimeError("Payment failed")
        tracking = self._shipping.create_shipment(address)
        self._notify.send_email(email, f"Order confirmed! Tracking: {tracking}")
        return {"order": "confirmed", "tracking": tracking}

order = OrderFacade()
result = order.place_order("Laptop", 1, 999.99, "123 Main St", "alice@x.com")
print(result)


# ------------------------------------------------------------
# 5. PROXY — control access to another object
# ------------------------------------------------------------
# Problem:  You need to control access to an object —
#           add lazy loading, caching, access control,
#           or logging — without changing the real object.
#
# Solution: A Proxy has the SAME interface as the real object
#           but controls access to it.
#
# Types: Virtual (lazy load), Protection (access control),
#        Remote (network), Caching, Logging

class DatabaseQuery:
    """The real object — expensive to use."""
    def execute(self, sql):
        print(f"  [DB] Executing: {sql}")
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


class CachingProxy:
    """Caching proxy — returns cached result if available, else calls real DB."""
    def __init__(self, database):
        self._db    = database    # reference to the real object
        self._cache = {}          # our cache storage: {sql: result}

    def execute(self, sql):
        if sql in self._cache:
            print(f"  [CACHE] Cache hit for: {sql}")
            return self._cache[sql]    # return cached result immediately

        print(f"  [CACHE] Cache miss — querying database...")
        result = self._db.execute(sql)    # call the real database
        self._cache[sql] = result         # store result in cache for next time
        return result


class LoggingProxy:
    """Logging proxy — logs every call to the real object."""
    def __init__(self, database):
        self._db   = database
        self._log  = []    # store query history

    def execute(self, sql):
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        self._log.append({"time": timestamp, "sql": sql})
        print(f"  [LOG] {timestamp}: {sql}")
        return self._db.execute(sql)

    def get_log(self):
        return self._log


class ProtectionProxy:
    """Protection proxy — checks permissions before allowing access."""
    def __init__(self, database, user_role):
        self._db        = database
        self._user_role = user_role    # the role of the current user

    def execute(self, sql):
        # Allow SELECT for all users
        if sql.strip().upper().startswith("SELECT"):
            return self._db.execute(sql)

        # Only admins can run INSERT, UPDATE, DELETE
        if self._user_role != "admin":
            raise PermissionError(
                f"User with role '{self._user_role}' cannot run: {sql}"
            )
        return self._db.execute(sql)


# All proxies have the same interface as DatabaseQuery — transparent to caller
real_db   = DatabaseQuery()
cached_db = CachingProxy(real_db)

print(cached_db.execute("SELECT * FROM users"))    # hits DB
print(cached_db.execute("SELECT * FROM users"))    # hits cache — fast!
print(cached_db.execute("SELECT * FROM users"))    # hits cache again

logged_db = LoggingProxy(real_db)
logged_db.execute("SELECT * FROM orders")

protected = ProtectionProxy(real_db, user_role="guest")
protected.execute("SELECT * FROM users")           # OK — SELECT allowed

try:
    protected.execute("DELETE FROM users")         # blocked — not admin
except PermissionError as e:
    print(f"Blocked: {e}")

admin_db = ProtectionProxy(real_db, user_role="admin")
admin_db.execute("DELETE FROM users WHERE id=99")  # allowed — admin


# ------------------------------------------------------------
# 6. COMPOSITE — treat individuals and groups the same way
# ------------------------------------------------------------
# Problem:  You have a tree structure (files/folders, org chart,
#           UI components) and want to treat single items and
#           groups of items IDENTICALLY.
#
# Solution: Both individual objects (Leaf) and containers (Composite)
#           implement the SAME interface. Containers delegate
#           operations to their children.

class FileSystemItem(ABC):
    """Common interface for both files and folders."""
    @abstractmethod
    def get_size(self) -> int: pass

    @abstractmethod
    def display(self, indent=0): pass


class File(FileSystemItem):
    """Leaf — a single item with no children."""
    def __init__(self, name, size):
        self.name = name
        self._size = size    # files have a fixed size

    def get_size(self):
        return self._size    # just return own size

    def display(self, indent=0):
        print(" " * indent + f"📄 {self.name} ({self._size} KB)")


class Folder(FileSystemItem):
    """Composite — contains other FileSystemItems (files or folders)."""
    def __init__(self, name):
        self.name     = name
        self._children = []    # can hold files AND other folders

    def add(self, item: FileSystemItem):
        self._children.append(item)    # add child (file or folder)
        return self

    def remove(self, item: FileSystemItem):
        self._children.remove(item)

    def get_size(self):
        # total size = sum of all children's sizes (recursive)
        return sum(child.get_size() for child in self._children)

    def display(self, indent=0):
        print(" " * indent + f"📁 {self.name}/ ({self.get_size()} KB)")
        for child in self._children:
            child.display(indent + 2)    # indent children for tree view


# Build a file system tree
root = Folder("root")
src  = Folder("src")
docs = Folder("docs")

src.add(File("main.py",   10))
src.add(File("utils.py",   5))
src.add(File("config.py",  2))

docs.add(File("README.md",  3))
docs.add(File("API.md",     7))

tests = Folder("tests")
tests.add(File("test_main.py",   8))
tests.add(File("test_utils.py",  4))

root.add(src)
root.add(docs)
root.add(tests)
root.add(File("setup.py", 1))

# Treat entire tree and individual files EXACTLY the same way
root.display()
print(f"\nTotal size: {root.get_size()} KB")
print(f"src size:   {src.get_size()} KB")
print(f"README size: {docs._children[0].get_size()} KB")


# ------------------------------------------------------------
# 7. BRIDGE — separate abstraction from implementation
# ------------------------------------------------------------
# Problem:  You have two independent dimensions of variation.
#           E.g., shapes (circle, square) AND renderers (vector, raster).
#           Using inheritance creates an explosion of subclasses:
#           VectorCircle, RasterCircle, VectorSquare, RasterSquare...
#
# Solution: Bridge separates them into two class hierarchies
#           connected by a reference (a "bridge").
#           Each dimension can vary independently.

class Renderer(ABC):
    """Implementation hierarchy — HOW to render."""
    @abstractmethod
    def render_circle(self, radius): pass

    @abstractmethod
    def render_square(self, side): pass


class VectorRenderer(Renderer):
    """Renders shapes as vector graphics (scalable, precise)."""
    def render_circle(self, radius):
        print(f"Drawing circle (r={radius}) as vector SVG path")

    def render_square(self, side):
        print(f"Drawing square (s={side}) as vector SVG rect")


class RasterRenderer(Renderer):
    """Renders shapes as pixel bitmaps."""
    def render_circle(self, radius):
        print(f"Drawing circle (r={radius}) as {radius*2}x{radius*2} pixel bitmap")

    def render_square(self, side):
        print(f"Drawing square (s={side}) as {side}x{side} pixel grid")


class Shape(ABC):
    """Abstraction hierarchy — WHAT to draw."""
    def __init__(self, renderer: Renderer):
        self._renderer = renderer    # BRIDGE: hold a reference to the implementation

    @abstractmethod
    def draw(self): pass

    @abstractmethod
    def resize(self, factor): pass


class Circle(Shape):
    def __init__(self, renderer, radius):
        super().__init__(renderer)
        self.radius = radius

    def draw(self):
        self._renderer.render_circle(self.radius)    # delegate to whichever renderer

    def resize(self, factor):
        self.radius *= factor


class Square(Shape):
    def __init__(self, renderer, side):
        super().__init__(renderer)
        self.side = side

    def draw(self):
        self._renderer.render_square(self.side)

    def resize(self, factor):
        self.side *= factor


# Mix and match shapes with renderers — no subclass explosion!
vector  = VectorRenderer()
raster  = RasterRenderer()

Circle(vector, 5).draw()     # vector circle
Circle(raster, 5).draw()     # raster circle
Square(vector, 4).draw()     # vector square
Square(raster, 4).draw()     # raster square

# Change renderer at runtime
c = Circle(vector, 10)
c.draw()
c._renderer = raster    # swap renderer — same shape, different output
c.draw()


# ------------------------------------------------------------
# 8. FLYWEIGHT — share data to support many small objects
# ------------------------------------------------------------
# Problem:  You need to create MILLIONS of similar objects.
#           Each has intrinsic data (shared, same for many)
#           and extrinsic data (unique per object, passed in).
#           Storing all data in each object wastes huge memory.
#
# Solution: Store shared (intrinsic) data in a Flyweight object.
#           Many objects SHARE the same flyweight.
#           Unique (extrinsic) data is passed in at use time.

class TreeType:
    """Flyweight — holds SHARED data for all trees of the same type.
    One TreeType object is shared by potentially thousands of Tree objects."""

    def __init__(self, name, color, texture):
        self.name    = name      # intrinsic: same for all oak trees
        self.color   = color     # intrinsic: same for all oak trees
        self.texture = texture   # intrinsic: same for all oak trees
        print(f"  [Flyweight] Created TreeType: {name}")

    def draw(self, x, y):
        # x, y are extrinsic — unique per tree, passed in at draw time
        print(f"  Drawing {self.name} tree at ({x},{y}) "
              f"color={self.color}")


class TreeTypeFactory:
    """Flyweight factory — ensures we reuse existing flyweights."""
    _types = {}    # cache of already-created TreeType objects

    @classmethod
    def get_tree_type(cls, name, color, texture):
        key = (name, color, texture)    # unique key for this combination
        if key not in cls._types:
            cls._types[key] = TreeType(name, color, texture)   # create once
        return cls._types[key]          # reuse the existing flyweight


class Tree:
    """Context — has unique (extrinsic) data AND a reference to shared flyweight."""
    def __init__(self, x, y, tree_type: TreeType):
        self.x         = x           # extrinsic: this tree's unique position
        self.y         = y           # extrinsic: this tree's unique position
        self._type     = tree_type   # intrinsic: SHARED flyweight object

    def draw(self):
        self._type.draw(self.x, self.y)   # pass extrinsic data to flyweight


class Forest:
    """Creates many trees — demonstrates flyweight memory savings."""
    def __init__(self):
        self._trees = []

    def plant_tree(self, x, y, name, color, texture):
        # Get (or reuse) the flyweight for this tree type
        tree_type = TreeTypeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, tree_type)    # tree only stores x, y + reference
        self._trees.append(tree)

    def draw(self):
        for tree in self._trees:
            tree.draw()

    def stats(self):
        unique_types = len(TreeTypeFactory._types)
        total_trees  = len(self._trees)
        print(f"\n{total_trees} trees drawn using only {unique_types} "
              f"TreeType objects (flyweights)")


forest = Forest()
import random
random.seed(42)

# Plant 1000 trees — but only 3 unique TreeType flyweights are created!
tree_types = [
    ("Oak",   "green",  "rough"),
    ("Pine",  "darkgreen", "smooth"),
    ("Maple", "orange", "medium"),
]
for _ in range(1000):
    name, color, texture = random.choice(tree_types)
    x, y = random.randint(0, 100), random.randint(0, 100)
    forest.plant_tree(x, y, name, color, texture)

forest.stats()
# 1000 trees but only 3 TreeType objects — massive memory saving


# ============================================================
# SUMMARY
# ============================================================
# Adapter     → wraps incompatible interface to match expected one
#               use when integrating third-party or legacy code
#
# Decorator   → wraps object to add behaviour, same interface
#               use when you need to add features dynamically/combinably
#               key: return self._wrapped.method() to delegate
#
# Facade      → one simple interface over a complex subsystem
#               use when clients need a simpler view of many classes
#
# Proxy       → controls access to the real object, same interface
#               types: caching, logging, protection, lazy loading
#
# Composite   → tree structure, leaf and container same interface
#               use when you have part-whole hierarchies
#               key: container delegates to children recursively
#
# Bridge      → separates abstraction (what) from implementation (how)
#               use when two dimensions vary independently
#               avoids subclass explosion (M shapes × N renderers = M+N classes)
#
# Flyweight   → share intrinsic data, pass extrinsic data at use time
#               use when creating millions of similar objects
#               key: factory ensures one flyweight per unique config
# ============================================================