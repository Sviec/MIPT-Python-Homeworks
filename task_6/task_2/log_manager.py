import logging
import logging.handlers
from datetime import datetime
import os
import sys
import uuid
from typing import Optional, Dict, Any
from enum import Enum


class LogLevel(Enum):
    """Уровни событий"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


class LogManager:
    """
    Менеджер логирования с расширенной функциональностью
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_file: str = "log.txt", max_bytes: int = 10 * 1024 * 1024, backup_count: int = 5):
        if self._initialized:
            return

        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.current_session_id = str(uuid.uuid4())
        self.current_user = "system"

        log_dir = os.path.dirname(os.path.abspath(log_file))
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self._setup_logging()
        self._initialized = True

        self.info("LogManager инициализирован",
                  component="LogManager",
                  additional_info={"session_id": self.current_session_id})

    def _setup_logging(self):
        """Настройка системы логирования"""
        # Создаем логгер
        self.logger = logging.getLogger('ImageProcessor')
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _create_log_record(self, level: LogLevel, message: str, component: str,
                           event_id: Optional[str] = None, user: Optional[str] = None,
                           additional_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Создание структурированной записи лога"""
        if event_id is None:
            event_id = str(uuid.uuid4())[:8]

        if user is None:
            user = self.current_user

        record = {
            "timestamp": datetime.now().isoformat(),
            "level": level.value,
            "component": component,
            "message": message,
            "event_id": event_id,
            "user": user,
            "session_id": self.current_session_id,
            "additional_info": additional_info or {}
        }

        if level in [LogLevel.ERROR, LogLevel.FATAL]:
            import traceback
            record["additional_info"]["stack_trace"] = traceback.format_stack()

        return record

    @staticmethod
    def _format_log_message(record: Dict[str, Any]) -> str:
        """Форматирование записи лога в строку"""
        return f"[{record['event_id']}] {record['message']}"

    def _log(self, level: LogLevel, message: str, component: str,
             event_id: Optional[str] = None, user: Optional[str] = None,
             additional_info: Optional[Dict[str, Any]] = None):
        """Базовый метод логирования"""
        try:
            record = self._create_log_record(level, message, component, event_id, user, additional_info)
            formatted_message = self._format_log_message(record)

            if level == LogLevel.DEBUG:
                self.logger.debug(formatted_message)
            elif level == LogLevel.INFO:
                self.logger.info(formatted_message)
            elif level == LogLevel.WARN:
                self.logger.warning(formatted_message)
            elif level == LogLevel.ERROR:
                self.logger.error(formatted_message)
            elif level == LogLevel.FATAL:
                self.logger.critical(formatted_message)

        except Exception as e:
            print(f"LOG ERROR: {e}")

    def debug(self, message: str, component: str = "Unknown",
              event_id: Optional[str] = None, user: Optional[str] = None,
              additional_info: Optional[Dict[str, Any]] = None):
        """Запись отладочного сообщения"""
        self._log(LogLevel.DEBUG, message, component, event_id, user, additional_info)

    def info(self, message: str, component: str = "Unknown",
             event_id: Optional[str] = None, user: Optional[str] = None,
             additional_info: Optional[Dict[str, Any]] = None):
        """Запись информационного сообщения"""
        self._log(LogLevel.INFO, message, component, event_id, user, additional_info)

    def warn(self, message: str, component: str = "Unknown",
             event_id: Optional[str] = None, user: Optional[str] = None,
             additional_info: Optional[Dict[str, Any]] = None):
        """Запись предупреждения"""
        self._log(LogLevel.WARN, message, component, event_id, user, additional_info)

    def error(self, message: str, component: str = "Unknown",
              event_id: Optional[str] = None, user: Optional[str] = None,
              additional_info: Optional[Dict[str, Any]] = None):
        """Запись ошибки"""
        self._log(LogLevel.ERROR, message, component, event_id, user, additional_info)

    def fatal(self, message: str, component: str = "Unknown",
              event_id: Optional[str] = None, user: Optional[str] = None,
              additional_info: Optional[Dict[str, Any]] = None):
        """Запись фатальной ошибки"""
        self._log(LogLevel.FATAL, message, component, event_id, user, additional_info)

    def set_user(self, user: str):
        """Установка текущего пользователя"""
        self.current_user = user
        self.info(f"Пользователь установлен: {user}", "LogManager")

    def set_session_id(self, session_id: str):
        """Установка идентификатора сессии"""
        self.current_session_id = session_id
        self.info(f"ID сессии установлен: {session_id}", "LogManager")

    def cleanup(self):
        """Очистка ресурсов"""
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
        self.info("LogManager завершил работу", "LogManager")


log_manager = LogManager()
