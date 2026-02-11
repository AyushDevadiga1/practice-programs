import cowsay
def load_file(x):
    if not type(x) is bool:
        raise TypeError('Invalid Datatype passed . \n Please pass boolean value.')
    else:
        if x:
            try :
                filepath = 'test\\hello1.txt'
                with open(filepath,'r') as file:
                    data = file.read()
                    print(data)
            except Exception as e:
                print(f'An exception occured : {e}')
            finally:
                cowsay.cow('The file was loaded successfully')
        else:
            print('You dont want to load the FILE!!!')
load_file(True)

