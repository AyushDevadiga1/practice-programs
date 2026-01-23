import numpy as np
x=np.array([1.,2.,3.]) # Numpy mantains the original dtype so we cant just use int for calculating the unit vector
print(f'The original vector : {x}')
norm = 0
for i in range(len(x)):
    norm+=x[i]**2
norm=norm**(1/2)
print(f"The Magnitude  / norm of the vector is : {norm}")
print("The norm of the vector  by np.linalg.norm : ")
print(np.linalg.norm(x))
print("_"*60)
for i in range(len(x)):
    x[i]=float(x[i])/norm
print("The unit vector is :")
print(x)
user_magnitude = int(input(" Enter your desired magnitude for unit vector : \n"))
print(user_magnitude*x)