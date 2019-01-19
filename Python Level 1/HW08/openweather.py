__author__ = 'Ушаков Алексей Валериевич'

"""
== OpenWeatherMap ==

OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.

Необходимо решить следующие задачи:

== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.

    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID, 
    используя дополнительную библиотеку GRAB (pip install grab)

        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up

        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in

        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys

        Ключ имеет смысл сохранить в локальный файл, например, "app.id"


== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz

    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка 
     (воспользоваться модулем gzip 
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)

    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}


== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a

    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a

    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a


    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}    


== Сохранение данных в локальную БД ==    
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):

    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных

2. Выводить список стран из файла и предлагать пользователю выбрать страну 
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))

3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.


При работе с XML-файлами:

Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с пространствами имен удобно пользоваться такими функциями:

    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''

    tree = ET.parse(f)
    root = tree.getroot()

    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}

    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
"""

import sqlite3
import os
import requests
import json
import shutil
import gzip
import multiprocessing

# moscow 524901
appid = "644b15ff9d326552706df0bbb7e930a1" # oleksiy.ushakov@gmail.com
appid = '1390230d256a568a0bdf22e7dbce8c87' # дал преподаватель
appid = '47793943909f02040936b800b849efcf' # дал преподаватель

class MainMenu:

    def __init__(self):
        self.menu = {
            '1': ['[1] Скачать в базу данные о погоде в городах выбранной стране', self.menu_import_weather_by_country],
            '2': ['[2] Показать данные OpenWeather по погоде в городе и сохранить в базе', self.menu_print_online_weather_by_city],
            '3': ['[3] Показать данные в базе по погоде в выбранном городе', self.menu_print_db_weather_by_city],
            '4': ['[4] Показать все данные базы по погоде', self.menu_print_db_weather_all],
            '0': ['[0] Выйти из программы', self.menu_finish]}
        self.finish = False

    def __del__(self):
        print('\nДо новых встреч!')

    def get_command(self):
        command = ''
        while command not in self.menu.keys():
            print('\n' * 2 + '\n'.join([self.menu.get(i)[0] for i in self.menu.keys()]))
            command = input("Введите номер команды из списка выше [0-" + max(self.menu.keys()) + "]:")
        print()
        command = self.menu.get(command)[1]
        return command()

    def menu_import_weather_by_country(self, country_code="Auto"):
        try:
            country_code = my_db.get_country_code() if country_code == "Auto" else country_code
            # ограничиваемся 20 кодами, т.к. если превысить лимит в 60 запросов в минуту appid будет заблокирован
            city_id_list = my_db.get_city_id_list_by_country(country_code)[0:20]
            if city_id_list:
                if len(city_id_list) > 1 and get_answer_y_n("Сделать запросы к серверу параллельно? [Y/N]"):
                    p = multiprocessing.Pool(len(city_id_list) if len(city_id_list) < 100 else 100)
                    weather_list = p.map(get_online_weather, city_id_list)
                    p.close()
                else:
                    weather_list = [get_online_weather(i) for i in city_id_list]
                my_db.write_city_weather_list(weather_list)
                return True
            else:
                return False
        except Exception as e:
            print("Произошла ошибка при загрузке online данных и записи их в базу:", e)

    def menu_print_online_weather_by_city(self):
        weather_list = [get_online_weather()]
        my_db.print_json_weather(weather_list[0])
        my_db.write_city_weather_list(weather_list)

    def menu_print_db_weather_by_city(self):
        my_db.print_city_weather_from_db()

    def menu_print_db_weather_all(self):
        my_db.cursor.execute("SELECT * FROM 'weather_table' ORDER BY city_name, weather_date DESC")
        result = list(my_db.cursor.fetchall())
        result = [list(i) for i in result]
        print_table([['City ID', 'City Name', 'Date', 'Temperature', 'Weather ID']] + result, "Данные в базе",
                    "  " + chr(124) + "  ", True)

    def menu_finish(self):
        self.finish = True


class WeatherDB:
    # создание базы данных если ее нет, загрузка в базу данных из json файла для ускорения работы
    def __init__(self, path_db):
        self.path_db = path_db
        if not os.path.exists(self.path_db):
            try:
                self.conn = sqlite3.connect(self.path_db)
                self.cursor = self.conn.cursor()
                # создание таблицы погоды
                self.cursor.executescript("""BEGIN TRANSACTION; CREATE TABLE "weather_table" (
                    'city_id'       INTEGER,
                    'city_name'     TEXT,
                    'weather_date'  DATE,
                    'weather_temp'  INTEGER,
                    'weather_id'    INTEGER);
                    COMMIT; """)
                # создание таблицы городов
                self.cursor.executescript("""BEGIN TRANSACTION; CREATE TABLE    "city_table" (
                    'city_id'       INTEGER,
                    'city_name'     TEXT,
                    'country_code'  TEXT,
                    'coord_lon'     TEXT,
                    'coord_lat'     TEXT);        
                    COMMIT; """)
                print('Создана база данных для сохраниения данных о погоде:\n' + path_db)
                self.download_city_list_from_json_file()
            except Exception as e:
                print("Произошла ошибка при формировании базы данных для сохраниения данных о погоде:", e)

        else:
            self.conn = sqlite3.connect(self.path_db)
            self.cursor = self.conn.cursor()

        self.city_list = self.get_city_list()
        if len(self.city_list) == 0:
            self.download_city_list_from_json_file()
            self.city_list = self.get_city_list()
        self.country_list = list({i[2] for i in self.city_list if i[2] != ''})
        self.country_list.sort()

    def __del__(self):
        self.conn.close()
        print("База закрыта")

    def get_city_list(self):
        try:
            self.cursor.execute("SELECT * FROM 'city_table'")
            result = list(self.cursor.fetchall())
            result = [list(i) for i in result]
            print('Городов в базе: ', len(result))
            self.city_list = result
            return result
        except Exception as e:
            print("Не удалось сформирровать список городов из таблицы базы данных", e)
            return False

    def get_country_code(self):
        country_list = list({i[2] for i in self.city_list if i[2] != ''})
        country_list.sort()
        answer_country = ''
        while answer_country not in (country_list + ['q', 'Q', 'й', 'Й']) or not answer_country:
            print_list_by_column(country_list, 20, 'Доступные коды стран')
            answer_country = input('Введите код страны из списка выше, или введите [Q] для отказа от операции:').upper()
        return answer_country if answer_country not in ['q', 'Q', 'й', 'Й'] else False

    def get_city_id(self, country_code="Auto"):
        country_code = self.get_country_code() if country_code == "Auto" else country_code
        if country_code:
            city_column = ['{} - {}'.format(i[1], i[0]) for i in self.city_list if
                           i[2] == country_code and i[1] != '-' and i[1] != '']
            city_column.sort()
            answer_city_id = ''
            while answer_city_id not in [str(i[0]) for i in self.city_list if i[2] == country_code] + ['q', 'Q', 'й',
                                                                                                       'Й']:
                print_list_by_column(city_column, 5, 'Доступные города')
                answer_city_id = input('Введите код города из списка, или введите [Q] для отказа от операции:\n')
            return answer_city_id if answer_city_id not in ['q', 'Q', 'й', 'Й'] else False
        else:
            return False

    def get_city_id_list_by_country(self, country_code="Auto"):
        country_code = self.get_country_code() if country_code == "Auto" else country_code
        return [i[0] for i in self.city_list if i[2] == country_code] if country_code else False

    def download_city_list_from_json_file(self):
        try:
            my_path = os.path.join(os.getcwd(), 'city.list.json')
            if not os.path.exists(my_path):
                if get_answer_y_n("Файл " + my_path + " не найден скачать его [Y/N]?"):
                    self.download_city_list_json_file()
                else:
                    print("Таблицы городов из JSON файла не сформирована. Продолжать работу с базой нет возможности.")
                    my_menu.finish = True
            if os.path.exists(my_path):
                print('Обработка JSON файла с городами...', end='')
                with open(my_path, 'r', encoding='UTF-8') as my_file:
                    file_string = my_file.read()
                my_file.close()
                # автоматически парсить файл не получается т.к. он содержит ошибки вроде лишних символов, потому, чищу файл самостоятельно
                file_string = file_string[2:]
                for i in ['\n', ']    }  }', ']', '      ', '    ']:
                    file_string = file_string.replace(i, '')
                # разбиваю на строки и уже строки преобразую в словари python с структурой city_list_json: 'id':, 'name':, 'country':, 'coord': {'lon':, 'lat':}
                city_list_json = [json.loads(i) for i in file_string.split(',  ')]
                city_list = [
                    [i.get('id'), i.get('name'), i.get('country'), i.get('coord').get('lon'), i.get('coord').get('lat')]
                    for i in city_list_json]
                if city_list:
                    print('Формирование таблицы городов из JSON файла для ускорения работы...', end="")
                    SQL_script = "BEGIN TRANSACTION; INSERT INTO 'city_table'  (city_id, city_name, country_code, coord_lon, coord_lat) VALUES "
                    SQL_script += ', '.join(['(' + str(i[0]) + ', "' + str(i[1]) + '", "' + str(i[2]) + '", "' + str(
                        i[3]) + '", "' + str(i[4]) + '")' for i in city_list])
                    SQL_script += "; COMMIT;"
                    self.cursor.executescript(SQL_script)
                print(' список городов из JSON файла перенесен в базу')
            else:
                pass
        except Exception as e:
            print("Произошла ошибка при формировании таблицы городов из JSON файла: ", e)

    def download_city_list_json_file(self):  # загрузка файла city.list.json из интернета в рабочую директорию
        try:
            file_path = os.path.join(os.getcwd(), 'city.list.json.gz')
            link = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
            print('Скачивание файла', link, '... ', end='')
            filereq = requests.get(link, stream=True)
            with open(file_path, "wb") as receive:
                shutil.copyfileobj(filereq.raw, receive)
            del filereq
            print('завершено успешно')

            print('Распаковка файла', file_path, '... ', end='')
            with gzip.open(file_path, 'rb') as arc_file, open(os.path.join(os.getcwd(), 'city.list.json'),'wb') as dest:
                shutil.copyfileobj(arc_file, dest)
            print('завершено успешно')
            return True

        except Exception as e:
            link = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
            print("\nПроизошла ошибка при загрузке и распаковке файла", link, e)
            return False

    def print_json_weather(self, json_w):
        if json_w:
            weather_str = '\nДанные о погоде в городе ' + str(json_w['name']) + ' (' + str(str(json_w['id'])) + '):\n'
            for i in json_w.keys():
                weather_str += '    ' + str(i) + ': ' + str(json_w.get(i)) + '\n'
            print(weather_str)

    def print_city_weather_from_db(self, city_id='Auto'):
        city_id = self.get_city_id() if city_id == "Auto" else city_id
        if city_id:
            try:
                self.cursor.execute(
                    "SELECT * FROM 'weather_table' WHERE city_id = " + str(city_id) + " ORDER BY weather_date DESC")
                result = list(my_db.cursor.fetchall())
                if result:
                    result = [['City ID', 'City Name', 'Date', 'Temperature', 'Weather ID']] + [list(i) for i in result]
                    print_table(result, "\nДанные в базе", "  " + chr(124) + "  ", True)
                else:
                    if get_answer_y_n('Данных по городу ' + city_id + ' не найдено. Загрузить online данные [Y/N]'):
                        json_weather = get_online_weather(city_id)
                        self.write_city_weather_list([json_weather])
                        self.print_json_weather(json_weather)
                    else:
                        return False
                return True
            except Exception as e:
                print("Не удалось сформирровать список городов из таблицы базы данных", e)
                return False

    def write_city_weather_list(self, weather_list):
        if weather_list:
            try:
                print('\nДобавление запис{} в базу данных...'.format('и' if len(weather_list) == 1 else 'ей'), end="")
                SQLscript = "BEGIN TRANSACTION; DELETE FROM 'weather_table' WHERE city_id in (" + ', '.join(
                    [str(i["id"]) for i in weather_list]) + ") AND weather_date = date('now'); COMMIT;"
                my_db.cursor.executescript(SQLscript)
                SQLscript = "BEGIN TRANSACTION; INSERT INTO 'weather_table'  (city_id, city_name, weather_date, weather_temp, weather_id) VALUES "
                SQLscript += ', '.join(['(' + str(i["id"]) + ', "' + str(i["name"]) + '", date("now"),' + str(
                    int(i["main"]["temp"])) + ', ' + str(int(i["weather"][0]["id"])) + ')' for i in weather_list])
                SQLscript += "; COMMIT;"
                self.cursor.executescript(SQLscript)
                print('запис{} добавлен{}!'.format('ь' if len(weather_list) == 1 else 'и',
                                                   'а' if len(weather_list) == 1 else 'ы'))
                return True
            except Exception as e:
                print("Не удалось записать даннве в базу: ", e)
                return False
        else:
            return False

    class CityWeather:

        def __init__(self, city_id='Auto'):
            self.city_id = my_db.get_city_id() if city_id == "Auto" else city_id
            print("Запрос данных по городу:", self.city_id, "...")
            res = requests.get("http://ru.api.openweathermap.org/data/2.5/weather",
                               params={'id': self.city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            self.json = data
            self.city_name = data["name"]
            self.date = None  # нужно сохранить текущую дату и время
            self.coord_lon = data["coord"]["lon"]
            self.coord_lat = data["coord"]["lat"]
            self.weather_id = data["weather"][0]["id"]
            self.weather_main = data["weather"][0]["main"]
            self.weather_description = data["weather"][0]["description"]
            self.weather_icon = data["weather"][0]["icon"]
            self.base = data["base"]
            self.main_temp = data["main"]["temp"]
            self.main_pressure = data["main"]["pressure"]
            self.main_humidity = data["main"]["humidity"]
            self.main_temp_min = data["main"]["temp_min"]
            self.main_temp_max = data["main"]["temp_max"]
            self.wind_speed = data["wind"]['speed']
            self.sys_message = data["sys"]['message']
            self.sys_country = data["sys"]['country']
            self.sys_sunrise = data["sys"]['sunrise']
            self.sys_sunset = data["sys"]['sunset']
            self.cod = data["cod"]
            print("Данные по городу:", self.city_id, "(", self.city_name, ") получены")


def get_online_weather(city_id):
    if city_id:
        try:
            print("Запрос online данных по городу:", city_id, "...")
            result = requests.get("http://ru.api.openweathermap.org/data/2.5/weather",
                                   params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = result.json()
            print("Данные по городу:", data["name"], "(", data["id"], ") - получены")
            return data
        except Exception as e:
            print("Ошибка при получении online данных:", e)
            return False
    else:
        return False


def print_table(table, title, delimiter, header_true_false=False):
    """
    Print table ([['', ''..''],['', ''..'']...['', ''..'']) in readable way, with proper columns width and alignment
    :param table: list of lists
    :return: none
    """

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    import math
    column_width = [max([len(str(i[j])) for i in table]) for j in range(len(table[0]))]

    print(title + ':')
    for i in range(len(table)):
        string_len = 0
        for j in range(len(table[i])):
            alignment = '>' if is_number(str(table[i][j])) else '<'
            string_format = '{:' + alignment + str(column_width[j]) + '}'
            print(string_format.format(table[i][j]), end=(delimiter if j < len(table[i]) - 1 else '\n'))
            string_len += column_width[j] + (len(delimiter) if j < len(table[i]) - 1 else 0)
        string_len = print('-' * string_len) if i == 0 and header_true_false else print('', end='')
    print()


def print_list_by_column(column, column_number=1, title=''):
    if len(column) % column_number != 0:
        for i in range(column_number - len(column) % column_number):
            column.append('')
    column_table = [[column[i * (len(column) // column_number) + j] for i in range(column_number)] for j in
                    range(len(column) // column_number)]
    print_table(column_table, title, '  ' + chr(124) + '  ', False)


def get_answer_y_n(msg='[Y/N]?'):
    answer = input(msg)
    while answer not in ['Y', 'y', 'Н', 'н', 'N', 'n', 'Т', 'т']:
        answer = input()
    if answer in ['Y', 'y', 'Н', 'н']:
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        my_menu = MainMenu()
        my_db = WeatherDB(os.path.join(os.getcwd(), 'my_weather.db'))
        while not my_menu.finish:
            my_menu.get_command()
    except Exception as e:
        print("Произошла ошибка:", e)
    my_db.conn.close()