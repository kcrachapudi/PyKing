# ============================================================
#  CHAPTER 8 — TESTING WITH pytest
#  Your complete reference. Come back anytime.
# ============================================================
# The code being tested lives in GuineaTestPig.py
# Run tests with:  pytest 02_pytest.py -v

import pytest

# Import everything we want to test from GuineaTestPig.py
# All the functions and classes live there — we just test them here
from GuineaTestPig import (
    add,
    subtract,
    multiply,
    divide,
    is_palindrome,
    celsius_to_fahrenheit,
    BankAccount,
)


# ------------------------------------------------------------
# 1. WHAT IS pytest AND WHY USE IT?
# ------------------------------------------------------------
# pytest is the most popular Python testing framework.
# Install it first:  pip install pytest
#
# Why pytest over unittest?
#   unittest                      pytest
#   ─────────────────────────     ──────────────────────────
#   Must inherit TestCase         Plain functions, no class needed
#   self.assertEqual(a, b)        just write: assert a == b
#   Verbose setup                 Minimal boilerplate
#   Limited failure output        Rich detailed failure output
#   Fixtures are manual           Powerful built-in fixture system
#   No parametrize                @pytest.mark.parametrize built in
#
# How to run:
#   pytest                        run all test_*.py files
#   pytest -v                     verbose, show each test name
#   pytest -v -k "bank"           only tests whose name contains "bank"
#   pytest -v -x                  stop on first failure
#   pytest -v -s                  show print() output


# ------------------------------------------------------------
# 2. BASIC TESTS — just functions with assert
# ------------------------------------------------------------
# A test is a function whose name starts with test_
# Use plain 'assert' — no self.assertEqual() needed.
# pytest intercepts assert and shows exactly what went wrong.

def test_add_basic():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2
    assert add(-5, 10) == 5

def test_add_zero():
    assert add(0, 5) == 5
    assert add(5, 0) == 5

def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(0, 5)  == -5

def test_multiply():
    assert multiply(3, 4)   == 12
    assert multiply(0, 100) == 0
    assert multiply(-2, 5)  == -10

def test_divide_normal():
    assert divide(10, 2) == 5.0
    assert divide(9, 3)  == 3.0

def test_palindrome_true():
    assert is_palindrome("racecar")
    assert is_palindrome("level")
    assert is_palindrome("")                              # empty string
    assert is_palindrome("A man a plan a canal Panama")  # spaces and case ignored

def test_palindrome_false():
    assert not is_palindrome("hello")
    assert not is_palindrome("python")


# ------------------------------------------------------------
# 3. TESTING EXCEPTIONS WITH pytest.raises
# ------------------------------------------------------------
# Use pytest.raises() as a context manager to assert that
# specific code raises a specific exception.

def test_divide_by_zero():
    """Dividing by zero must raise ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)    # this line MUST raise ZeroDivisionError

def test_divide_by_zero_message():
    """Also verify the exception message."""
    with pytest.raises(ZeroDivisionError) as exc_info:
        divide(10, 0)
    # exc_info.value holds the actual exception object
    assert "zero" in str(exc_info.value).lower()

def test_deposit_zero_raises():
    account = BankAccount("Alice", 100)
    # match= checks the exception message against a regex pattern
    with pytest.raises(ValueError, match="positive"):
        account.deposit(0)

def test_withdraw_overdraft():
    account = BankAccount("Bob", 50)
    with pytest.raises(ValueError, match="Insufficient"):
        account.withdraw(100)    # only $50 in account


# ------------------------------------------------------------
# 4. FIXTURES — reusable setup and teardown
# ------------------------------------------------------------
# A fixture is a function decorated with @pytest.fixture.
# Tests REQUEST a fixture by including its name as a parameter.
# pytest automatically calls the fixture and injects the result.
#
# Replaces setUp() from unittest — but much more powerful:
#   → Shared across multiple test files via conftest.py
#   → Different scopes (function, class, module, session)
#   → yield gives you setup AND teardown in one place

@pytest.fixture
def bank_account():
    """Fresh BankAccount with $1000 — created before EACH test that requests it."""
    account = BankAccount("Alice", balance=1000)    # SETUP: create the account
    yield account       # give account to the test — the test body runs here
                        # TEARDOWN: anything after yield runs after the test
                        # (close files, DB connections, delete temp data, etc.)

@pytest.fixture
def empty_account():
    """A bank account starting at zero balance."""
    return BankAccount("Bob", balance=0)    # simple fixture, no teardown needed

# Tests request fixtures by matching parameter name exactly
def test_deposit(bank_account):            # pytest sees 'bank_account', calls the fixture
    bank_account.deposit(500)
    assert bank_account.balance == 1500    # started at $1000, deposited $500

def test_withdraw(bank_account):           # gets its OWN FRESH account — not shared with above
    bank_account.withdraw(300)
    assert bank_account.balance == 700     # started at $1000, withdrew $300

def test_withdraw_from_empty(empty_account):
    with pytest.raises(ValueError):
        empty_account.withdraw(1)          # can't withdraw from $0 balance


# ------------------------------------------------------------
# 5. FIXTURE SCOPE — control how often a fixture runs
# ------------------------------------------------------------
# scope="function" → default, fresh fixture for EVERY single test
# scope="class"    → one fixture for all tests in a class
# scope="module"   → one fixture for all tests in this file
# scope="session"  → one fixture for the entire test run (all files)
# Use wider scope for expensive setup like DB connections.

@pytest.fixture(scope="module")    # runs ONCE for this whole file, not once per test
def shared_data():
    """Expensive setup — loaded once, shared by all tests in this file."""
    print("\n[module fixture] Loading large dataset once...")
    data = {"records": list(range(1000)), "config": {"env": "test"}}
    yield data
    print("\n[module fixture] Tearing down dataset...")

def test_data_length(shared_data):
    assert len(shared_data["records"]) == 1000

def test_data_config(shared_data):
    assert shared_data["config"]["env"] == "test"    # same object — not recreated


# ------------------------------------------------------------
# 6. FIXTURE DEPENDENCIES — fixtures using other fixtures
# ------------------------------------------------------------

@pytest.fixture
def funded_account(bank_account):    # request bank_account fixture as a dependency
    """A well-funded account — builds on top of bank_account fixture."""
    bank_account.deposit(4000)       # add $4000 to the $1000 already in bank_account
    return bank_account              # now has $5000 total

def test_large_withdrawal(funded_account):
    funded_account.withdraw(4500)
    assert funded_account.balance == 500


# ------------------------------------------------------------
# 7. PARAMETRIZE — run one test with many inputs
# ------------------------------------------------------------
# @pytest.mark.parametrize runs the SAME test function multiple
# times with different data. Each row is a SEPARATE test result.

@pytest.mark.parametrize("a, b, expected", [
    # (input_a, input_b, expected_output)
    (1,    2,   3),      # test case 1
    (0,    0,   0),      # test case 2
    (-1,   1,   0),      # test case 3
    (100, -50,  50),     # test case 4
])
def test_add_parametrized(a, b, expected):
    """Runs 4 times — once per row above. Each is a separate test."""
    assert add(a, b) == expected

@pytest.mark.parametrize("text, expected", [
    ("racecar",                     True),
    ("hello",                       False),
    ("level",                       True),
    ("python",                      False),
    ("",                            True),
    ("A man a plan a canal Panama", True),
])
def test_palindrome_parametrized(text, expected):
    """6 separate test cases — all failures reported independently."""
    assert is_palindrome(text) == expected

@pytest.mark.parametrize("celsius, fahrenheit", [
    (0,   32.0),
    (100, 212.0),
    (-40, -40.0),
    (37,  98.6),
])
def test_celsius_parametrized(celsius, fahrenheit):
    result = celsius_to_fahrenheit(celsius)
    assert result == pytest.approx(fahrenheit, abs=0.1)    # within 0.1 degree


# ------------------------------------------------------------
# 8. MARKS — categorize and control tests
# ------------------------------------------------------------

@pytest.mark.skip(reason="Feature not implemented yet")    # always skip
def test_future_feature():
    assert False

import sys
@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")   # skip on Windows
def test_unix_only():
    assert True

@pytest.mark.xfail(reason="Known float precision issue")   # expected to fail
def test_known_bug():
    assert 0.1 + 0.2 == 0.3    # will fail — float precision — that's expected

@pytest.mark.slow                      # custom mark — run with: pytest -m slow
def test_slow_operation():
    import time; time.sleep(0.01)
    assert True


# ------------------------------------------------------------
# 9. MONKEYPATCHING — replace functions/attributes temporarily
# ------------------------------------------------------------
# monkeypatch is a built-in fixture that replaces functions,
# attributes, or env vars — original is restored after each test.

import random

def get_lucky_number():
    return random.randint(1, 100)    # we want to control this in tests

def test_monkeypatch_function(monkeypatch):
    """Replace random.randint with a fixed value for deterministic tests."""
    monkeypatch.setattr(random, "randint", lambda a, b: 42)
    # Now random.randint ALWAYS returns 42 — no real randomness in test
    assert get_lucky_number() == 42
    # After test: random.randint is automatically restored to the real version

def test_monkeypatch_env_var(monkeypatch):
    """Set an environment variable just for the duration of this test."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    import os
    assert os.environ["DATABASE_URL"] == "sqlite:///:memory:"
    # After test: env var automatically removed


# ------------------------------------------------------------
# 10. CAPTURING OUTPUT
# ------------------------------------------------------------

def greet_user(name):
    print(f"Hello, {name}!")
    print(f"Welcome to Python King!")

def test_output(capsys):
    """capsys is a built-in fixture — captures everything printed to stdout."""
    greet_user("Alice")
    captured = capsys.readouterr()     # captured.out = stdout, captured.err = stderr
    assert "Hello, Alice!" in captured.out
    assert "Welcome" in captured.out


# ------------------------------------------------------------
# 11. tmp_path — temporary files
# ------------------------------------------------------------
# Built-in fixture — gives a real temp directory, auto-deleted after test.

def save_to_file(data, filepath):
    with open(filepath, "w") as f:
        f.write(data)

def load_from_file(filepath):
    with open(filepath, "r") as f:
        return f.read()

def test_file_operations(tmp_path):
    file = tmp_path / "test.txt"           # pathlib.Path inside the temp dir
    save_to_file("Hello, World!", file)
    result = load_from_file(file)
    assert result == "Hello, World!"
    # temp directory deleted automatically after this test


# ------------------------------------------------------------
# 12. pytest.approx — clean float comparisons
# ------------------------------------------------------------

def test_float_approx():
    assert 0.1 + 0.2    == pytest.approx(0.3)               # default tolerance
    assert 0.1 + 0.2    == pytest.approx(0.3, rel=1e-6)     # relative tolerance
    assert [0.1, 0.2]   == pytest.approx([0.1, 0.2])        # works on lists
    assert {"a": 0.1+0.2} == pytest.approx({"a": 0.3})      # works on dicts


# ------------------------------------------------------------
# 13. GROUPING TESTS IN A CLASS
# ------------------------------------------------------------

class TestBankAccount:
    """Group related tests in a class — no TestCase inheritance needed."""

    @pytest.fixture(autouse=True)       # autouse=True: applies to ALL methods in class
    def setup(self):                    # without needing to name it as a parameter
        self.account = BankAccount("Alice", 1000)    # fresh account before each test

    def test_initial_balance(self):
        assert self.account.balance == 1000

    def test_owner(self):
        assert self.account.owner == "Alice"

    def test_deposit(self):
        self.account.deposit(500)
        assert self.account.balance == 1500

    def test_withdraw(self):
        self.account.withdraw(400)
        assert self.account.balance == 600

    def test_multiple_operations(self):
        self.account.deposit(500)      # 1000 + 500 = 1500
        self.account.withdraw(200)     # 1500 - 200 = 1300
        self.account.deposit(100)      # 1300 + 100 = 1400
        assert self.account.balance == 1400

    @pytest.mark.parametrize("amount", [-100, 0, -1])
    def test_invalid_deposit(self, amount):
        with pytest.raises(ValueError):
            self.account.deposit(amount)    # all three amounts should raise


# ============================================================
# SUMMARY
# ============================================================
# Install              → pip install pytest
# Run all              → pytest
# Run verbose          → pytest -v
# Show prints          → pytest -s
# Run matching name    → pytest -k "bank"
# Stop on failure      → pytest -x
#
# Import source        → from GuineaTestPig import add, BankAccount
# Test function        → def test_*(): plain assert
# pytest.raises()      → assert exception is raised
# @pytest.fixture      → reusable setup/teardown, injected by name
# yield in fixture     → before = setup, after = teardown
# scope=               → "function" "class" "module" "session"
# autouse=True         → apply fixture without naming it in params
# @parametrize         → run same test with many inputs
# @mark.skip           → always skip
# @mark.skipif(cond)   → skip if condition is True
# @mark.xfail          → expected to fail
# monkeypatch          → replace functions/attrs/env vars temporarily
# capsys               → capture stdout/stderr
# tmp_path             → auto-cleaned temporary directory
# pytest.approx()      → float comparison with tolerance
# conftest.py          → share fixtures across ALL test files
# ============================================================