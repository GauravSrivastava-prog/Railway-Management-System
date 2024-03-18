print("Enter name : ")
str = input()
l = str.split(" ")
name = ""
res = ""
for i in range(len(l) - 1):
    name = l[i]
    res = res + name[0].upper() + " "
res = res + l[-1].title()
print(res)
