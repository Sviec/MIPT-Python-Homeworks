def binary_search(left, right, n):
    median = (right + left) // 2
    while True:
        answer = int(input(f"Загаданное число равно {median}? (Если да, введите 1, если нет введите 0):\n"))
        if answer == 1:
            return median
        elif answer == 0:
            while True:
                answer = int(input(f"Загаданное число меньше {median}? (Если да, введите 1, если нет введите 0):\n"))
                if answer == 0:
                    return binary_search(median+1, right, n)
                elif answer == 1:
                    return binary_search(left, median, n)
                else:
                    print('Некорректный ввод, попробуйте снова')
        else:
            print('Некорректный ввод, попробуйте снова')


num = int(input('Введите число: '))
a, b = map(int, input('Введите интервал: ').split())
print(f"Загаданное число: {binary_search(a, b, num)}")


