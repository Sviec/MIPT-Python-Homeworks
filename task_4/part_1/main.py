from task_4.part_1.task_1 import *
from numpy.random import randint
import time


def test_multiply_matrix_by_matrix():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[3, 4], [2, 6], [1, 3]]
    print(multiply_matrix_by_matrix(A, B))


def test_multiply_vector_by_matrix():
    v = [7, 8, 9]
    A = [[1, 2, 3], [4, 5, 6]]
    print(multiply_vector_by_matrix(A, v))


def test_dot_product():
    u = [1, 2, 3]
    v = [7, 8, 9]
    print(dot_product(u, v))


def test_trace_matrix():
    C = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(trace_matrix(C))


def test_histogram():
    data = [1, 2, 2.5, 3, 5, 7, 8, 9, 10]
    counts, ranges = histogram(data, bins=4)

    print("Частоты:", counts)
    print("Интервалы:", ranges)


def test_convolve():
    data = [1, 2, 4, 7, 11, 16]
    kernel = [-1, 0, 1]

    filtered = convolve(data, kernel)

    print("Исходный вектор: ", data)
    print("После фильтрации:", filtered)


def benchmarks(func, repeats=100):
    start = time.time()
    for i in range(repeats):
        func()
    end = time.time()
    return (end - start)/repeats


functions = {
    "multiply_matrix_by_matrix": lambda: multiply_matrix_by_matrix(
        [[randint(-1000, 1000) for _ in range(100)] for _ in range(100)],
        [[randint(-1000, 1000) for _ in range(100)] for _ in range(100)]
    ),
    "multiply_vector_by_matrix": lambda: multiply_vector_by_matrix(
        [[randint(-1000, 1000) for _ in range(100)] for _ in range(100)],
        [randint(-1000, 1000) for _ in range(100)]
    ),
    "trace_matrix": lambda: trace_matrix([[randint(-1000, 1000) for _ in range(100)] for _ in range(100)]),
    "dot_product": lambda: dot_product(
        [randint(-1000, 1000) for _ in range(100)],
        [randint(-1000, 1000) for _ in range(100)]
    ),
    "histogram": lambda: histogram([randint(-1000, 1000) for _ in range(100)], 10),
    "convolve": lambda: convolve(
        [randint(-1000, 1000) for _ in range(100)],
        [randint(-5, 5) for _ in range(10)]
    )
}


def main():
    results = {}
    for name, func in functions.items():
        t = benchmarks(func)
        results[name] = t

    with open("timing_results.txt", "w", encoding="utf-8") as f:
        f.write("Функция:\tСреднее время выполнения (секунды)\n")
        for name, t in results.items():
            f.write(f"{name}:\t{t:.8f}\n")

main()