import math

# Basic functions
def add(a, b):
    return a + b    

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

# Scientific functions
def power(a, b):
    return math.pow(a, b)

def square_root(a):
    if a < 0:
        return "Cannot take square root of negative number"
    return math.sqrt(a)

def sine(x):
    return math.sin(math.radians(x))

def cosine(x):
    return math.cos(math.radians(x))

def tangent(x):
    return math.tan(math.radians(x))

# Example usage
print(add(3, 5))
print(add("Hello ", "World"))
print(add([1, 2, 3], [4, 5, 6]))

print(subtract(10, 4))
print(multiply(6, 7))
print(divide(20, 4))

print("Power:", power(2, 3))
print("Square root:", square_root(16))
print("Sine 30°:", sine(30))
print("Cosine 60°:", cosine(60))
print("Tangent 45°:", tangent(45))