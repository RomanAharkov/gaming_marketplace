from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=6)
    password: str = Field(min_length=10)
