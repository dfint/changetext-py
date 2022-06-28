import functools
import re

from changetext.logging_tools import get_logger


class CorrectorRegistry:
    def __init__(self):
        self.changes = list()

    def register(self, regex=None, predicate=None):
        def decorator(func):
            nonlocal regex, predicate

            if regex is not None:
                if isinstance(regex, str):
                    regex = re.compile(regex)

                predicate = lambda text: regex.search(text)

            if predicate is None:
                predicate = lambda _text: True

            self.changes.append((predicate, func))

            @functools.wraps(func)
            def wrapper(text, predicate_result=None):
                if predicate_result is None:
                    predicate_result = predicate(text)

                return func(text, predicate_result)

            return wrapper

        return decorator

    def incremental_changes(self, text):
        for predicate, func in self.changes:
            predicate_result = predicate(text)
            if predicate_result:
                result = func(text, predicate_result)
                if result:
                    get_logger().write("{}({!r}) -> {!r}".format(func.__name__, text, result))
                text = result or text

        return text

    def exclusive_changes(self, text):
        for predicate, func in self.changes:
            predicate_result = predicate(text)
            if predicate_result:
                result = func(text, predicate_result)
                if result:
                    get_logger().write("{}({!r}) -> {!r}".format(func.__name__, text, result))
                return result or text

        return text
