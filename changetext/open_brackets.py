import functools

opening = "!(*+-[{«р☼Xx"
closing = {"«": "»", "[": "]", "(": ")", "{": "}"}


def open_brackets(func):
    @functools.wraps(func)
    def wrapper(text):
        start_i = 0
        end_i = len(text) - 1
        for c in text:
            if c in opening:
                start_i += 1
                if text[end_i] == closing.get(c, c):
                    end_i -= 1
            else:
                break

        if (
            start_i > 0
            and text[start_i - 1] == "р"
            and (end_i == len(text) - 1 or text[end_i + 1] != "р")
            and not text[start_i:].startswith("из")
        ) and not text[start_i].isupper():
            start_i -= 1

        leading_symbols = text[:start_i].replace("р", "≡")
        trailing_symbols = text[end_i + 1 :].replace("р", "≡")

        return leading_symbols + func(text[start_i : end_i + 1]) + trailing_symbols

    return wrapper
