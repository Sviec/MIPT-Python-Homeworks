from typing import Any
import numpy as np
from task_5.task_2.image_types.image import Image
from task_5.task_2.utils.image_exceptions import (
    ImageError, DataSizeError, DataFormatError, DataIntegrityError,
    MemoryAllocationError, ValueRangeError
)


class MonochromeImage(Image):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        try:
            self.data = np.zeros((height, width), dtype=np.uint8)
        except MemoryError:
            raise MemoryAllocationError(f"Недостаточно памяти для создания изображения {width}x{height}")
        except Exception as e:
            raise ImageError(f"Ошибка инициализации MonochromeImage: {str(e)}")

    def _validate_monochrome_value(self, value: int) -> None:
        """Проверка корректности монохромного значения"""
        if not (0 <= value <= 255):
            raise ValueRangeError(f"Недопустимое значение яркости: {value}. Допустимый диапазон [0, 255]")

    def get_pixel(self, x: int, y: int) -> Any:
        try:
            self._validate_coordinates(x, y)
            return self.data[y, x]
        except Exception as e:
            raise ImageError(f"Ошибка получения пикселя ({x}, {y}): {str(e)}")

    def set_pixel(self, x: int, y: int, value: int):
        try:
            self._validate_coordinates(x, y)
            self._validate_monochrome_value(value)
            self.data[y, x] = max(0, min(255, value))
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

            if self.data.shape != (self.height, self.width):
                raise DataSizeError(
                    f"Несоответствие размеров данных: ожидалось ({self.height}, {self.width}), "
                    f"получено {self.data.shape}"
                )

            if self.data.dtype != np.uint8:
                raise DataFormatError(f"Неверный тип данных: ожидался uint8, получен {self.data.dtype}")

            # Проверка диапазона значений
            if np.min(self.data) < 0 or np.max(self.data) > 255:
                raise ValueRangeError(
                    f"Значения яркости вне диапазона [0, 255]: [{np.min(self.data)}, {np.max(self.data)}]"
                )

        except Exception as e:
            raise DataIntegrityError(f"Ошибка проверки целостности данных: {str(e)}")