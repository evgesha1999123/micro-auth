from typing import Optional

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from core.di import container
from model.user import UserRegistrationSchema, UserSchema, UserLoginSchema
from model.user_role import UserWithRoleSchema
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)
service = container.get(AuthService)

@router.post("/register")
async def register(user_registration_schema: UserRegistrationSchema) -> UserSchema | None:
    return await service.register(user_registration_schema)

@router.get("/login")
async def login(login_: str, password: str) -> Optional[UserWithRoleSchema]:
    return await service.login(UserLoginSchema(login=login_, password=password))

@router.post("/logout")
async def logout(username: str) -> bool:
    pass