def travel(car,color):
    print(f'The {color} colored {car} goes vroom !!!.')

travel(car='Mistubishi',color='red') # Key value paired Arguments
travel('red','Mitsubishi') # <-- Positional Arguments
travel('Mitsubishi',color='red') # <-- Mixed Arguments 
# Here we always make sure the positional defalut arguments is first same case for the parameters in the above functions

print(f'\n {f'-'*147} \n')

# Args and Kwargs

def classroom(*students):
    print(f'{students[0]} is the oldest student') 
    print(f'{students[1]} is the 2nd oldest student') 


names = ['Devon','Dante']
names_t = ('Devon','Dante')

classroom('Devon','Dante') # <== If u try using names we will have an error cause only a tuple is accepted here that too directly

print(f'\n {f'-'*147} \n')

def play(sport,*player):
    for i in range(len(player)):
        print(f'Sport:{sport}\tPlayer:{player[i]}')

play('Cricket','Gayle','ABD','Sangakara') # When dealing with multiple types of arguments

print(f'\n {f'-'*147} \n')

# When we dont know how many variables are needed to be accessed we use kwargs

def race(**info):
    for key,value in info.items():
        print(f'{key}:{value}')
race(name='Akame',age=21,side='Revolutionary Army',relic='Murasame')

print(f'\n {f'-'*147} \n')

## Now using args and kwargs to unpack variables

# Lets take the above example which was not possible now done


def classroom(*students):
    print(f'{students[0]} is the oldest student') 
    print(f'{students[1]} is the 2nd oldest student') 


names = ['Devon','Dante']

classroom(*names) # we use * to unpack 1D dtypes

print(f'\n {f'-'*147} \n')

# Now using a dict 

def cars(a,a_color,b,b_color):
    print(f'{a_color} colored {a}')
    print(f'{b_color} colored {b}')

cars_obj = {
                'a' : 'toyota',
                'b' : 'hayabusa',
                'a_color' : 'blue',
                'b_color' : 'white',
}
cars(**cars_obj)

print(f'\n {f'-'*147} \n')

# We see here both packing and unpacking of the variables .

def key_value(**dict1):
    for key,value in dict1.items():
        print(f'key = {key} | \tvalue = {value}')
objects_dict = {
                    'name' : ['Pichu','Pikachu','Raichu'],
                    'stage' : [1,2,3]
}

key_value(**objects_dict)