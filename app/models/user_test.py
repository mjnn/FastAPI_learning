from typing import Annotated
from sqlmodel import SQLModel,Field
from pydantic import BaseModel, EmailStr, field_validator

class userModel(SQLModel, table=True):
    userid: int | None = Field(None, primary_key=True)
    username: str | None
    hashed_password: str | None
    email: Annotated[str, EmailStr]
