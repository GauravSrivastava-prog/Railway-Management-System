def fib1(n):
    a = 0
    b = 1
    c = 0
    print(a,b,end=' ')
    while (c <= n):
        c = a + b
        a = b
        b = c
        print(c,end=' ')
    print()

def fib2(n):
    result = []
    a = 0
    b = 1
    while (a < n):
        result.append(a)
        a = b
        b = a + b
        return result 