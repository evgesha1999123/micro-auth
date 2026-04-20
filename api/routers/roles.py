from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from model.role import RoleSchema
from core.di import container
from service.role import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"], route_class=DishkaRoute)
service = container.get(RoleService)


@router.post("/")
async def create(name: str) -> RoleSchema:
    return await service.create_role(name)


@router.get("/{role_id}")
async def get_by_id(role_id: int) -> RoleSchema:
    return await service.get_by_id(role_id)


@router.get("/name/{name}")
async def get_by_name(name: str) -> RoleSchema:
    return await service.get_by_name(name)


@router.put("/{role_id}")
async def change_name_by_id(role_id: int, new_name: str) -> RoleSchema:
    return await service.change_name_by_id(role_id, new_name)


@router.put("/name/{old_name}")
async def change_name_by_old_name(old_name: str, new_name: str) -> RoleSchema:
    return await service.change_name_by_old_name(old_name, new_name)


@router.delete("/{role_id}")
async def delete_by_id(role_id: int) -> bool:
    return await service.delete_by_id(role_id)


@router.delete("/name/{name}")
async def delete_by_name(name: str) -> bool:
    return await service.delete_by_name(name)


@router.get("/")
async def get_all() -> list[RoleSchema]:
    return await service.get_all()


@router.delete("/")
async def delete_all() -> bool:
    return await service.delete_all()