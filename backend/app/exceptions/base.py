class ResourceNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class UnauthorizedAccessError(Exception):
    def __init__(self, message: str):
        super().__init__(message)