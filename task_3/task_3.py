import numpy as np


def multichannel_convolution(func):
    def wrapper(image, *args, **kwargs):
        if image.ndim != 3:
            raise ValueError("Некорректный формат изображения. Ожидается изображение формата [M, N, C]")

        channels = []
        for c in range(image.shape[2]):
            channel = image[:, :, c]
            conv_res = func(channel, *args, **kwargs)
            channels.append(conv_res)

        return np.stack(channels, axis=2)

    return wrapper


