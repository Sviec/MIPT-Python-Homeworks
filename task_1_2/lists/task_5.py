arr = list(map(int, input('Введите массив: ').split()))
n = len(arr)
result = arr.copy()

for i in range(n):
    if arr[i] < 0:
        left_positive = None
        for l in range(i - 1, -1, -1):
            if arr[l] > 0:
                left_positive = arr[l]
                break

        right_positive = None
        for r in range(i + 1, n):
            if arr[r] > 0:
                right_positive = arr[r]
                break

        if left_positive and right_positive:
            result[i] = (left_positive + right_positive) / 2
        elif left_positive:
            result[i] = left_positive
        elif right_positive:
            result[i] = right_positive

print(result)


