import argparse
import math
import random
import sys
from dataclasses import dataclass
from typing import Callable, Final


COLOR_WHITE = '\33[0m'
COLOR_RED = '\33[31m'
COLOR_GREEN = '\33[32m'
COLOR_YELLOW = '\33[33m'
COLOR_BLUE = '\33[34m'
COLOR_VIOLET2 = '\33[95m'


def create_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-m', '--number_of_values', type=int, help="Number of values in the table (m+1)")
    args_parser.add_argument('-a', '--start', type=int, help="Start of the segment")
    args_parser.add_argument('-b', '--end', type=int, help="End of the segment")

    return args_parser


parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])

m: Final[int] = 10 if namespace.number_of_values is None else namespace.number_of_values
a: Final[int] = 0 if namespace.start is None else namespace.start
b: Final[int] = 1 if namespace.end is None else namespace.end


@dataclass(slots=True, frozen=True)
class Segment:
    start: float
    end: float


@dataclass(slots=True, frozen=True)
class ResultOfMethod:
    x_0: float
    counter: int
    x: float
    delta: float


@dataclass(slots=True)
class TableValue:
    x: float
    f_x: float


def print_header():
    print(COLOR_YELLOW +
          "Задание #3. Тема: Задача обратного интерполирования\n"
          "Вариант 7\n"
          "Исходные параметры задачи:\n"
          f"   f(x)=exp(-x) – x²/2         a={a}     b={b}     F=0.5     n=7       m={m}\n"
          )


def test_f(x: float) -> float:
    return 5 * x**2 - 10 * x - 9


def function(x: float) -> float:
    return math.exp(-x) - (x ** 2) / 2


def get_interpolation_value() -> float:
    try:
        f = float(input(COLOR_GREEN + ">>> Введите значение F;  F="))
    except ValueError:
        f: float = 0.5
        print(f"Оставлено значение F по умолчанию;   F={f}")
    return f


def get_epsilon() -> float:
    try:
        epsilon = float(input(">>> Введите значение ε;  ε="))
    except ValueError:
        epsilon: float = 1e-8
        print(f"Оставлено значение ε по умолчанию;   ε={epsilon}")
    return epsilon


def get_degree_of_interpolation_polynomial() -> int:
    try:
        n = int(input(f">>> Введите степень интерполяционного многочлена n≤m={m};    n="))
    except ValueError:
        n: int = 7
        print(f"Оставлено значение n по умолчанию;   n={n}")
    if n > m:
        print("Ошибка! n>m!")
        n = get_degree_of_interpolation_polynomial()
    return n


def print_table_of_function_values(table: list[TableValue]) -> None:
    print(COLOR_WHITE + "       Таблица значений      ")
    print("┌╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┐")
    print("╎        x         ╎        f(x)      ╎")
    print("├╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┤")
    for table_value in table:
        print(f"╎ {table_value.x:^ 15.9f}  ╎ {table_value.f_x:^ 15.9f}  ╎")
    print("└╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┘")


def get_table_of_function_values() -> list[TableValue]:
    h = (b - a) / m
    values: list[TableValue] = []
    for i in range(m + 1):
        x = a + h * i * (0.95 + random.random() % 0.05)
        values.append(TableValue(x=x, f_x=function(x)))
    return values


def secants_method(func: Callable, segment: Segment, eps: float) -> float:
    results = [segment.start, segment.end]
    while abs(results[-1] - results[-2]) > eps:
        x_k = results[-1]
        x_k_1 = results[-2]
        if abs(func(x_k) - func(x_k_1)) < eps:  # to avoid division by zero
            break
        results.append(x_k - func(x_k) * (x_k - x_k_1) / (func(x_k) - func(x_k_1)))
    return results[-1]


def sort_table_by_dist_from_value(table: list[TableValue], f_x: float):
    return sorted(table, key=lambda value: abs(f_x - value.f_x))


def get_multiply(x: float, k: int, x_table_values: list[float]):
    result = 1
    for index in range(k):
        result *= x - x_table_values[index]
    return result


def newton_reverse_interpolate(table: list[TableValue], n: int, f: float) -> float:
    f_x_table_values = list(map(lambda value: value.f_x, table[:n + 1]))
    divided_differences_table = [[] for _ in range(n + 1)]
    for i in range(n+1):
        divided_differences_table[0].append(table[i].x)
    for i in range(1, n + 1):
        for j in range(n - i):
            row = divided_differences_table[i - 1]
            new_element = (row[j+1] - row[j]) / (f_x_table_values[i+j] - f_x_table_values[j])
            divided_differences_table[i].append(new_element)
    return sum(divided_differences_table[i][0] * get_multiply(f, i, f_x_table_values) for i in range(n))


def newton_interpolate(table: list[TableValue], n: int) -> Callable:
    def polynomial(f: float) -> float:
        x_table_values = list(map(lambda value: value.x, table[:n + 1]))
        divided_differences_table = [[] for _ in range(n + 1)]
        for i in range(n+1):
            divided_differences_table[0].append(table[i].f_x)
        for i in range(1, n + 1):
            for j in range(n - i):
                row = divided_differences_table[i - 1]
                new_element = (row[j+1] - row[j]) / (x_table_values[i+j] - x_table_values[j])
                divided_differences_table[i].append(new_element)
        return sum(divided_differences_table[i][0] * get_multiply(f, i, x_table_values) for i in range(n))
    return polynomial


def get_results(table: list[TableValue]):
    f = get_interpolation_value()
    n = get_degree_of_interpolation_polynomial()
    epsilon = get_epsilon()
    sorted_table_by_dist_from_value = sort_table_by_dist_from_value(table, f)
    print_table_of_function_values(sorted_table_by_dist_from_value)
    print(COLOR_BLUE + "Способ 1: интерполирование обратной функции")
    q_n = newton_reverse_interpolate(sorted_table_by_dist_from_value, n, f)
    print(f"Значение интерполяционного многочлена Qₙ(F), найденное при помощи представления в форме Ньютона: {q_n}")
    print(f"Модуль невязки rₙ(X)=│f(x)‒F|: {abs(function(q_n) - f)}")

    print(COLOR_VIOLET2 + "Способ 2: численное решение уравнения Pₙ(x) = F")
    newton_interpolation_polynomial = newton_interpolate(sorted_table_by_dist_from_value, n)
    q_n = secants_method(lambda x: newton_interpolation_polynomial(x) - f, Segment(start=a, end=b), epsilon)
    print(f"Решение уравнения Pₙ(x) = F, полученное методом секущих {q_n}")
    print(f"Модуль невязки rₙ(X)=│f(x)‒F|: {abs(function(q_n) - f)}")


def main():
    try:
        print_header()
        table = get_table_of_function_values()
        print_table_of_function_values(table)
        get_results(table)
        while True:
            choice = input(COLOR_GREEN + ">>> Напишите \"1\", если хотите ввести новые значения F и n:   ")
            if choice == '1':
                get_results(table)
            else:
                print(COLOR_RED + f"Выход из программы..." + COLOR_WHITE)
                break
    except Exception:
        print(COLOR_RED + f"Ошибка!\nВыход из программы..." + COLOR_WHITE)
        return


if __name__ == '__main__':
    main()
