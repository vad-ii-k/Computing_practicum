import argparse
import math
import random
import sys
from dataclasses import dataclass
from typing import Final, Literal


def create_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-m', '--number_of_values', type=int, help="Number of values in the table (m+1)")
    args_parser.add_argument('-a', '--start', type=int, help="Start of the segment")
    args_parser.add_argument('-b', '--end', type=int, help="End of the segment")

    return args_parser


parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])

m: Final[int] = 15 if namespace.number_of_values is None else namespace.number_of_values
a: Final[int] = 0 if namespace.start is None else namespace.start
b: Final[int] = 1 if namespace.end is None else namespace.end
EPSILON: Final[float] = 1e-12


@dataclass(slots=True)
class TableValue:
    x: float
    f_x: float


def print_header():
    print(
        "Задание #2. Тема: Задача алгебраического интерполирования\n"
        "Вариант 7\n"
        "Исходные параметры задачи:\n"
        "   f(x)=exp(-x) – x²/2         a=0     b=1     x=0,65\n"
        "   xⱼ=a+j·(b-a)/m   j=0,1..m    n=7     m=15\n"
    )


def test_f(x: float) -> float:
    return 5 * x**2 - 10 * x - 9


def f(x: float) -> float:
    return math.exp(-x) - (x ** 2) / 2


def get_interpolation_point() -> float:
    try:
        x = float(input(">>> Введите точку интерполирования x;  x="))
    except ValueError:
        x: float = 0.65
        print(f"Оставлено значение x по умолчанию;   x={x}")
    return x


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


def get_table_of_function_values() -> list[TableValue]:
    h = (b - a) / m
    values: list[TableValue] = []
    for i in range(m + 1):
        x = a + h * i * (0.95 + random.random() % 0.05)
        values.append(TableValue(x=x, f_x=f(x)))
    return values


def print_table_of_function_values(table: list[TableValue]) -> None:
    print("       Таблица значений      ")
    print("┌╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴┐")
    print("╎       x      ╎      f(x)    ╎")
    print("├╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴┤")
    for table_value in table:
        print(f"╎{table_value.x:^ 13.9f} ╎{table_value.f_x:^ 13.9f} ╎")
    print("└╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┘")


def sort_table_by_dist_from_point(table: list[TableValue], x: float):
    return sorted(table, key=lambda value: abs(x - value.x))


def omega(x: float, k: int, x_table_values: list[float]):
    result = 1
    for index, x_i in enumerate(x_table_values):
        if index != k:
            result *= x - x_i
    return result


def lagrange_interpolate(table: list[TableValue], n: int, x: float) -> float:
    value_of_polynomial: float = 0
    x_table_values = list(map(lambda value: value.x, table[:n + 1]))
    for k in range(n + 1):
        value_of_polynomial += table[k].f_x * omega(x, k, x_table_values) / omega(x_table_values[k], k, x_table_values)
    return value_of_polynomial


def get_multiply(x: float, k: int, x_table_values: list[float]):
    result = 1
    for index in range(k):
        result *= x - x_table_values[index]
    return result


def newton_interpolate(table: list[TableValue], n: int, x: float) -> float:
    x_table_values = list(map(lambda value: value.x, table[:n + 1]))
    divided_differences_table = [[] for _ in range(n + 1)]
    for i in range(n+1):
        divided_differences_table[0].append(table[i].f_x)
    for i in range(1, n + 1):
        for j in range(n - i):
            row = divided_differences_table[i - 1]
            new_element = (row[j+1] - row[j]) / (x_table_values[i+j] - x_table_values[j])
            divided_differences_table[i].append(new_element)
    value_of_polynomial = sum(divided_differences_table[i][0] * get_multiply(x, i, x_table_values) for i in range(n))
    return value_of_polynomial


def print_interpolation_results(p_n: float, x: float, method: Literal["Лагранжа", "Ньютона"]):
    print(f"Значение интерполяционного многочлена Pₙ(x), найденное при помощи представления в форме {method}:   {p_n}")
    print(f"Значение абсолютной фактической погрешности для формы {method} │f(x)‒ Pₙ(x)|:   {abs(f(x) - p_n)}")


def get_interpolation_results(table: list[TableValue]):
    x = get_interpolation_point()
    n = get_degree_of_interpolation_polynomial()
    sorted_table_by_dist_from_point = sort_table_by_dist_from_point(table, x)
    print_table_of_function_values(sorted_table_by_dist_from_point)
    p_n = lagrange_interpolate(sorted_table_by_dist_from_point, n, x)
    print_interpolation_results(p_n, x, "Лагранжа")
    p_n = newton_interpolate(sorted_table_by_dist_from_point, n, x)
    print_interpolation_results(p_n, x, "Ньютона")


def main():
    print_header()
    get_table_of_function_values()
    table = get_table_of_function_values()
    print_table_of_function_values(table)
    get_interpolation_results(table)
    while True:
        choice = input(">>> Напишите \"1\", если хотите ввести новые значения x и n:   ")
        if choice == '1':
            get_interpolation_results(table)
        else:
            print(f"Выход из программы...")
            break


if __name__ == '__main__':
    main()
