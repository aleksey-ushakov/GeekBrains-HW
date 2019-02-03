#HW06 Aleksey Ushakov
#Python 3.7 64bit



import random
import timeit
import math
import numpy
from memory_profiler import profile
import timeit
import datetime


def time(func):
    def t(*args, **kwargs):
        start = datetime.time()
        res = func(*args, **kwargs)
        print("Время выполнения алгоритма:", datetime.timedelta(datetime.time(), start))
        return res
    return t

print("""\n\nЗадача 1
Отсортируйте по убыванию методом "пузырька" одномерный целочисленный массив, заданный случайными числами на промежутке [-100; 100).
Выведите на экран исходный и отсортированный массивы. Сортировка должна быть реализована в виде функции. По возможности доработайте алгоритм (сделайте его умнее).
""")

def bubble_sort(lst):
    work_lst = lst[:]
    for j in range(len(work_lst)-1, 1, -1):
        k = 0
        for i in range(j):
            if work_lst[i] < work_lst[i+1]:
                work_lst[i + 1], work_lst[i], k = work_lst[i], work_lst[i+1], k + 1
        if not k: break
    print("Исходный массив:            ", lst)
    print("Отсортированный пузырьком:  ", work_lst)
    print("Алгоритм отсортировал список за {} проходов из максимально возможных {}".format(len(work_lst) - j,
                                                                                           len(work_lst) - 1))
    print("Проверка сортировки массива:", sorted(lst, reverse=True) == work_lst)
    return work_lst


lst = [random.randint(-100, 100) for i in range(21)]
sorted_lst = bubble_sort(lst)


print("""\n\nЗадача 2
Отсортируйте по возрастанию методом слияния одномерный вещественный массив, заданный случайными числами на промежутке [0; 50).
Выведите на экран исходный и отсортированный массивы.
""")

def quick_sort(lst):
    return (fast_sort([i for i in lst if i < lst[len(lst) // 2]]) + [i for i in lst if i == lst[len(lst) // 2]] + fast_sort([i for i in lst if i > lst[len(lst) // 2]])) if len(lst) > 1 else lst


def merge_sort(lst):
    if len(lst) > 1:
        h = len(lst) // 2
        l_half, r_half, i, j, k = merge_sort(lst[:h]), merge_sort(lst[h:]), 0, 0, 0
        while i < len(l_half) and j < len(r_half):
            if l_half[i] < r_half[j]:
                lst[k], i = l_half[i], i + 1
            else:
                lst[k], j = r_half[j], j + 1
            k += 1
        while i < len(l_half):
            lst[k], i, k = l_half[i], i + 1, k + 1
        while j < len(r_half):
            lst[k], j, k = r_half[j], j + 1, k + 1
    return lst

lst = [random.randint(0, 100) for i in range(21)]
sorted_lst = merge_sort(lst[:])
print("Исходный массив:            ", lst, "\nОтсортированный слиянием:   ", sorted_lst, "\nПроверка сортировки массива:", sorted(lst) == sorted_lst)


print("""\n\nЗадача 3
Массив размером 2m + 1, где m – натуральное число, заполнен случайным образом. Найдите в массиве медиану.
Медианой называется элемент ряда, делящий его на две равные части: в одной находятся элементы, которые не меньше медианы,
в другой – не больше медианы. Задачу можно решить без сортировки исходного массива.
Но если это слишком сложно, то используйте метод сортировки, который не рассматривался на уроках
""")
lst = [random.randint(0, 100) for i in range(21)]
for j in lst:
    if len([i for i in lst if i >= j]) == len([i for i in lst if i <= j]): break
print("Исходный массив:                  ", lst, "\nМедиана массива:                  ", j, "\nCортированный массив для проверки:", sorted(lst))

