
""" OpenWeatherMap (экспорт)

Сделать скрипт, экспортирующий данные из базы данных погоды, 
созданной скриптом openweather.py. Экспорт происходит в формате CSV или JSON.

Скрипт запускается из командной строки и получает на входе:
    export_openweather.py --csv filename [<город>]
    export_openweather.py --json filename [<город>]
    export_openweather.py --html filename [<город>]
    
При выгрузке в html можно по коду погоды (weather.id) подтянуть 
соответствующие картинки отсюда:  http://openweathermap.org/weather-conditions

Экспорт происходит в файл filename.

Опционально можно задать в командной строке город. В этом случае 
экспортируются только данные по указанному городу. Если города нет в базе -
выводится соответствующее сообщение.

"""

import sqlite3
import os
import requests
import json
import csv
import sys

def print_help():
    print('Cкрипт, экспортирует данные из базы данных погоды, созданной скриптом openweather.py.')
    print('Экспорт происходит в формате CSV или JSON.')
    print('Скрипт запускается из командной строки и получает на входе два обязательных и один опциональный аргумент:')
    print('export_openweather.py --csv filename [<city_id>]')
    print('export_openweather.py --json filename [<city_id>]')


def export_weather(file_name, file_format, city_id):
    path_db = os.path.join(os.getcwd(), 'my_weather.db')
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if city_id:
        cursor.execute("SELECT * FROM 'weather_table' WHERE city_id = " + str(city_id))
    else:
        cursor.execute("SELECT * FROM 'weather_table'")
    data = list(cursor.fetchall())
    conn.close
    data = [list(i) for i in data]

    with open(file_name, "w", newline='', encoding='UTF-8') as export_file:
        if file_format == '--csv':
            writer = csv.writer(export_file, delimiter=',')
            for i in data:
                writer.writerow(i)
        elif file_format == '--json':
            export_file.write(str([{'city_id':i[0], 'city_name':i[1],'date':i[2],'temperature':i[3],'weather_id':i[4],} for i in data]))
    for i in data:
        print(i)

try:
    city_id = sys.argv[3]
except IndexError:
    city_id = ''

try:
    file_name = sys.argv[2]
except IndexError:
    file_name = ''

try:
    file_format = sys.argv[1]
except IndexError:
    file_format = ''


if file_format not in ['--csv', '--json'] or not file_name:
    print_help()
else:
    export_weather(os.path.join(os.getcwd(), file_name), file_format, city_id)