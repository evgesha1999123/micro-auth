from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from model.role import RoleSchema
from model.user import UserWithRoleSchema

router = APIRouter(prefix="/user-role", tags=["UserRole"], route_class=DishkaRoute)

@router.patch("/bind/{login}")
async def bind_role_to_user(login_: str, role: RoleSchema) -> UserWithRoleSchema:
    pass

@router.delete("/unbind/{login}")
async def unbind_role_from_user(login_: str, role: RoleSchema) -> UserWithRoleSchema:
    pass