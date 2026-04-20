from typing import Optional

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from model.user import UserRegistrationSchema, UserSchema, UserLoginSchema, UserWithRoleSchema

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)

@router.post("/register")
async def register(user_registration_schema: UserRegistrationSchema) -> UserSchema:
    pass

@router.get("/login")
async def login(user_login_schema: UserLoginSchema) -> Optional[UserWithRoleSchema]:
    pass

@router.post("/logout")
async def logout(username: str) -> bool:
    pass