__author__ = 'Ушаков Алексей Валериевич'


# Задание-1:
# Напишите функцию, возвращающую ряд Фибоначчи с n-элемента до m-элемента.
# Первыми элементами ряда считать цифры 1 1


def fibonacci(n, m):
    '''
    :param n:
    :param m:
    :return: функциz, возвращаетряд Фибоначчи с n-элемента до m-элемента
    '''
    f_arr = [1, 1]
    for i in range(2, m):
        f_arr.append(f_arr[i-2]+f_arr[i-1])
    return f_arr[n-1: m]


print(fibonacci(10, 20))

# Задача-2:
# Напишите функцию, сортирующую принимаемый список по возрастанию.
# Для сортировки используйте любой алгоритм (например пузырьковый).
# Для решения данной задачи нельзя использовать встроенную функцию и метод sort()


def sort_to_max(origin_list):
    unsorted_list = origin_list[::1]
    sorted_list = []
    for i in range(len(origin_list)):
        min = unsorted_list[0]
        for j in unsorted_list:
            min = j if min > j else min
        sorted_list.append(min)
        unsorted_list.remove(min)
    return sorted_list


print(sort_to_max([2, 10, -12, 2.5, 20, -11, 4, 4, 0]))

# Задача-3:
# Напишите собственную реализацию стандартной функции filter.
# Разумеется, внутри нельзя использовать саму функцию filter.


def filter_new (origin_list, func):
    return [i for i in origin_list if func(i)]


# Задача-4:
# Даны четыре точки А1(х1, у1), А2(x2 ,у2), А3(x3 , у3), А4(х4, у4).
# Определить, будут ли они вершинами параллелограмма.


def is_parallelogram(A1_x_y, A2_x_y, A3_x_y, A4_x_y):
    k = lambda A1, A2: (A1[1] - A2[1]) / (A1[0] - A2[0]) if (A1[0] - A2[0]) != 0 else math.inf
    a = int(k(A1_x_y, A2_x_y) == k(A3_x_y, A4_x_y)) + int(k(A1_x_y, A3_x_y) == k(A2_x_y, A4_x_y)) + int(k(A1_x_y, A4_x_y) == k(A2_x_y, A3_x_y))
    return True if a ==2 else False


print(is_parallelogram([0, 0], [1, 1], [0, 1], [1, 0]))
print(is_parallelogram([1, 1], [4, 5], [3, 2], [2, 4]))
