from pydantic import BaseModel


class UserDBSchema(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    refresh_token: str


class UserInSchema(BaseModel):
    username: str
    email: str
    hashed_password: str

class UserOutSchema(BaseModel):
    id: int
    username: str
    email: str


