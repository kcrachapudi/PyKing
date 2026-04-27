

def read_numbers(numbers):
    """First stage: yield each number."""
    for n in numbers:
        print(f"Reading number: {n}")
        yield n

def filter_evens(gen_nums):
    """Second stage: only pass through even numbers."""
    for n in gen_nums:
        print(f"Filtering {n}...")
        if n % 2 == 0:      # only yield if even
            yield n

def square_them(gen_filters):
    """Third stage: square each number."""
    for n in gen_filters:
        print(f"Squaring {n} to get {n**2}")
        yield n ** 2        # yield the square


if __name__ == "__main__":
    # Chain the stages — nothing runs until you iterate!
    gen_nums      = read_numbers(range(100))      # stage 1
    gen_filters    = filter_evens(gen_nums=gen_nums)            # stage 2 — wraps stage 1
    gen_squared  = square_them(gen_filters=gen_filters)           # stage 3 — wraps stage 2

    print(type(gen_nums))      # <generator object read_numbers at 0x...>
    print(type(gen_filters))    # <generator object filter_evens at 0x...>
    print(type(gen_squared))  # <generator object square_them at 0x...

    for result in gen_squared:
        print(result)