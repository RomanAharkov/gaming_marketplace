from fastapi import FastAPI
from app.routers.auth import authRouter
from app.routers.verification import authRouter as verificationRouter
from app.exceptions.handlers.auth import invalid_verification_token_error_handler, registration_error_handler
from app.exceptions.auth import InvalidVerificationTokenError, RegistrationError


app = FastAPI()

app.add_exception_handler(RegistrationError, registration_error_handler)
app.add_exception_handler(InvalidVerificationTokenError, invalid_verification_token_error_handler)

app.include_router(authRouter)
app.include_router(verificationRouter)