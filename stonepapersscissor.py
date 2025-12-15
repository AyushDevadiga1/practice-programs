import random
l1=("stone","paper","scissor ")
r1=random.choice(l1)
print(f"Random choice {r1} ")
random.shuffle(l1)
print(f"Random Shuffle {l1} ")
guess=input("Enter a choice from STONE | PAPER | SCISSOR ").lower()
if guess.isalpha() or guess.isdigit() :
   print("Invalid Input") 
   guess=input("Enter a choice from STONE | PAPER | SCISSOR ").lower()
else :
  print(guess)  
