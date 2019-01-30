import random
import timeit
import collections
import math


# Примечание: для решения задач попробуйте применить какую-нибудь коллекцию из модуля collections

# 1. Пользователь вводит данные о количестве предприятий, их наименования и прибыль за 4 квартала
# (т.е. 4 отдельных числа) для каждого предприятия.. Программа должна определить среднюю прибыль
# (за год для всех предприятий) и вывести наименования предприятий, чья прибыль выше среднего
# и отдельно вывести наименования предприятий, чья прибыль ниже среднего.
print("\nЗадача 1")
#n = int(input("Введите кол-во предприятий: 5"))
n = 5
companies = collections.OrderedDict()
companies.update([('Ростех', [10, 20, 30, 40]), ('Гринантом', [20, 30, 40, 50]), ('"Электрон', [30, 40, 50, 60]), ('Русклимат', [40, 50, 60, 70]), ('Тех-Креп', [50, 40, 50, 60])])
#for i in range(n):
#    companies.update([(input("\nВведите название предприятия ({}): ".format(i+1)), [int(input("Введите прибыль за {}-й квартал: ".format(j+1))) for j in range(4)])])
print(companies)
avg_profit = sum([sum(companies.get(i)) for i in companies.keys()]) / len(companies)
print('Средняя прибыль за год по всем предприятиям: ', avg_profit)
print('Предприятия с прибылью выше средней: ', ", ".join([i for i in companies.keys() if sum(companies.get(i)) > avg_profit]))
print('Предприятия с прибылью не выше средней: ', ", ".join([i for i in companies.keys() if sum(companies.get(i)) <= avg_profit]))

# 2. Написать программу сложения и умножения двух шестнадцатеричных чисел.
# При этом каждое число представляется как массив, элементы которого это цифры числа.
# Например, пользователь ввёл A2 и C4F. Сохранить их как [‘A’, ‘2’] и [‘C’, ‘4’, ‘F’] соответственно.
# Сумма чисел из примера: [‘C’, ‘F’, ‘1’], произведение - [‘7’, ‘C’, ‘9’, ‘F’, ‘E’].
print("\nЗадача 1")

def sum_num_lst(number_set, n_1, n_2):

    sys_num = len(number_set)
    num_1, num_2 = collections.Counter(), collections.Counter()
    for i in range(len(n_1)):
        num_1[n_1[i]] = sys_num ** (len(n_1) - i - 1)
    for i in range(len(n_2)):
        num_2[n_2[i]] = sys_num ** (len(n_2) - i - 1)

    num_sum = sum([number_set.index(i) * num_1[i] for i in num_1]) + sum([number_set.index(i) * num_2[i] for i in num_2])
    sum_result = list()

    for i in range(math.trunc(math.log(num_sum, sys_num)), -1, -1):
        sum_result.append(num_sum // (sys_num ** i))
        num_sum -= sum_result[-1] * sys_num ** i

    return [number_set[i] for i in sum_result]

def prod_num_lst(number_set, n_1, n_2):
    sys_num = len(number_set)
    num_1, num_2 = collections.Counter(), collections.Counter()
    for i in range(len(n_1)):
        num_1[n_1[i]] = sys_num ** (len(n_1) - i - 1)
    for i in range(len(n_2)):
        num_2[n_2[i]] = sys_num ** (len(n_2) - i - 1)

    num_sum = sum([number_set.index(i) * num_1[i] for i in num_1]) * sum([number_set.index(i) * num_2[i] for i in num_2])
    sum_result = list()

    for i in range(math.trunc(math.log(num_sum, sys_num)), -1, -1):
        sum_result.append(num_sum // (sys_num ** i))
        num_sum -= sum_result[-1] * sys_num ** i

    return [number_set[i] for i in sum_result]


number_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
n_1 = ['A', '2']
n_2 = ['C', '4', 'F']

print("Цифры системы исчисления:", number_set)
print("Первое число:", n_1)
print("Второе число:", n_2)
print("Сумма чисел:", sum_num_lst(number_set, n_1, n_2))
print("Произведение чисел:", prod_num_lst(number_set, n_1, n_2), "\n*Программа позволяет производить рассчеты для любой системы исчислений")



