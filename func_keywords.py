'''
x = 20
def hello():
    x = 100
    print('Inside a Local Hello function')
    print(f'X is {x}')
hello()
print(f'In the global function x is {x}')
'''

x = 20
def hello():
    global x # This keywords changes the scope of it to be global and is used to make global changes
    x = 100
    print('Inside a Local Hello function')
    print(f'X is {x}')
hello()
print(f'In the global function x is {x}')

'''
The LEGB Rule
Python follows the LEGB rule when looking up variable names, and searches for them in this order:

Local - Inside the current function
Enclosing - Inside enclosing functions (from inner to outer)
Global - At the top level of the module
Built-in - In Python's built-in namespace

'''

x = "global"
def outer():
  x = "enclosing"
  def inner():
    x = "local"
    print("Inner:", x)
  inner()
  print("Outer:", x)

outer()
print("Global:", x)
