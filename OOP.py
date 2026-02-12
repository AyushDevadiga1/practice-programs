'''
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

'''

'''
#                                   Inheritance

# PARENT
class Person:
    def __init__(self,name,age,height,weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
    
    def introduction(self):
        print(f'My name is {self.name} and I am {self.age} years old.')

person1 = Person('Austin',18,6.4,120)
person1.introduction()

print(f'_'*149)

# Now we will create a student function which inherit the properties of a Person

#CHILD
class Student(Person):
    pass

student1 = Student('Tu',19,7.3,135)
# Student 1 inherited the properties of the Person
student1.introduction()

print(f'_'*149)

# Now instead of this we will make such changes that the Student not only inherits but also adds Its own properties

class Student(Person):
    def __init__(self, name, age, height, weight,student_id,branch):
        super().__init__(name, age, height, weight)
        self.student_id = student_id
        self.branch = branch
    
    def student_information(self):
        print(f'I am {self.name} and I specialize in {self.branch} branch .')


student2 = Student('Ann',26,5.8,56,'A101','AIML')
student2.student_information()

print(f'_'*149)


'''


