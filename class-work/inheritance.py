class shape: #base
    
    len = 0.0
    brd = 0.0
    rad = 0.0
    area = 0.0
    def show(self):
        print("I am here in the base class...")
        print(self.area)


class polygons(shape):

    def square(self):
        print("Rendering Square...")
        self.area = self.len * self.len

    def rectangle(self):
        print("Rendering Rectangle...")
        self.area = self.len * self.brd

    def triangle(self):
        print("Rendering Triangle...")
        self.area = 0.5 * self.brd * self.len

    def circle(self):
        print("Rendering Circle...")
        self.area = 3.14 * self.rad * self.rad

obj = polygons()
ask = input("Which area of shape you wanna calculate ? (S/R/T/C):\t")

if (ask == 's' or ask == 'S'):
    obj.len = int(input("Enter Length of Square :\t"))
    obj.square()
    obj.show()

elif (ask == 'r' or ask == 'R'):
    obj.len = int(input("Enter Length of Rectangle :\t"))
    obj.brd = int(input("Enter Breadth of Rectangle :\t "))
    obj.rectangle()
    obj.show()

elif (ask == 't' or ask == 'T'):
    obj.len = int(input("Enter base of Triangle :\t"))
    obj.brd = int(input("Enter height of Rectangle :\t "))
    obj.triangle()
    obj.show()

elif (ask == 'c' or ask == 'C'):
    obj.rad = int(input("Enter Radius of the circle :\t"))
    obj.circle()
    obj.show()

else:
    print("Wrong Input !")
    