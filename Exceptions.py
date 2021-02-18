class InputError(RuntimeError):
    """
    For when the input file containing the events or other input stream is corrupted
    """

    def __init__(self, arg):
        self.arg = arg


class URLError(ValueError):
    """
    If a URL is invalid
    """

    def __init__(self, arg):
        self.arg = arg
