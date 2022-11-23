import argparse
import math
import sys
from typing import Callable

from scipy.integrate import quad
from tabulate import tabulate

from lw5_1 import function_tabulation, secants_method
from lw5_helpers import add_match_highlighting, FunctionInfo, print_warning, check_coefficients, check_roots


def print_header():
    print("Задание #5_2. КФ Гаусса, ее узлы и коэффициенты. Вычисление интегралов при помощи КФ Гаусса\n"
          "Вариант 7\n"
          "- Найти при помощи КФ Гаусса ∫((x+0.8) / √(x^2 + 1.2))dx   a=1.6  b=2.7  N=4,5,7,8\n")


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


def get_gauss_results(f: FunctionInfo, n: int, a: float, b: float):
    print(f"Вычисление интеграла ∫({f.representation})dx при помощи КФ Гаусса на отрезке [{a:.2f}, {b:.2f}]")

    legendre_roots = get_legendre_roots(n)
    mapped_legendre_roots = list(map(lambda t_k: (b - a) / 2 * t_k + (b + a) / 2, legendre_roots))
    coefficients = get_gauss_coefficients(n, legendre_roots)
    if abs(sum(coefficients) - (b - a)) > 1e12:
        print_warning(f'SUM OF THE COEFFICIENTS IS NOT EQUAL TO {b - a}')
    mapped_coefficients = list(map(lambda c_k: (b - a) / 2 * c_k, coefficients))

    results_table = {
        "Корни многочлена Лежандра tᵢ": legendre_roots,
        "Коэффициенты КФ Гаусса Cₖ": coefficients,
        "Корни многочлена Лежандра xᵢ": mapped_legendre_roots,
        "Коэффициенты КФ Гаусса Aₖ": mapped_coefficients,
    }
    print(tabulate(results_table, "keys", "mixed_outline", numalign="center", floatfmt=f".12f", showindex=True))

    gauss_value = sum([a_k * f.function(x_k) for a_k, x_k in zip(mapped_coefficients, mapped_legendre_roots)])
    print(f"Значение интеграла, полученное при помощи КФ Гаусса: {gauss_value:.12f} при N={n}\n")
    return gauss_value


def print_results(list_of_n: list[int], a: float, b: float):
    def check_on_polynomial():
        print_warning("TESTING...", error=False)
        degree = 2 * max(list_of_n) - 1
        polynomial = FunctionInfo(lambda x: x ** degree / 999 + 2 * x ** degree + 0.5 * x, "polynomial")
        polynomial_result = get_gauss_results(polynomial, max(list_of_n), a, b)
        polynomial_accurate = quad(func=lambda x: polynomial.function(x), a=a, b=b)[0]
        if abs(polynomial_accurate - polynomial_result) > 1e8:
            print_warning("TESTING ON A POLYNOMIAL FAILED")
            print(abs(polynomial_accurate - polynomial_result))
            raise Exception
        else:
            print_warning("TESTING ON THE POLYNOMIAL WAS COMPLETED SUCCESSFULLY", error=False)

    check_on_polynomial()

    gauss_function = FunctionInfo(lambda x: (x + 0.8) / math.sqrt(x ** 2 + 1.2), "((x + 0.8) / √(x² + 1.2))")
    gauss_results = [get_gauss_results(gauss_function, n, a, b) for n in list_of_n]

    accurate_value = quad(func=lambda x: gauss_function.function(x), a=a, b=b)[0]
    print(f"\nРезультаты по Гауссу для ∫{gauss_function.representation}dx на [{a:.2f}, {b:.2f}]")
    results_table = {
        "N": list_of_n,
        "С подсветкой": add_match_highlighting(gauss_results),
        "Без подсветки": gauss_results,
        "Фактическая погрешность": list(map(lambda x: f"{abs(accurate_value - x):.15f}", gauss_results))
    }
    print(tabulate(results_table, "keys", "mixed_outline", numalign="center", stralign="center", disable_numparse=True))



def create_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-n', '--list_of_n', nargs="+", type=int, help="List of N", default=[4, 5, 7, 8])
    args_parser.add_argument('-a', '--start', type=float, help="Start of the segment", default=1.6)
    args_parser.add_argument('-b', '--end', type=float, help="End of the segment", default=2.7)
    return args_parser


def main():
    print_header()

    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    try:
        print_results(namespace.list_of_n, namespace.start, namespace.end)
    except (Exception, KeyboardInterrupt):
        print(f"Ошибка!\nВыход из программы...")
        return


if __name__ == '__main__':
    main()
