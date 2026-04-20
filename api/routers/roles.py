from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from model.role import RoleSchema
from di import container
from service.user_role.role import RoleDbService

router = APIRouter(prefix="/roles", tags=["Roles"], route_class=DishkaRoute)
role_service = container.get(RoleDbService)

@router.post("/{name}")
async def create(name: str) -> RoleSchema:
    return await role_service.create(RoleSchema(role_name=name))

@router.get("/by-id/{id}")
async def get_by_id(role_id: int) -> RoleSchema:
    return await role_service.get_by_id(RoleSchema(id=role_id))

@router.get("/by-name/{name}")
async def get_by_name(name: str) -> RoleSchema:
    return await role_service.get_by_name(RoleSchema(role_name=name))

@router.put("/by-id/{id}{new-name}")
async def change_name_by_id(role_id: int, new_name: str) -> RoleSchema:
    return await role_service.update_by_id(
        old_params=RoleSchema(id=role_id),
        new_params=RoleSchema(role_name=new_name)
    )

@router.put("/by-name/{old-name}{new-name}")
async def change_name_by_old_name(old_name: str, new_name: str) -> RoleSchema:
    return await role_service.update_by_name(
        old_params=RoleSchema(role_name=old_name),
        new_params=RoleSchema(role_name=new_name)
    )

@router.delete("/by-id/{id}")
async def delete_by_id(role_id: int) -> bool:
    return await role_service.delete_by_id(RoleSchema(id=role_id))

@router.delete("/by-name/{name}")
async def delete_by_name(name: str) -> bool:
    return await role_service.delete_by_name(RoleSchema(role_name=name))

@router.get("/all")
async def get_all() -> list[RoleSchema]:
    return await role_service.get_all()

@router.delete("/all")
async def delete_all() -> bool:
    return await role_service.delete_all()