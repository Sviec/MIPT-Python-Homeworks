embedding = list(map(int, input('Введите входной список элементов: ').split()))
kernel = list(map(int, input('Введите ядро свертки: ').split()))
embedding_size = len(embedding)
kernel_size = len(kernel)
if kernel_size > embedding_size:
    raise Exception("Ядро свертки не может быть меньше размера входного изображения")
result = []
for i in range(len(embedding) - len(kernel) + 1):
    scalar = sum([x * y for x, y in zip(embedding[i:i+kernel_size], kernel)])
    result.append(scalar)

print(f"Результат свертки: {result}")