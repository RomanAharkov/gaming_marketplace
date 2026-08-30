from fastapi import FastAPI
from app.routers.auth import authRouter

app = FastAPI()

app.include_router(authRouter)