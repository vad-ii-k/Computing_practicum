import argparse
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Callable


def get_input(value_name: str, msg: str, default_value: float) -> float:
    try:
        value = float(input(f">>> Введите {msg} {value_name}="))
    except ValueError:
        value: float = default_value
        print(f"Оставлено значение {value_name} по умолчанию;   {value_name}={default_value}")
    return value


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
        if abs(x_k - x_prev) < 1e-12 or x_k == x_next:
            break
        x_prev = x_k
        x_k = x_next
    return x_k


@dataclass
class FunctionInfo:
    function: Callable
    representation: str
    integral: Callable = None


def add_match_highlighting(arr: list[float]) -> list[str]:
    arr_with_highlighting = [f"\33[0m{arr[0]:.16f}\33[0m"]
    for i in range(1, len(arr)):
        current_value = f"{arr[i]:.16f}"
        matcher = SequenceMatcher(None, f"{arr[i - 1]:.16f}", current_value).find_longest_match()
        if matcher.a != 0 or matcher.b != 0:
            arr_with_highlighting.append(current_value)
        else:
            arr_with_highlighting.append(f"\33[44m{current_value[:matcher.size]}\33[0m{current_value[matcher.size:]}")
    return arr_with_highlighting


def create_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-n', '--list_of_n', nargs="+", type=int, help="List of N", default=[4, 5, 7, 8])
    args_parser.add_argument('-a', '--start', type=float, help="Start of the segment", default=1.6)
    args_parser.add_argument('-b', '--end', type=float, help="End of the segment", default=2.7)
    return args_parser
