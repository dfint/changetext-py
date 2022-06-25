import functools
import re


class Corrector:
    def __init__(self):
        self.preliminary_changes = list()
        self.final_changes = list()

    def preliminary_change(self, regex=None, predicate=None):
        def decorator(func):
            nonlocal regex, predicate

            if regex is not None:
                if isinstance(regex, str):
                    regex = re.compile(regex)

                predicate = lambda text: regex.search(text)

            assert predicate is not None
            self.preliminary_changes.append((predicate, func))

            return func
        return decorator

    def final_change(self, regex=None, predicate=None):
        def decorator(func):
            nonlocal regex, predicate

            if regex is not None:
                if isinstance(regex, str):
                    regex = re.compile(regex)

                predicate = lambda text: regex.search(text)

            @functools.wraps(func)
            def wrapper(text, predicate_result=None):
                if predicate_result is None:
                    predicate_result = predicate(text)

                return func(text, predicate_result)

            assert predicate is not None
            self.final_changes.append((predicate, func))

            return wrapper
        return decorator

    def change_text(self, text):
        result = None
        for predicate, func in self.preliminary_changes:
            predicate_result = predicate(text)
            if predicate_result:
                result = func(text, predicate_result) or result
                if result:
                    text = result

        for predicate, func in self.final_changes:
            predicate_result = predicate(text)
            if predicate_result:
                return func(text, predicate_result)
