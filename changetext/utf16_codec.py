import functools


def utf16_codec(func):
    @functools.wraps(func)
    def wrapper(data):
        if isinstance(data, bytes):
            data = data.decode("utf-16-le")
            output = func(data)
            return output if output is None else output.encode("utf-16-le") + b"\0\0"

        return func(data)

    return wrapper
