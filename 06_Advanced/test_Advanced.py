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

if __name__ == "__main__":
    test_closures()