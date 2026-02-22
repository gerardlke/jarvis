import logging


class Logger:
    logger = None

    @classmethod
    def setup(cls, file=r"myapp.log", level=logging.INFO):
        if not cls.logger:
            # Create formatter
            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
                datefmt="%H:%M:%S"
            )

            # Create file handler
            file_handler = logging.FileHandler(file)
            file_handler.setFormatter(formatter)

            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            # Main logger
            cls.logger = logging.getLogger("Jarvis")
            cls.logger.setLevel(level)
            cls.logger.addHandler(file_handler)
            cls.logger.addHandler(console_handler)

    @classmethod
    def info(cls, sender, message):
        if cls.logger:
            cls.logger.info(f"[{sender}]: {message}")

    @classmethod
    def error(cls, sender, message):
        if cls.logger:
            cls.logger.error(f"[{sender}]: {message}")

    @classmethod
    def warning(cls, sender, message):
        if cls.logger:
            cls.logger.warning(f"[{sender}]: {message}")
