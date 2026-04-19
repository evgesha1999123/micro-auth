from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from model.role import RoleSchema
from model.user import UserRegistrationSchema, UserSchema, UserLoginSchema, UserWithRoleSchema

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)

@router.post("/register")
async def register(user_registration_schema: UserRegistrationSchema) -> UserSchema:
    pass

@router.get("/login")
async def login(user_login_schema: UserLoginSchema) -> UserWithRoleSchema:
    pass

@router.post("/logout")
async def logout(username: str) -> bool:
    pass

@router.post("/update/{username}")
async def change_username(username: str) -> UserSchema:
    pass

@router.post("/update/{password}")
async def change_password(email: str, password: str) -> UserSchema:
    pass

@router.post("/update/{email}")
async def update_email(email: str) -> UserSchema:
    pass

@router.get("/me")
async def get(login_: str) -> UserSchema:
    pass

@router.get("/me/roles")
async def get_with_roles(login_: str) -> UserWithRoleSchema:
    pass

@router.get("/roles")
async def get_roles(login_: str) -> list[RoleSchema]:
    pass

@router.delete("/")
async def delete(user_id) -> bool:
    pass

@router.get("/all")
async def get_all() -> list[UserSchema]:
    pass

@router.post("/all/with-roles")
async def all_with_roles() -> list[UserWithRoleSchema]:
    pass

@router.patch("/role/bind/{login}")
async def bind_role_to_user(login_: str, role: RoleSchema) -> UserWithRoleSchema:
    pass

@router.delete("/role/unbind/{login}")
async def unbind_role_from_user(login_: str, role: RoleSchema) -> UserWithRoleSchema:
    pass