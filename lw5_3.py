import argparse
import math
import sys
from distutils.util import strtobool
from typing import Callable

from tabulate import tabulate

from lw5_1 import function_tabulation, secants_method
from lw5_helpers import FunctionInfo, get_input, print_warning, check_coefficients, check_roots


def print_header():
    print("Задание #5_3. Приближённое вычисление интеграла при помощи составной КФ Гаусса\n"
          "Вариант 7\n"
          " f(x) = sin(x)   ρ(x) = |x − 0.5|   [a, b] = [0, 1]\n")


def get_legendre_polynomial(n: int) -> Callable:
    def inner(x: float) -> float:
        if n == 0:
            return 1
        if n == 1:
            return x
        else:
            prev = get_legendre_polynomial(n - 1)(x)
            prev_prev = get_legendre_polynomial(n - 2)(x)
            return (2 * n - 1) / n * prev * x - (n - 1) / n * prev_prev

    return inner


def get_legendre_roots(n: int) -> list[float]:
    p_legendre_n = get_legendre_polynomial(n)
    roots = [secants_method(segment, p_legendre_n) for segment in function_tabulation(n * 10, -1, 1, p_legendre_n)]
    check_roots(roots)
    return roots


def get_gauss_c_k(x_k: float, n: int, prev_legendre_polynomial: Callable):
    return (2 * (1 - x_k ** 2)) / ((n ** 2) * (prev_legendre_polynomial(x_k) ** 2))


def get_gauss_coefficients(n: int, legendre_roots: list) -> list[float]:
    coefficients = [get_gauss_c_k(x_k, n, get_legendre_polynomial(n - 1)) for x_k in legendre_roots]
    check_coefficients(coefficients)
    return coefficients


def get_gauss_results(f: FunctionInfo, n: int, a: float, b: float, h: float, verbose: bool):
    legendre_roots = get_legendre_roots(n)
    mapped_legendre_roots = list(map(lambda t_k: h / 2 * t_k + (b + a) / 2, legendre_roots))
    coefficients = get_gauss_coefficients(n, legendre_roots)
    if abs(sum(coefficients) - (b - a)) > 1e12:
        print_warning(f'SUM OF THE COEFFICIENTS IS NOT EQUAL TO {b - a}')
    mapped_coefficients = list(map(lambda c_k: h / 2 * c_k, coefficients))

    results_table = {
        "Корни многочлена Лежандра tᵢ": legendre_roots,
        "Коэффициенты КФ Гаусса Cₖ": coefficients,
        "Корни многочлена Лежандра xᵢ": mapped_legendre_roots,
        "Коэффициенты КФ Гаусса Aₖ": mapped_coefficients,
    }
    gauss_value = sum([a_k * f.function(x_k) for a_k, x_k in zip(mapped_coefficients, mapped_legendre_roots)])

    if verbose:
        print(f"Вычисление интеграла ∫({f.representation})dx при помощи КФ Гаусса на отрезке [{a:.2f}, {b:.2f}]")
        print(tabulate(results_table, "keys", "mixed_outline", numalign="center", floatfmt=f".12f", showindex=True))
        print(f"Значение интеграла, полученное при помощи КФ Гаусса: {gauss_value:.12f} при N={n}\n")
    return gauss_value


def print_results(n: int, m: int, a: int, b: int, verbose: bool) -> float:
    gauss_function = FunctionInfo(lambda x: math.sin(x) * abs(x - 0.5), "sin(x) · |x − 0.5|")

    h = (b - a) / m
    list_of_z = [a + j * h for j in range(m + 1)]
    gauss_results = [get_gauss_results(gauss_function, n, list_of_z[i], list_of_z[i + 1], h, verbose) for i in range(m)]
    gauss_result = sum(gauss_results)
    print(f"\nРезультат по Гауссу для ∫{gauss_function.representation}dx на [{a:.2f}, {b:.2f}] при N={n} и m={m}: \t"
          f"{gauss_result:.13f}")
    return gauss_result


def create_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        '-v', '--verbose', type=lambda x: bool(strtobool(x)), help="Output intermediate results", default=True
    )
    args_parser.add_argument('-a', '--start', type=float, help="Start of the segment", default=0)
    args_parser.add_argument('-b', '--end', type=float, help="End of the segment", default=1)
    return args_parser


def main():
    print_header()

    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    results = {"N": [], "m": [], "Result": []}

    choice = '1'
    try:
        while True:
            if choice == '1':
                n = int(get_input('N', 'количество узлов', 3))
                m = int(get_input('m', 'число разбиений', 10))
                results["Result"].append(print_results(n, m, namespace.start, namespace.end, namespace.verbose))
                results["N"].append(n)
                results["m"].append(m)
            else:
                print(tabulate(results, "keys", "mixed_outline", numalign="center", floatfmt=f".12f", showindex=True))
                print(f"Выход из программы...")
                break
            choice = input(">>> Напишите \"1\", если хотите ввести новые значения:   ")
    except (Exception, KeyboardInterrupt):
        print(f"Ошибка!\nВыход из программы...")
        return


if __name__ == '__main__':
    main()
