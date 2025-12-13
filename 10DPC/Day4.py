"""
# Looping
for i in range(0,10):
    print(i)
    
list = ['a','b',5,6]

for i in list:
    print(i)
"""    
    
# Dictionary looping
d = {'name':'John', 'age':30}
for key in d:   
    print(key, d[key])
    
for key, value in d.items():
    print(key, value)

l1 = ["name", "age","Gender"]
l2 = ["John",30,"Male"]

for i in range(len(l1)):
    d[l1[i]] = l2[i]
print(d)
for key, value in zip(l1, l2):
    d[key] = value
print(d)