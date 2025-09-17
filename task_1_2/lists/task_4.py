from numpy.random import randint


n = int(input("Введите размерность: "))
matrix = [[randint(1, 10) for _ in range(n)] for _ in range(n)]
vector = [randint(1, 10) for _ in range(n)]

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
print(result)


