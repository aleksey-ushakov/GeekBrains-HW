#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87      
      16 49    55 77    88    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""
import random


class loto_card:
    # При инициации экземпляра класса loto_card генерируется рандомная карточка, которая содержит список из 15 чисел,
    # а также списко из 27 элементов для отображения как карточка
    def __init__(self):
        numbers = random.sample(range(1, 91), 15)
        numbers = sorted(numbers[:5]) + sorted(numbers[5:10]) + sorted(numbers[10:15])
        card = random.sample([1, 1, 1, 1, 1, '', '', '', ''], 9) + random.sample([1, 1, 1, 1, 1, '', '', '', ''], 9) + random.sample([1, 1, 1, 1, 1, '', '', '', ''], 9)
        i = 0
        for num in range(len(card)):
            if card[num]:
                card[num] = numbers[i]
                i += 1
        card = [[i, True] for i in card]

        self.numbers = numbers
        self.order = card

    # функция помечает номер в карточке как вычеркнутый если он есть и возвращает True. если номера нет возвращает False
    def cross_number(self, number):
        if number in self.numbers:
            for i in range(27):
                self.order[i][1] = False if self.order[i][0] == number else self.order[i][1]
            return True
        else:
            return False

    @property
    # функция/атрибут для определения сколько осталось незачеркнутых чисел в карточке
    def numbers_left(self):
        n = 0
        for i in range(27):
            n = (n+1) if self.order[i][0] and self.order[i][1] else n
        return n


class loto_game:
    # При старте выдается по карте компьютеру и игроку, а также формируется список с бочонками
    def __init__(self):
        self.computer_card = loto_card()
        self.player_card = loto_card()
        self.moves_left = list(range(1, 91))
        self.moves_done = []
        self.finished = False
        print("Ну чтож, начнем игру в РУССКОЕ ЛОТО!!!\n")
        self.move
    # Выводит сообщение при окончании игры
    def __del__(self):
        print('Спасибо за игру')

    # Функция для того, чтоб сделать ход
    def move(self):
        x = random.sample(self.moves_left, 1)[0]
        print('Новый' if len(self.moves_done) else 'Первый', 'бочонок: {} (осталось {})'.format(x, len(self.moves_left)))
        self.moves_left.remove(x)
        self.moves_done.append(x)
        self.print_cards()
        self.computer_card.cross_number(x)
        answer = ''

        while answer not in ['Y','y','Н','н','N','n','Т','т']:
            answer = input ('Зачеркнуть число? (y/n)')

        if answer in ['Y','y','Н','н'] and not self.player_card.cross_number(x):
            print("\nНомера {} нет в Вашей карточке\nGAME OVER".format(x))
            self.finished = True
        if answer in ['N','n','Т','т'] and self.player_card.cross_number(x):
            print("\nНомер {} был в Вашей карточке\nGAME OVER".format(x))
            self.finished = True
        if not self.finished and (not self.computer_card.numbers_left or not self.player_card.numbers_left):
            if self.computer_card.numbers_left != self.player_card.numbers_left:
                message = print(
                    "\n\nПоздравляю Вы выиграли - Вы вычеркнули все числа") if not self.player_card.numbers_left else print("\n\nВы проиграли, компьютер вычеркнул все чисела")
            else:
                print("\n\nНичья!!! Вы и компьютер завершили партию одновременно")
            self.print_cards()
            self.finished = True
        message = print("Играем дальше!\nОсталось чисел:\nУ Вас - {} \nУ компьютера - {}\n\n".format(self.player_card.numbers_left, self.computer_card.numbers_left)) if not self.finished else False

    # функция для вывода карточки в заданном формате (удобнее играть когда карты выводятся параллельно)
    def print_cards(self):
        print('------ Ваша карточка -----' + ' ' * 10 + '-- Карточка компьютера ---')
        for j in range(3):
            player_line = ' '.join(['{:>2}'.format(self.player_card.order[j * 9 + i][0]) if self.player_card.order[j * 9 + i][1] else ' -' for i in range(9)])
            computer_line = ' '.join(['{:>2}'.format(self.computer_card.order[j * 9 + i][0]) if self.computer_card.order[j * 9 + i][1] else ' -' for i in range(9)])
            print(player_line+ ' ' * 10 + computer_line)
        print('--------------------------' + ' ' * 10 + '--------------------------')


my_game = loto_game()
while not my_game.finished:
    my_game.move()
