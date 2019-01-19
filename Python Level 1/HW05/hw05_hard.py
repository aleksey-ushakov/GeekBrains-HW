# Задание-1:
# Доработайте реализацию программы из примера examples/5_with_args.py,
# добавив реализацию следующих команд (переданных в качестве аргументов):
#   cp <file_name> - создает копию указанного файла
#   rm <file_name> - удаляет указанный файл (запросить подтверждение операции)
#   cd <full_path or relative_path> - меняет текущую директорию на указанную
#   ls - отображение полного пути текущей директории
# путь считать абсолютным (full_path) -
# в Linux начинается с /, в Windows с имени диска,
# все остальные пути считать относительными.

# Важно! Все операции должны выполняться в той директории, в который вы находитесь.
# Исходной директорией считать ту, в которой был запущен скрипт.

# P.S. По возможности, сделайте кросс-платформенную реализацию.

import os
import sys
import shutil


def print_help():
    print("help - получение справки")
    print("mkdir <dir_name> - создание директории")
    print("ping - тестовый ключ")
    print("cp <file_name> - создает копию указанного файла")
    print("rm <file_name> - удаляет указанный файл (запросить подтверждение операции)")
    print("cd <full_path or relative_path> - меняет текущую директорию на указанную")
    print("ls - отображение полного пути текущей директории")


def make_dir():
    if not dir_name:
        print("Необходимо указать имя директории вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.mkdir(dir_path)
        print('директория {} создана'.format(dir_name))
    except OSError:
        print('директория {} уже существует'.format(dir_path))


def ping():
    print("pong")


def copy_path():
    if not dir_name:
        print("Необходимо указать имя фaйла для копирования вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    copy_dir_path = os.path.join(os.path.dirname(dir_path), os.path.basename(dir_path)[:os.path.basename(dir_path).find('.')]+'-copy'+ os.path.basename(dir_path)[os.path.basename(dir_path).find('.'):])
    try:
        shutil.copy(dir_path, copy_dir_path)
        print('Фаил {} скопирован в {}'.format(dir_name, copy_dir_path))
    except Error:
        print('Фаил {} не получилось скопировать'.format(dir_path))


def remove_file():
    if not dir_name:
        print("Необходимо указать имя фaйла для удаления вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.remove(dir_path)
        print('Фаил {} удален'.format(dir_name))
    except OSError:
        print('Фаил {} не получилось удалить'.format(dir_path))

def change_direcotry():
    if not dir_name:
        print("Необходимо указать имя директории вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.chdir(dir_path)
        print('Вы перешли в директорию {}'.format(os.getcwd()))
    except OSError:
        print('Не удалось перейти в директорию {}'.format(dir_path))


def print_cwd():
    print('Полный путь текущей директории: ', os.getcwd())

do = {
    "help": print_help,
    "mkdir": make_dir,
    "ping": ping,
    "cp": copy_path,
    "rm": remove_file,
    "cd": change_direcotry,
    "ls": print_cwd
}

print('sys.argv = ', sys.argv)

try:
    dir_name = sys.argv[2]
except IndexError:
    dir_name = None

try:
    key = sys.argv[1]
except IndexError:
    key = None


if key:
    if do.get(key):
        do[key]()
    else:
        print("Задан неверный ключ")
        print("Укажите ключ help для получения справки")
