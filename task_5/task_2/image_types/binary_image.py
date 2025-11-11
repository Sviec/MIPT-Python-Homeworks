import numpy as np
from task_5.task_2.image_types.image import Image
from task_5.task_2.utils.image_exceptions import (
    ImageError, DataSizeError, DataFormatError, DataIntegrityError,
    MemoryAllocationError, ValueRangeError
)


class BinaryImage(Image):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        try:
            self.data = np.zeros((height, width), dtype=np.uint8)
        except MemoryError:
            raise MemoryAllocationError(f"Недостаточно памяти для создания изображения {width}x{height}")
        except Exception as e:
            raise ImageError(f"Ошибка инициализации BinaryImage: {str(e)}")

    def _validate_binary_value(self, value: int) -> None:
        """Проверка корректности бинарного значения"""
        if value not in (0, 1):
            raise ValueRangeError(f"Недопустимое бинарное значение: {value}. Допустимы 0 или 1")

    def get_pixel(self, x: int, y: int):
        try:
            self._validate_coordinates(x, y)
            return self.data[y, x]
        except Exception as e:
            raise ImageError(f"Ошибка получения пикселя ({x}, {y}): {str(e)}")

    def set_pixel(self, x: int, y: int, value: int):
        try:
            self._validate_coordinates(x, y)
            self._validate_binary_value(value)
            self.data[y, x] = 1 if value else 0
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

            # Проверка что все значения 0 или 1
            unique_values = np.unique(self.data)
            if not set(unique_values).issubset({0, 1}):
                raise ValueRangeError(
                    f"Обнаружены небинарные значения: {unique_values}. Допустимы только 0 и 1"
                )

        except Exception as e:
            raise DataIntegrityError(f"Ошибка проверки целостности данных: {str(e)}")