from ..auth.utils import *
from ..models import models

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException as fastapi_HTTPException, status


async def create_user(user, db_: AsyncSession):
    user = user.dict()
    user["hashed_password"] = await hash_password(user["hashed_password"])
    user_in_db = models.UserModel(**user)
    db_.add(user_in_db)
    await db_.commit()
    await db_.refresh(user_in_db)
    return user_in_db


async def validate_user(username: str, password: str, db_: AsyncSession) -> models.UserModel:
    query = select(models.UserModel).where(models.UserModel.username == username)
    result = await db_.execute(query)
    result = result.scalar()
    if not result:
        raise fastapi_HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"User with name: {username} doesn't exist")
    if not await verify_password(password, result.hashed_password):
        raise fastapi_HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    else:
        return result

