__author__ = 'Ушаков Алексей Валериевич'

# Задача-1: Написать класс для фигуры-треугольника, заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.
print('\nЗадание-1')
import math


def dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


class triangle():

    def __init__(self, a=[0, 0], b=[0, 1], c=[1, 0]):
        self.a = a
        self.b = b
        self.c = c

    def square(self):
        p = (dist(self.a, self.b) + dist(self.b, self.c) + dist(self.c, self.a)) / 2
        return round(math.sqrt(p * (p - dist(self.a, self.b)) * (p - dist(self.b, self.c)) * (p - dist(self.c, self.a))), 2)


    def hight(self, vertex = 'a'):
        return round(2 * self.square() / (dist(self.b, self.c) if vertex == 'a' else (dist(self.c, self.a) if vertex == 'b' else dist(self.a, self.b))), 2)


    def perimetr(self):
        return round(dist(self.a, self.b) + dist(self.b, self.c) + dist(self.c, self.a), 2)

triangle_1 = triangle([0, 0], [-10, 10], [10, 10])
print('Площадь треугольника a{} b{} c{}: {}'.format(triangle_1.a, triangle_1.b, triangle_1.c, triangle_1.square()))
print('Периметр треугольника a{} b{} c{}: {}'.format(triangle_1.a, triangle_1.b, triangle_1.c, triangle_1.perimetr()))
vertex = 'c'
print('Высота треугольника a{} b{} c{} из вершины {}: {}'.format(triangle_1.a, triangle_1.b, triangle_1.c, vertex, triangle_1.hight(vertex)))


# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы:
# проверка, является ли фигура равнобочной трапецией;
# вычисления: длины сторон, периметр, площадь.
print('\nЗадание-2')


class trapezium():
    def __init__(self, a=[0, 0], b=[0, 0], c=[0, 0], d=[0, 0]):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        # Переставляем точки так, чтоб abcd был выпуклый четырехугольник
        abcd = dist(self.a, self.b) + dist(self.b, self.c) + dist(self.c, self.d)+ dist(self.d, self.a)
        acbd = dist(self.a, self.c) + dist(self.c, self.b) + dist(self.b, self.d)+ dist(self.d, self.a)
        acdb = dist(self.a, self.c) + dist(self.c, self.d) + dist(self.d, self.b)+ dist(self.b, self.a)
        if acbd == min(abcd, acbd, acdb):
            self.b, self.c = self.c, self.b
        elif acdb == min(abcd, acbd, acdb):
            self.b, self.c, self.d = self.c, self.d, self.b
        # Переставляем точки так, чтоб если есть паралельные стороны то это были bc и ad
        if (self.a[0] != self.b[0] and self.c[0] != self.d[0] and (self.a[1] - self.b[1]) / (self.a[0] - self.b[0]) == (self.c[1] - self.d[1]) / (self.c[0] - self.d[0])) or (
                self.a[0] == self.b[0] and self.c[0] == self.d[0]):
            self.a, self.b, self.c, self.d = self.d, self.a, self.b, self.c

    # Площадь как сумма площадей двух треугольников через метод класса треугольников предыдущего задания
    def square(self):
        triangl_1 = triangle(self.a, self.b, self.c)
        triangl_2 = triangle(self.a, self.c, self.d)
        return round(triangl_1.square() + triangl_2.square(), 2)

    # функция выводит длинны всех сторон
    def sides(self):
        print('Длинны сторон трапеции:')
        print('a{:<12} - b{:<12} - {:>8}'.format(str(self.a), str(self.b), str(round(dist(self.a, self.b), 2))))
        print('b{:<12} - c{:<12} - {:>8}'.format(str(self.b), str(self.c), str(round(dist(self.b, self.c), 2))))
        print('c{:<12} - d{:<12} - {:>8}'.format(str(self.c), str(self.d), str(round(dist(self.c, self.d), 2))))
        print('d{:<12} - a{:<12} - {:>8}'.format(str(self.d), str(self.a), str(round(dist(self.d, self.a), 2))))

    # функция возвращает периметр фигуры abcd
    def perimetr(self):
        return round(dist(self.a, self.b) + dist(self.b, self.c) + dist(self.c, self.d)+ dist(self.d, self.a), 2)

    # функция возвращает True если фигура трапеция
    def is_trapezium(self):
        return True if (self.b[0] != self.c[0] and self.a[0] != self.d[0] and (self.b[1] - self.c[1]) / (self.b[0] - self.c[0]) == (self.a[1] - self.d[1]) / (self.a[0] - self.d[0])) or (
                self.b[0] == self.c[0] and self.a[0] == self.d[0]) else False

    # функция возвращает True если фигура равнобедренная трапеция
    def is_eq_trapezium(self):
        return True if self.is_trapezium() and dist(self.b, self.c) == dist(self.a, self.d) else False
    # функция возвращает описание фигуры в виде строки a[] b[] c[] d[]
    def string(self):
        return 'a{} b{} c{} d{}'.format(self.a, self.b, self.c, self.d)

#trap_1 = trapezium([0, 0], [-10, 11], [10, 10], [0, 20])
#trap_1 = trapezium([0, 0], [10, 5], [10, 0], [0, 20])
trap_1 = trapezium([0, 0], [10, 2], [1, 2], [9, 0])

trap_1.sides()
print('Площадь фигуры {}: {}'.format(trap_1.string(), trap_1.square()))
print('Периметр фигуры {}: {}'.format(trap_1.string(), trap_1.perimetr()))
print('Фигура {}'.format(trap_1.string()), 'является трапецией' if trap_1.is_trapezium() else 'не является трапецией')
print('Фигура {}'.format(trap_1.string()), 'является равносторонней трапецией' if trap_1.is_eq_trapezium() else 'не является равносторонней трапецией')