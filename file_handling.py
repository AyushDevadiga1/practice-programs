'''

file_path = 'dummy_text.txt'

file_opened = open(file_path,'r')

print(file_opened.read())

print(f'_'*149)

# Alternatively we can use the with statement which can be used for better handling 
# as the reader/scanner is automatically closed here

file_path = 'dummy_text.txt'

with open(file_path,'r') as f:
    data = f.read()

print(data)

print(f'_'*149)

'''

'''

file_path = 'dummy_text.txt'

file_opened = open(file_path,'r')

print(file_opened.read(5)) # We can pass a parameter here which is the no of characters to read.

file_opened.close() # Good Practice is to close close the Reader


print(f'_'*149)

file_path = 'dummy_text.txt'

with open(file_path,'r') as f:
    print(f.readline()) # Reads a Single line if para passed 

file_opened.close() # Good Practice is to close close the Reader

print(f'_'*149)

file_path = 'dummy_text.txt'

with open(file_path,'r') as f:
    for x in f : # <-- This helps to loop each line
        print(x)
        print('-'*149)

file_opened.close() # Good Practice is to close close the Reader

'''

