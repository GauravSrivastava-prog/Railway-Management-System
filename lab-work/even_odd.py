print("Enter number")
x = int(input())
if (x % 2 == 0):
    print("Even")
else:
    print("Odd")
for i in range(2, int(x/2) + 1):
    if (x % i == 0):
        print("Not Prime")
        break
else:                #python has a special property where we can use else with for.... if for loop ache se chal ke exhaust ho gya toh woh else mai jayega... nahi toh nahi jayega
    print("Prime")
