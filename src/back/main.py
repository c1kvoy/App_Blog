from fastapi import FastAPI
from .routers.auth_router import auth_router
from .routers.user_router import user_router

app = FastAPI()
app.include_router(auth_router)

app.include_router(user_router)
@app.get("/")
async def home():
    return {"Hello": "World"}
