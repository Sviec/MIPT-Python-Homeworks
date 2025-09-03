def print_list_of_numbers_with_star():
    try:
        n = int(input("Введите N: "))
        for i in range(1, n+1):
            print('*', i, end=' ')
        print('*')
    except ValueError as ve:
        print('Некорректный ввод, попробуйте снова')


print_list_of_numbers_with_star()
