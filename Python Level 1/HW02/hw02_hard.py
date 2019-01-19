__author__ = 'Ушаков Алексей Валериевич'

# Задание-1: уравнение прямой вида y = kx + b задано в виде строки.
# Определить координату y точки с заданной координатой x.

equation = 'y = -12x + 11111140.2121'
x = 2.5
# вычислите и выведите y


# Задание-2: Дата задана в виде строки формата 'dd.mm.yyyy'.
# Проверить, корректно ли введена дата.
# Условия корректности:
# 1. День должен приводиться к целому числу в диапазоне от 1 до 30(31)
#  (в зависимости от месяца, февраль не учитываем)
# 2. Месяц должен приводиться к целому числу в диапазоне от 1 до 12
# 3. Год должен приводиться к целому положительному числу в диапазоне от 1 до 9999
# 4. Длина исходной строки для частей должна быть в соответствии с форматом 
#  (т.е. 2 символа для дня, 2 - для месяца, 4 - для года)

# Пример корректной даты
date = '01.11.1985'

# Примеры некорректных дат
date = '01.22.1001'
date = '1.12.1001'
date = '-2.10.3001'


# Задание-3: "Перевёрнутая башня" (Задача олимпиадного уровня)
#
# Вавилонцы решили построить удивительную башню —
# расширяющуюся к верху и содержащую бесконечное число этажей и комнат.
# Она устроена следующим образом — на первом этаже одна комната,
# затем идет два этажа, на каждом из которых по две комнаты,
# затем идёт три этажа, на каждом из которых по три комнаты и так далее:
#         ...
#     12  13  14
#     9   10  11
#     6   7   8
#       4   5
#       2   3
#         1
#
# Эту башню решили оборудовать лифтом --- и вот задача:
# нужно научиться по номеру комнаты определять,
# на каком этаже она находится и какая она по счету слева на этом этаже.
#
# Входные данные: В первой строчке задан номер комнаты N, 1 ≤ N ≤ 2 000 000 000.
#
# Выходные данные:  Два целых числа — номер этажа и порядковый номер слева на этаже.
#
# Пример:
# Вход: 13
# Выход: 6 2
#
# Вход: 11
# Выход: 5 3
import math
#1
print('\n\n# Задача-1:')
equation = 'y = -12x + 11111140.2121'
equation_1 = ''.join([i for i in equation if i != ' '])
x = 2.5
k = float(equation_1[equation_1.find('=')+1: equation_1.find('x')])
b_string = equation_1[equation_1.find('x') + 1:]
b = float(b_string[b_string.find('+')+1:]) if b_string.find('+') != -1 else - float(b_string[b_string.find('-')+1:])
y = k * x + b
print(equation, '\nk = ', k, '\nb = ', b, '\ny = ', y)


#2
print('\n\n# Задача-2:')
string_date = input('Введите дату в формате dd.mm.yyyy:')
#string_date = "30.06.2000"
max_month_day = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}
err_set = set()

if string_date.count('.') != 2:
    err_set.add("Неверный формат даты. Дата должна быть в виде строки формата 'dd.mm.yyyy', и содержать два разделителя '.'")
else:
    day_string = string_date[:string_date.find('.')]
    month_string = string_date[string_date.find('.')+1: string_date.find('.', string_date.find('.')+1)]
    year_string = string_date[-string_date[::-1].find('.'):]

    if not day_string.isdigit():
        err_set.add("День должен приводиться к целому числу в диапазоне от 1 до 30(31) (в зависимости от месяца, февраль не учитываем)")
    else:
        if not 31 >= int(day_string) >= 1:
            err_set.add("День должен приводиться к целому числу в диапазоне от 1 до 30(31) (в зависимости от месяца, февраль не учитываем)")

    if not month_string.isdigit():
        err_set.add("Месяц должен приводиться к целому числу в диапазоне от 1 до 12")
    else:
        if not 12 >= int(month_string) >= 1:
            err_set.add("Месяц должен приводиться к целому числу в диапазоне от 1 до 12")

    if not year_string.isdigit():
        err_set.add("Год должен приводиться к целому положительному числу в диапазоне от 1 до 9999")
    else:
        if not 9999 >= int(year_string) >= 1:
            err_set.add("Год должен приводиться к целому положительному числу в диапазоне от 1 до 9999")

    if day_string.isdigit() and month_string.isdigit():
        if 1 <= int(month_string) <= 12:
            if not 1 <= int(day_string) <= max_month_day[month_string]:
                err_set.add("День должен приводиться к целому числу в диапазоне от 1 до 30(31) (в зависимости от месяца, февраль не учитываем)")
        else:
            err_set.add("Месяц должен приводиться к целому числу в диапазоне от 1 до 12")
    if len(day_string) != 2 or len(month_string) != 2 or len(year_string) != 4 or len(string_date) != 10:
        err_set.add("Длина исходной строки для частей должна быть в соответствии с форматом")

msg = '\n'.join(err_set) if err_set else "Дата заведена корректно"
print(msg)


#3
print('\n\n# Задача-3:')
my_room_number = int(input())   #my_room_number = int(input("Введите номер комнаты"))
#my_room_number = 10
last_room_in_current_block = 0  # последняя комната в текущем блоке:
last_floor_in_previose_block = 0  # последняя комната в предыдущем блоке:
last_block = 0  # последний обработанный блок

while last_room_in_current_block < my_room_number:
    last_room_in_previouse_block = last_room_in_current_block
    last_floor_in_previose_block += last_block
    last_block += 1
    last_room_in_current_block = last_room_in_previouse_block + last_block ** 2

floor = last_floor_in_previose_block + (my_room_number - last_room_in_previouse_block) // (last_block + 1) + 1
room_on_floor = last_block if not (my_room_number - last_room_in_previouse_block) % (last_block) else (my_room_number - last_room_in_previouse_block) % (last_block)
print(floor, room_on_floor)
#print('Комната:', my_room_number, end=' ')
#print('Блок:', last_block, end=' ')
#print('Этаж:', last_floor_in_previose_block + (my_room_number - last_room_in_previouse_block) // (last_block + 1) + 1, end=' ')
#print('Порядковый номер слева:', last_block if not (my_room_number - last_room_in_previouse_block) % (last_block) else (my_room_number - last_room_in_previouse_block) % (last_block))