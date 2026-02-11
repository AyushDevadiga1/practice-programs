def travel(car,color):
    print(f'The {color} colored {car} goes vroom !!!.')

travel(car='Mistubishi',color='red') # Key value paired Arguments
travel('red','Mitsubishi') # <-- Positional Arguments
travel('Mitsubishi',color='red') # <-- Mixed Arguments 
# Here we always make sure the positional defalut arguments is first same case for the parameters in the above functions

# Args and Kwargs

def classroom(*students):
    print(f'{students[0]} is the oldest student') 
    print(f'{students[1]} is the 2nd oldest student') 


names = ['Devon','Dante']
names_t = ('Devon','Dante')

classroom('Devon','Dante') # <== If u try using names we will have an error cause only a tuple is accepted here that too directly

def play(sport,*player):
    for i in range(len(player)):
        print(f'Sport:{sport}\tPlayer:{player[i]}')

play('Cricket','Gayle','ABD','Sangakara') # When dealing with multiple types of arguments