from fastapi import FastAPI
from .routers.auth_router import auth_router
from .routers.user_router import user_router
from src.back import database
app = FastAPI()
app.include_router(auth_router)

app.include_router(user_router)

@auth_router.on_event("startup")
async def on_startup():
    await database.create_tables()


@app.get("/")
async def home():
    return {"Hello": "World"}
