import logging
import os
import gzip
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

class LogHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LogHandler, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.log_file_path = os.getenv("LOG_FILE_PATH", "log/app.log")
        self.logger = self._setup_logger()

    def _setup_logger(self):
        log_dir = os.path.dirname(self.log_file_path)
        # Create the log directory if it does not exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger("app_logger")
        logger.setLevel(self.log_level)

        # Create handlers
        file_handler = TimedRotatingFileHandler(
            self.log_file_path, when="midnight", interval=1, backupCount=7
        )
        file_handler.suffix = "%Y-%m-%d.gz"
        file_handler.rotator = self._rotator
        file_handler.namer = self._namer

        size_handler = RotatingFileHandler(
            self.log_file_path, maxBytes=10*1024*1024, backupCount=5
        )

        console_handler = logging.StreamHandler()

        # Set level for handlers
        file_handler.setLevel(self.log_level)
        size_handler.setLevel(self.log_level)
        console_handler.setLevel(self.log_level)

        # Create formatters and add them to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        size_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(size_handler)
        logger.addHandler(console_handler)

        return logger

    def _rotator(self, source, dest):
        with open(source, "rb") as f_in, gzip.open(dest, "wb") as f_out:
            f_out.writelines(f_in)
        os.remove(source)

    def _namer(self, name):
        return name + ".gz"

    def get_logger(self):
        return self.logger