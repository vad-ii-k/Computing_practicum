import math
from dataclasses import dataclass


COLOR_WHITE = '\33[0m'
COLOR_RED = '\33[31m'
COLOR_GREEN = '\33[32m'
COLOR_YELLOW = '\33[33m'
COLOR_BLUE = '\33[34m'
COLOR_VIOLET2 = '\33[95m'


K = 3


@dataclass(slots=True)
class TableValue:
    x: float
    f_x: float


def print_header():
    print(COLOR_YELLOW +
          "Задание #3. Нахождение производных таблично-заданной функции по формулам численного дифференцирования\n"
          "Вариант 7\n"
          "Исходные параметры задачи:\n"
          f"   f(x)=exp(1,5*k*x),      k={K}\n"
          + COLOR_GREEN)


def function(x: float) -> float:
    return math.exp(1.5 * K * x)


def d_function(x: float) -> float:
    return 1.5 * K * math.exp(1.5 * K * x)


def dd_function(x: float) -> float:
    return (1.5 * K) ** 2 * math.exp(1.5 * K * x)


def get_a() -> float:
    try:
        a = float(input(f">>> Введите a="))
    except ValueError:
        a: float = 0
        print(f"Оставлено значение a по умолчанию;   a={a}")
    return a


def get_m() -> int:
    try:
        m = int(input(f">>> Введите m="))
    except ValueError:
        m: int = 10
        print(f"Оставлено значение m по умолчанию;   m={m}")
    return m


def get_h() -> float:
    try:
        h = float(input(f">>> Введите h="))
    except ValueError:
        h: float = 0.1
        print(f"Оставлено значение h по умолчанию;   h={h}")
    if h <= 0:
        print("Ошибка h<=0!")
        h = get_h()
    return h


def get_input() -> tuple[int, float, float]:
    return get_m(), get_a(), get_h()


def print_table_of_function_values(table: list[TableValue]) -> None:
    print(COLOR_WHITE + "       Таблица значений      ")
    print("┌╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┐")
    print("╎        x         ╎        f(x)      ╎")
    print("├╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┤")
    for table_value in table:
        print(f"╎ {table_value.x:^ 15.9f}  ╎ {table_value.f_x:^ 15.9f}  ╎")
    print("└╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┘")


def get_table_of_function_values(m: int, a: float, h: float) -> list[TableValue]:
    values: list[TableValue] = []
    for i in range(m + 1):
        x = a + h * i
        values.append(TableValue(x=x, f_x=function(x)))
    return values


def print_results_table(results_table: list[list[float]]) -> None:
    print(COLOR_WHITE + "                                         Таблица результатов численного дифференцирования")
    print("┌╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┬╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┐")
    print("╎        xᵢ       ╎      f(xᵢ)      ╎     f'(xᵢ)чд    ╎ абс.погрешность ╎ отн.погрешность ╎    f''(xᵢ)чд    ╎ абс.погрешность ╎ отн.погрешность ╎")
    print("├╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┼╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┤")
    for row in results_table:
        for value in row:
            print(f"╎ {value:^ 15.7f} ", end='')
        print("╎")
    print("└╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┘")


def get_results(table: list[TableValue], h: float) -> None:
    m = len(table)
    results_table = [[0.0 for i in range(8)] for j in range(m)]
    for i in range(m):
        results_table[i][0] = table[i].x
        results_table[i][1] = table[i].f_x

    results_table[0][2] = (-3 * results_table[0][1] + 4 * results_table[1][1] - results_table[2][1]) / (2 * h)
    for i in range(1, m - 1):
        results_table[i][2] = (results_table[i+1][1] - results_table[i-1][1]) / (2 * h)
    results_table[-1][2] = (3 * results_table[-1][1] - 4 * results_table[-2][1] + results_table[-3][1]) / (2 * h)

    for i in range(m):
        results_table[i][3] = abs(d_function(results_table[i][0]) - results_table[i][2])

    for i in range(m):
        results_table[i][4] = results_table[i][3] / results_table[i][2]

    for i in range(1, m - 1):
        results_table[i][5] = (results_table[i + 1][1] - 2 * results_table[i][1] + results_table[i - 1][1]) / (h ** 2)

    for i in range(m):
        results_table[i][6] = abs(dd_function(results_table[i][0]) - results_table[i][5])

    for i in range(m):
        if results_table[i][5] != 0:
            results_table[i][7] = results_table[i][6] / results_table[i][5]
        else:
            results_table[i][7] = 100

    print_results_table(results_table)


def main():
    try:
        print_header()
        m, a, h = get_input()
        table = get_table_of_function_values(m, a, h)
        print_table_of_function_values(table)
        get_results(table, h)
        while True:
            choice = input(COLOR_GREEN + ">>> Напишите \"1\", если хотите ввести новые значения:   ")
            if choice == '1':
                m, a, h = get_input()
                table = get_table_of_function_values(m, a, h)
                print_table_of_function_values(table)
                get_results(table, h)
            else:
                print(COLOR_RED + f"Выход из программы..." + COLOR_WHITE)
                break
    except Exception:
        print(COLOR_RED + f"Ошибка!\nВыход из программы..." + COLOR_WHITE)
        return


if __name__ == '__main__':
    main()
