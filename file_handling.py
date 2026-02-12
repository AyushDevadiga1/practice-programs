file_path = 'dummy_text.txt'

'''

file_opened = open(file_path,'r')

print(file_opened.read())

print(f'_'*149)

# Alternatively we can use the with statement which can be used for better handling 
# as the reader/scanner is automatically closed here



with open(file_path,'r') as f:
    data = f.read()

print(data)

print(f'_'*149)

'''

'''



file_opened = open(file_path,'r')

print(file_opened.read(5)) # We can pass a parameter here which is the no of characters to read.

file_opened.close() # Good Practice is to close close the Reader


print(f'_'*149)



with open(file_path,'r') as f:
    print(f.readline()) # Reads a Single line if para passed 

file_opened.close() # Good Practice is to close close the Reader

print(f'_'*149)



with open(file_path,'r') as f:
    for x in f : # <-- This helps to loop each line
        print(x)
        print('-'*149)

file_opened.close() # Good Practice is to close close the Reader

'''

'''

To create a new file in Python, use the open() method, with one of the following parameters:

"x" - Create - will create a file, returns an error if the file exists

"a" - Append - will create a file if the specified file does not exists

"w" - Write - will create a file if the specified file does not exists

'''

'''

new_file = open('new_demo_file','x') 

print(f'_'*149)

print('Before Appending')

print(f'_'*149)

with open(file_path,'r') as f:
    print(f.read())

print(f'_'*149)

with open(file_path,'a') as f:
    f.write(' Something\'s in the way ... ')

print(f'_'*149)

print('After Appending')

print(f'_'*149)

with open(file_path,'r') as f:
    print(f.read())

print(f'_'*149)

'''

'''
# Now deleting files

import os

path_for_deletion = 'new_demo_file.txt'

if path_for_deletion:
    os.remove(path_for_deletion)
else:
    print('The path does not exists !!! ')
'''