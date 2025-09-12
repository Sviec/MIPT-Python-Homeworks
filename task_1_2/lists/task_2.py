from numpy.random import randint


def get_hist_probabilities():
    nums = randint(1, 100, size=20)
    hist_values = {}
    for num in nums:
        if hist_values.get(num//10):
            hist_values[num//10] += 1
        else:
            hist_values[num//10] = 1
    print(nums)
    for i in range(10):
        if hist_values.get(i):
            print(f"Вероятность получить {i+1} бин: {hist_values[i]/len(nums)*100}%")
        else:
            print(f"Вероятность получить {i+1} бин: 0%")


get_hist_probabilities()
