import tkinter as tk
import turtle
import random
import math
import datetime
import os
import multiprocessing
import itertools

script_version = '1.0'

def draw_line(dot_list, draw_lines_true_false, draw_dots_true_false, draw_dots_coordinates_True_False):
    """
    Функция рисует линии между точками входного списка в той последовательности в которой они указану
    :param dot_list: список координат точек: [[x1, y1],[x2, y2],[x3, y3],...,[xn, yn]]
    :param draw_lines_true_false:
    :param draw_dots_true_false:
    :param draw_dots_coordinates_True_False:
    :return: None
    """
    for i in range(len(dot_list)-1):
        turtle.penup()
        turtle.goto(dot_list[i][0] - 2, dot_list[i][1] + 3)
        tool = turtle.write(str(i) + " " + str(dot_list[i])) if draw_dots_coordinates_True_False else False
        turtle.goto(dot_list[i][0], dot_list[i][1])
        tool = turtle.dot(5, 'blue') if draw_dots_true_false else False
        turtle.pendown()
        tool = turtle.goto(dot_list[i+1][0], dot_list[i+1][1]) if draw_lines_true_false else False
        turtle.penup()
        turtle.goto(dot_list[i+1][0] - 2, dot_list[i+1][1] + 3)
        if dot_list[i+1] not in dot_list[:i]:
            tool = turtle.write(str(i+1) + " " + str(dot_list[i+1])) if draw_dots_coordinates_True_False else False


def draw_axes(x_max, y_max, big_scale, small_scale):
    """
    Функция прорисовывает оси координат с шкалой основных и второстепенных делений
    :param x_max:
    :param y_max:
    :param big_scale:
    :param small_scale:
    :return: None
    """
    turtle.pencolor('black')
    draw_line([[-x_max, 0], [x_max, 0]], True, False, False)
    for i in range(-x_max, x_max + 1, big_scale):
        draw_line([[i, 0 - 5], [i, 0 + 5]], True, False, False)
    for i in range(-x_max, x_max + 1, small_scale):
        draw_line([[i, 0 - 2], [i, 0 + 2]], True, False, False)
    draw_line([[0, -y_max], [0, y_max]], True, False, False)
    for i in range(-y_max, y_max + 1, big_scale):
        draw_line([[0 - 5, i], [0 + 5, i]], True, False, False)
    for i in range(-y_max, y_max + 1, small_scale):
        draw_line([[0 - 2, i], [0 + 2, i]], True, False, False)


def slice_square(start, step, tolerance):
    global slices
    normal_square = abs(step * (func(start + step) - func(start))/2)
    half_step = step / 2
    precise_square = abs(half_step * (func(start + half_step) - func(start)) / 2) + abs(half_step * (func(start + half_step * 2) - func(start + half_step)) / 2) + abs(half_step * (func(start + half_step) - func(start)))
    if abs((normal_square + step) / (precise_square + step) - 1) < tolerance:
        dot_1 = [start, 0]
        dot_2 = [start, func(start)]
        dot_3 = [start + step, func(start + step)]
        dot_4 = [start + step, 0]
        draw_line([dot_1, dot_2, dot_3, dot_4], True, False, False)
        slices += 1
        print(start, step, normal_square)
        return abs(step * (func(start + step) + func(start))/2)
    else:
        return slice_square(start, half_step, tolerance) + slice_square(start + half_step, half_step, tolerance)


def func(x):
    return x / 3 + abs(math.cos(x / 40)) * 100 *abs(math.sin(x/120))


if __name__ == '__main__':
    #command = turtle.textinput("Уравнение кривой", "введите уравнение кривой для 'x':")
    #func = lambda x: eval(command)

    x_min, x_max, y_min, y_max = -900, 900, -450, 450

    turtle.tracer(False)
    draw_axes(x_max, y_max, 50, 5)
    draw_line([[x] + [func(x)] for x in range(x_min, x_max + 1)], True, False, False)

    # Основной цикл перебора комбинаций
    slice_number = 20
    step = (x_max - x_min) / slice_number

    slices = 0
    square = 0
    for i in range(slice_number):
        square += slice_square(x_min + step * i, step, 0.05)

    str_res = "Кол-во срезов: " + str(slices)
    str_res += ". Площадь: " + str(square)
    print(str_res)
    turtle.goto(-450, -495)
    turtle.write(str_res)
    turtle.tracer(True)
    turtle.speed(9)
    turtle.mainloop()
