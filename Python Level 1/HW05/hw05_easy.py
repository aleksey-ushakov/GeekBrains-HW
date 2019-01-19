# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.
import os
import sys
import shutil


def zadanie_easy_1_1():
    for i in [os.path.join(os.getcwd(), 'dir_' + str(i + 1)) for i in range(9)]:
        try:
            os.mkdir(i)
            print('\x1b[32mДиректория {} создана\x1b[0m'.format(i))
        except OSError:
            print('\x1b[31mДиректория {} уже существует\x1b[0m'.format(i))


def zadanie_easy_1_2():
    delete = ''
    while delete not in ['y', 'n', 'Y', 'N', 'Н', 'н', 'Т', 'т']:
        delete = input('Удалить директории dir_1 - dir_9 из текущей папки [y/n] ?')

    if delete in ['Y', 'y', 'Н', 'н']:
        for i in [os.path.join(os.getcwd(), 'dir_' + str(i + 1)) for i in range(9)]:
            if os.path.exists(i):
                try:
                    os.rmdir(i)
                    print('\x1b[32mДиректория {} удалена\x1b[0m'.format(i))
                except OSError:
                    print('\x1b[31mПроизошла ошибка при удалении директория {}\x1b[0m'.format(i))
            else:
                print('\x1b[31mДиректрии {} не существует\x1b[0m'.format(i))

# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.


def zadanie_easy_2():
    print('Папки текущей директории:\n' + '\n'.join([i for i in os.listdir(os.getcwd()) if os.path.isdir(i)]))

# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.


def zadanie_easy_3():
    print('Создана копия файла из которого запущен данный скрипт: ', shutil.copy(__file__, os.path.join(os.path.dirname(__file__), os.path.basename(__file__)[:os.path.basename(__file__).find('.')]+'-copy'+ os.path.basename(__file__)[os.path.basename(__file__).find('.'):])))