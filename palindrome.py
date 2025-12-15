number=1231321
string=str(number)
i=0
j=len(string)-1
for value in string:
    if i==j:
        print("The String is a Palindrome")
        break
    elif int(string[i]) == int(string[j]):
        print("---")
    else:
        print("Not Palindrome")
        break
    i+=1
    j-=1
    