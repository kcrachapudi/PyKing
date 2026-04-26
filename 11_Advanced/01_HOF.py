"""
1. Higher-Order Functions (HOFs)
A higher-order function is any function that either takes a function as an argument 
or returns a function as its result. In Python, functions are "first-class objects," 
meaning you can treat them like variables. 
Example: Using map() to apply a function to every item in a list. 
"""
def square(x):
    return x * x

numbers = [1, 2, 3, 4]
# map is a higher-order function because it takes 'square' as an argument
squared_numbers = map(square, numbers)
print(list(squared_numbers))  # Output: [1, 4, 9, 16]

