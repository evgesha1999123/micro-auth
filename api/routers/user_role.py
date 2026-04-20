from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from model.role import RoleSchema
from model.user_role import UserWithRoleSchema

router = APIRouter(prefix="/user-role", tags=["UserRole"], route_class=DishkaRoute)

@router.patch("/bind/{login}")
async def bind_role_to_user(login_: str, role: RoleSchema) -> UserWithRoleSchema:
    pass

@router.delete("/unbind/{login}")
async def unbind_role_from_user(login_: str, role: RoleSchema) -> UserWithRoleSchema:
    pass

@router.get("/me/roles")
async def get_with_roles(login_: str) -> UserWithRoleSchema:
    pass

@router.get("/roles")
async def get_roles(login_: str) -> list[RoleSchema]:
    pass

@router.post("/all/with-roles")
async def all_with_roles() -> list[UserWithRoleSchema]:
    pass