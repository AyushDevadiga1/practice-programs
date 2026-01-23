import re
import numpy as np
import pandas as pd
pattern = r'>(\d)|(\d)|<(\d)'
text = '''
1 : 01-01-2015,
2 : 02-09-2007  
'''
text1='''
City  131,
city  382,
city  383
'''
text2='''
1,2,4,5,<1,>500,92,100,<1,>29,>23,<292,2929,2929,22,77
'''
matches = np.array(re.findall(pattern,text2))
print(matches)
print()
print("After Transformation")
print()
for i in matches:
    if i[1]=="":
        i[1]=0
        if i[2]=="":
            i[2]='inf'
        else:
            
            i[0]='inf'
    else:
        i[0]=0
        i[2]=0
print(matches)
print()  
df = pd.DataFrame((matches),columns=["start","absolute","end"])
print(df)