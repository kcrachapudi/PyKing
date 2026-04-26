"""
4. Generators and yield
A generator is a special function that returns an iterator. 
Instead of using return to send back a value and end the function, 
it uses the yield keyword. 
yield: This keyword pauses the function and saves its state, 
returning a value to the caller. When the caller asks for the "next" value, 
the function resumes exactly where it left off.
Memory Efficiency: Generators use "lazy evaluation," 
meaning they produce values one at a time on demand instead of storing a huge list in 
memory.
Example: Creating an infinite sequence of numbers. 
"""
def count_up_to(max_val):
    count = 1
    while count <= max_val:
        yield count  # Pauses here and returns the current count
        count += 1

counter = count_up_to(3)
print(next(counter)) # 1
sleep(1)  # Simulating some delay
print(next(counter)) # 2
sleep(1)  # Simulating some delay
print(next(counter)) # 3
# next(counter) now would raise StopIteration





