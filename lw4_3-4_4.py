import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable


def print_header():
    print("Задание #4_3-4_4. Приближённое вычисление интеграла по составным квадратурным формулам\n")


def get_input(value_name: str, msg: str, default_value: float) -> float:
    try:
        value = float(input(f">>> Введите {msg} \t{value_name}="))
    except ValueError:
        value: float = default_value
        print(f"Оставлено значение {value_name} по умолчанию;   {value_name}={default_value}")
    return value


@dataclass
class CompositeMethod(ABC):
    name: str
    ast: int
    const: float

    @staticmethod
    @abstractmethod
    def calculate(values_table: list[float], h: float, **kwargs) -> float:
        pass


@dataclass
class LeftRectangles(CompositeMethod):
    name = "СКФ левых прямоугольников"
    ast = 0
    const = 1 / 2

    @staticmethod
    def calculate(values_table: list[float], h: float, **kwargs) -> float:
        return h * sum(values_table[:-1])


@dataclass
class RightRectangles(CompositeMethod):
    name = "СКФ правых прямоугольников"
    ast = 0
    const = 1 / 2

    @staticmethod
    def calculate(values_table: list[float], h: float, **kwargs) -> float:
        return h * sum(values_table[1:])


@dataclass
class MiddleRectangles(CompositeMethod):
    name = "СКФ средних прямоугольников"
    ast = 1
    const = 1 / 24

    @staticmethod
    def calculate(values_table: list[float], h: float, **kwargs) -> float:
        middle_values_table = kwargs.get('middle_values_table')
        return h * sum(middle_values_table)


@dataclass
class Trapezes(CompositeMethod):
    name = "СКФ трапеций"
    ast = 1
    const = 1 / 12

    @staticmethod
    def calculate(values_table: list[float], h: float, **kwargs) -> float:
        return h / 2 * (values_table[0] + 2 * sum(values_table[1:-1]) + values_table[-1])


@dataclass
class Simpson(CompositeMethod):
    name = "СКФ Симпсона"
    ast = 3
    const = 1 / 2880

    @staticmethod
    def calculate(values_table: list[float], h: float, **kwargs) -> float:
        middle_values_table = kwargs.get('middle_values_table')
        return h / 6 * (values_table[0] + 2 * sum(values_table[1:-1]) + 4 * sum(middle_values_table) + values_table[-1])


@dataclass
class FunctionInfo:
    function: Callable
    integral: Callable
    representation: str
    derivatives: list[Callable]


def get_values_table(f: Callable, points: list[float]):
    return [f(x) for x in points]


def print_results_3(a: float, b: float, m: int, functions: list[FunctionInfo], polynomials: list[FunctionInfo]):
    print("――――――――――――――――――――――――――――――――――――――――――――――――")
    methods = [LeftRectangles, RightRectangles, MiddleRectangles, Trapezes, Simpson]
    h = (b - a) / m
    points = [a + i * h for i in range(m + 1)]
    middle_points = [a + (h / 2) + i * h for i in range(m)]
    for function_info in polynomials + functions:
        values_table = get_values_table(function_info.function, points)
        middle_values_table = get_values_table(function_info.function, middle_points)
        print(f" Функция f(x) = {function_info.representation}")
        value_of_integral = function_info.integral(b) - function_info.integral(a)
        print(f" Точное значение интеграла: {round(value_of_integral, 6)}\n")
        for method in methods:
            print(f"   Метод: {method.name}")
            result = method.calculate(values_table, h, middle_values_table=middle_values_table)
            print(f"    Результат метода: {result:.4f}")
            print(f"    Абсолютная фактическая погрешность: {abs(value_of_integral - result):.6f}")
            print(f"    Относительная фактическая погрешность: "
                  f"{(abs(value_of_integral - result) / abs(value_of_integral) * 100):.4f}%")
            f_max = max(*list(map(abs, get_values_table(function_info.derivatives[method.ast], points))))
            print(f"    Теоретическая погрешность: {method.const * f_max * (b - a) * (h ** (method.ast + 1))}\n")
        print("――――――――――――――――――――――――――――――――――――――――――――――――")


def print_results_4(a: float, b: float, m: int, k: int, functions: list[FunctionInfo], polynomials: list[FunctionInfo]):
    print("――――――――――――――――――――――――――――――――――――――――――――――――")
    methods = [LeftRectangles, RightRectangles, MiddleRectangles, Trapezes, Simpson]
    h = (b - a) / m
    points = [a + i * h for i in range(m + 1)]
    middle_points = [a + (h / 2) + i * h for i in range(m)]

    m_l = m * k
    h_l = (b - a) / m_l
    points_l = [a + i * h_l for i in range(m_l + 1)]
    middle_points_l = [a + (h_l / 2) + i * h_l for i in range(m_l)]
    for function_info in polynomials + functions:
        values_table = get_values_table(function_info.function, points)
        middle_values_table = get_values_table(function_info.function, middle_points)
        values_table_l = get_values_table(function_info.function, points_l)
        middle_values_table_l = get_values_table(function_info.function, middle_points_l)

        print(f" Функция f(x) = {function_info.representation}")
        j = function_info.integral(b) - function_info.integral(a)
        print(f" Точное значение интеграла: {round(j, 6)}\n")
        for method in methods:
            print(f"   Метод: {method.name}")
            j_h = method.calculate(values_table, h, middle_values_table=middle_values_table)
            j_h_l = method.calculate(values_table_l, h_l, middle_values_table=middle_values_table_l)
            print(f"    Результат метода: {j_h_l:.4f}")
            print(f"    Абсолютная фактическая погрешность: {abs(j - j_h_l):.6f}")
            f_max = max(*list(map(abs, get_values_table(function_info.derivatives[method.ast], points_l))))
            print(f"    Теоретическая погрешность: {method.const * f_max * (b - a) * (h ** (method.ast + 1))}")
            j_middle = (k ** (method.ast + 1) * j_h_l - j_h) / (k ** (method.ast + 1) - 1)
            print(f"    Значение интеграла, уточнённое по принципу Рунге: {j_middle:.4f}")
            print(f"    Абсолютная фактическая погрешность после уточнения: {abs(j - j_middle):.6f}")
            print(f"    Относительная фактическая погрешность: {(abs(j - j_middle) / abs(j) * 100):.4f}%\n")
        print("――――――――――――――――――――――――――――――――――――――――――――――――")


def main():
    print_header()
    functions = [
        FunctionInfo(
            lambda x: math.cos(-x) - math.exp(2 * x), lambda x: math.sin(x) - math.exp(2 * x) / 2, 'cos(-x) - e^(2x)',
            [
                lambda x: -math.sin(x) - 2 * math.exp(2 * x),
                lambda x: -math.cos(x) - 4 * math.exp(2 * x),
                lambda x: math.sin(x) - 8 * math.exp(2 * x),
                lambda x: math.cos(x) - 16 * math.exp(2 * x),
             ]
        )
    ]
    polynomials = [
        FunctionInfo(lambda x: 10, lambda x: 10 * x, '10', [lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 0]),
        FunctionInfo(
            lambda x: 8.8 * x - 10, lambda x: 4.4 * x ** 2 - 10 * x, '8.8 * x - 10',
            [lambda x: 8.8, lambda x: 0, lambda x: 0, lambda x: 0]
        ),
        FunctionInfo(
            lambda x: 3 * x ** 2 + 8.8 * x - 10, lambda x: x ** 3 + 4.4 * x ** 2 - 10 * x, '3 * x² + 8.8 * x - 10',
            [lambda x: 6 * x + 8.8, lambda x: 6, lambda x: 0, lambda x: 0]
        ),
        FunctionInfo(
            lambda x: 16 * x ** 3 - 3 * x ** 2 + 8.8 * x - 10,
            lambda x: 4 * x ** 4 - x ** 3 + 4.4 * x ** 2 - 10 * x,
            '16 * x³ - 3 * x² + 8.8 * x - 10',
            [lambda x: 48 * x ** 2 - 6 * x + 8.8, lambda x: -6 * x + 8.8, lambda x: 6, lambda x: 0]
        ),
    ]
    a = get_input('A', 'нижний предел интегрирования', 0)
    b = get_input('B', 'верхний предел интегрирования', 1)
    m = get_input('m', 'число промежутков деления [A, B]', 10)
    print_results_3(a, b, int(m), functions, polynomials)
    try:
        while True:
            choice = input(">>> Напишите \"1\", если хотите увеличить m в l раз:   ")
            if choice == '1':
                k = get_input('l', 'коэффициент увеличения m', 2)
                print_results_4(a, b, int(m), int(k), functions, polynomials)
            else:
                print(f"Выход из программы...")
                break
    except Exception:
        print(f"Ошибка!\nВыход из программы...")
        return


if __name__ == '__main__':
    main()
