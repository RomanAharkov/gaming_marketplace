class RegistrationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class LoginError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class UserAlreadyExistsError(RegistrationError):
    pass

class UsernameIsTakenError(RegistrationError):
    pass

class UserVerificationPendingError(RegistrationError):
    pass

class InvalidVerificationTokenError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class IncorrectCredentialsError(LoginError):
    def __init__(self, message: str):
        super().__init__(message)

