# The Anonimousness makes this lambda function powerful.
# SEE below the user is just passing the values to squared and cubes and 
# doesnt really know that there is a function beneath which is actually doing the lifting.

def func_power(n):
    return lambda x : x**n
squared = func_power(2)
cubed = func_power(3)
print(squared(5))
print(cubed(5))

print(f'\n{f'-'*188}\n')

# Multiargument
y = lambda x,y,z : x*y*z
print(f'The product of three values using lambda function : {y(5.62,5,25)}')

print(f'\n{f'-'*188}\n')

# Now lets try using a list of values and passing it to lambda
# here we would need a special keywords map to make sure the logic is distributed

title_words = ['DAN','DA','DAN']
print(f'The old title : {title_words}')
# Map takes two arguments so we have to pass it while using the lambda function and for each loop we join with "" (nothing) so we get a concatenated string
new_title = "".join(map(lambda x : x.capitalize(),title_words))
print(new_title)

print(f'\n{f'-'*188}\n')

# Like map filter also takes the list as well as the func as parameter
numbers = [1,2,3,4,4,5,6,67,7,7,8,9,3]
even_numbers = list(filter(lambda x : x%2 ==0 , numbers)) # Note here we can also use other dtypes other than list
odd_numbers = [ x for x in numbers if x not in even_numbers ]
print(f'The numbers list : {numbers} \n Odd numbers  : {odd_numbers} \n Even numbers : {even_numbers}')


# Now lets also see how we can use this ins sorting
students = [    
                ('Austin',17) , ('Chris',18) , ('Jeff',17)
]
print(f'The actual list : {students}')

sorted_students_by_name = sorted(students,key = lambda x: x[0]) # Sorted takes two params : The iterable and the key = logical function
sorted_students_by_age = sorted(students,key = lambda x: x[1])

print(f'Sorted the students by name \n {sorted_students_by_name}')
print(f'Sorted the students by age \n {sorted_students_by_age}')

print(f'\n{f'-'*188}\n')

# Now lets see another function

fruits = ['Orange','Kiwi','Mango','Apple']
sorted_by_length = sorted(fruits,key=lambda x : len(x))
print(f'Sorted the fruits by length \n {sorted_by_length}')