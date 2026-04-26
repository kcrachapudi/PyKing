"""
2. Closures
A closure occurs when a nested function "remembers" variables from its 
parent function’s scope even after the parent function has finished executing.
 It "closes over" those variables to keep them alive. 
Example: A function factory that remembers a specific "multiplier". 
"""
def make_multiplier(n):
    def multiplier(x):
        return x * n  # 'n' is remembered from the outer scope
    return multiplier

double = make_multiplier(2)
print(double(5))  # Output: 10 (remembers n=2)

