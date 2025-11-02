from typing import Any

import numpy as np
from task_5.task_2.image_types.image import Image


class MonochromeImage(Image):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.data = np.zeros((height, width), dtype=np.uint8)

    def get_pixel(self, x: int, y: int) -> Any:
        return self.data[y, x]

    def set_pixel(self, x: int, y: int, value: int):
        self.data[y, x] = max(0, min(255, value))

    def get_data(self) -> np.ndarray:
        return self.data.copy()