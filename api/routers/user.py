from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from model.user import UserSchema

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)

@router.post("/me/username/")
async def change_username(username: str) -> UserSchema:
    pass

@router.post("/me/password/")
async def change_password(email: str, password: str) -> UserSchema:
    pass

@router.post("/me/email/")
async def change_email(email: str) -> UserSchema:
    pass

@router.get("/me")
async def get(login_: str) -> UserSchema:
    pass

@router.delete("/")
async def delete(user_id: int) -> bool:
    pass

@router.get("/all")
async def get_all() -> list[UserSchema]:
    pass