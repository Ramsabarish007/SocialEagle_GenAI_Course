task = ["eat","code","sleep"]

print(task)

task.append("repeat")
print(task)

for i in task:
    print(i)
    if i == "code":
        print("I love coding!")
    else:
        print("Just another task.")

task.remove("code")
print(task)

task.sort()
print(task)

task.reverse()
print(task)

task.extend(["exercise","read"])
print(task)

task.insert(2,"meditate")
print(task)

task.pop()
print(task)

sleep = task.index("sleep")
print(sleep)

eat = task.count("eat")
print(eat)

task2 = task.copy()
print(task2)

task.clear()
print(task)
print(task2)