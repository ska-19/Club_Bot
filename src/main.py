from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

from operations.router import router as router_operation
from pages.router import router as router_pages

app = FastAPI(
    title="Trading App"
)

app.mount("/images/", StaticFiles(directory="images"), name="images")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
app.include_router(router_pages)
