"""
3. Decorators
A decorator is a specific type of higher-order function that "wraps" 
another function to extend its behavior without changing its source code. 
Technically, most decorators are implemented using closures. 
Example: A simple logging decorator. 
"""
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello() 
# Output:
# Something is happening before...
# Hello!
# Something is happening after...

