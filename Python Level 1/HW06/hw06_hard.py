__author__ = 'Ушаков Алексей Валериевич'

# Задание-1: Решите задачу (дублированную ниже):

# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки они получают
# удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# С использованием классов.
# Реализуйте классы сотрудников так, чтобы на вход функции-конструктора
# каждый работник получал строку из файла


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


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


import os


class workers_and_hours:
    def __init__(self, worker_list=[], hour_worked_list=[]):
        self.worker_list = worker_list
        self.hour_worked_list = hour_worked_list


    def calculate_salary(self):
        for i in self.worker_list:
            i.hours_worked = [j.hours_worked for j in self.hour_worked_list if j.surname == i.surname and j.name == i.name][0]
            i.calculated_salary = round(i.standard_salary - (i.norm - i.hours_worked) * (1 if i.norm > i.hours_worked else 2) * (i.standard_salary / i.norm),2)
        captions = [['Имя', 'Фамилия', 'Зарплата', 'Должность', 'Норма_часов', 'Отработано', 'Начислено']]
        print_table(captions + [[i.name, i.surname, i.standard_salary, i.position, i.norm, i.hours_worked, i.calculated_salary] for i in worker_list], 'Ведомость расчета заработной платы', '  ' + chr(124) + '  ', True)


class worker:
    def __init__(self, file_string):
        self.name = file_string.split()[0]
        self.surname = file_string.split()[1]
        self.standard_salary = float(file_string.split()[2])
        self.position = file_string.split()[3]
        self.norm = float(file_string.split()[4])
        self.hours_worked = 0
        self.calculated_salary = 0


class hours_worked:
    def __init__(self, file_string):
        self.name = file_string.split()[0]
        self.surname = file_string.split()[1]
        self.hours_worked = float(file_string.split()[2])


my_path = os.path.join(os.getcwd(), 'data', 'workers')
with open(my_path, 'r', encoding='UTF-8') as my_file:
    file_lines = my_file.readlines()
    file_lines = file_lines[1:]
    worker_list = [worker(i) for i in file_lines]
my_file.close()

my_path = os.path.join(os.getcwd(), 'data', 'hours_of')
with open(my_path, 'r', encoding='UTF-8') as my_file:
    file_lines = my_file.readlines()
    file_lines = file_lines[1:]
    hours_worked_list = [hours_worked(i) for i in file_lines]
my_file.close()

workers_data = workers_and_hours(worker_list, hours_worked_list)
workers_data.calculate_salary()
