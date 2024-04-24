class polygon:
    
    def __init__(self,no_of_sides):
        self.n = no_of_sides
        self.sides = [0 for i in range(no_of_sides)]

    def input_sides(self):
        self.sides = [float(input("Enter Side "+str(i+1)+" : ")) for i in range(self.n)]

    def dispSides(self):
        for i in range(self.n):
            print("Side",i+1,"is",self.sides[i])

class triangle(polygon):

    def __init__(self):
        polygon.__init__(self,3)

    def findArea(self):
        a,b,c = self.sides
        # calculate the semi-perimeter
        s = (a+b+c)/2
        area = (s*(s-a)*(s-b)(s-c)) ** 0.5
        print("The area of the triangle is %0.2f"%area)

t = triangle()
t.input_sides()
t.dispSides()
t.findArea()