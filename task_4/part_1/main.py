from task_4.part_1.task_1 import *


# тест умножения матрицы на матрицу
A = [[1, 2, 3], [4, 5, 6]]
B = [[3, 4], [2, 6], [1, 3]]

print(multiply_matrix_by_matrix(A, B))


# тест умножения матрицы A на вектор
v = [7, 8, 9]
print(multiply_vector_by_matrix(A, v))


# тест скалярного произведения
u = [1, 2, 3]
print(dot_product(u, v))

# тест поиска следа матрицы
C = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(trace_matrix(C))

#  тест расчета гистограммы
data = [1, 2, 2.5, 3, 5, 7, 8, 9, 10]
counts, ranges = histogram(data, bins=4)

print("Частоты:", counts)
print("Интервалы:", ranges)


# тест свертки
data = [1, 2, 4, 7, 11, 16]
kernel = [-1, 0, 1]

filtered = convolve(data, kernel)

print("Исходный вектор: ", data)
print("После фильтрации:", filtered)