# ------------------------------------------------------------
# 2. THE CODE WE WILL TEST
# ------------------------------------------------------------
# Let's write some functions first, then test them.
# In a real project these would be in separate files.

def add(a, b):
    """Return the sum of a and b."""
    return a + b

def subtract(a, b):
    """Return a minus b."""
    return a - b

def multiply(a, b):
    """Return a multiplied by b."""
    return a * b

def divide(a, b):
    """Return a divided by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def is_palindrome(s):
    """Return True if string s reads the same forwards and backwards."""
    s = s.lower().replace(" ", "")    # normalize: lowercase and remove spaces
    return s == s[::-1]               # compare string to its reverse

def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit."""
    return (c * 9/5) + 32

class BankAccount:
    """A simple bank account for testing OOP."""
    def __init__(self, owner, balance=0):
        self.owner   = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"


