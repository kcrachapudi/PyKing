
from collections import namedtuple
from sqlite3 import Row


def exec1():
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    print(nums[2:5])      # [2, 3, 4]        start=2, stop=5
    print(nums[:4])       # [0, 1, 2, 3]     from beginning to 4
    print(nums[6:])       # [6, 7, 8, 9]     from 6 to end
    print(nums[:])        # full copy        entire list
    print(nums[::2])      # [0, 2, 4, 6, 8]  every other item
    print(nums[1::2])     # [1, 3, 5, 7, 9]  odd indices
    print(nums[::-1])     # [9,8,7,6,5,4,3,2,1,0]  reversed
    print(nums[7:2:-1])   # [7, 6, 5, 4, 3]  reverse slice


def exec2():
    numz = [0, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    print(numz[2:5])      
    print(numz[:4])       
    print(numz[6:])       
    print(numz[:])        
    print(numz[::2])      
    print(numz[1::2])     
    print(numz[::-1])     
    print(numz[7:2:-1])   


def exec3():
    fruits = ["apple", "banana", "cherry", "banana", "date"]
    fruits.remove("banana")
    print(fruits)


def exec4():
    grid = {}
    grid[(0, 0)] = "start"
    grid[(3, 4)] = "checkpoint"
    grid[(9, 9)] = "end"
    print(grid[(3, 4)])    


def exec5():
    Row = namedtuple("Row", ["id", "name", "score"])
    rows = [
        Row(1, "Alice", 92),
        Row(2, "Bob", 85),
        Row(3, "Charlie", 95),
    ]

    for row in rows:
        print(f"{row.name}: {row.score}")


def exec6():
    # Pattern 2: Iterate list of tuples
    students = [("Alice", 92), ("Bob", 85), ("Charlie", 95)]
    for name, score in students:        # tuple unpacking in for loop
        print(f"{name}: {score}")

    for name in students:        # tuple unpacking in for loop
        print(f"{name}: {score}")


def exec7():
    fruits = {"apple", "banana"}

    # add() — add one item
    fruits.add("cherry")
    print(fruits)    # {'apple', 'banana', 'cherry'}

    # add() is safe — adding a duplicate does nothing
    fruits.add("apple")
    print(fruits)    # still {'apple', 'banana', 'cherry'}

    # update() — add multiple items from any iterable
    fruits.update(["date", "elderberry"])
    fruits.update({"fig", "grape"})
    fruits.update(("honeydew", "kiwi"))
    print(fruits)

    # remove() — raises KeyError if item not found
    fruits.remove("banana")
    # fruits.remove("mango")   ← KeyError!

    # discard() — safe remove, no error if not found  ✅ prefer this
    fruits.discard("mango")    # no error
    fruits.discard("apple")    # removes it silently
    print(fruits)

    # pop() — removes and returns an ARBITRARY item (unpredictable)
    item = fruits.pop()
    print(f"Removed: {item}")

def itertools():
    # --- itertools — powerful iteration tools ---
    import itertools

    # chain — combine multiple iterables
    combined = list(itertools.chain([1,2,3], [4,5,6], [7,8]))
    print(combined)    # [1,2,3,4,5,6,7,8]

    # combinations — unique combinations
    print(list(itertools.combinations([1,2,3,4], 2)))
    # [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]

    # permutations
    print(list(itertools.permutations([1,2,3], 2)))

    # product — cartesian product
    print(list(itertools.product([0,1], repeat=3)))
    # all 3-bit binary numbers

    # groupby — group consecutive items
    data = [("A",1),("A",2),("B",3),("B",4),("C",5)]
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        print(key, list(group))

    # islice — lazy slice of any iterator
    first5 = list(itertools.islice(itertools.count(0), 5))
    print(first5)    # [0, 1, 2, 3, 4]


if __name__ == "__main__":
    print(f'name is {__name__}')
    itertools()
else:
    print(f'This is from module playground. Running externally as {__name__} imported')