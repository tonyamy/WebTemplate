from pydantic import BaseModel


class TokenRequest(BaseModel):
    username: str
    password: str


class RefreshToken(BaseModel):
    refreshToken: str
