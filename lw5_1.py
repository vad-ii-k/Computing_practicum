import argparse
import sys
from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.integrate import quad
from tabulate import tabulate


def print_header():
    print("Задание #5.1. Приближенное вычисление определённых интегралов\n"
          "Вариант 7\n"
          "Исходные параметры задачи:\n"
          f"   A = 0   B = 1   n = 2   ρ(x) = sqrt(1-x)   f(x) = e^x\n")


def custom_tabulate(arr: np.ndarray | list, char: str, pres: int = 2, note: str = ''):
    indexes = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']
    headers = list(map(lambda index: char + index, indexes))
    return tabulate([arr], headers=headers, tablefmt="mixed_outline", numalign="center", floatfmt=f".{pres}f") + note


def pho(x: np.float64) -> np.ndarray:
    return np.sqrt(1 - x)


def function(x: np.float64) -> np.ndarray:
    return np.exp(x)


def create_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-n', '--number_of_nodes', type=int, help="Number of nodes")
    return args_parser


@dataclass(slots=True, frozen=True)
class Segment:
    start: float
    end: float


def function_tabulation(n: int, a: float, b: float, f: Callable) -> list[Segment]:
    h = (b - a) / n
    x1 = a
    x2 = x1 + h
    y1 = f(x1)
    segments = list()
    while x2 <= b:
        y2 = f(x2)
        if y1 * y2 <= 0:
            segments.append(Segment(x1, x2))
        x1 = x2
        x2 = x1 + h
        y1 = y2
    return segments


def secants_method(segment: Segment, f: Callable):
    x_prev = segment.start
    x_k = segment.end
    while True:
        x_next = x_k - (f(x_k) / (f(x_k) - f(x_prev))) * (x_k - x_prev)
        if abs(x_k - x_prev) < 1e-10 or x_k == x_next:
            break
        x_prev = x_k
        x_k = x_next
    return x_k


def print_results(n: int, a: float, b: float):
    # Task 1
    integral_value = quad(func=(lambda x: np.multiply(function(x), pho(x))), a=a, b=b)[0]
    print(f"Точное значение интеграла: {integral_value:.12f}")

    h = 1 / n
    x_values = np.array([i * h for i in range(n + 1)])

    # Task 3
    print("\n――――――――――――task 3――――――――――――――")
    print(custom_tabulate(x_values, 'x', 2, ' 🡬 узлы КФ'))

    x_matrix = np.array([np.power(x_values, degree) for degree in range(n + 1)])
    mu_values = [quad(func=(lambda x: np.multiply(np.power(x, i), pho(x))), a=a, b=b)[0] for i in range(n + 1)]
    print(custom_tabulate(mu_values, 'μ', 5, ' 🡬 моменты весовой функции'))

    a_values = np.linalg.solve(x_matrix, mu_values)
    print(custom_tabulate(a_values, 'A', 5, ' 🡬 коэффициенты КФ'))

    approximate_value = sum([a_i * function(x_i) for a_i, x_i in zip(a_values, x_values)])
    print(f"Значение интеграла, полученное вычислением квадратур = {approximate_value:.8f}")
    print(f"Фактическая погрешность = {abs(integral_value - approximate_value):.8f}")

    # Task 5
    print("\n――――――――――――task 5――――――――――――――")
    print(custom_tabulate(x_values, 'x', 2, ' 🡬 узлы КФ'))

    mu_values = [quad(func=(lambda x: np.multiply(np.power(x, i), pho(x))), a=a, b=b)[0] for i in range(n * 2)]
    print(custom_tabulate(mu_values, 'μ', 5, ' 🡬 моменты весовой функции'))

    mu_matrix_left = [list(reversed(mu_values[i:n + i])) for i in range(n)]
    mu_matrix_right = list(map(lambda mu: -mu, mu_values[n:n * 2]))
    a_values: np.ndarray = np.array([1, *np.linalg.solve(mu_matrix_left, mu_matrix_right)])
    print(custom_tabulate(a_values, 'a', 5, ' 🡬 коэффициенты a₀xⁿ + a₁xⁿ⁻¹ + ··· + aₙ₋₁x + aₙ = 0'))

    def monomial(x: np.float64, degree: int, a_i: np.float64) -> np.float64:
        return np.multiply(np.power(x, degree), a_i)

    def polynomial(x: np.float64) -> np.ndarray:
        return np.sum([monomial(x, i, a_i) for i, a_i in enumerate(reversed(a_values))])

    segments = function_tabulation(n * 10, a, b, polynomial)
    roots = [secants_method(segment, polynomial) for segment in segments]
    print(custom_tabulate(roots, 'root', 5, ' 🡬 корни xⁿ + a₁xⁿ⁻¹ + ··· + aₙ₋₁x + aₙ = 0'))

    x_matrix = [[root_i ** degree for root_i in roots] for degree in range(n)]
    csf_values = np.linalg.solve(x_matrix, mu_values[:n])
    print(custom_tabulate(csf_values, 'A', 5, ' 🡬 коэффициенты КФ'))

    approximate_value = sum([a_i * function(x_i) for a_i, x_i in zip(csf_values, roots)])
    print(f"Значение интеграла, полученное по формуле типа Гаусса = {approximate_value:.8f}")
    print(f"Фактическая погрешность = {abs(integral_value - approximate_value):.8f}")


def main():
    print_header()

    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    n = 2 if namespace.number_of_nodes is None else namespace.number_of_nodes

    print_results(n, 0, 1)


if __name__ == "__main__":
    main()
