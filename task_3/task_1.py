def operation_table(operation: str):
    for i in range(1, 10):
        for j in range(1, 10):
            if operation == '1':
                print(f'{j} * {i} =', i * j, end="\t")
            if operation == '2':
                print(f'{j} + {i} =', i + j, end="\t")
            if operation == '3':
                print(f'{j} - {i} =', j - i, end="\t")
            if operation == '4':
                print(f'{j} / {i} =', round(j / i, 1), end="\t\t")
        print()


def main():
    try:
        op = input("Выберите таблицу:\n1. Таблица умножения\n2. Таблица сложения\n3. Таблица вычитания\n4. Таблица деления\n")
        if int(op) not in [1,2,3,4]:
            raise ValueError("")
        operation_table(op)
    except ValueError as ve:
        print('Некорректный ввод')
    except Exception as e:
        print(e)


main()