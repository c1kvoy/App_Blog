from fastapi import APIRouter, Depends

from .. import database
from ..auth.utils import *
from ..schemas import user_info
from ..methods.user_methods import *
from ..models.models import *


auth_router = APIRouter(tags=['auth'], prefix='/users/auth')

@auth_router.on_event("startup")
async def on_startup():
    await database.create_tables()

# @auth_router.post('/token', response_model=Token)
@auth_router.post('/register', response_model=user_info.UserOutSchema)
async def create_user_router(user: user_info.UserInSchema, db_=Depends(database.get_db)):
    user = await create_user(user, db_)
    return user
