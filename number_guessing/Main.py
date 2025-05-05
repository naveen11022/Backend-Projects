import random
print("""Welcome to the Number Guessing Game!""")
print("Please select the difficulty level:\n1. Easy (10 chances)\n2. Medium (5 chances)\n3. Hard (3 chances)")
user_choice = int(input("Enter the choice:"))
def func(num):
    for i in range(num):
        output = int(input("Enter the number:\t"))
        number = random.randrange(0,100)
        if number == output:
            return("Correct!!!")
            
    return("Better luck next time!!!")
    
if user_choice == 1:
    func(10)

elif user_choice == 2:
   func(5)
else:
    func(3)

