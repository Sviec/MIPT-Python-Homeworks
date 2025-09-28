def multiply_matrix_by_matrix(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Матрицы нельзя перемножить, так как размеры не совпадают")
    B_T = list(zip(*B))
    result = [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in B_T] for row_a in A]
    return result


def multiply_vector_by_matrix(A, v):
    if len(A[0]) != len(v):
        raise ValueError("Размеры матрицы и вектора не совпадают")
    result = [sum(a * b for a, b in zip(row, v)) for row in A]
    return result


def trace_matrix(A):
    if len(A[0]) != len(A):
        raise ValueError("Матрица не является квадратной")
    return sum([A[i][i] for i in range(len(A))])


def dot_product(u, v):
    if len(u) != len(v):
        raise ValueError("Не совпадает размерность у векторов")
    return sum([u[i] * v[i] for i in range(len(u))])


def histogram(vector, bins):
    if not vector:
        return [], []

    v_min, v_max = min(vector), max(vector)
    if v_min == v_max:
        return [len(vector)], [(v_min, v_max)]

    step = (v_max - v_min) / bins
    counts = [0] * bins
    ranges = []

    for i in range(bins):
        left = v_min + i * step
        right = v_min + (i + 1) * step
        ranges.append((left, right))

    for x in vector:
        idx = int((x - v_min) / step)
        if idx == bins:
            idx -= 1
        counts[idx] += 1
    return counts, ranges


def convolve(vector, kernel):
    n, k = len(vector), len(kernel)

    result = []
    for i in range(n-k+1):
        result.append(sum([x * y for x, y in zip(vector[i:i+k], kernel)]))

    return result


# чтение/запись данных в файл, из файла ???????????
