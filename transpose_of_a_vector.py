# To make a transpose of a given vector
import numpy as np
x=np.array([[1.,2.,3.]]) # Numpy mantains the original dtype so we cant just use int for calculating the unit vector
print(f'The original vector : {x}')
print(f"The original shape : ")
print(x.shape)
def row_to_column_vector(x):
    ncv=np.zeros(shape=(x.shape[1],x.shape[0]))
    for i in range (x.shape[1]):
        #    print(ncv[i][0])
            ncv[i][0] = x[0][i]
        #    print(ncv[i][0])
    return ncv
print(f'The transposed vector : {x}')
transposed_vector = (row_to_column_vector(x))
print(transposed_vector)
print(f"The new vector shape : ")
print(transposed_vector.shape)