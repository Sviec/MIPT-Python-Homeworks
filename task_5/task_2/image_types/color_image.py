from typing import Any, Tuple

import numpy as np

from task_5.task_2.image_types.image import Image

class ColorImage(Image):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.data = np.zeros((height, width, 3), dtype=np.uint8)

    def get_pixel(self, x: int, y: int):
        return tuple(self.data[y, x])

    def set_pixel(self, x: int, y: int, value: Tuple[int, int, int]):
        r, g, b = value
        self.data[y, x] = [
            max(0, min(255, r)),
            max(0, min(255, g)),
            max(0, min(255, b))
        ]

    def get_data(self) -> np.ndarray:
        return self.data.copy()