#HW06 Aleksey Ushakov
#Python 3.7 64bit

import random
import timeit
import math
import numpy
from pympler import asizeof
from memory_profiler import profile

#Подсчитать, сколько было выделено памяти под переменные в ранее разработанных программах в рамках первых трех уроков.
# Проанализировать результат и определить программы с наиболее эффективным использованием памяти.
#Примечание: Для анализа возьмите любые 1-3 ваших программы или несколько вариантов кода для одной и той же задачи.
# Результаты анализа вставьте в виде комментариев к коду. Также укажите в комментариях версию Python и разрядность вашей ОС.


print("\nЗадача 1")
# В диапазоне натуральных чисел от 2 до 10000 определить, сколько из них кратны любому из чисел в диапазоне от 2 до 100.


@profile
def normal_solution(lower, upper, devider_lower, devider_upper):
    n = 0
    for i in range(lower, upper):
        j = devider_lower
        while i % j != 0 and j <= devider_upper:
            j += 1
        n = (n + 1) if j <= devider_upper else n
    print("Нормальный алгоритм проверки (перебор до первого деления без остатка):", n)
    del n
    del i
    del j

@profile
def optimal_solution(lower, upper, devider_lower, devider_upper):

    prime_lst = [2]
    for chek_num in range(prime_lst[0] + 1, devider_upper + 1):
        for i in prime_lst:
            if chek_num % i == 0: break
            if i == prime_lst[-1]: prime_lst.append(chek_num)

    n = 0
    for i in range(lower, upper):
        for j in prime_lst:
            if i % j == 0:
                n += 1
                break
    print("Оптимальный алгоритм проверки (перебор до первого деления без остатка):", n)
    del n
    del i
    del j
    del prime_lst
    del chek_num

print("Расчет кол-ва чисел в диапазоне 2-10000 кратных хотя бы одному числу от 2 до 100")
print("Время расчета:", timeit.timeit("normal_solution(2, 10000, 2, 100)", setup="from __main__ import normal_solution", number=1), "\n")
print("Время расчета:", timeit.timeit("optimal_solution(2, 10000, 2, 100)", setup="from __main__ import optimal_solution", number=1), "\n")

# 2. Сравнить три алгоритма нахождения i-го по счёту простого числа.
# Без использования «Решета Эратосфена»;
# Используя алгоритм «Решето Эратосфена» (каждое последующее число делится на каждое простое из списка простых чисел до деления без остатка)
# Используя алгоритм «Решето Эратосфена» (создается массив последовательных чисел и и з него последовательно вычеркиваются числа кратные простым числам)

print("\nЗадача 2")

@profile
def prime_eratosfen_1(n):
    prime_lst = [2]
    chek_num = 3
    while len(prime_lst) < n:
        for i in prime_lst:
            if chek_num % i == 0: break
            if i > chek_num ** (1 / 2):
                prime_lst.append(chek_num)
                break
        chek_num += 1
    print("Алгоритм проверки - Решето Эратосфена(последовательное деление на все простые числа не большие корня квадратного проверяемого числа):", prime_lst[n-1])
    print("Размер масивв простых чисел:", prime_lst.__sizeof__())
    del i
    del prime_lst
    del chek_num



@profile
def prime_eratosfen_2(q):
    n = int(q * math.log2(q))
    a = list(range(n))  # создание заполнение массива с n количеством элементов
    len_prime_lst, a[1] = 0, 0  # вторым элементом является единица, - не простое, забиваем нулем.
    for m in range(2, n):  # перебор всех элементов до заданного числа
        if a[m]:  # если он не равен нулю, то
            len_prime_lst += 1
            if len_prime_lst == q: break
            for i in range(2, n // m):
                a[i * m] = 0  # заменить на 0
    print("Алгоритм проверки - Решето Эратосфена(последовательное обнуление элементов массива кратных простым числам):", m)
    print("Размер масивв чисел:", a.__sizeof__())
    del n
    del m
    del i
    del len_prime_lst
    del a


@profile
def prime_eratosfen_3(q):
    n = int(q * math.log2(q))  # размер массива для просеивания
    a = numpy.arange(n)  # создание заполнение массива с n количеством элементов
    len_prime_lst, a[1] = 0, 0  # вторым элементом является единица, - не простое, забиваем нулем.
    for m in range(2, n):  # перебор всех элементов до заданного числа
        if a[m]:  # если он не равен нулю, то
            len_prime_lst += 1
            if len_prime_lst == q: break
            for i in range(2, n // m):
                a[i * m] = 0  # заменить на 0
    print("Алгоритм проверки - Решето Эратосфена(последовательное обнуление элементов массива (numpy) кратных простым числам):", m)
    print("Размер масивв чисел:", a.__sizeof__())
    del n
    del m
    del i
    del len_prime_lst
    del a

if __name__ == "__main__":
    n = 10000
    print("Расчет " + str(n) + "-го простого числа")
    time_prime_eratosfen_1 = timeit.timeit("prime_eratosfen_1(" + str(n) + ")", setup="from __main__ import prime_eratosfen_1", number=1)
    print("Время расчета:", time_prime_eratosfen_1, "\n")
    time_prime_eratosfen_2 = timeit.timeit("prime_eratosfen_2(" + str(n) + ")", setup="from __main__ import prime_eratosfen_2", number=1)
    print("Время расчета:", time_prime_eratosfen_2, "\n")
    time_prime_eratosfen_3 = timeit.timeit("prime_eratosfen_3(" + str(n) + ")", setup="from __main__ import prime_eratosfen_3", number=1)
    print("Время расчета:", time_prime_eratosfen_3, "\n")

    print('''1) Библиотека memory_profiler катастрофически увеличивает время работы алгортма.
к примеру время расчета милионного простого числа без этой библиотеке в 2 раза быстрее чем в    ремя расчета 10-тысячного
пришлось сильно уменьшить кол-во вычислений (до 100-10000 раз меньше пороги выставлять)
\n2) Массивы Библиотеки numpy более чем в два раза занимает меньше памяти, но при наличии ресурса это не является проблемой и не влияет на скорость работы
\n3) Больше всего памяти потребляет @profile - до 27 МБ''')

