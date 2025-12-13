# score = int(input("Enter your score: "))
# if score > 100:
#     print("Invalid score")
# elif score >= 90:
#     print("Your grade is A+")
# elif score >= 80:
#     print("Your grade is B")    
# elif score >= 70:
#     print("Your grade is C")
# else:
#     print("Your grade is Fail")   
    
age = int(input("Enter your age: "))

if age>=18:
    Pro = input("Enter your sub plan (Basic/Premium): ")
    if Pro=="Basic":
        print("you have basic access granted")
    elif Pro=="Premium":
        print("You have premium access granted")
    else:
        print("Invalid sub plan")
else:
    print("Access denied due to age restriction")
 
# Ternanry operator   
Status = "Adult" if age>=18 else "Minor"
print("You are an", Status)