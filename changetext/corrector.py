import functools
import re

from changetext.logging_tools import get_logger


class CorrectorRegistry:
    def __init__(self):
        self.changes = []

    def register(self, regex=None, predicate=None):
        def decorator(func):
            nonlocal regex, predicate

            if regex is not None:
                if isinstance(regex, str):
                    regex = re.compile(regex)

                def predicate(text):
                    return regex.search(text)

            if predicate is None:
                def predicate(_text):
                    return True

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
                    get_logger().write(f"{func.__name__}({text!r}) -> {result!r}")
                text = result or text

        return text

    def exclusive_changes(self, text):
        for predicate, func in self.changes:
            predicate_result = predicate(text)
            if predicate_result:
                result = func(text, predicate_result)
                if result:
                    get_logger().write(f"{func.__name__}({text!r}) -> {result!r}")
                return result or text

        return text
