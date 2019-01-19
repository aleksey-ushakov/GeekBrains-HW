__author__ = 'Ушаков Алексей Валериевич'

# Задание-1:
# Реализуйте описаную ниже задачу, используя парадигмы ООП:
# В школе есть Классы(5А, 7Б и т.д.), в которых учатся Ученики.
# У каждого ученика есть два Родителя(мама и папа).
# Также в школе преподают Учителя. Один учитель может преподавать 
# в неограниченном кол-ве классов свой определенный предмет. 
# Т.е. Учитель Иванов может преподавать математику у 5А и 6Б,
# но больше математику не может преподавать никто другой.


# Выбранная и заполненная данными структура должна решать следующие задачи:
# 1. Получить полный список всех классов школы
# 2. Получить список всех учеников в указанном классе
#  (каждый ученик отображается в формате "Фамилия И.О.")
# 3. Получить список всех предметов указанного ученика 
#  (Ученик --> Класс --> Учителя --> Предметы)
# 4. Узнать ФИО родителей указанного ученика
# 5. Получить список всех Учителей, преподающих в указанном классе

class school:
    def __init__(self, school_name, student_list=[], teacher_list=[]):
        self.school_name = school_name
        self.student_list = student_list
        self.teacher_list = teacher_list


class People:
    def __init__(self, surname, name, patronim, birth_date):
        self.name = name
        self.surname = surname
        self.patronim = patronim
        self.birth_date = birth_date

    def get_fio(self):
        return self.surname + ' ' + self.name[0] + '.' + self.patronim[0] + '.'


class Student(People):
    def __init__(self, surname, name, patronim, birth_date, class_room_name, mama='', papa=''):
        People.__init__(self, surname, name, patronim, birth_date)
        self.class_room_name = class_room_name
        self.class_room_grade = int(class_room_name.split()[0])
        self.class_room_char = class_room_name.split()[1]
        self.mama = mama
        self.papa = papa


class teacher(People):
    def __init__(self, surname, name, patronim, birth_date, subject, teach_classes=[]):
        People.__init__(self, surname, name, patronim, birth_date)
        self.subject = subject
        self.teach_classes = teach_classes


my_school = school("Гимназия №8")
my_school.student_list.append(Student('Иванов', 'Александр', 'Петрович', '10.11.1998', '5 А', 'Баранова Виктория Андреевна', 'Иванов Петр Васильевич'))
my_school.student_list.append(Student('Петров', 'Алексей', 'Иванович', '03.09.1996', '7 Б', 'Петрова Мария Ивановна', 'Птеров Иван Сергеевич'))
my_school.student_list.append(Student('Сидоров', 'Фома', 'Константинович', '01.05.1996', '7 Б', 'Сидорова Анна Анатолиевна', 'Сидоров Константин Сергеевич'))
my_school.student_list.append(Student('Сидоров', 'Сергей', 'Константинович', '30.07.1995', '8 В', 'Сидорова Анна Анатолиевна', 'Сидоров Константин Сергеевич'))
my_school.student_list.append(Student('Иванов', 'Константин', 'Петрович', '10.11.1995', '8 В', 'Баранова Виктория Андреевна', 'Иванов Петр Васильевич'))

my_school.teacher_list.append(teacher('Карамзин', 'Фархуд', 'Сумуилович', '01.01.1961', 'Математика', ['5 А', '7 Б', '8 В']))
my_school.teacher_list.append(teacher('Достоевский', 'Федор', 'Михайлович', '01.01.1861', 'История', ['5 А', '7 Б', '8 В']))

# 1. Получить полный список всех классов школы
print('1. Полный список всех классов школы: ', ', '.join({i.class_room_name for i in my_school.student_list}))
my_class = '7 Б'
print('2. Cписок всех учеников в классе {}:\n    '.format(my_class) + '\n    '.join([i.get_fio() for i in my_school.student_list if i.class_room_name == my_class]))

my_student = 'Сидоров Фома Константинович'
my_class = [i.class_room_name for i in my_school.student_list if i.surname == my_student.split()[0] and i.name == my_student.split()[1] and i.patronim == my_student.split()[2]][0]
print('3. Cписок всех предметов ученика {}:\n    '.format(my_student) + '\n    '.join([i.subject for i in my_school.teacher_list if my_class in i.teach_classes]))
print('4. Родители ученика {}:\n    '.format(my_student) + '\n    '.join(['Мама - ' + [i.mama for i in my_school.student_list if i.surname == my_student.split()[0] and i.name == my_student.split()[1] and i.patronim == my_student.split()[2]][0], 'Папа - ' + [i.papa for i in my_school.student_list if i.surname == my_student.split()[0] and i.name == my_student.split()[1] and i.patronim == my_student.split()[2]][0]]))

my_class = '7 Б'
print('5. Cписок всех учителей преподающих в классе {}:\n    '.format(my_class) + '\n    '.join(['ФИО Преподавателя: {:<20} Предмет: {:<20}'.format(i.get_fio(), i.subject) for i in my_school.teacher_list if my_class in i.teach_classes]))