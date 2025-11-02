from typing import Tuple, Optional, Dict

import numpy as np

from task_5.task_2.image_types.binary_image import BinaryImage
from task_5.task_2.image_types.color_image import ColorImage
from task_5.task_2.image_types.monochrome_image import MonochromeImage


class ImageConverter:
    @staticmethod
    def monochrome_to_monochrome_correction(
            src: MonochromeImage,
            target_mean: int = 128,
            target_std: int = 50
    ) -> MonochromeImage:
        """Статистическая цветокоррекция для монохромных изображений"""
        result = MonochromeImage(src.width, src.height)
        data = src.get_data().astype(np.float32)

        cur_mean = np.mean(data)
        cur_std = np.std(data)

        if cur_std > 0:
            corrected_data = (data - cur_mean) * (target_std / cur_std) + target_mean
            corrected_data = np.clip(corrected_data, 0, 255).astype(np.uint8)
        else:
            corrected_data = np.full_like(data, target_mean, dtype=np.uint8)

        result.data = corrected_data
        return result

    @staticmethod
    def color_to_color_correction(
            src: ColorImage,
            target_means: Tuple[int, int, int] = (128, 128, 128),
            target_stds: Tuple[int, int, int] = (50, 50, 50)
    ) -> ColorImage:
        """Поканальная статистическая цветокоррекция для цветных изображений"""
        result = ColorImage(src.width, src.height)
        data = src.get_data().astype(np.float32)

        corrected_data = np.zeros_like(data)

        for channel in range(3):
            channel_data = data[:, :, channel]
            cur_mean = np.mean(channel_data)
            cur_std = np.std(channel_data)

            if cur_std > 0:
                corrected_channel = (channel_data - cur_mean) * (target_stds[channel] / cur_std) + target_means[channel]
                corrected_channel = np.clip(corrected_channel, 0, 255)
            else:
                corrected_channel = np.full_like(channel_data, target_means[channel])
            corrected_data[:, :, channel] = corrected_channel

        result.data = corrected_data.astype(np.uint8)
        return result

    @staticmethod
    def binary_to_binary(src: BinaryImage) -> BinaryImage:
        """Бинарное в бинарное (без изменений)"""
        result = BinaryImage(src.width, src.height)
        result.data = src.get_data().copy()
        return result

    @staticmethod
    def color_to_monochrome(src: ColorImage) -> MonochromeImage:
        """Цветное в монохромное (среднее по каналам)"""
        result = MonochromeImage(src.width, src.height)
        data = src.get_data().astype(np.float32)

        gray_data = (0.299 * data[:, :, 0] +
                     0.587 * data[:, :, 1] +
                     0.114 * data[:, :, 2])
        gray_data = np.clip(gray_data, 0, 255).astype(np.uint8)
        result.data = gray_data
        return result

    @staticmethod
    def monochrome_to_color(
            src: MonochromeImage,
            palette: Optional[Dict[int, Tuple[int, int, int]]] = None
    ) -> ColorImage:
        """Монохромное в цветное с использованием палитры"""
        result = ColorImage(src.width, src.height)

        if palette is None:
            palette = {
                i: (0, 0, i * 2) if i < 128
                else ((i - 128) * 2, (i - 128) * 2, 255)
                for i in range(256)
            }

        data = src.get_data()

        for y in range(src.height):
            for x in range(src.width):
                gray_value = int(data[y, x])  # Явное преобразование к int
                if gray_value in palette:
                    color = palette[gray_value]
                else:
                    # Интерполяция для значений вне палитры
                    if gray_value < 128:
                        color = (0, 0, gray_value * 2)
                    else:
                        color = ((gray_value - 128) * 2, (gray_value - 128) * 2, 255)

                result.set_pixel(x, y, color)

        return result

    @staticmethod
    def monochrome_to_binary(
            src: MonochromeImage,
            threshold: Optional[int] = None,
            method: str = "otsu"
    ) -> BinaryImage:
        """Монохромное в бинарное"""
        result = BinaryImage(src.width, src.height)
        data = src.get_data()

        if threshold is None:
            if method == "otsu":
                threshold = ImageConverter._otsu_threshold(data)
            else:
                threshold = 128

        binary_data = (data > threshold).astype(np.uint8)
        result.data = binary_data
        return result

    @staticmethod
    def _otsu_threshold(data: np.ndarray) -> int:
        """Алгоритм Отсу для автоматического определения порога"""
        histogram, _ = np.histogram(data.flatten(), bins=256, range=(0, 256))
        total_pixels = data.size

        sum_total = np.sum(np.arange(256) * histogram)
        sum_back = 0
        weight_back = 0
        variance_max = 0
        threshold = 0

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

    @staticmethod
    def binary_to_monochrome(src: BinaryImage) -> MonochromeImage:
        """Бинарное в монохромное (distance transform)"""
        result = MonochromeImage(src.width, src.height)
        binary_data = src.get_data()

        distance_map = ImageConverter._distance_transform(binary_data)

        if np.max(distance_map) > 0:
            normalized = (distance_map / np.max(distance_map) * 255).astype(np.uint8)
        else:
            normalized = np.zeros_like(distance_map, dtype=np.uint8)

        result.data = normalized
        return result

    @staticmethod
    def _distance_transform(binary_data: np.ndarray) -> np.ndarray:
        """Вычисление distance transform"""
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

    @staticmethod
    def color_to_binary(src: ColorImage, threshold: Optional[int] = None) -> BinaryImage:
        """Цветное в бинарное через монохромное"""
        monochrome = ImageConverter.color_to_monochrome(src)
        return ImageConverter.monochrome_to_binary(monochrome, threshold)

    @staticmethod
    def binary_to_color(src: BinaryImage, palette=None) -> ColorImage:
        """Бинарное в цветное через монохромное"""
        monochrome = ImageConverter.binary_to_monochrome(src)
        return ImageConverter.monochrome_to_color(monochrome, palette)
