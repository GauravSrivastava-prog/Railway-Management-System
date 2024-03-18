import math
print("Enter argument:")
argument = str(input())
if ("sum" in argument):
    print("Enter two numbers:")
    a = int(input())
    b = int(input())
    print(a+b)
elif ("concat" in argument):
    print("Enter two strings:")
    str1 = str(input())
    str2 = str(input())
    print(str1+str2)
elif ("cir-area" in argument):
    print("Enter the radius of the circle:")
    r = int(input())
    print(3.14*r*r)
elif ("rec-area" in argument):
    print("Enter the length and bredth of the rectangle:")
    l = int(input())
    b = int(input())
    print(l*b)
elif ("cube-root" in argument):
    print("Enter number:")
    num = int(input())
    ans = math.pow(num, 1/3)
    print(ans)
elif ("average" in argument):
    print("Enter three numbers:")
    num1 = int(input())
    num2 = int(input())
    num3 = int(input())
    print((num1+num2+num3)/3)
elif ("swap" in argument):
    print("Enter two numbers:")
    swap1 = int(input())
    swap2 = int(input())
    print("First Number : ",swap1)
    print("Second Number : ",swap2)
    swap1 = swap1 + swap2
    swap2 = swap1 - swap2
    swap1 = swap1 - swap2
    print("First Number : ",swap1)
    print("Second Number : ",swap2)
elif ("odd-even" in argument):
    print("Enter a number")
    number = int(input())
    if (number % 2 == 0):
        print("Even Number")
    else:
        print("Odd Number")
elif ("marks" in argument):
    print("Enter Marks:")
    marks = int(input())
    if (marks > 90 and marks <= 100):
        print("O Grade")
    elif (marks > 80 and marks <= 90):
        print("A+ Grade")
    elif (marks > 70 and marks <= 80):
        print("A Grade")
    elif (marks > 60 and marks <= 70):
        print("B+ Grade")
    elif (marks > 50 and marks <= 60):
        print("B Grade")
    elif (marks > 40 and marks <= 50):
        print("C+ Grade")
    elif (marks > 34 and marks <= 40):
        print("C Grade")
    else:
        print("FAIL")
    