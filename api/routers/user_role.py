from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from core.di import container
from model.role import RoleSchema
from model.user_role import UserWithRoleSchema
from service.user_role import UserRoleService

router = APIRouter(prefix="/user-role", tags=["UserRole"], route_class=DishkaRoute)
service = container.get(UserRoleService)

@router.patch("/bind/{login}")
async def bind_role_to_user(login_: str, role_name: str) -> UserWithRoleSchema:
    return await service.bind_role_to_user(login_, role_name)

@router.delete("/unbind/{login}")
async def unbind_role_from_user(login_: str, role_name: str) -> UserWithRoleSchema:
    return await service.unbind_role_from_user(login_, role_name)

@router.get("/me/roles")
async def get_with_roles(login_: str) -> UserWithRoleSchema:
    return await service.get_with_roles(login_)

@router.get("/roles")
async def get_roles(login_: str) -> list[RoleSchema]:
    return await service.get_user_roles(login_)

@router.post("/all/with-roles")
async def all_with_roles() -> list[UserWithRoleSchema]:
    return await service.get_all_with_roles()