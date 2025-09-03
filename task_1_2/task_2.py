def print_list_of_numbers_with_star():
    try:
        n = int(input("Введите N: "))
        m = 0
        for i in range(1, n+1):
            if m % 5 == 0:
                print()
            print('*', end=' ')
            m += 1
            if m % 5 == 0:
                print()
            print(i, end=' ')
            m += 1
        if m % 5 == 0:
            print()
        print('*', end=' ')
    except ValueError as ve:
        print('Некорректный ввод, попробуйте снова')


print_list_of_numbers_with_star()
