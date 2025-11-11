from typing import Tuple, Optional, Dict
import numpy as np
import logging

from task_5.task_2.image_types.binary_image import BinaryImage
from task_5.task_2.image_types.color_image import ColorImage
from task_5.task_2.image_types.monochrome_image import MonochromeImage
from task_5.task_2.utils.image_exceptions import (
    ImageError, DataFormatError, DataSizeError, DataIntegrityError,
    ValueRangeError, CoordinateError
)

logger = logging.getLogger(__name__)


class ImageConverter:

    @staticmethod
    def _validate_conversion_parameters(target_mean: int = None, target_std: int = None,
                                        target_means: Tuple = None, target_stds: Tuple = None,
                                        threshold: int = None, method: str = None) -> None:
        """Валидация параметров преобразования"""
        if target_mean is not None and not (0 <= target_mean <= 255):
            raise ValueRangeError(f"Недопустимое целевое среднее: {target_mean}. Допустимый диапазон [0, 255]")

        if target_std is not None and target_std < 0:
            raise ValueRangeError(f"Недопустимое целевое СКО: {target_std}. Должно быть неотрицательным")

        if target_means is not None:
            for i, mean in enumerate(target_means):
                if not (0 <= mean <= 255):
                    raise ValueRangeError(f"Недопустимое среднее для канала {i}: {mean}")

        if target_stds is not None:
            for i, std in enumerate(target_stds):
                if std < 0:
                    raise ValueRangeError(f"Недопустимое СКО для канала {i}: {std}")

        if threshold is not None and not (0 <= threshold <= 255):
            raise ValueRangeError(f"Недопустимый порог: {threshold}. Допустимый диапазон [0, 255]")

        if method is not None and method not in ["otsu", "fixed"]:
            raise DataFormatError(f"Неизвестный метод: {method}. Допустимы: 'otsu', 'fixed'")

    @staticmethod
    def _validate_image_data(data: np.ndarray, expected_shape: Tuple = None,
                             value_range: Tuple = None, data_type: type = None) -> None:
        """Валидация данных изображения"""
        if data is None:
            raise DataIntegrityError("Данные изображения не инициализированы")

        if not isinstance(data, np.ndarray):
            raise DataFormatError(f"Ожидался numpy array, получен {type(data)}")

        if expected_shape and data.shape != expected_shape:
            raise DataSizeError(f"Неверный размер данных: ожидалось {expected_shape}, получено {data.shape}")

        if data_type and data.dtype != data_type:
            raise DataFormatError(f"Неверный тип данных: ожидался {data_type}, получен {data.dtype}")

        if value_range and data.size > 0:
            min_val, max_val = np.min(data), np.max(data)
            if min_val < value_range[0] or max_val > value_range[1]:
                raise DataIntegrityError(
                    f"Значения данных вне допустимого диапазона: [{min_val}, {max_val}] "
                    f"вместо [{value_range[0]}, {value_range[1]}]"
                )

    @staticmethod
    def monochrome_to_monochrome_correction(
            src: MonochromeImage,
            target_mean: int = 128,
            target_std: int = 50
    ) -> MonochromeImage:
        """Статистическая цветокоррекция для монохромных изображений"""
        try:
            logger.info("Начало монохромной коррекции")

            ImageConverter._validate_conversion_parameters(target_mean=target_mean, target_std=target_std)

            if not isinstance(src, MonochromeImage):
                raise DataFormatError(f"Ожидался MonochromeImage, получен {type(src).__name__}")

            src.validate_data_integrity()

            result = MonochromeImage(src.width, src.height)
            data = src.get_data().astype(np.float32)

            ImageConverter._validate_image_data(data, (src.height, src.width), (0, 255), np.float32)

            cur_mean = np.mean(data)
            cur_std = np.std(data)

            if cur_std > 0:
                corrected_data = (data - cur_mean) * (target_std / cur_std) + target_mean
                corrected_data = np.clip(corrected_data, 0, 255).astype(np.uint8)
            else:
                corrected_data = np.full_like(data, target_mean, dtype=np.uint8)

            ImageConverter._validate_image_data(corrected_data, (src.height, src.width), (0, 255), np.uint8)

            result.data = corrected_data
            result.validate_data_integrity()

            logger.info("Монохромная коррекция завершена успешно")
            return result

        except Exception as e:
            logger.error(f"Ошибка в монохромной коррекции: {str(e)}")
            if isinstance(e, (DataFormatError, DataSizeError, DataIntegrityError, ValueRangeError)):
                raise
            raise ImageError(f"Ошибка монохромной коррекции: {str(e)}")

    @staticmethod
    def color_to_color_correction(
            src: ColorImage,
            target_means: Tuple[int, int, int] = (128, 128, 128),
            target_stds: Tuple[int, int, int] = (50, 50, 50)
    ) -> ColorImage:
        """Поканальная статистическая цветокоррекция для цветных изображений"""
        try:
            logger.info("Начало цветной коррекции")

            ImageConverter._validate_conversion_parameters(target_means=target_means, target_stds=target_stds)

            if not isinstance(src, ColorImage):
                raise DataFormatError(f"Ожидался ColorImage, получен {type(src).__name__}")

            src.validate_data_integrity()

            result = ColorImage(src.width, src.height)
            data = src.get_data().astype(np.float32)

            ImageConverter._validate_image_data(data, (src.height, src.width, 3), (0, 255), np.float32)

            corrected_data = np.zeros_like(data)

            for channel in range(3):
                channel_data = data[:, :, channel]
                cur_mean = np.mean(channel_data)
                cur_std = np.std(channel_data)

                if cur_std > 0:
                    corrected_channel = (channel_data - cur_mean) * (target_stds[channel] / cur_std) + target_means[
                        channel]
                    corrected_channel = np.clip(corrected_channel, 0, 255)
                else:
                    corrected_channel = np.full_like(channel_data, target_means[channel])
                corrected_data[:, :, channel] = corrected_channel

            result_data = corrected_data.astype(np.uint8)
            ImageConverter._validate_image_data(result_data, (src.height, src.width, 3), (0, 255), np.uint8)

            result.data = result_data
            result.validate_data_integrity()

            logger.info("Цветная коррекция завершена успешно")
            return result

        except Exception as e:
            logger.error(f"Ошибка в цветной коррекции: {str(e)}")
            if isinstance(e, (DataFormatError, DataSizeError, DataIntegrityError, ValueRangeError)):
                raise
            raise ImageError(f"Ошибка цветной коррекции: {str(e)}")

    @staticmethod
    def binary_to_binary(src: BinaryImage) -> BinaryImage:
        """Бинарное в бинарное (без изменений)"""
        try:
            logger.info("Начало бинарного преобразования")

            if not isinstance(src, BinaryImage):
                raise DataFormatError(f"Ожидался BinaryImage, получен {type(src).__name__}")

            src.validate_data_integrity()

            result = BinaryImage(src.width, src.height)
            data = src.get_data().copy()

            ImageConverter._validate_image_data(data, (src.height, src.width), (0, 1), np.uint8)

            result.data = data
            result.validate_data_integrity()

            logger.info("Бинарное преобразование завершено успешно")
            return result

        except Exception as e:
            logger.error(f"Ошибка в бинарном преобразовании: {str(e)}")
            if isinstance(e, (DataFormatError, DataSizeError, DataIntegrityError)):
                raise
            raise ImageError(f"Ошибка бинарного преобразования: {str(e)}")

    @staticmethod
    def color_to_monochrome(src: ColorImage) -> MonochromeImage:
        """Цветное в монохромное (среднее по каналам)"""
        try:
            logger.info("Начало преобразования цветное -> монохромное")

            if not isinstance(src, ColorImage):
                raise DataFormatError(f"Ожидался ColorImage, получен {type(src).__name__}")

            src.validate_data_integrity()

            result = MonochromeImage(src.width, src.height)
            data = src.get_data().astype(np.float32)

            ImageConverter._validate_image_data(data, (src.height, src.width, 3), (0, 255), np.float32)

            gray_data = (0.299 * data[:, :, 0] +
                         0.587 * data[:, :, 1] +
                         0.114 * data[:, :, 2])
            gray_data = np.clip(gray_data, 0, 255).astype(np.uint8)

            ImageConverter._validate_image_data(gray_data, (src.height, src.width), (0, 255), np.uint8)

            result.data = gray_data
            result.validate_data_integrity()

            logger.info("Преобразование цветное -> монохромное завершено успешно")
            return result

        except Exception as e:
            logger.error(f"Ошибка в преобразовании цветное -> монохромное: {str(e)}")
            if isinstance(e, (DataFormatError, DataSizeError, DataIntegrityError)):
                raise
            raise ImageError(f"Ошибка преобразования цветное -> монохромное: {str(e)}")

    @staticmethod
    def monochrome_to_color(
            src: MonochromeImage,
            palette: Optional[Dict[int, Tuple[int, int, int]]] = None
    ) -> ColorImage:
        """Монохромное в цветное с использованием палитры"""
        try:
            logger.info("Начало преобразования монохромное -> цветное")

            if not isinstance(src, MonochromeImage):
                raise DataFormatError(f"Ожидался MonochromeImage, получен {type(src).__name__}")

            src.validate_data_integrity()

            result = ColorImage(src.width, src.height)

            if palette is None:
                palette = {
                    i: (0, 0, i * 2) if i < 128
                    else ((i - 128) * 2, (i - 128) * 2, 255)
                    for i in range(256)
                }

            data = src.get_data()
            ImageConverter._validate_image_data(data, (src.height, src.width), (0, 255), np.uint8)

            for y in range(src.height):
                for x in range(src.width):
                    gray_value = int(data[y, x])
                    if not (0 <= gray_value <= 255):
                        raise DataIntegrityError(f"Недопустимое значение серого: {gray_value}")

                    if gray_value in palette:
                        color = palette[gray_value]
                    else:
                        if gray_value < 128:
                            color = (0, 0, gray_value * 2)
                        else:
                            color = ((gray_value - 128) * 2, (gray_value - 128) * 2, 255)

                    for channel in color:
                        if not (0 <= channel <= 255):
                            raise DataIntegrityError(f"Недопустимое значение цвета: {channel}")

                    result.set_pixel(x, y, color)

            result_data = result.get_data()
            ImageConverter._validate_image_data(result_data, (src.height, src.width, 3), (0, 255), np.uint8)
            result.validate_data_integrity()

            logger.info("Преобразование монохромное -> цветное завершено успешно")
            return result

        except Exception as e:
            logger.error(f"Ошибка в преобразовании монохромное -> цветное: {str(e)}")
            if isinstance(e, (DataFormatError, DataSizeError, DataIntegrityError, ValueRangeError, CoordinateError)):
                raise
            raise ImageError(f"Ошибка преобразования монохромное -> цветное: {str(e)}")

    @staticmethod
    def monochrome_to_binary(
            src: MonochromeImage,
            threshold: Optional[int] = None,
            method: str = "otsu"
    ) -> BinaryImage:
        """Монохромное в бинарное"""
        try:
            logger.info("Начало преобразования монохромное -> бинарное")

            if not isinstance(src, MonochromeImage):
                raise DataFormatError(f"Ожидался MonochromeImage, получен {type(src).__name__}")

            ImageConverter._validate_conversion_parameters(threshold=threshold, method=method)

            src.validate_data_integrity()

            result = BinaryImage(src.width, src.height)
            data = src.get_data()

            ImageConverter._validate_image_data(data, (src.height, src.width), (0, 255), np.uint8)

            if threshold is None:
                if method == "otsu":
                    threshold = ImageConverter._otsu_threshold(data)
                else:
                    threshold = 128

            binary_data = (data > threshold).astype(np.uint8)
            ImageConverter._validate_image_data(binary_data, (src.height, src.width), (0, 1), np.uint8)

            result.data = binary_data
            result.validate_data_integrity()

            logger.info("Преобразование монохромное -> бинарное завершено успешно")
            return result

        except Exception as e:
            logger.error(f"Ошибка в преобразовании монохромное -> бинарное: {str(e)}")
            if isinstance(e, (DataFormatError, DataSizeError, DataIntegrityError, ValueRangeError)):
                raise
            raise ImageError(f"Ошибка преобразования монохромное -> бинарное: {str(e)}")

    @staticmethod
    def _otsu_threshold(data: np.ndarray) -> int:
        """Алгоритм Отсу для автоматического определения порога"""
        try:
            ImageConverter._validate_image_data(data, value_range=(0, 255))

            histogram, _ = np.histogram(data.flatten(), bins=256, range=(0, 256))
            total_pixels = data.size

            if total_pixels == 0:
                raise DataIntegrityError("Пустые данные для алгоритма Отсу")

            sum_total = np.sum(np.arange(256) * histogram)
            sum_back = 0
            weight_back = 0
            variance_max = 0
            threshold = 128

            for i in range(256):
                weight_back += histogram[i]
                if weight_back == 0:
                    continue

                weight_fore = total_pixels - weight_back
                if weight_fore == 0:
                    break

                sum_back += i * histogram[i]
                mean_back = sum_back / weight_back
                mean_fore = (sum_total - sum_back) / weight_fore

                variance_between = weight_back * weight_fore * (mean_back - mean_fore) ** 2

                if variance_between > variance_max:
                    variance_max = variance_between
                    threshold = i

            return threshold

        except Exception as e:
            logger.error(f"Ошибка в алгоритме Отсу: {str(e)}")
            if isinstance(e, (DataFormatError, DataSizeError, DataIntegrityError)):
                raise
            raise ImageError(f"Ошибка алгоритма Отсу: {str(e)}")

    @staticmethod
    def binary_to_monochrome(src: BinaryImage) -> MonochromeImage:
        """Бинарное в монохромное (distance transform)"""
        try:
            logger.info("Начало преобразования бинарное -> монохромное")

            if not isinstance(src, BinaryImage):
                raise DataFormatError(f"Ожидался BinaryImage, получен {type(src).__name__}")

            src.validate_data_integrity()

            result = MonochromeImage(src.width, src.height)
            binary_data = src.get_data()

            ImageConverter._validate_image_data(binary_data, (src.height, src.width), (0, 1), np.uint8)

            distance_map = ImageConverter._distance_transform(binary_data)

            ImageConverter._validate_image_data(distance_map, (src.height, src.width))

            if np.max(distance_map) > 0:
                normalized = (distance_map / np.max(distance_map) * 255).astype(np.uint8)
            else:
                normalized = np.zeros_like(distance_map, dtype=np.uint8)

            ImageConverter._validate_image_data(normalized, (src.height, src.width), (0, 255), np.uint8)

            result.data = normalized
            result.validate_data_integrity()

            logger.info("Преобразование бинарное -> монохромное завершено успешно")
            return result

        except Exception as e:
            logger.error(f"Ошибка в преобразовании бинарное -> монохромное: {str(e)}")
            if isinstance(e, (DataFormatError, DataSizeError, DataIntegrityError)):
                raise
            raise ImageError(f"Ошибка преобразования бинарное -> монохромное: {str(e)}")

    @staticmethod
    def _distance_transform(binary_data: np.ndarray) -> np.ndarray:
        """Вычисление distance transform"""
        try:
            height, width = binary_data.shape
            distance_map = np.full((height, width), float('inf'), dtype=np.float32)

            for y in range(height):
                for x in range(width):
                    if binary_data[y, x] == 1:
                        distance_map[y, x] = 0
                    else:
                        if y > 0:
                            current_val = float(distance_map[y, x])
                            compare_val = float(distance_map[y - 1, x] + 1)
                            distance_map[y, x] = min(current_val, compare_val)
                        if x > 0:
                            current_val = float(distance_map[y, x])
                            compare_val = float(distance_map[y, x - 1] + 1)
                            distance_map[y, x] = min(current_val, compare_val)

            for y in range(height - 1, -1, -1):
                for x in range(width - 1, -1, -1):
                    if y < height - 1:
                        current_val = float(distance_map[y, x])
                        compare_val = float(distance_map[y + 1, x] + 1)
                        distance_map[y, x] = min(current_val, compare_val)
                    if x < width - 1:
                        current_val = float(distance_map[y, x])
                        compare_val = float(distance_map[y, x + 1] + 1)
                        distance_map[y, x] = min(current_val, compare_val)

            return distance_map

        except Exception as e:
            logger.error(f"Ошибка в distance transform: {str(e)}")
            raise ImageError(f"Ошибка distance transform: {str(e)}")

    @staticmethod
    def color_to_binary(src: ColorImage, threshold: Optional[int] = None) -> BinaryImage:
        """Цветное в бинарное через монохромное"""
        try:
            monochrome = ImageConverter.color_to_monochrome(src)
            return ImageConverter.monochrome_to_binary(monochrome, threshold)
        except Exception as e:
            logger.error(f"Ошибка в преобразовании цветное -> бинарное: {str(e)}")
            if isinstance(e, ImageError):
                raise
            raise ImageError(f"Ошибка преобразования цветное -> бинарное: {str(e)}")

    @staticmethod
    def binary_to_color(src: BinaryImage, palette=None) -> ColorImage:
        """Бинарное в цветное через монохромное"""
        try:
            monochrome = ImageConverter.binary_to_monochrome(src)
            return ImageConverter.monochrome_to_color(monochrome, palette)
        except Exception as e:
            logger.error(f"Ошибка в преобразовании бинарное -> цветное: {str(e)}")
            if isinstance(e, ImageError):
                raise
            raise ImageError(f"Ошибка преобразования бинарное -> цветное: {str(e)}")
