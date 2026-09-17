import logging
from datetime import datetime
from pathlib import Path

#DEBUG<INFO<WARNING<ERROR<CRITICAL

def configure_logging():
    # Создаем общую папку logs в корне проекта.
    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Для каждого запуска создаем отдельный файл с датой и временем.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    log_path = logs_dir / f"test_{timestamp}.log"
    # Получаем главный logger, через который проходят сообщения всего проекта.
    logger = logging.getLogger()
    # Разрешаем logger принимать сообщения всех уровней, включая DEBUG.
    logger.setLevel(logging.DEBUG)

    # Скрываем подробные внутренние логи Selenium и оставляем только важные ошибки.
    logging.getLogger("selenium").setLevel(logging.WARNING)

    # Задаем единый вид каждой строки лога: время, уровень, имя и сообщение.
    formatter = logging.Formatter(
        "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
    )

    # Создаем handler для вывода логов в консоль.
    console_handler = logging.StreamHandler()
    # В консоль выводим INFO и более важные сообщения, но скрываем DEBUG.
    console_handler.setLevel(logging.INFO)
    # Применяем к консольным сообщениям общий формат.
    console_handler.setFormatter(formatter)

    # Создаем handler для записи логов в файл.
    file_handler = logging.FileHandler(
        log_path,
        mode="w",
        encoding="utf-8",
    )
    # В файл записываем INFO и DEBUG, включая события нашего listener.
    file_handler.setLevel(logging.DEBUG)
    # Применяем к файлу тот же формат, что и к консоли.
    file_handler.setFormatter(formatter)

    # Удаляем старые handlers, чтобы сообщения не дублировались.
    logger.handlers.clear()
    # Подключаем handler консоли к главному logger.
    logger.addHandler(console_handler)
    # Подключаем handler файла к главному logger.
    logger.addHandler(file_handler)