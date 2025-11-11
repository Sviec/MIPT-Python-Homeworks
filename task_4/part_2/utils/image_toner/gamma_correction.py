import cv2
import numpy as np


def gamma_correction(img, gamma: float = 1.0, save_as: str = 'gamma_correction.png'):
    inv_g = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_g) * 255 for i in np.arange(0, 256)]).astype("uint8")
    cv2.imwrite(cv2.LUT(img, table), save_as)
