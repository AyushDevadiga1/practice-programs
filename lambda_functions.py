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