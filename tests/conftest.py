
def pytest_make_parametrize_id(val):
    return repr(val)
