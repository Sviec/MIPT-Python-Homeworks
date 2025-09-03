def print_multiplication_table():
    for i in range(1, 10):
        for j in range(1, 10):
            print(f'{j} * {i} =', i * j, end="\t")
        print()


print_multiplication_table()