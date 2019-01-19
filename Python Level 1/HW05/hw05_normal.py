# Задача-1:
# Напишите небольшую консольную утилиту,
# позволяющую работать с папками текущей директории.
# Утилита должна иметь меню выбора действия, в котором будут пункты:
# 1. Перейти в папку
# 2. Просмотреть содержимое текущей папки
# 3. Удалить папку
# 4. Создать папку
# При выборе пунктов 1, 3, 4 программа запрашивает название папки
# и выводит результат действия: "Успешно создано/удалено/перешел",
# "Невозможно создать/удалить/перейти"

# Для решения данной задачи используйте алгоритмы из задания easy,
# оформленные в виде соответствующих функций,
# и импортированные в данный файл из easy.py

from hw05_easy import zadanie_easy_1_1, zadanie_easy_1_2, zadanie_easy_2,zadanie_easy_3
import os
import shutil
import sys

def get_command():
    print('\nЧто будем делать?')
    print('[1] Перейти в папку...')
    print('[2] Просмотреть содержимое текущей папки')
    print('[3] Удалить папку...')
    print('[4] Создать папку...')
    print('[5] Cоздать директории dir_1 - dir_9 в текущей папке')
    print('[6] Удалить директории dir_1 - dir_9 в текущей папке')
    print('[7] Вывести папки текущей директории:')
    print('[8] Создать копию файла из которого запущен данный скрипт')
    print('[0] Выйти из программы')
    print('Текущая папка', os.getcwd(), '\n')
    print('\x1b[31mВведите команду из списка выше\x1b[0m')
    command = input()
    return command if command in ['1', '2', '3', '4', '5', '6', '7', '8', '0'] else get_command()

def command_1(path):
    try:
        os.chdir(path)
        print ("Успешно создано/удалено/перешел")
    except OSError:
        print("Невозможно перейти")

def command_3(path):
    delete = ''
    while delete not in ['y', 'n', 'Y', 'N', 'Н', 'н', 'Т', 'т']:
        delete = input('Удалить директории {} из текущей папки [y/n] ?'.format(path))

    if delete in ['Y', 'y', 'Н', 'н']:
        i = os.path.join(os.getcwd(), path )
        if os.path.exists(i):
            try:
                os.rmdir(i)
                print('\x1b[32mДиректория {} удалена\x1b[0m'.format(i))
            except OSError:
                print('\x1b[31mПроизошла ошибка при удалении директория {}\x1b[0m'.format(i))
        else:
            print('\x1b[31mДиректрии {} не существует\x1b[0m'.format(i))

def command_4(path):
    i = os.path.join(os.getcwd(), path)
    try:
        os.mkdir(i)
        print('\x1b[32mДиректория {} создана\x1b[0m'.format(i))
    except OSError:
        print('\x1b[31mДиректория {} уже существует\x1b[0m'.format(i))

command = get_command()
while command != '0':
    x = command_1(input('Введите название папки: ')) if command == '1' else False
    x = print('Содержимое текущей папки:\n' + '\n'.join([i for i in os.listdir(os.getcwd())])) if command == '2' else False
    x = command_3(input('Введите название папки: ')) if command == '3' else False
    x = command_4(input('Введите название папки: ')) if command == '4' else False
    x = zadanie_easy_1_1() if command == '5' else False
    x = zadanie_easy_1_2() if command == '6' else False
    x = zadanie_easy_2() if command == '7' else False
    x = zadanie_easy_3() if command == '8' else False
    command = get_command()
print('До новых встреч')