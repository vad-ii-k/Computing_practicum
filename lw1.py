import argparse
import math
import sys
from dataclasses import dataclass
from typing import Final, List


def create_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-A', '--start', type=int, help="Start of the segment")
    args_parser.add_argument('-B', '--end', type=int, help="End of the segment")
    args_parser.add_argument('-e', '--epsilon', type=float, help="Solution accuracy")
    args_parser.add_argument('-N', '--segments_count', type=int, help="Number of segments to tabulate")

    return args_parser


parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])

A: Final[int] = -8 if namespace.start is None else namespace.start
B: Final[int] = 2 if namespace.end is None else namespace.end
EPSILON: Final[float] = 1e-5 if namespace.epsilon is None else namespace.epsilon
N: Final[int] = 100 if namespace.segments_count is None else namespace.segments_count


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


def print_header():
    print(
        "Задание #1. Тема: Численные методы решения нелинейных уравнений\n"
        "Вариант 7\n"
        "Исходные параметры задачи:\n"
        f"   A = {A}   B = {B}   ε = {EPSILON}   f(x) = 10*cos(x) - 0,1*x²\n"
    )


def f(x: float) -> float:
    return 10 * math.cos(x) - 0.1 * x ** 2


def f_derivative(x: float) -> float:
    return -10 * math.sin(x) - 0.2 * x


def function_tabulation(n: int = N, a: int = A, b: int = B) -> List[Segment]:
    h = (b - a) / n
    print(f"> Отделение корней способом табулирования...  N = {n}   h = {h}")
    counter = 0
    x1 = a
    x2 = x1 + h
    y1 = f(x1)
    segments = []
    while x2 <= b:
        y2 = f(x2)
        if y1 * y2 <= 0:
            counter += 1
            segments.append(Segment(x1, x2))
        x1 = x2
        x2 = x1 + h
        y1 = y2
    return segments


def bisection_method(segment: Segment, epsilon: float = EPSILON) -> ResultOfMethod:
    counter = 0
    a, b = segment.start, segment.end
    x_0 = (a + b) / 2
    while True:
        counter += 1
        c = (a + b) / 2
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
        if b - a < epsilon:
            break
    x = (a + b) / 2
    delta = b - a
    return ResultOfMethod(x_0, counter, x, delta)


def newton_method(segment: Segment, epsilon: float = EPSILON):
    counter = 0
    x_0 = (segment.start + segment.end) / 2
    x_prev = x_0
    while True:
        counter += 1
        x_k = x_prev - f(x_prev) / f_derivative(x_prev)
        if abs(x_k - x_prev) < epsilon:
            break
        x_prev = x_k
    delta = abs(x_k - x_prev)
    return ResultOfMethod(x_0, counter, x_k, delta)


def modified_newton_method(segment: Segment, epsilon: float = EPSILON):
    counter = 0
    x_0 = (segment.start + segment.end) / 2
    x_prev = x_0
    f_der_x_0 = f_derivative(x_0)
    while True:
        counter += 1
        x_k = x_prev - f(x_prev) / f_der_x_0
        if abs(x_k - x_prev) < epsilon:
            break
        x_prev = x_k
    delta = abs(x_k - x_prev)
    return ResultOfMethod(x_0, counter, x_k, delta)


def secants_method(segment: Segment, epsilon: float = EPSILON):
    counter = 0
    x_0 = (segment.start + segment.end) / 2
    x_prev = segment.start
    x_k = segment.end
    while True:
        counter += 1
        x_next = x_k - (f(x_k) / (f(x_k) - f(x_prev))) * (x_k - x_prev)
        if abs(x_k - x_prev) < epsilon:
            break
        x_prev = x_k
        x_k = x_next
    delta = abs(x_k - x_prev)
    return ResultOfMethod(x_0, counter, x_k, delta)


def print_result_of_method(res: ResultOfMethod):
    print(f"   x₀={res.x_0:.7}\t m={res.counter}\t xₘ={res.x:.7}\t Δ={res.delta:.3e}\t |f(X)-0|={abs(f(res.x) - 0):.3}")


def getting_results():
    segments: List[Segment] = function_tabulation()
    [print(f"   {i + 1}. [{segment.start:.6f}, {segment.end:.6f}]") for i, segment in enumerate(segments)]
    print(f"   Количество отрезков: {len(segments)}\n")
    print("> Уточнение корней")
    print("\n>> a. Метод половинного деления (метод бисекции)")
    for segment in segments:
        result = bisection_method(segment)
        print_result_of_method(result)
    print("\n>> b. Метод Ньютона (метод касательных)")
    for segment in segments:
        result = newton_method(segment)
        print_result_of_method(result)
    print("\n>> c. Модифицированный метод Ньютона")
    for segment in segments:
        result = modified_newton_method(segment)
        print_result_of_method(result)
    print("\n>> d. Метод секущих")
    for segment in segments:
        result = secants_method(segment)
        print_result_of_method(result)


def main():
    print_header()
    getting_results()


if __name__ == '__main__':
    main()
