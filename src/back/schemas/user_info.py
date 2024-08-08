from pydantic import BaseModel


class UserDBSchema(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool


class UserInSchema(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active: bool

class UserOutSchema(BaseModel):
    id: int
    username: str
    email: str


