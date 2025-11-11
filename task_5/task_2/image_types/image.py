import numpy as np
from typing import Any
from task_5.task_2.utils.image_exceptions import DataSizeError, CoordinateError


class Image:
    def __init__(self, width: int, height: int):
        if width <= 0 or height <= 0:
            raise DataSizeError(f"Неверные размеры изображения: {width}x{height}")
        self.width = width
        self.height = height

    def get_pixel(self, x: int, y: int) -> Any:
        raise NotImplementedError("Метод get_pixel должен быть реализован в подклассе")

    def set_pixel(self, x: int, y: int, value: Any):
        raise NotImplementedError("Метод set_pixel должен быть реализован в подклассе")

    def get_data(self) -> np.ndarray:
        raise NotImplementedError("Метод get_data должен быть реализован в подклассе")

    def validate_data_integrity(self) -> None:
        """Проверка целостности данных изображения - должен быть реализован в подклассе"""
        raise NotImplementedError("Метод validate_data_integrity должен быть реализован в подклассе")

    def _validate_coordinates(self, x: int, y: int) -> None:
        """Базовая проверка корректности координат"""
        if not (0 <= x < self.width):
            raise CoordinateError(f"Координата x={x} выходит за границы [0, {self.width-1}]")
        if not (0 <= y < self.height):
            raise CoordinateError(f"Координата y={y} выходит за границы [0, {self.height-1}]")



