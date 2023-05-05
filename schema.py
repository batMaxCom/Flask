import pydantic
from typing import Optional


class CreateUser(pydantic.BaseModel):
    username: str
    email: str
    password_hash: str

    @pydantic.validator('password_hash')
    def validate_password_hash(cls, value):
        if len(value) < 8:
            raise ValueError('password is too short')
        return value
