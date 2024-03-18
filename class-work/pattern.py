i = 1
j = 1
print("Enter rows: ",end='')
rows = int(input())
for i in range(1, rows+1):
    for j in range(1, i+1):
        print(i,end='')
    print()