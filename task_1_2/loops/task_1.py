while True:
    try:
        a, b = map(int, input().split())
        print(a+b)
    except ValueError as ve:
        print("Некорректный ввод, попробуйте снова")


