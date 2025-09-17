import numpy as np  # для рандома и квадратного корня


n = int(input("Введите размерность векторов: "))
vec1 = np.random.randint(1, 10, n)
vec2 = np.random.randint(1, 10, n)
print(f"Вектор 1: {vec1}")
print(f"Вектор 2: {vec2}")
print(f"Покомпонентная сумма: {[int(x + y) for x, y in zip(vec1, vec2)]}")
print(f"Покомпонентное умножение: {[int(x * y) for x, y in zip(vec1, vec2)]}")

scalar = int(input("Введите скаляр: "))
norm1 = np.sqrt(sum([x**2 for x in vec1]))
norm2 = np.sqrt(sum([x**2 for x in vec2]))
print(f"Норма 1 вектора: {norm1}\nНорма 2 вектора: {norm2}")
result = vec1 if norm1 > norm2 else vec2
print(f"Результат умножения скаляра = {scalar} на наибольший вектор по норме {result}: {scalar*result}")


