'''
# IF we run this the printing statement will be : In the Decorator and then the body of the my_function which we dont want 
# as we are wrapping the gift without changing whats inside.

def my_decorator(function_passed):
    print('In the Decorator')
    return function_passed
'''

# Instead of Executing the function we return it so that it runs in the correct order

def my_decorator(function_passed):
    def wrapper():
        print('Something Before the Function')
        result = function_passed()
        print('Something After the function')
        return result
    return wrapper


# We will create a decorator ; Note the decorator must always be above the function which is being wrapped.
@my_decorator
def my_function():
    print('Hello Everyone') 
my_function()

print(f'\n {f'-'*147} \n')


## A wrapper doesnt know in most cases what it is wrapping so we use *args and **kwargs to store values

import time as t

def age_decorator(age_func):
    def age_wrapper(*args,**kwargs):

        time_start = t.time()

        result = age_func(*args,**kwargs)
    
        time_end = t.time()

        print(f'The time taken to for function execution is  : {time_end-time_start:.10f}')

        return result
    
    return age_wrapper


@age_decorator
def age_func(name,age):
    if age>100 or age<0 : print('You Do NOT Exist')
    print(f'{name} is Legal') if age>18 else print('You are a Minor')
    
age_func('Dave',17)