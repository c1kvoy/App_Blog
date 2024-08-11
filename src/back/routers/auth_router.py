from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .. import database
from ..auth.utils import *
from ..schemas import user_info
from ..methods.user_methods import *
from ..models.models import *

auth_router = APIRouter(tags=['auth'], prefix='/users/auth')


@auth_router.post('/register', response_model=user_info.UserOutSchema)
async def create_user_router(user: user_info.UserInSchema, db_=Depends(database.get_db)):
    user = await create_user(user, db_)
    return user


@auth_router.post('/login')
async def login_router(form: OAuth2PasswordRequestForm = Depends(), db_=Depends(database.get_db)):
    user_from_db = await validate_user(form.username, form.password, db_)
    payload = {
        'sub': user_from_db.id,
        'username': user_from_db.username,
    }
    user_from_db.refresh_token = await create_refresh_token(payload)
    access_token = await create_access_token(payload)
    db_.add(user_from_db)
    await db_.commit()
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }

