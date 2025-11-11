from typing import Any, Tuple
import numpy as np
from task_5.task_2.image_types.image import Image
from task_5.task_2.utils.image_exceptions import (
    ImageError, DataSizeError, DataFormatError, DataIntegrityError,
    MemoryAllocationError, ValueRangeError
)


class ColorImage(Image):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        try:
            self.data = np.zeros((height, width, 3), dtype=np.uint8)
        except MemoryError:
            raise MemoryAllocationError(f"Недостаточно памяти для создания изображения {width}x{height}")
        except Exception as e:
            raise ImageError(f"Ошибка инициализации ColorImage: {str(e)}")

    def _validate_color_value(self, value: Tuple[int, int, int]) -> None:
        """Проверка корректности цветового значения"""
        if not isinstance(value, (tuple, list)) or len(value) != 3:
            raise DataFormatError(f"Цвет должен быть кортежем/списком из 3 значений, получено: {value}")

        r, g, b = value
        for i, channel_value in enumerate([r, g, b]):
            if not (0 <= channel_value <= 255):
                raise ValueRangeError(
                    f"Недопустимое значение канала {['R', 'G', 'B'][i]}: {channel_value}. "
                    f"Допустимый диапазон [0, 255]"
                )

    def get_pixel(self, x: int, y: int):
        try:
            self._validate_coordinates(x, y)
            return tuple(self.data[y, x])
        except Exception as e:
            raise ImageError(f"Ошибка получения пикселя ({x}, {y}): {str(e)}")

    def set_pixel(self, x: int, y: int, value: Tuple[int, int, int]):
        try:
            self._validate_coordinates(x, y)
            self._validate_color_value(value)

            r, g, b = value
            self.data[y, x] = [
                max(0, min(255, r)),
                max(0, min(255, g)),
                max(0, min(255, b))
            ]
        except Exception as e:
            raise ImageError(f"Ошибка установки пикселя ({x}, {y}): {str(e)}")

    def get_data(self) -> np.ndarray:
        try:
            if self.data is None:
                raise DataIntegrityError("Данные изображения не инициализированы")
            return self.data.copy()
        except Exception as e:
            raise ImageError(f"Ошибка получения данных: {str(e)}")

    def validate_data_integrity(self) -> None:
        """Проверка целостности данных изображения"""
        try:
            if self.data is None:
                raise DataIntegrityError("Данные изображения не инициализированы")

            if self.data.shape != (self.height, self.width, 3):
                raise DataSizeError(
                    f"Несоответствие размеров данных: ожидалось ({self.height}, {self.width}, 3), "
                    f"получено {self.data.shape}"
                )

            if self.data.dtype != np.uint8:
                raise DataFormatError(f"Неверный тип данных: ожидался uint8, получен {self.data.dtype}")

            # Проверка диапазона значений
            if np.min(self.data) < 0 or np.max(self.data) > 255:
                raise ValueRangeError(
                    f"Значения цветовых каналов вне диапазона [0, 255]: "
                    f"[{np.min(self.data)}, {np.max(self.data)}]"
                )

        except Exception as e:
            raise DataIntegrityError(f"Ошибка проверки целостности данных: {str(e)}")