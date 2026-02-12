
# Self is just an instance reference to the current object we are pointing to ; used to seperate an object from other .
class Animal:
    def __init__(myAnimal,type,blood):
        myAnimal.type = type
        myAnimal.blood = blood
    def __str__(myAnimal):
        return f'This Animal is a {myAnimal.blood} {myAnimal.type}'
    
animal1 = Animal('mammal','homiothermic')
print(animal1)

animal1.age = 18
print(animal1.age)

del animal1.blood # Used to delete the attribute

print(f'_-'*149)
