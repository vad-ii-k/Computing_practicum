import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable


def print_header():
    print("Задание #4_2. Приближённое вычисление интеграла по квадратурным формулам\n")


def get_input(value_name: str, msg: str, default_value: float) -> float:
    try:
        value = float(input(f">>> Введите {msg} {value_name}="))
    except ValueError:
        value: float = default_value
        print(f"Оставлено значение {value_name} по умолчанию;   {value_name}={default_value}")
    return value


@dataclass
class Method(ABC):
    name: str

    @staticmethod
    @abstractmethod
    def calculate(f: Callable, a: float, b: float) -> float:
        pass


@dataclass
class LeftRectangle(Method):
    name: str = "КФ левого прямоугольника"

    @staticmethod
    def calculate(f: Callable, a: float, b: float) -> float:
        return (b - a) * f(a)


@dataclass
class RightRectangle(Method):
    name: str = "КФ правого прямоугольника"

    @staticmethod
    def calculate(f: Callable, a: float, b: float) -> float:
        return (b - a) * f(b)


@dataclass
class MiddleRectangle(Method):
    name: str = "КФ среднего прямоугольника"

    @staticmethod
    def calculate(f: Callable, a: float, b: float) -> float:
        return (b - a) * f((a + b) / 2)


@dataclass
class Trapeze(Method):
    name: str = "КФ трапеции"

    @staticmethod
    def calculate(f: Callable, a: float, b: float) -> float:
        return ((b - a) / 2) * (f(a) + f(b))


@dataclass
class Simpson(Method):
    name: str = "КФ Симпсона"

    @staticmethod
    def calculate(f: Callable, a: float, b: float) -> float:
        return ((b - a) / 6) * (f(a) + 4 * f((a + b) / 2) + f(b))


@dataclass
class ThreeEighths(Method):
    name: str = "КФ 3/8"

    @staticmethod
    def calculate(f: Callable, a: float, b: float) -> float:
        h = (b - a) / 3
        return (b - a) * (f(a) + 3 * f(a + h) + 3 * f(a + 2 * h) + f(b)) / 8


def print_results(a: float, b: float, functions: [Callable, Callable, str], polynomials: [Callable, Callable, str]):
    print("――――――――――――――――――――――――――――――――――――――――――――――――")
    for function, integral, formula in polynomials + functions:
        print(f" Функция f(x) = {formula}")
        value_of_integral = integral(b) - integral(a)
        print(f" Точное значение интеграла: {round(value_of_integral, 6)}\n")
        for method in [LeftRectangle, RightRectangle, MiddleRectangle, Trapeze, Simpson, ThreeEighths]:
            print(f"   Метод: {method.name}")
            result = method.calculate(function, a, b)
            print(f"    Результат метода: {round(result, 6)}")
            print(f"    Абсолютная фактическая погрешность: {round(abs(value_of_integral - result), 6)}\n")
        print("――――――――――――――――――――――――――――――――――――――――――――――――")


def main():
    print_header()
    functions = [
        (lambda x: math.cos(x) * math.exp(math.sin(x)), lambda x: math.exp(math.sin(x)), 'cos(x) * e^(sin(x))'),
    ]
    polynomials = [
        (lambda x: 10, lambda x: 10 * x, '10'),
        (lambda x: 8.8 * x - 10, lambda x: 4.4 * x ** 2 - 10 * x, '8.8 * x - 10'),
        (lambda x: 3 * x ** 2 + 8.8 * x - 10, lambda x: x ** 3 + 4.4 * x ** 2 - 10 * x, '3 * x² + 8.8 * x - 10'),
        (
            lambda x: 16 * x ** 3 - 3 * x ** 2 + 8.8 * x - 10,
            lambda x: 4 * x ** 4 - x ** 3 + 4.4 * x ** 2 - 10 * x,
            '16 * x³ - 3 * x² + 8.8 * x - 10'
        ),
    ]
    a = get_input('A', 'нижний предел интегрирования', 0)
    b = get_input('B', 'верхний предел интегрирования', 1)
    print_results(a, b, functions, polynomials)
    try:
        while True:
            choice = input(">>> Напишите \"1\", если хотите ввести новые значения:   ")
            if choice == '1':
                a = get_input('A', 'нижний предел интегрирования', 0)
                b = get_input('B', 'верхний предел интегрирования', 1)
                print_results(a, b, functions, polynomials)
            else:
                print(f"Выход из программы...")
                break
    except Exception:
        print(f"Ошибка!\nВыход из программы...")
        return


if __name__ == '__main__':
    main()
