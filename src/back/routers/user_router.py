from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database
from ..auth import utils
from ..schemas import user_info
from ..methods import user_methods
from ..models.models import *

user_router = APIRouter(tags=['users'], prefix='/users')


@user_router.get('/', tags=['users'], response_model=list[user_info.UserOutSchema])
async def get_users_router(db: Session = Depends(database.get_db), token: str = Depends(utils.authorize)):
    return await user_methods.get_users(db)


