from typing import Callable

import numpy as np
from scipy.integrate import quad


def print_header():
    print("Задание #4.1. Приближенное вычисление определённых интегралов\n"
          "Вариант 7\n"
          "Исходные параметры задачи:\n"
          f"   A = 0   B = 1   ρ(x) = sqrt(1-x)   f(x) = e^x\n")


def print_results():
    def pho(x: np.float64) -> Callable:
        return np.sqrt(1 - x)

    def function(x: np.float64) -> Callable:
        return np.exp(x)

    integral_value = quad(func=(lambda x: np.multiply(function(x), pho(x))), a=0, b=1)[0]
    print(f"Точное значение интеграла: {integral_value:.8f}")
    x_values = np.array([0, 0.5, 1])
    [print(f"Узел x{index} = {x}") for x, index in zip(x_values, ['₀', '₁', '₂'])]
    mu_values = [quad(func=(lambda x: np.multiply(np.power(x, i), pho(x))), a=0, b=1)[0] for i in range(3)]
    [print(f"Момент μ{index} = {mu:.8f}") for mu, index in zip(mu_values, ['₀', '₁', '₂'])]

    x_matrix = np.array([np.power(x_values, 0), np.power(x_values, 1), np.power(x_values, 2)])
    a_matrix = np.linalg.solve(x_matrix, mu_values)

    approximate_value = 0
    for a, x, index in zip(a_matrix, x_values, ['₀', '₁', '₂']):
        f_x = function(x)
        approximate_value += a * f_x
        print(f"A{index} = {a:.8f}   f(x{index}) = {f_x:.8f}")

    print(f"Значение интеграла, полученное вычислением квадратур = {approximate_value:.8f}")
    print(f"Фактическая погрешность = {abs(integral_value - approximate_value):.8f}")


def main():
    print_header()
    print_results()


if __name__ == "__main__":
    main()
