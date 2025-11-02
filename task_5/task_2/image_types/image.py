import numpy as np
from typing import Any


class Image:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def get_pixel(self, x: int, y: int) -> Any:
        raise NotImplemented

    def set_pixel(self, x: int, y: int, value: Any):
        raise NotImplemented

    def get_data(self) -> np.ndarray:
        raise NotImplemented
