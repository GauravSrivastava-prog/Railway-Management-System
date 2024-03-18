print("Enter range: ")
n = int(input())
for i in range(n, 0, -1):
    for k in range(n, i, -1):
        print(" ",end='')
    for j in range(1, i+1, 1):
        print("*",end='')
    print()