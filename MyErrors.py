class BoardOutException(ValueError):
    def __init__(self, *args):
        super().__init__(self, *args)


class BoardOverFull(ValueError):
    def __init__(self, *args):
        super().__init__(self, *args)


class NotCorrectInput(ValueError):
    def __init__(self, *args):
        super().__init__(self, *args)


class ErrorPlaced(ValueError):
    def __init__(self, *args):
        super().__init__(self, *args)


class RepietDot(ValueError):
    def __init__(self, *args):
        super().__init__(self, *args)
