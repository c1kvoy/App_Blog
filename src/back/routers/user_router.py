from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database
from ..auth.utils import *
from ..schemas import user_info
from ..methods.user_methods import *
from ..models.models import *

user_router = APIRouter(tags=['users'], prefix='/users')


