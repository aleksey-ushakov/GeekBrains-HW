__author__ = 'Ушаков Алексей Валериевич'


# Задание-1:
# Написать программу, выполняющую операции (сложение и вычитание) с простыми дробями.
# Дроби вводятся и выводятся в формате:
# n x/y ,где n - целая часть, x - числитель, у - знаменатель.
# Дроби могут быть отрицательные и не иметь целой части, или иметь только целую часть.
# Примеры:
# Ввод: 5/6 + 4/7 (всё выражение вводится целиком в виде строки)
# Вывод: 1 17/42  (результат обязательно упростить и выделить целую часть)
# Ввод: -2/3 - -2
# Вывод: 1 1/3


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def dec_str_to_num(dec_str):
    """
    Функция преобразует строковую запись дроби в список [chislitel, znamenatel] с двумя целыми числами
    :param вводится строковая запись дроби которая может содержать или не содержать знак и цеую часть
    :return: Функция преобразует строковую запись дроби в список [chislitel, znamenatel] с двумя целыми числами
    """
    chislitel_znak = (-1 if dec_str[0] == '-' else 1)
    znam = int(dec_str[dec_str.find('/')+1:].strip()) if dec_str.find('/') != -1 else 1
    dec_str = dec_str[1:].strip() if dec_str[0] == '-' else dec_str.strip()
    if znam == 1:
        chisl = chislitel_znak * int(dec_str)
    else:
        chisl = dec_str[0:dec_str.find('/')].strip()
        chisl = chislitel_znak * (int(chisl) if chisl.find(' ') == -1 else int(chisl[:chisl.find(' ')]) * znam + int(chisl[chisl.find(' ')+1:]))
    return [chisl, znam]


def dec_num_to_str(dec_chis_znam):
    """
    Функция преобразует список [chislitel, znamenatel] с двумя целыми числами в строковую запись дроби
    :param dec_chis_znam: вводится список [chislitel, znamenatel] с двумя целыми числами
    :return: Функция преобразует список [chislitel, znamenatel] с двумя целыми числами в строковую запись дроби
    """
    d = [abs(dec_chis_znam[0]), abs(dec_chis_znam[1])]
    d_str = (str(d[0] // d[1]) + (' ' + str(d[0] % d[1]) + '/' + str(d[1]) if d[0] % d[1] else '')) if d[0] >= d[1] else str(d[0]) + '/' + str(d[1])
    return ('-' if dec_chis_znam[0]/dec_chis_znam[1] <0 else '') + d_str


def dec_operation (Dec1, Dec2, str_operaetor):
    """
    Функция возвращает результат операции с дробями в виде списка [chislitel, znamenatel] с двумя целыми числами
    :param Dec1: дробь в виде списка [chislitel, znamenatel] с двумя целыми числами
    :param Dec2: дробь в виде списка [chislitel, znamenatel] с двумя целыми числами
    :param str_operaetor: оператор в виде строки с одним символом, может быть '-','+','*' или '/'
    :return: возвращает результат операции с дробями в виде списка [chislitel, znamenatel] с двумя целыми числами
    """
    # вычисление максимального общего делителя для списка чисел X
    max_com_factor = lambda x: max([i for i in range(1, min(map(abs, x))+1) if not sum(map(lambda k: k % i, x))])
    dec_opt = lambda x: list(map(lambda k: int(k / max_com_factor(x)), x))    # сокращение дроби
    if str_operaetor == '+':
        return dec_opt([Dec1[0] * Dec2[1] + Dec2[0] * Dec1[1], Dec1[1] * Dec2[1]])
    elif str_operaetor == '-':
        return dec_opt([Dec1[0] * Dec2[1] - Dec2[0] * Dec1[1], Dec1[1] * Dec2[1]])
    elif str_operaetor == '/':
        return dec_opt([Dec1[0] * Dec2[1], Dec1[1] * Dec2[0]])
    elif str_operaetor == '*':
        return dec_opt([Dec1[0] * Dec2[0], Dec1[1] * Dec2[1]])
    else:
        return False


print('Задание-1\n')

str_exp = input('Программа для вычисления операции (сложение, вычитание, умножение) с дробями.\n\
Дроби вводятся и выводятся в формате: x/y ,где n - целая часть, x - числитель, у - знаменатель\n\
Дроби могут быть отрицательные и не иметь целой части, или иметь только целую часть\n\
Всё выражение вводится целиком в виде строки\n\
Пример 1: 5/6 + 4/7\n\
Пример 2: -2/3 - -2\n\nВведите задачу:').strip()

#str_exp = '5/6 + 4/7'

if str_exp.find('+') != -1:
    str_op = '+'
    str_dec_1 = str_exp[:str_exp.find('+')].strip()
    str_dec_2 = str_exp[str_exp.find('+') + 1:].strip()

elif str_exp.find('*') != -1:
    str_op = '*'
    str_dec_1 = str_exp[:str_exp.find('*', 1)].strip()
    str_dec_2 = str_exp[str_exp.find('*', 1) + 1:].strip()

else:
    str_op = '-'
    str_dec_1 = str_exp[:str_exp.find('-', 1)].strip()
    str_dec_2 = str_exp[str_exp.find('-', 1) + 1:].strip()

print('Результат расчета:', dec_num_to_str(dec_operation(dec_str_to_num(str_dec_1), dec_str_to_num(str_dec_2), str_op)))


# Задание-2:
# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки
# они получают удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"
print('Задание-2\n')

def print_table(table, table_name, delimiter, header_true_false):
    """
    Print table ([['', ''..''],['', ''..'']...['', ''..'']) in readable way, with proper columns width and alignment
    :param table: list of lists
    :return: none
    """
    import math
    print(table_name + ':')
    for i in range(len(table)):
        string_len = 0
        for j in range(len(table[i])):
            alignment = '>' if is_number(str(table[i][j])) else '<'
            column_width = max([len(str(table[k][j])) for k in range(len(table))])
            string_format = '{:' + alignment + str(column_width) + '}'
            print(string_format.format(table[i][j]), end=(delimiter if j < len(table[i])-1 else '\n'))
            string_len += column_width + (len(delimiter) if j < len(table[i])-1 else 0)
        string_len = print(''+'-'*string_len) if i == 0 and header_true_false else print('', end='')
    print()


def string_list_to_table(string_list, delimiter):
    """
    Convert list of string delimited (by delmiter) to table (list of lists)
    :param string_list: list lines (returned by readlines() or similar)
    :param delimiter:
    :return:
    """
    z = 0
    while z < len(string_list):
        if string_list[z].strip() == '':
            string_list.pop(z)
        elif string_list[z] == '\n':
            string_list.pop(z)
        elif string_list[z][-1:] == '\n':
            string_list[z] = string_list[z][0:-1]
        else:
            z += 1

    string_list = [[i] for i in string_list]
    for i in range(len(string_list)):
        position = 0
        string = string_list[i]
        while string[position].strip().find(delimiter) != -1:
            string.append(string[position][string[position].find(' ') + 1:].strip())
            string[position] = string[position][:string[position].find(' ')].strip()
            position += 1
    for i in string_list:
        for j in range(len(i), max([len(k) for k in string_list])):
            i.append('-')
    return string_list
import os

my_path = os.path.join(os.getcwd(), 'data', 'workers')
with open(my_path, 'r', encoding = 'UTF-8') as my_file:
    workers = my_file.readlines()
    print_table(string_list_to_table(workers, ' '), my_path, '  ' + chr(124)+'  ', True)
    workers = string_list_to_table(workers, ' ')
my_file.close()

my_path = os.path.join(os.getcwd(), 'data', 'hours_of')
with open(my_path, 'r', encoding = 'UTF-8') as my_file:
    hours_of = my_file.readlines()
    print_table(string_list_to_table(hours_of, ' '), my_path, '  ' + chr(124) + '  ', True)
    hours_of = string_list_to_table(hours_of, ' ')
my_file.close()

workers[0].append('Отработано')
workers[0].append('Начислено')
for i in range(1, len(workers)):
    workers[i].append('--')
    workers[i].append('--')
    for j in hours_of:
        if workers[i][0]+workers[i][1] == j[0] + j[1]:
            workers[i][5] = j[2]
            workers[i][6] = round(float(workers[i][2]) - (float(workers[i][2])/float(workers[i][4])) * (float(workers[i][4]) - float(j[2])) * (1 if float(workers[i][4]) > float(j[2]) else 2),2)

print_table(workers, 'Ведомость расчета заработной платы', '  ' + chr(124) + '  ', True)

# Задание-3:
# Дан файл ("data/fruits") со списком фруктов.
# Записать в новые файлы все фрукты, начинающиеся с определенной буквы.
# Т.е. в одном файле будут все фрукты на букву “А”, во втором на “Б” и т.д.
# Файлы назвать соответственно.
# Пример имен файлов: fruits_А, fruits_Б, fruits_В ….
# Важно! Обратите внимание, что нет фруктов, начинающихся с некоторых букв.
# Напишите универсальный код, который будет работать с любым списком фруктов
# и распределять по файлам в зависимости от первых букв, имеющихся в списке фруктов.
# Подсказка:
# Чтобы получить список больших букв русского алфавита:
# print(list(map(chr, range(ord('А'), ord('Я')+1))))


my_path = os.path.join(os.getcwd(), 'data', 'fruits.txt')
with open(my_path, 'r', encoding = 'UTF-8') as my_file:
    fruits = my_file.readlines()
    fruits = string_list_to_table(fruits, chr(124))
my_file.close()

for i in list(map(chr, range(ord('А'), ord('Я')+1))):
    if len([k for k in fruits if k[0][:1] == i]) > 0:
        my_path = os.path.join(os.getcwd(), 'data', 'fruits_' + i + '.txt')
        with open (my_path, 'w', encoding='UTF-8') as my_file:
            my_file.write('\n'.join([k[0] for k in fruits if k[0][:1] == i]))
            my_file.close()
