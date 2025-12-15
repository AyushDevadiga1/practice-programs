import random 
r1=random.randint(1,10)
guess=input("Enter a guessing number in between 1 and 10 ")
while guess != r1:
    Bool1=guess.isdigit()
    if Bool1:
        guess=int(guess)
        if guess> 10 or guess<1:
            print("Invalid number range ")
            guess=input("Enter a guessing number in between 1 and 10 ")
        elif guess>r1:
            print("Your guess is too high ")
            guess=input("Enter a guessing number in between 1 and 10 ")
        elif guess<r1:
            print("Your guess is too low ")
            guess=input("Enter a guessing number in between 1 and 10 ")
        else :
            print("Your guess is absolutely right ") 
            print(f" Random No : {r1} = Guess : {guess} ")
            break       
    else :
        print("INVALID INPUT DATATYPE ")
        guess=input("Enter a guessing number in between 1 and 10 ")
