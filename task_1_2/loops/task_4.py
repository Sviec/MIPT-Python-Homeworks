try:
    nums = []
    n = -1
    while len(nums) == 0 or n != 0:
        n = int(input())
        nums.append(n)
    print(max(nums))
except ValueError as ve:
    print('Некорректный ввод, попробуйте снова')


