profile = {"name":"ram","age":31,"city":"Chennai"}

print(profile["age"])

profile["Skill"] = "AI"
print(profile)

profile["age"] += 32
print(profile)

profile2 = {"name":"sita","age":28,"city":"Bangalore"}

profile.update(profile2)
print(profile)

profile = {"name":"ram","age":31,"city":"Chennai"}
profile2 = {"name":"sita","age":28,"city":"Bangalore"}

# Merge using dictionary unpacking
merged_profile = {**profile, **profile2}
print("merged dict :",merged_profile)

del profile["city"]
print(profile)


profile = {"name":"ram","age":31,"city":"Chennai"}
profile2 = {"name":"sita","age":28,"city":"Bangalore"}

# Merge using a for loop
for key, value in profile2.items():
    profile[key] = value

print("Merged dict using for loop:", profile)

# Merge using a for loop
for key, value in profile.items():
    profile2[key] = value

print("Merged dict using for loop:", profile2)

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

merged_dict = {**dict1, **dict2}
print(merged_dict)

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

merged_dict = dict1.copy()
merged_dict.update(dict2)
print(merged_dict)