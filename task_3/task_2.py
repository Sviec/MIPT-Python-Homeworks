import numpy as np
from task_3 import multichannel_convolution


def create_vector(n):
    print_vector([np.random.randint(10) for _ in range(n)])


def create_matrix(n, m):
    print_matrix([[np.random.randint(10) for _ in range(n)] for _ in range(m)])


def multiply_matrix_by_vector(n):
    matrix = [[np.random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    vector = [np.random.randint(1, 10) for _ in range(n)]

    print('Полученная матрица:')
    for row in matrix:
        print(row)
    print('Полученный вектор:')
    print(vector)
    result = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += vector[j] * matrix[j][i]
        result.append(s)

    print('Результат перемножения матрицы на вектор:')
    print_matrix(result)


def print_matrix(matrix):
    for row in matrix:
        for element in row:
            print(element, end=' ')
        print()


def print_vector(vector):
    for i in vector:
        print(i, end=' ')


def get_matrix_trace(matrix):
    print(sum([matrix[i][i] for i in range(max(len(matrix), len(matrix[0])))]))


@multichannel_convolution
def conv2d(matrix, kernel, stride=1):
    rows, cols = matrix.shape
    k_rows, k_cols = kernel.shape

    out_rows = (rows - k_rows) // stride + 1
    out_cols = (cols - k_cols) // stride + 1
    result = np.zeros((out_rows, out_cols))

    for i in range(out_rows):
        for j in range(out_cols):
            patch = matrix[i * stride:i * stride + k_rows, j * stride:j * stride + k_cols]
            result[i, j] = np.sum(patch * kernel)

    return result


image = np.random.rand(5, 5, 3)

kernel = np.array([
    [1, 0, -1],
    [1, 0, -1],
    [1, 0, -1]
])

out = conv2d(image, kernel, stride=1)
print("Исходное изображение:", image)
print("Исходная форма:", image.shape)
print("Ядро:", kernel)
print("Результат свертки:", out)
print("Результат свертки (формат):", out.shape)