import numpy as np
x = np.array([[1,2,3]])
y = np.array([[1],[2],[3]])
dot_product_1 = 0
dot_product_2 = 0
for i in range(x.shape[1]):
    dot_product_1 += x[0][i]*y[i][0]
    dot_product_2 += y[i][0]*x[0][i]
    #print(x[0][i])
    #print(y[i][0])
if dot_product_1 == dot_product_2: print(" Identity is true")