'''
1. The Stack vs. The Heap
Standard Function: When called, it gets a "frame" on the Call Stack. Once the function hits return,
 that frame is "popped" (deleted) from the stack, and all its local variables are destroyed.
Generator: When you call a generator, it creates a Generator Object on the Heap (long-term memory). 
This object contains the function’s entire "execution context"—including its local variables, current instruction pointer, and the internal state of its loops. 


2. Suspension vs. Termination
The Pause: When a generator hits a yield statement, it doesn't exit; it suspends. 
The computer saves the exact "line number" and the values of every local variable into that Generator Object on the heap.
The Resume: When you call next(), the engine pulls that saved state back onto the stack and resumes execution from the exact millisecond it stopped. 

3. Ownership of Variables
In a regular function, the operating system/language runtime owns the variables and cleans them up immediately. 
In a generator, the Generator Object you hold in your code owns the variables. As long as you keep that generator object alive in your code,
the "background" state remains ready to resume

'''

'''
Generators are used in programming, particularly Python, to achieve lazy evaluation, 
which significantly reduces memory consumption by producing items one at a time on demand, rather than storing large datasets in memory at once. 
'''

'''
def my_generator():
  yield 1
  yield 2
  yield 3

for value in my_generator():
  print(value)

'''

def fibonacci():
  a, b = 0, 1
  while True:
    yield a
    a, b = b, a + b

# Get first 100 Fibonacci numbers
gen = fibonacci()
for _ in range(100):
  print(next(gen))


print(f'\n {f'-'*147} \n')

# List comprehension - creates a list
list_comp = [x * x for x in range(5)]
print(list_comp)

# Generator expression - creates a generator
gen_exp = (x * x for x in range(5)) # The Set operator is the one making the expression generator ; also note to convert it to list again as set is returned.
print(gen_exp)
print(list(gen_exp))

print(f'\n {f'-'*147} \n')

# The send method

def echo_generator():
  while True:
    received = yield
    print("Received:", received)

gen = echo_generator()
next(gen) # Prime the generator
gen.send("Hello")
gen.send("World")

print(f'\n {f'-'*147} \n')

# The close method

def my_gen():
  try:
    yield 1
    yield 2
    yield 3
  finally:
    print("Generator closed")

gen = my_gen()
print(next(gen)) 
gen.close() # <-- Closes the generator and the heap stack