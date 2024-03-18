#OPERATORS---->
x=15
y=(float)(x) #type-casting
print(x)
print(y)
print(type(y)) #type of data
print(bool("hello")) #Non-Zero values return "True"
print(bool(1)) 
print(bool(" "))
print(bool(0)) #Zero returns "False"
print(10 > 9)
str1 = "Hello"
str2 = "Hello"
if str1 in str2: #compare two strings ..... it is case-sensitive.
    print("True")
else:
    print("False")
if (type(str1) is str): #checks type of variables.
    print("String")
print("It is equal") if ("Hello" in str1) else print("It is not same") #One-line if-else...
