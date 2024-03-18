print("Enter a number")
n = int(input())
if (n % 2 != 0):
    print("Weird")
if (n > 2 and n < 5):
    if (n % 2 == 0):
        print("Not Weird")
if (n > 6 and n < 20):
    if (n % 2 == 0):
        print("Weird")
if (n > 20):
    if (n % 2 == 0):
        print("Not Weird")