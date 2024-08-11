import uuid

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.back import database
from ..methods import user_methods
from ..core.config import settings

from datetime import datetime, timedelta
import jwt
import bcrypt

from fastapi import HTTPException as fastapi_HTTPException, Depends

from ..models import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth/login")

async def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    pwd: bytes = password.encode()
    return bcrypt.hashpw(pwd, salt).decode()


async def verify_password(form_password: str, db_password: str) -> bool:
    return bcrypt.checkpw(password=form_password.encode(), hashed_password=db_password.encode())


async def jwt_encode(payload: dict,
                     token_type: str,
                     private_key: str = settings.auth.private_key_path.read_text(),
                     algorithm: str = settings.auth.algorithm,
                     expires_delta: timedelta | None = None
                     ) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.auth.expires_minutes)
    to_encode.update(type=token_type,
                     exp=expire,
                     iat=now,
                     unique_id=str(uuid.uuid4()))
    return jwt.encode(to_encode, private_key, algorithm)


async def jwt_decode(token: str,
                     public_key: str = settings.auth.public_key_path.read_text()
                     ) -> dict:
    return jwt.decode(token, public_key, algorithms=settings.auth.algorithm)


async def type_validator(cur: str, required: str):
    if cur != required:
        raise fastapi_HTTPException(status_code=401,
                                    detail=f"Incorrect type of token: '{cur}' given, but '{required}' required")


async def create_access_token(payload: dict,
                              token_type: str = settings.auth.ACCESS_TOKEN_TYPE,
                              expires_delta: timedelta = timedelta(minutes=settings.auth.expire_minutes)
                              ):
    return await jwt_encode(payload=payload, token_type=token_type, expires_delta=expires_delta)


async def create_refresh_token(payload: dict,
                               token_type: str = settings.auth.REFRESH_TOKEN_TYPE,
                               expires_delta: timedelta = timedelta(minutes=settings.auth.expire_days)
                               ):
    return await jwt_encode(payload=payload, token_type=token_type, expires_delta=expires_delta)


async def expire_validator(payload: dict):
    exp_timestamp = payload.get('exp')
    exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
    if exp_datetime <= datetime.utcnow():
        raise fastapi_HTTPException(status_code=401,detail=f"Token expired, refresh it")


async def authorize(token: str = Depends(oauth2_scheme), db_=Depends(database.get_db)) -> models.UserModel:
    payload = await jwt_decode(token=token)
    await expire_validator(payload=payload)
    await type_validator(payload['type'], settings.auth.ACCESS_TOKEN_TYPE)
    user = await user_methods.get_user_by_id(payload['sub'], db_)
    return user

