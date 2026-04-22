from functools import reduce
#You have a list of tuples representing students and their grades:
#Write a sorted() function using a lambda as the key that sorts the students primarily by grade 
# (highest to lowest), and secondarily by name (alphabetically) if the grades are tied.
#students = [("Alice", 88), ("Bob", 95), ("Charlie", 88), ("David", 92)]
#sorted_students = sorted(students, lambda s: )


#Write a lambda function called check_val that takes a number x.
#If x is greater than 10, return "High".
#If x is between 5 and 10 (inclusive), return "Medium". Otherwise, return "Low".
#Constraint: You must do this in a single lambda line using nested ternary operators.
check_val = lambda x: "High" if x>10 else "Medium" if 5<=x<=10 else "Low"
print(check_val(4))

#Question 4: Dictionary Mapping
#Given a list of dictionaries:
data = [{"id": 1, "val": 10}, {"id": 2, "val": 20}, {"id": 3, "val": 30}]
#Use the map() function and a lambda to return a list of just the "val" numbers, 
# but multiply each value by 2 only if the "id" is an odd number.
#new_data = list(map(lambda x: list(x.items())[1]*2 if list(x.items())[0]%2==0 else list(x.items())[1], data))
#print(new_data)
#Question 5: The "Self-Executing" Challenge
#Write a single line of code using a lambda that calculates the factorial of 5 
# without using the math module or defining a standard def function.
#Hint: You’ll need to pass the lambda into itself or use a functional tool like reduce.
#Take your time—I'm ready when you are! Which one do you want to tackle first?

print(list(range(5, 0, -1)))
factorial = reduce(lambda x, y: x*y, list(range(5, 1, -1)))
print(factorial)
