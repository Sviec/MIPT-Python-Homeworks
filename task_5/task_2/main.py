import numpy as np

from task_5.task_2.image_converter.image_converter import ImageConverter
from task_5.task_2.image_types.binary_image import BinaryImage
from task_5.task_2.image_types.color_image import ColorImage
from task_5.task_2.image_types.monochrome_image import MonochromeImage

binary_img = BinaryImage(10, 10)
monochrome_img = MonochromeImage(10, 10)
color_img = ColorImage(10, 10)

for y in range(10):
    for x in range(10):
        binary_img.set_pixel(x, y, (x + y) % 2)
        monochrome_img.set_pixel(x, y, (x * 25 + y * 25) % 256)
        color_img.set_pixel(x, y, (x * 25, y * 25, (x + y) * 12))

corrected_mono = ImageConverter.monochrome_to_monochrome_correction(monochrome_img)
print(
    f"1. Монохромная коррекция: {np.mean(monochrome_img.get_data()):.1f} -> {np.mean(corrected_mono.get_data()):.1f}"
)

corrected_color = ImageConverter.color_to_color_correction(color_img)
print(f"2. Цветная коррекция выполнена")

same_binary = ImageConverter.binary_to_binary(binary_img)
print(f"3. Бинарное -> Бинарное: идентично")

gray_from_color = ImageConverter.color_to_monochrome(color_img)
print(f"4. Цветное -> Монохромное: средняя яркость {np.mean(gray_from_color.get_data()):.1f}")

color_from_mono = ImageConverter.monochrome_to_color(monochrome_img)
print(f"5. Монохромное -> Цветное: размер {color_from_mono.data.shape}")

binary_from_mono = ImageConverter.monochrome_to_binary(monochrome_img)
print(f"6. Монохромное -> Бинарное: {np.sum(binary_from_mono.get_data())} белых пикселей")

mono_from_binary = ImageConverter.binary_to_monochrome(binary_img)
print(f"7. Бинарное -> Монохромное: макс. расстояние {np.max(mono_from_binary.get_data())}")

binary_from_color = ImageConverter.color_to_binary(color_img)
print(f"8. Цветное -> Бинарное: {np.sum(binary_from_color.get_data())} белых пикселей")

color_from_binary = ImageConverter.binary_to_color(binary_img)
print(f"9. Бинарное -> Цветное: размер {color_from_binary.data.shape}")