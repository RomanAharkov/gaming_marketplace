from app.exceptions.base import ResourceNotFoundError, UnauthorizedAccessError


class ListingNotFoundError(ResourceNotFoundError):
    pass

class CategoryNotFoundError(ResourceNotFoundError):
    pass

class UnauthorizedListingAccessError(UnauthorizedAccessError):
    pass

class IncorrectListingCategoryError(Exception):
    def __init__(self, message: str):
        super().__init__(message)