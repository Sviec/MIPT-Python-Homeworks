class ImageError(Exception):
    """Базовое исключение для ошибок изображений"""
    pass


class FileOperationError(ImageError):
    """Ошибка операций с файлами"""
    pass


class DataFormatError(ImageError):
    """Ошибка формата данных"""
    pass


class DataSizeError(ImageError):
    """Ошибка размеров данных"""
    pass


class DataIntegrityError(ImageError):
    """Ошибка целостности данных"""
    pass


class MemoryAllocationError(ImageError):
    """Ошибка выделения памяти"""
    pass


class CoordinateError(DataSizeError):
    """Ошибка координат"""
    pass


class ValueRangeError(DataIntegrityError):
    """Ошибка диапазона значений"""
    pass
