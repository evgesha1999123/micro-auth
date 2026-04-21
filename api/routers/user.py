from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from core.di import container
from model.user import UserSchema
from service.user import UserService

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)
service = container.get(UserService)

@router.post("/me/username/")
async def change_username(old: str, new: str) -> UserSchema:
    return await service.change_username(old, new)

@router.post("/me/password/")
async def change_password(username: str, old: str, new: str) -> UserSchema:
    return await service.change_password(username, old, new)

@router.post("/me/email/")
async def change_email(old: str, new: str) -> UserSchema:
    return await service.change_email(old, new)

@router.get("/me")
async def get(login_: str) -> UserSchema:
    return await service.get_user(login_)

@router.delete("/")
async def delete(user_id: int) -> bool:
    return await service.delete_user(user_id)

@router.get("/all")
async def get_all() -> list[UserSchema]:
    return await service.get_all()