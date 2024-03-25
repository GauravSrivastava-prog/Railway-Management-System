#Q -> Print a list of all possible coordinates in python, given by (i,j,k)  on a 3D grid where the sum of i + j + k  is not equal to n . 
#Here x,y,z,n are user inputs and 0 <= i <= x and 0 <= j <= y and 0 <= k <= z .Please use list comprehensions rather than multiple loops.

x = int(input("Enter the value of x: "))
y = int(input("Enter the value of y: "))
z = int(input("Enter the value of z: "))
n = int(input("Enter the value of n: "))

#List Comprehension
coordinates = [(i, j, k) for i in range(x + 1) for j in range(y + 1) for k in range(z + 1) if (i + j + k) != n]

print("List of all possible coordinates:")
print(coordinates)
