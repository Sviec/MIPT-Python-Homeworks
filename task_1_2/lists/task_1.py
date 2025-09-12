def find_min_max_median():
    try:
        nums = list(map(int, input().split()))
        print(nums)
        print(type(nums))
        print(f'Максимальное число в списке: {max(nums)}')
        print(f'Минимальное число в списке: {min(nums)}')

        nums = sorted(nums)
        n = len(nums)
        if n % 2 == 1:
            print(f'Медиана в списке: {nums[n // 2]}')
        else:
            print(f'Медиана в списке: {(nums[n // 2] + nums[n // 2 - 1]) / 2}')
    except ValueError as ve:
        print('Некорректный ввод, попробуйте снова')


find_min_max_median()