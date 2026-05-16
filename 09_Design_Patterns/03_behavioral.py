# ============================================================
#  CHAPTER 9 — DESIGN PATTERNS: BEHAVIORAL
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHAT ARE BEHAVIORAL PATTERNS?
# ------------------------------------------------------------
# Behavioral patterns deal with how objects COMMUNICATE
# and INTERACT with each other.
#
# They help you:
#   → Define a family of algorithms and swap them (Strategy)
#   → Notify many objects when one changes (Observer)
#   → Encapsulate a request as an object (Command)
#   → Define a skeleton algorithm, let subclasses fill in steps (Template Method)
#   → Pass requests along a chain of handlers (Chain of Responsibility)
#   → Allow an object to change behavior when state changes (State)
#   → Traverse a collection without knowing its structure (Iterator)
#   → Define grammar and interpret sentences (Interpreter)
#   → Capture and restore object state (Memento)
#   → Simplify communication between objects (Mediator)
#   → Add operations to objects without changing them (Visitor)
#
# THIS FILE covers the most important ones:
#   1. Strategy              → swap algorithms at runtime
#   2. Observer              → event/notification system
#   3. Command               → encapsulate requests as objects
#   4. Template Method       → define skeleton, subclasses fill steps
#   5. Chain of Responsibility→ pass request along a chain
#   6. State                 → behavior changes with state
#   7. Memento               → save and restore state


# ------------------------------------------------------------
# 2. STRATEGY — swap algorithms at runtime
# ------------------------------------------------------------
# Problem:  You have multiple ways to do something (sort, pay,
#           compress, validate) and want to switch between them
#           without changing the code that uses them.
#
# Solution: Define each algorithm in its own class (Strategy).
#           The context holds a reference to a strategy and
#           delegates the work to it. Swap strategy = swap behavior.

from abc import ABC, abstractmethod

class SortStrategy(ABC):
    """Abstract strategy — defines the interface all sort algorithms share."""
    @abstractmethod
    def sort(self, data: list) -> list:
        pass


class BubbleSortStrategy(SortStrategy):
    """Concrete strategy — bubble sort algorithm."""
    def sort(self, data: list) -> list:
        data = data.copy()           # don't modify the original list
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):    # compare adjacent elements
                if data[j] > data[j + 1]:    # if out of order
                    data[j], data[j+1] = data[j+1], data[j]    # swap them
        print("  Used: Bubble Sort")
        return data


class QuickSortStrategy(SortStrategy):
    """Concrete strategy — quick sort algorithm."""
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data                      # base case — already sorted
        pivot  = data[len(data) // 2]        # pick middle element as pivot
        left   = [x for x in data if x < pivot]   # elements less than pivot
        middle = [x for x in data if x == pivot]  # elements equal to pivot
        right  = [x for x in data if x > pivot]   # elements greater than pivot
        print("  Used: Quick Sort")
        return self.sort(left) + middle + self.sort(right)  # recursively sort


class PythonSortStrategy(SortStrategy):
    """Concrete strategy — just use Python's built-in sort (Timsort)."""
    def sort(self, data: list) -> list:
        print("  Used: Python Built-in Sort (Timsort)")
        return sorted(data)    # Python's sorted() returns a new sorted list


class Sorter:
    """Context — uses a strategy to sort data. Doesn't know which algorithm."""
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy    # hold the current strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy    # swap strategy at runtime — no other code changes

    def sort(self, data: list) -> list:
        print(f"Sorting {len(data)} items...")
        return self._strategy.sort(data)    # delegate to whichever strategy is set


data = [5, 2, 8, 1, 9, 3, 7, 4, 6]

sorter = Sorter(BubbleSortStrategy())
print(sorter.sort(data))

sorter.set_strategy(QuickSortStrategy())    # swap algorithm — context unchanged
print(sorter.sort(data))

sorter.set_strategy(PythonSortStrategy())
print(sorter.sort(data))


# Real-world: payment strategy
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool: pass

class CreditCardStrategy(PaymentStrategy):
    def __init__(self, card_number, cvv):
        self._card = card_number
        self._cvv  = cvv

    def pay(self, amount):
        print(f"  Charging ${amount:.2f} to card ending {self._card[-4:]}")
        return True    # simulate successful payment

class PayPalStrategy(PaymentStrategy):
    def __init__(self, email):
        self._email = email

    def pay(self, amount):
        print(f"  Sending ${amount:.2f} via PayPal to {self._email}")
        return True

class CryptoStrategy(PaymentStrategy):
    def __init__(self, wallet):
        self._wallet = wallet

    def pay(self, amount):
        print(f"  Sending ${amount:.2f} in BTC to {self._wallet[:8]}...")
        return True

class ShoppingCart:
    """Context — processes payment using whatever strategy is set."""
    def __init__(self):
        self._items   = []
        self._payment = None    # no payment method set yet

    def add_item(self, name, price):
        self._items.append((name, price))

    def set_payment(self, strategy: PaymentStrategy):
        self._payment = strategy    # inject the payment strategy

    def checkout(self):
        total = sum(price for _, price in self._items)
        print(f"Total: ${total:.2f}")
        if not self._payment:
            raise ValueError("No payment method set")
        return self._payment.pay(total)    # delegate to whichever payment strategy

cart = ShoppingCart()
cart.add_item("Laptop", 999.99)
cart.add_item("Mouse", 29.99)

cart.set_payment(CreditCardStrategy("4111111111111111", "123"))
cart.checkout()

cart.set_payment(PayPalStrategy("alice@example.com"))   # swap strategy
cart.checkout()


# ------------------------------------------------------------
# 3. OBSERVER — notify many objects when one changes
# ------------------------------------------------------------
# Problem:  One object (subject) changes state, and many other
#           objects (observers) need to know about it.
#           You don't want the subject to be tightly coupled
#           to the observers — it shouldn't know their details.
#
# Solution: Observers REGISTER with the subject.
#           When subject changes, it NOTIFIES all registered observers.
#           Subject knows nothing about observers except they have update().
#
# Also called: Event system, Publish-Subscribe, Listener pattern.

class Observer(ABC):
    """Abstract observer — all observers implement update()."""
    @abstractmethod
    def update(self, event: str, data: dict): pass


class Subject:
    """Subject (publisher) — maintains list of observers and notifies them."""

    def __init__(self):
        self._observers = []    # list of registered observers

    def subscribe(self, observer: Observer):
        """Register an observer to receive notifications."""
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        """Remove an observer — it will no longer receive notifications."""
        self._observers.remove(observer)

    def notify(self, event: str, data: dict):
        """Notify ALL registered observers of an event."""
        for observer in self._observers:
            observer.update(event, data)    # each observer handles it its own way


class StockMarket(Subject):
    """Concrete subject — stock prices change, observers are notified."""

    def __init__(self):
        super().__init__()
        self._prices = {}    # stock symbol → price

    def update_price(self, symbol, price):
        old_price = self._prices.get(symbol, 0)
        self._prices[symbol] = price
        change = price - old_price
        # Notify all observers with event details
        self.notify("price_change", {
            "symbol": symbol,
            "price":  price,
            "change": change,
            "pct":    (change / old_price * 100) if old_price else 0
        })


class AlertObserver(Observer):
    """Sends an alert if price changes significantly."""
    def __init__(self, threshold_pct):
        self._threshold = threshold_pct    # alert if change > threshold %

    def update(self, event, data):
        if event == "price_change" and abs(data["pct"]) >= self._threshold:
            direction = "📈" if data["change"] > 0 else "📉"
            print(f"  [ALERT] {direction} {data['symbol']}: "
                  f"${data['price']:.2f} ({data['pct']:+.1f}%)")


class PortfolioObserver(Observer):
    """Tracks portfolio value."""
    def __init__(self, holdings: dict):
        self._holdings = holdings    # {symbol: shares_owned}
        self._prices   = {}

    def update(self, event, data):
        if event == "price_change":
            self._prices[data["symbol"]] = data["price"]
            total = sum(
                self._prices.get(sym, 0) * shares
                for sym, shares in self._holdings.items()
            )
            print(f"  [PORTFOLIO] Total value: ${total:,.2f}")


class LogObserver(Observer):
    """Logs every price change."""
    def update(self, event, data):
        if event == "price_change":
            print(f"  [LOG] {data['symbol']}: ${data['price']:.2f}")


market   = StockMarket()
alerter  = AlertObserver(threshold_pct=5.0)    # alert on 5%+ change
portfolio= PortfolioObserver({"AAPL": 10, "GOOG": 5})
logger   = LogObserver()

# Register observers
market.subscribe(alerter)
market.subscribe(portfolio)
market.subscribe(logger)

print("\n--- Market Updates ---")
market.update_price("AAPL", 150.00)
market.update_price("GOOG", 2800.00)
market.update_price("AAPL", 162.00)    # 8% jump — alert fires!

# Unsubscribe logger — won't receive future updates
market.unsubscribe(logger)
print("\n--- After unsubscribing logger ---")
market.update_price("GOOG", 2750.00)


# ------------------------------------------------------------
# 4. COMMAND — encapsulate a request as an object
# ------------------------------------------------------------
# Problem:  You want to parameterize operations, queue them,
#           log them, or support UNDO/REDO — but the operations
#           are tightly coupled to the objects that execute them.
#
# Solution: Wrap each operation in a Command object.
#           Command has execute() and optionally undo().
#           Commands can be stored, queued, logged, replayed.

class Command(ABC):
    """Abstract command — all commands implement execute() and undo()."""
    @abstractmethod
    def execute(self): pass

    @abstractmethod
    def undo(self): pass


class TextEditor:
    """Receiver — the object that actually performs the work."""
    def __init__(self):
        self.text = ""

    def insert(self, text, position):
        self.text = self.text[:position] + text + self.text[position:]

    def delete(self, position, length):
        self.text = self.text[:position] + self.text[position + length:]

    def __str__(self):
        return f"Text: '{self.text}'"


class InsertCommand(Command):
    """Command that inserts text — stores enough to undo it."""
    def __init__(self, editor: TextEditor, text: str, position: int):
        self._editor   = editor
        self._text     = text
        self._position = position

    def execute(self):
        self._editor.insert(self._text, self._position)   # do the insert
        print(f"  Inserted '{self._text}' at {self._position}")

    def undo(self):
        # Undo insert by deleting the inserted text
        self._editor.delete(self._position, len(self._text))
        print(f"  Undid: removed '{self._text}' at {self._position}")


class DeleteCommand(Command):
    """Command that deletes text — saves deleted text for undo."""
    def __init__(self, editor: TextEditor, position: int, length: int):
        self._editor   = editor
        self._position = position
        self._length   = length
        self._deleted  = ""    # will store deleted text so we can restore it

    def execute(self):
        # Save the text we're about to delete (needed for undo)
        self._deleted = self._editor.text[self._position:self._position+self._length]
        self._editor.delete(self._position, self._length)
        print(f"  Deleted '{self._deleted}' at {self._position}")

    def undo(self):
        # Undo delete by re-inserting the saved text
        self._editor.insert(self._deleted, self._position)
        print(f"  Undid: restored '{self._deleted}' at {self._position}")


class CommandHistory:
    """Invoker — executes commands and maintains history for undo/redo."""

    def __init__(self):
        self._history = []    # stack of executed commands
        self._undone  = []    # stack of undone commands (for redo)

    def execute(self, command: Command):
        command.execute()              # run the command
        self._history.append(command) # add to history
        self._undone.clear()          # new command clears redo stack

    def undo(self):
        if not self._history:
            print("  Nothing to undo")
            return
        command = self._history.pop()   # get last command
        command.undo()                  # reverse it
        self._undone.append(command)    # save for potential redo

    def redo(self):
        if not self._undone:
            print("  Nothing to redo")
            return
        command = self._undone.pop()    # get last undone command
        command.execute()               # re-execute it
        self._history.append(command)   # back in history


editor  = TextEditor()
history = CommandHistory()

print("\n--- Text Editor with Undo/Redo ---")
history.execute(InsertCommand(editor, "Hello", 0))
print(editor)

history.execute(InsertCommand(editor, " World", 5))
print(editor)

history.execute(DeleteCommand(editor, 0, 5))    # delete "Hello"
print(editor)

history.undo()    # undo the delete
print(editor)

history.undo()    # undo " World" insert
print(editor)

history.redo()    # redo " World" insert
print(editor)


# ------------------------------------------------------------
# 5. TEMPLATE METHOD — define skeleton, subclasses fill steps
# ------------------------------------------------------------
# Problem:  Multiple classes share the same OVERALL algorithm
#           but differ in SPECIFIC STEPS.
#           Duplicating the structure in each class is error-prone.
#
# Solution: Base class defines the algorithm skeleton in a
#           template method. Specific steps are abstract methods
#           that subclasses implement.

class DataMigration(ABC):
    """Abstract class — defines the migration algorithm skeleton."""

    def migrate(self):
        """Template method — the overall algorithm is fixed here."""
        print(f"\n=== Starting {self.__class__.__name__} ===")
        data = self.extract()          # step 1: get the data
        data = self.transform(data)    # step 2: transform it
        self.load(data)                # step 3: store it
        self.send_report()             # step 4: always send report (not abstract)
        print("=== Migration complete ===")

    @abstractmethod
    def extract(self) -> list:
        """Subclass defines: WHERE to get data from."""
        pass

    @abstractmethod
    def transform(self, data: list) -> list:
        """Subclass defines: HOW to transform the data."""
        pass

    @abstractmethod
    def load(self, data: list):
        """Subclass defines: WHERE to put the data."""
        pass

    def send_report(self):
        """Hook — subclasses can override, but it has a default implementation."""
        print("  Report: Migration completed successfully.")


class CSVToDatabase(DataMigration):
    """Concrete class — migrates from CSV file to a database."""

    def extract(self):
        print("  Extracting from CSV file...")
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]    # simulate

    def transform(self, data):
        print("  Transforming: normalizing names to uppercase...")
        return [{**row, "name": row["name"].upper()} for row in data]

    def load(self, data):
        print(f"  Loading {len(data)} records into PostgreSQL...")

    def send_report(self):
        print("  Sending detailed CSV migration report via email...")


class APIToCache(DataMigration):
    """Concrete class — migrates from an API to a cache."""

    def extract(self):
        print("  Fetching data from REST API...")
        return [{"key": "user:1", "val": "Alice"}, {"key": "user:2", "val": "Bob"}]

    def transform(self, data):
        print("  Transforming: adding TTL to each record...")
        return [{**row, "ttl": 3600} for row in data]    # add 1 hour TTL

    def load(self, data):
        print(f"  Writing {len(data)} entries to Redis cache...")
    # uses default send_report() from base class


CSVToDatabase().migrate()
APIToCache().migrate()


# ------------------------------------------------------------
# 6. CHAIN OF RESPONSIBILITY
# ------------------------------------------------------------
# Problem:  A request needs to be processed by one of multiple
#           handlers, but you don't know WHICH one at compile time.
#           Hardcoding the logic creates complex if/elif chains.
#
# Solution: Chain handlers together. Each handler either processes
#           the request OR passes it to the next handler in the chain.

class Handler(ABC):
    """Abstract handler — every handler knows about the next one."""

    def __init__(self):
        self._next = None    # reference to the next handler in the chain

    def set_next(self, handler):
        self._next = handler    # link this handler to the next one
        return handler          # return handler to allow chaining: a.set_next(b).set_next(c)

    def handle(self, request):
        if self._next:
            return self._next.handle(request)    # pass to next handler
        return None    # end of chain — nobody handled it


class AuthHandler(Handler):
    """Checks if user is authenticated."""
    def handle(self, request):
        if not request.get("authenticated"):
            print("  [Auth] REJECTED: User not authenticated")
            return "401 Unauthorized"
        print("  [Auth] Passed: user is authenticated")
        return super().handle(request)    # pass to next handler


class RateLimitHandler(Handler):
    """Checks if request rate limit is exceeded."""
    def __init__(self, max_per_minute):
        super().__init__()
        self._max      = max_per_minute
        self._requests = 0    # simple counter (real code would use time windows)

    def handle(self, request):
        self._requests += 1
        if self._requests > self._max:
            print(f"  [RateLimit] REJECTED: Limit of {self._max}/min exceeded")
            return "429 Too Many Requests"
        print(f"  [RateLimit] Passed: {self._requests}/{self._max}")
        return super().handle(request)


class ValidationHandler(Handler):
    """Validates request data."""
    def handle(self, request):
        if not request.get("data"):
            print("  [Validation] REJECTED: Missing required 'data' field")
            return "400 Bad Request"
        print("  [Validation] Passed: data field present")
        return super().handle(request)


class BusinessLogicHandler(Handler):
    """Final handler — actually processes the request."""
    def handle(self, request):
        print(f"  [Business] Processing: {request['data']}")
        return "200 OK"    # success — handled!


# Build the chain: Auth → RateLimit → Validation → BusinessLogic
auth     = AuthHandler()
rate     = RateLimitHandler(max_per_minute=3)
validate = ValidationHandler()
business = BusinessLogicHandler()

auth.set_next(rate).set_next(validate).set_next(business)
# reads as: auth → rate → validate → business

print("\n--- Chain of Responsibility ---")
requests = [
    {"authenticated": True,  "data": "create user"},
    {"authenticated": False, "data": "delete user"},    # fails auth
    {"authenticated": True,  "data": "update profile"},
    {"authenticated": True,  "data": "get report"},
    {"authenticated": True,  "data": "fetch data"},    # fails rate limit
    {"authenticated": True},                           # fails validation
]

for req in requests:
    print(f"\nRequest: {req}")
    result = auth.handle(req)    # always start at the first handler
    print(f"Result: {result}")


# ------------------------------------------------------------
# 7. STATE — behavior changes when internal state changes
# ------------------------------------------------------------
# Problem:  An object behaves DIFFERENTLY depending on its
#           internal state. Managing this with if/elif chains
#           becomes complex and hard to maintain.
#
# Solution: Each state is its own class. The object delegates
#           behavior to its current state object.
#           Changing state = swapping the state object.

class TrafficLightState(ABC):
    """Abstract state — defines interface for all traffic light states."""
    @abstractmethod
    def handle(self, light) -> None: pass

    @abstractmethod
    def __str__(self) -> str: pass


class RedState(TrafficLightState):
    """Red light — stop! Transitions to green."""
    def handle(self, light):
        print("  🔴 RED: Stop! Switching to Green...")
        light.set_state(GreenState())    # transition to next state

    def __str__(self): return "RED"


class GreenState(TrafficLightState):
    """Green light — go! Transitions to yellow."""
    def handle(self, light):
        print("  🟢 GREEN: Go! Switching to Yellow...")
        light.set_state(YellowState())

    def __str__(self): return "GREEN"


class YellowState(TrafficLightState):
    """Yellow light — slow down! Transitions to red."""
    def handle(self, light):
        print("  🟡 YELLOW: Slow down! Switching to Red...")
        light.set_state(RedState())

    def __str__(self): return "YELLOW"


class TrafficLight:
    """Context — holds current state, delegates behavior to it."""
    def __init__(self):
        self._state = RedState()    # start in red state

    def set_state(self, state: TrafficLightState):
        self._state = state    # change the current state

    def change(self):
        print(f"Current: {self._state}")
        self._state.handle(self)    # delegate to current state

light = TrafficLight()
for _ in range(6):    # cycle through 6 changes
    light.change()


# Real-world: Order state machine
class OrderState(ABC):
    @abstractmethod
    def confirm(self, order): pass
    @abstractmethod
    def ship(self, order): pass
    @abstractmethod
    def deliver(self, order): pass
    @abstractmethod
    def cancel(self, order): pass
    def __str__(self): return self.__class__.__name__.replace("State", "")

class PendingState(OrderState):
    def confirm(self, order):
        print("  Order confirmed!")
        order.set_state(ConfirmedState())
    def ship(self, order):    print("  Cannot ship — not confirmed yet")
    def deliver(self, order): print("  Cannot deliver — not shipped yet")
    def cancel(self, order):
        print("  Order cancelled while pending")
        order.set_state(CancelledState())

class ConfirmedState(OrderState):
    def confirm(self, order): print("  Already confirmed")
    def ship(self, order):
        print("  Order shipped!")
        order.set_state(ShippedState())
    def deliver(self, order): print("  Cannot deliver — not shipped yet")
    def cancel(self, order):
        print("  Order cancelled after confirmation")
        order.set_state(CancelledState())

class ShippedState(OrderState):
    def confirm(self, order): print("  Already confirmed and shipped")
    def ship(self, order):    print("  Already shipped")
    def deliver(self, order):
        print("  Order delivered!")
        order.set_state(DeliveredState())
    def cancel(self, order):  print("  Cannot cancel — already shipped")

class DeliveredState(OrderState):
    def confirm(self, order): print("  Already delivered")
    def ship(self, order):    print("  Already delivered")
    def deliver(self, order): print("  Already delivered")
    def cancel(self, order):  print("  Cannot cancel — already delivered")

class CancelledState(OrderState):
    def confirm(self, order): print("  Cannot confirm — cancelled")
    def ship(self, order):    print("  Cannot ship — cancelled")
    def deliver(self, order): print("  Cannot deliver — cancelled")
    def cancel(self, order):  print("  Already cancelled")

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self._state   = PendingState()    # all orders start as pending

    def set_state(self, state):
        self._state = state

    def confirm(self): print(f"[{self._state}]", end=" "); self._state.confirm(self)
    def ship(self):    print(f"[{self._state}]", end=" "); self._state.ship(self)
    def deliver(self): print(f"[{self._state}]", end=" "); self._state.deliver(self)
    def cancel(self):  print(f"[{self._state}]", end=" "); self._state.cancel(self)

print("\n--- Order State Machine ---")
order = Order("ORD-001")
order.ship()       # can't ship — not confirmed
order.confirm()    # confirm it
order.confirm()    # already confirmed
order.ship()       # ship it
order.cancel()     # can't cancel — already shipped
order.deliver()    # deliver it


# ------------------------------------------------------------
# 8. MEMENTO — save and restore object state
# ------------------------------------------------------------
# Problem:  You need to implement undo/redo, snapshots, or
#           save points — but you don't want to expose the
#           object's internal state to the outside world.
#
# Solution: Memento captures the state of an object (originator)
#           into a memento object. The caretaker stores mementos.
#           The originator can restore itself from a memento.

class EditorMemento:
    """Memento — stores a snapshot of the editor's state.
    Immutable — once created, state cannot be changed."""

    def __init__(self, text, cursor, selection):
        self._text      = text       # snapshot of text content
        self._cursor    = cursor     # snapshot of cursor position
        self._selection = selection  # snapshot of selected text

    def get_state(self):
        """Return the saved state — only the originator should call this."""
        return self._text, self._cursor, self._selection


class CodeEditor:
    """Originator — creates mementos of its state and can restore them."""

    def __init__(self):
        self._text      = ""
        self._cursor    = 0
        self._selection = None

    def type(self, text):
        self._text   += text             # append typed text
        self._cursor  = len(self._text)  # cursor moves to end

    def select(self, start, end):
        self._selection = (start, end)

    def save(self) -> EditorMemento:
        """Create and return a memento of current state."""
        return EditorMemento(self._text, self._cursor, self._selection)

    def restore(self, memento: EditorMemento):
        """Restore state from a memento."""
        self._text, self._cursor, self._selection = memento.get_state()

    def __str__(self):
        return (f"Editor[text='{self._text}', "
                f"cursor={self._cursor}, "
                f"selection={self._selection}]")


class History:
    """Caretaker — stores mementos, knows WHEN to save/restore.
    Does NOT look inside mementos — that's the originator's job."""

    def __init__(self):
        self._mementos = []    # stack of saved states

    def save(self, memento: EditorMemento):
        self._mementos.append(memento)    # push snapshot onto stack

    def undo(self) -> EditorMemento:
        if len(self._mementos) < 2:
            print("  Nothing to undo")
            return self._mementos[0] if self._mementos else None
        self._mementos.pop()             # remove current state
        return self._mementos[-1]        # return previous state


print("\n--- Memento: Code Editor Undo ---")
editor  = CodeEditor()
history = History()

editor.type("def hello")
history.save(editor.save())    # save snapshot 1
print(editor)

editor.type("():")
history.save(editor.save())    # save snapshot 2
print(editor)

editor.type("\n    print('hi')")
history.save(editor.save())    # save snapshot 3
print(editor)

print("\nUndoing...")
editor.restore(history.undo())    # go back to snapshot 2
print(editor)

editor.restore(history.undo())    # go back to snapshot 1
print(editor)


# ============================================================
# SUMMARY
# ============================================================
# Strategy          → family of interchangeable algorithms
#                     context holds strategy, delegates to it
#                     use when: sorting, payments, compression
#
# Observer          → subject notifies all registered observers
#                     observers subscribe/unsubscribe at runtime
#                     use w