import numpy as np

from task_5.task_2.image_types.image import Image


class BinaryImage(Image):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.data = np.zeros((height, width), dtype=np.uint8)

    def get_pixel(self, x: int, y: int):
        return self.data[y, x]

    def set_pixel(self, x: int, y: int, value: int):
        self.data[y, x] = 1 if value else 0

    def get_data(self) -> np.ndarray:
        return self.data.copy()
