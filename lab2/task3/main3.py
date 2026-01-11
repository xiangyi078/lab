import math

class Shape:
    """Базовый класс для геометрических фигур"""
    
    def S(self):
        pass
    
    def C(self):
        pass
    
    def compare_S(self, other):
        area1 = self.S()
        area2 = other.S()
        
        if area1 > area2:
            return "larger"
        elif area1 < area2:
            return "smaller"
        else:
            return "equal"
    
    def compare_C(self, other):
        peri1 = self.C()
        peri2 = other.C()
        
        if peri1 > peri2:
            return "larger"
        elif peri1 < peri2:
            return "smaller"
        else:
            return "equal"

class Square(Shape):
    def __init__(self, a):
        self.a = a
    
    def S(self):
        return self.a * self.a
    
    def C(self):
        return 4 * self.a

class Rectangle(Shape):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def S(self):
        return self.a * self.b
    
    def C(self):
        return 2 * (self.a + self.b)

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def S(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def C(self):
        return self.a + self.b + self.c

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    
    def S(self):
        return math.pi * self.r * self.r
    
    def C(self):
        return 2 * math.pi * self.r

if __name__ == "__main__":
    square = Square(5)
    rectangle = Rectangle(4, 6)
    triangle = Triangle(3, 4, 5)
    circle = Circle(3)
    
    print("Площадь квадрата:", square.S(), "Периметр квадрата:", square.C())
    print("Площадь прямоугольника:", rectangle.S(), "Периметр прямоугольника:", rectangle.C())
    print("Площадь треугольника:", triangle.S(), "Периметр треугольника:", triangle.C())
    print("Площадь круга:", circle.S(), "Периметр круга:", circle.C())
    
    print("\nсравнение площади:")
    print("Сравнение площади квадрата и прямоугольника:", square.compare_S(rectangle))
    print("Сравнение площади круга и треугольника:", circle.compare_S(triangle))
    
    print("\nсравнение периметра:")
    print("Сравнение периметра квадрата и прямоугольника:", square.compare_C(rectangle))
    print("Сравнение периметра круга и треугольника:", circle.compare_C(triangle))