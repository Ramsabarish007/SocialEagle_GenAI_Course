# function
def add(a,b):
    return a + b    

print(add(3,5))
print(add("Hello ","World"))
print(add([1,2,3],[4,5,6]))

def greet(name, msg="Good Morning"):
    return f"{msg}, {name}!"
print(greet("Alice"))
print(greet("Bob", "Hello"))