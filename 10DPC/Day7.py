skill = {"python","git","Python","docker"}
print(skill)

required_skill = {"python","sql","aws"}
print(required_skill)   

common_skill = skill.intersection(required_skill)
print("Common Skills:",common_skill)

skill = {"python","git","Python","docker"}
print(skill)

required_skill = {"python","sql","aws"}
print(required_skill)  

common_skill = skill & required_skill
print("Common Skills:",common_skill)

common_skill = skill | required_skill
print("All Skills:",common_skill)

frozen = frozenset(skill)
print(frozen)

s = set()
d = {}
c = 0
for i in frozen:
    s.add(i)
    c +=1 
    n = "skill"+str(c)
    d[n] = i
print(s)
print(d)