def make_multiplier(factor):    # outer function — 'factor' lives here
    def multiply(n):            # inner function — 'factor' is remembered
        return n * factor       # uses 'factor' from the outer scope
    return multiply             # return the inner function

def test_closures():
    double = make_multiplier(2)     # factor=2 is "locked in" to double
    triple = make_multiplier(3)     # factor=3 is "locked in" to triple

    print(double(5))    # 10  →  5 * 2  (remembers factor=2)
    print(triple(5))    # 15  →  5 * 3  (remembers factor=3)
    print(double(9))    # 18  →  9 * 2

def read_numbers(numbers):
    """First stage: yield each number."""
    for n in numbers:
        yield n

def filter_evens(numbers):
    """Second stage: only pass through even numbers."""
    for n in numbers:
        if n % 2 == 0:      # only yield if even
            yield n

def square_them(numbers):
    """Third stage: square each number."""
    for n in numbers:
        yield n ** 2        # yield the square

    # Chain the stages — nothing runs until you iterate!
    raw      = read_numbers(range(20))      # stage 1
    evens    = filter_evens(raw)            # stage 2 — wraps stage 1
    squared  = square_them(evens)           # stage 3 — wraps stage 2

    # Only NOW does data flow through the pipeline, one item at a time
    result = list(squared)
    print(result)    # [0, 4, 16, 36, 64, 100, 144, 196, 256, 324]


if __name__ == "__main__":
    test_closures()
