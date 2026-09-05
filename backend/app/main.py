import app.models
from fastapi import FastAPI
from app.routers.auth import authRouter
from app.routers.verification import verificationRouter
from app.routers.user import userRouter
from app.routers.listing import listingRouter
from app.exceptions.handlers.auth import incorrect_credentials_error_handler, invalid_verification_token_error_handler, registration_error_handler
from app.exceptions.auth import IncorrectCredentialsError, InvalidVerificationTokenError, RegistrationError


app = FastAPI()

app.add_exception_handler(RegistrationError, registration_error_handler)
app.add_exception_handler(InvalidVerificationTokenError, invalid_verification_token_error_handler)
app.add_exception_handler(IncorrectCredentialsError, incorrect_credentials_error_handler)

app.include_router(authRouter)
app.include_router(verificationRouter)
app.include_router(userRouter)
app.include_router(listingRouter)