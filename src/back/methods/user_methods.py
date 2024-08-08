from ..auth.utils import *
from ..models import models
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(user, db_: AsyncSession):
    user = user.dict()
    user["hashed_password"] = await hash_password(user["hashed_password"])
    user_in_db = models.UserModel(**user)
    db_.add(user_in_db)
    await db_.commit()
    await db_.refresh(user_in_db)
    return user_in_db


