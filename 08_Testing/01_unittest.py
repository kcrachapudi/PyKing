# ============================================================
#  CHAPTER 8 — TESTING WITH unittest
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. WHY TESTING?
# ------------------------------------------------------------
# Tests are code that verifies YOUR code works correctly.
#
# Without tests:
#   → You manually run the program to check if it works
#   → One change can silently break something else
#   → You're afraid to refactor because "what if it breaks?"
#   → Bugs reach production and real users
#
# With tests:
#   → Run hundreds of checks in seconds automatically
#   → Catch bugs BEFORE they reach production
#   → Confidently refactor — tests tell you if you broke something
#   → Tests act as DOCUMENTATION of expected behavior
#
# Types of tests:
#   Unit tests       → test one small piece (one function/method)
#   Integration tests→ test how pieces work TOGETHER
#   End-to-end tests → test the entire system as a user would
#
# THIS FILE covers unittest — Python's built-in testing framework.


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


# ------------------------------------------------------------
# 3. WRITING YOUR FIRST TEST
# ------------------------------------------------------------
# A test in unittest is a class that:
#   → inherits from unittest.TestCase
#   → has methods starting with 'test_'
#   → uses self.assert*() methods to check expected vs actual

import unittest

class TestMathFunctions(unittest.TestCase):
    """Tests for our math functions."""
    # Each method that starts with 'test_' is run as a separate test.
    # If an assertion fails, that test FAILS. Others still run.

    def test_add_positive_numbers(self):
        """Test that add() correctly adds two positive numbers."""
        result = add(3, 5)           # call the function we're testing
        self.assertEqual(result, 8)  # assert: result MUST equal 8

    def test_add_negative_numbers(self):
        """Test add() with negative numbers."""
        self.assertEqual(add(-1, -1), -2)    # -1 + -1 = -2

    def test_add_mixed_signs(self):
        """Test add() with positive and negative."""
        self.assertEqual(add(-3, 5), 2)      # -3 + 5 = 2

    def test_add_zero(self):
        """Test add() with zero."""
        self.assertEqual(add(0, 5), 5)       # 0 + 5 = 5
        self.assertEqual(add(5, 0), 5)       # 5 + 0 = 5

    def test_subtract(self):
        """Test subtract()."""
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(0, 5), -5)

    def test_multiply(self):
        """Test multiply()."""
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(0, 100), 0)    # anything times 0 is 0
        self.assertEqual(multiply(-2, 5), -10)

    def test_divide_normal(self):
        """Test divide() with valid inputs."""
        self.assertEqual(divide(10, 2), 5.0)
        self.assertAlmostEqual(divide(1, 3), 0.333, places=3)
        # assertAlmostEqual checks floating point numbers to N decimal places
        # because 1/3 = 0.33333... and assertEqual(0.333333, 0.333) would fail


# ------------------------------------------------------------
# 4. TESTING EXCEPTIONS
# ------------------------------------------------------------

class TestDivide(unittest.TestCase):

    def test_divide_by_zero_raises(self):
        """Test that dividing by zero raises ZeroDivisionError."""
        # assertRaises(ExceptionType, callable, *args) checks that
        # calling callable(*args) raises the expected exception
        self.assertRaises(ZeroDivisionError, divide, 10, 0)

    def test_divide_by_zero_context_manager(self):
        """Alternative: use assertRaises as a context manager."""
        # This is cleaner — lets you check the exception MESSAGE too
        with self.assertRaises(ZeroDivisionError) as context:
            divide(10, 0)    # this line must raise ZeroDivisionError
        # context.exception holds the actual exception object
        self.assertIn("zero", str(context.exception).lower())


# ------------------------------------------------------------
# 5. ALL THE assert METHODS — your testing toolkit
# ------------------------------------------------------------

class TestAssertMethods(unittest.TestCase):

    def test_equality_checks(self):
        # assertEqual — check two values are equal
        self.assertEqual(1 + 1, 2)
        self.assertEqual("hello".upper(), "HELLO")

        # assertNotEqual — check two values are NOT equal
        self.assertNotEqual(1, 2)

    def test_boolean_checks(self):
        # assertTrue — check value is truthy
        self.assertTrue(1 == 1)
        self.assertTrue([1, 2, 3])       # non-empty list is truthy

        # assertFalse — check value is falsy
        self.assertFalse(1 == 2)
        self.assertFalse([])             # empty list is falsy

    def test_none_checks(self):
        # assertIsNone — check value IS None
        result = None
        self.assertIsNone(result)

        # assertIsNotNone — check value is NOT None
        self.assertIsNotNone(42)
        self.assertIsNotNone("hello")

    def test_identity_checks(self):
        a = [1, 2, 3]
        b = a                # b points to same object

        # assertIs — check same OBJECT (like 'is')
        self.assertIs(a, b)

        # assertIsNot — check different OBJECTS (like 'is not')
        c = [1, 2, 3]        # c is a different object with same values
        self.assertIsNot(a, c)

    def test_membership_checks(self):
        fruits = ["apple", "banana", "cherry"]

        # assertIn — check item IS in container
        self.assertIn("apple", fruits)
        self.assertIn("py", "python")       # substring check on strings

        # assertNotIn — check item is NOT in container
        self.assertNotIn("mango", fruits)

    def test_type_checks(self):
        # assertIsInstance — check object is instance of class
        self.assertIsInstance(42, int)
        self.assertIsInstance("hi", str)
        self.assertIsInstance([1,2], list)
        self.assertIsInstance(3.14, (int, float))  # can pass tuple of types

    def test_comparison_checks(self):
        # assertGreater — check a > b
        self.assertGreater(5, 3)

        # assertGreaterEqual — check a >= b
        self.assertGreaterEqual(5, 5)

        # assertLess — check a < b
        self.assertLess(3, 5)

        # assertLessEqual — check a <= b
        self.assertLessEqual(3, 3)

    def test_float_comparison(self):
        # assertAlmostEqual — for floating point (avoid exact == with floats!)
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=10)
        # places=10 means accurate to 10 decimal places

        # assertNotAlmostEqual — check floats are NOT approximately equal
        self.assertNotAlmostEqual(0.1, 0.9)

    def test_string_checks(self):
        text = "Hello, World!"

        # assertIn for substrings
        self.assertIn("World", text)

        # Use regex matching for patterns
        import re
        self.assertRegex(text, r"Hello.*World")      # matches pattern
        self.assertNotRegex(text, r"^\d+")           # does NOT match digits at start

    def test_sequence_checks(self):
        # assertListEqual — compares lists AND shows diff if they differ
        self.assertListEqual([1, 2, 3], [1, 2, 3])

        # assertTupleEqual
        self.assertTupleEqual((1, "a"), (1, "a"))

        # assertDictEqual
        self.assertDictEqual({"a": 1}, {"a": 1})

        # assertSetEqual
        self.assertSetEqual({1, 2, 3}, {3, 1, 2})   # order doesn't matter for sets

    def test_raises(self):
        # assertRaises — check specific exception is raised
        with self.assertRaises(ValueError):
            int("not a number")

        with self.assertRaises(KeyError):
            d = {}
            _ = d["missing"]

        with self.assertRaises(IndexError):
            lst = [1, 2, 3]
            _ = lst[10]


# ------------------------------------------------------------
# 6. setUp AND tearDown — run code before/after each test
# ------------------------------------------------------------
# setUp()    → runs BEFORE every single test method
# tearDown() → runs AFTER every single test method (even if test fails)
# Use for: creating objects, opening files, DB connections etc.

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Create a fresh BankAccount before EACH test.
        This ensures tests are independent — one test can't affect another."""
        self.account = BankAccount("Alice", balance=1000)
        # Now every test starts with a fresh account with $1000

    def tearDown(self):
        """Runs after EACH test — clean up resources."""
        # For a BankAccount there's nothing to clean up.
        # But for files/DB connections you would close them here.
        pass

    def test_initial_balance(self):
        """Account starts with the balance passed to __init__."""
        self.assertEqual(self.account.balance, 1000)

    def test_deposit_increases_balance(self):
        """Depositing money should increase balance."""
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_deposit_returns_new_balance(self):
        """deposit() should return the new balance."""
        new_balance = self.account.deposit(200)
        self.assertEqual(new_balance, 1200)

    def test_withdraw_decreases_balance(self):
        """Withdrawing money should decrease balance."""
        self.account.withdraw(300)
        self.assertEqual(self.account.balance, 700)

    def test_withdraw_all_money(self):
        """Should be able to withdraw the entire balance."""
        self.account.withdraw(1000)
        self.assertEqual(self.account.balance, 0)

    def test_deposit_zero_raises(self):
        """Depositing zero should raise ValueError."""
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_deposit_negative_raises(self):
        """Depositing negative amount should raise ValueError."""
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_withdraw_more_than_balance_raises(self):
        """Withdrawing more than balance should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.account.withdraw(5000)    # only $1000 in account
        self.assertIn("Insufficient", str(ctx.exception))

    def test_multiple_operations(self):
        """Test a sequence of operations."""
        self.account.deposit(500)      # 1000 + 500 = 1500
        self.account.withdraw(200)     # 1500 - 200 = 1300
        self.account.deposit(100)      # 1300 + 100 = 1400
        self.assertEqual(self.account.balance, 1400)


# ------------------------------------------------------------
# 7. setUpClass AND tearDownClass — run once for the whole class
# ------------------------------------------------------------

class TestWithSharedSetup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs ONCE before ALL tests in this class.
        Use for expensive setup: connecting to a DB, loading large data."""
        print("\n[setUpClass] Setting up shared resources...")
        cls.shared_data = list(range(1000))    # expensive to create, shared by all tests
        cls.lookup      = {x: x**2 for x in range(100)}

    @classmethod
    def tearDownClass(cls):
        """Runs ONCE after ALL tests in this class."""
        print("\n[tearDownClass] Cleaning up shared resources...")
        # close DB connection, delete temp files, etc.

    def test_data_length(self):
        self.assertEqual(len(self.shared_data), 1000)

    def test_lookup_values(self):
        self.assertEqual(self.lookup[5], 25)    # 5² = 25
        self.assertEqual(self.lookup[10], 100)  # 10² = 100


# ------------------------------------------------------------
# 8. SKIPPING TESTS
# ------------------------------------------------------------

class TestSkipping(unittest.TestCase):

    @unittest.skip("Not implemented yet")    # always skip this test
    def test_not_ready(self):
        pass

    @unittest.skipIf(1 + 1 != 2, "Math is broken")  # skip if condition is True
    def test_skip_if(self):
        self.assertEqual(1 + 1, 2)    # won't be skipped — condition is False

    @unittest.skipUnless(True, "Requires True")   # skip UNLESS condition is True
    def test_skip_unless(self):
        self.assertTrue(True)    # runs because condition is True

    @unittest.expectedFailure    # test PASSES if it fails, FAILS if it passes
    def test_known_bug(self):
        self.assertEqual(1, 2)   # this always fails — marked as expected


# ------------------------------------------------------------
# 9. SUBTESTS — test multiple inputs in one test
# ------------------------------------------------------------

class TestPalindrome(unittest.TestCase):

    def test_palindromes(self):
        """Test multiple palindrome cases using subTest."""
        # Without subTest, if one input fails, others aren't tested.
        # With subTest, ALL inputs are tested and ALL failures reported.

        palindromes = [
            ("racecar",     True),
            ("hello",       False),
            ("A man a plan a canal Panama", True),  # spaces ignored
            ("Was it a car or a cat I saw", True),
            ("python",      False),
            ("level",       True),
            ("",            True),     # empty string is a palindrome
        ]

        for word, expected in palindromes:
            with self.subTest(word=word):   # label each sub-test with the input
                result = is_palindrome(word)
                self.assertEqual(result, expected,
                    msg=f"is_palindrome({word!r}) should be {expected}")

    def test_celsius_conversion(self):
        """Test multiple temperature conversions."""
        cases = [
            (0,    32.0),     # freezing point
            (100,  212.0),    # boiling point
            (-40,  -40.0),    # same in both scales
            (37,   98.6),     # body temperature
        ]
        for celsius, expected_f in cases:
            with self.subTest(celsius=celsius):
                result = celsius_to_fahrenheit(celsius)
                self.assertAlmostEqual(result, expected_f, places=1)


# ------------------------------------------------------------
# 10. ORGANIZING TESTS INTO A SUITE
# ------------------------------------------------------------

def make_suite():
    """Build a test suite from specific test cases."""
    suite = unittest.TestSuite()    # a collection of tests

    # Add specific test classes
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMathFunctions))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBankAccount))

    # Add a specific test method
    suite.addTest(TestDivide("test_divide_by_zero_raises"))

    return suite


# ------------------------------------------------------------
# 11. RUNNING TESTS
# ------------------------------------------------------------
# Ways to run tests:
#
# 1. Run this file directly:
#    python 01_unittest.py
#
# 2. Run with unittest discovery (finds all test_*.py files):
#    python -m unittest discover
#
# 3. Run a specific test class:
#    python -m unittest 01_unittest.TestBankAccount
#
# 4. Run a specific test method:
#    python -m unittest 01_unittest.TestBankAccount.test_deposit_increases_balance
#
# 5. Verbose output (shows test names):
#    python -m unittest -v 01_unittest
#
# Flags:
#   -v       verbose (shows each test name)
#   -f       fail fast (stop after first failure)
#   -k expr  only run tests matching expression

if __name__ == "__main__":
    # unittest.main() discovers and runs all TestCase classes in this file
    # verbosity=2 prints the name of each test as it runs
    unittest.main(verbosity=2)


# ============================================================
# SUMMARY
# ============================================================
# TestCase            → base class for all test classes (inherit from it)
# test_*              → any method starting with test_ is run as a test
# assertEqual(a, b)   → check a == b
# assertNotEqual      → check a != b
# assertTrue(x)       → check bool(x) is True
# assertFalse(x)      → check bool(x) is False
# assertIsNone(x)     → check x is None
# assertIn(a, b)      → check a in b
# assertIsInstance    → check isinstance(obj, type)
# assertRaises(Err)   → check exception is raised (use as context manager)
# assertAlmostEqual   → check floats are approximately equal
# assertGreater etc.  → comparison assertions
# assertListEqual etc.→ sequence assertions with diff output
# setUp()             → runs before EACH test (create fresh objects here)
# tearDown()          → runs after EACH test (cleanup here)
# setUpClass()        → runs once before ALL tests in class
# tearDownClass()     → runs once after ALL tests in class
# @skip               → skip a test
# @skipIf(cond)       → skip if condition is True
# @expectedFailure    → pass if test fails, fail if test passes
# subTest(label=val)  → test multiple inputs, report all failures
# ============================================================