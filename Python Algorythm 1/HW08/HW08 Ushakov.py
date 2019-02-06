#HW06 Aleksey Ushakov
#Python 3.7 64bit

import random
import timeit
import math
import numpy
from memory_profiler import profile
import timeit
import datetime
import hashlib
import collections

def time(func):
    def t(*args, **kwargs):
        print(datetime.time())
        res = func(*args, **kwargs)
        print(datetime.time())
        return res
    return t





print("""\n\nЗадача 1
1. Определение количества различных подстрок с использованием хэш-функции.
Пусть дана строка S длиной N, состоящая только из маленьких латинских букв.
Требуется найти количество различных подстрок в этой строке.
""")
n = 200
s = ''.join([chr(random.randint(ord("a"), ord("z"))) for i in range(n)])
print("Оригинальная строка:", s)

sub_s = set()
sub_s_hash = set()


for i in range(n):
    for j in range(i+1, n+1):
            sub_s.add(s[i:j])
            #sub_s_hash.add(hashlib.sha1(bytes(s[i:j], encoding="UTF-8")).hexdigest())

print("Кол-во подстрок:", len(sub_s))
#print("Кол-во подстрок:", len(sub_s_hash))
print("Вывод: результат получается одинаковый, но время затраченное на работу с хэшем вышло значительно больше чем без хэша. Видимо встроенные коллекция множества куда быстрее работает чем SHA1 ")

#print("Подстроки:\n" + "\n".join(sorted(list(sub_s))))

print("""\n\nЗадача 2
2. Закодируйте любую строку из трех слов по алгоритму Хаффмана.
""")

s = "мама мыла раму"

f_s = collections.Counter()
#f_s = [[i for i in s, count(i)/] ]
for i in s:
    f_s[i] += 1

for i in f_s :
    print(f_s[i])
print(f_s)

