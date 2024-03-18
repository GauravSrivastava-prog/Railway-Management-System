print("Enter string : ")
str = (input())
print("Forward Order ->")
for i in str:
    print(i, end='')
print("\nReverse Order ->")
for i in str[::-1]:
    print(i, end='')

#without calculating length

len = 0
for i in str:
    len = len + 1
print("\nLength of the string",len)
print("Reverse Order ->")

while (len >= 0):
    print(str[len-1], end='')
    len = len - 1