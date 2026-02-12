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

file_path = 'dummy_text.txt'

file_opened = open(file_path,'r')

print(file_opened.read())

# Good Practice is to close close the Reader

file_opened.close()