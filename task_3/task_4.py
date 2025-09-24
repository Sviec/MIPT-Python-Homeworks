import numpy as np


def convert_color(vec):
    vec = np.array(vec, dtype=float)

    if vec[3] == 0:
        R, G, B = vec[:3]
        Y = 0.299 * R + 0.587 * G + 0.114 * B
        I = 0.5959 * R - 0.2746 * G - 0.3213 * B
        Q = 0.2115 * R - 0.5227 * G + 0.3112 * B
        return np.array([Y, I, Q, 1])
    elif vec[3] == 1:
        Y, I, Q = vec[:3]
        R = Y + 0.956 * I + 0.619 * Q
        G = Y - 0.272 * I - 0.647 * Q
        B = Y - 1.106 * I + 1.703 * Q
        return np.array([R, G, B, 0])
    else:
        raise ValueError("Неверный формат: четвёртая компонента должна быть 0 (RGB) или 1 (YIQ)")


rgb_vec = [0.5, 0.2, 0.7, 0]
yiq_vec = convert_color(rgb_vec)
print("Из RGB в YIQ:", yiq_vec)

back_to_rgb = convert_color(yiq_vec)
print("Из YIQ в RGB:", back_to_rgb)
