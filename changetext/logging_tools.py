import functools
import logging
import sys
from logging.handlers import RotatingFileHandler


class LoggerWrapper:
    def __init__(self, stream=None):
        self.logged = set()
        self.logger = logging.Logger(name=__name__, level=logging.DEBUG)

        if not stream:
            stream = sys.stdout

        file_handler = RotatingFileHandler("changetext.log", encoding="utf-8", backupCount=0, maxBytes=1024**2)
        file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        stream_handler = logging.StreamHandler(stream)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def write(self, text, output):
        if text not in self.logged:
            self.logger.debug("{!r} --> {!r}".format(text, output))
            self.logged.add(text)


@functools.lru_cache()
def get_logger(stream=None) -> LoggerWrapper:
    return LoggerWrapper(stream)


def log_exceptions(func):
    @functools.wraps(func)
    def wrapper(text):
        try:
            return func(text)
        except Exception:
            get_logger().logger.exception("An exception occurred. Initial string: {!r}".format(text))

    return wrapper
