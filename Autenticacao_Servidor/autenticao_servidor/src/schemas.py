from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class FilterPage(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)