import argparse
import math
import sys

from tabulate import tabulate

from lw5_helpers import FunctionInfo, add_match_highlighting


def print_header():
    print("Задание #5_2. КФ Мелера, ее узлы и коэффициенты. Вычисление интегралов при помощи КФ Мелера\n"
          "Вариант 7\n"
          "- Для КФ Мелера f(x) = exp(2x) · x^2\n")


def get_mehler_results(f: FunctionInfo, n: int):
    print(f"\nВычисление интеграла ∫{f.representation}dx при помощи КФ Мелера")

    roots = [math.cos((2 * k - 1) * math.pi / (2 * n)) for k in range(1, n + 1)]
    coefficient = math.pi / n

    results_table = {
        "Коэффициенты КФ Мелера Aₖ": [coefficient] * n,
        "Корни многочлена Чебышева xₖ": roots,
    }
    print(tabulate(results_table, "keys", "mixed_outline", numalign="center", floatfmt=f".12f", showindex=True))

    mehler_value = coefficient * sum([f.function(x_k) for x_k in roots])
    print(f"Значение интеграла, полученное при помощи КФ Мелера: {mehler_value:.12f} при N={n}")
    return mehler_value


def print_results(list_of_n: list[int]):
    mehler_function = FunctionInfo(
        function=lambda x: math.exp(2 * x) * x ** 2,
        representation="(exp(2x) · x^2 / √(1 - x²))"
    )
    mehler_results = [get_mehler_results(mehler_function, n) for n in list_of_n]

    print(f"\nРезультаты по Мелеру для ∫{mehler_function.representation}dx")
    results_table = {
        "N": list_of_n,
        "с подсветкой": add_match_highlighting(mehler_results),
        "без подсветки": mehler_results,
    }
    print(tabulate(results_table, "keys", "mixed_outline", numalign="center", stralign="center", disable_numparse=True))


def create_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-n', '--list_of_n', nargs="+", type=int, help="List of N", default=[4, 5, 7, 8])
    return args_parser


def main():
    print_header()

    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    try:
        print_results(namespace.list_of_n)
    except (Exception, KeyboardInterrupt):
        print(f"Ошибка!\nВыход из программы...")
        return


if __name__ == '__main__':
    main()
