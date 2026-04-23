from typing import Optional
from fastapi import Response

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from core.di import container
from model.auth import UserRegistrationSchema, UserLoginSchema, LoginResponseSchema, LogoutResponseSchema
from model.user import UserSchema
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)
service = container.get(AuthService)

@router.post("/register")
async def register(user_registration_schema: UserRegistrationSchema) -> UserSchema | None:
    return await service.register(user_registration_schema)

@router.get("/login")
async def login(response: Response, login_: str, password: str) -> Optional[LoginResponseSchema]:
    return await service.login(response=response, login_schema=UserLoginSchema(login=login_, password=password))

@router.post("/logout")
async def logout(response: Response) -> LogoutResponseSchema:
    return await service.logout(response=response)