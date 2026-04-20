from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from model.role import RoleSchema

router = APIRouter(prefix="/roles", tags=["Roles"], route_class=DishkaRoute)

@router.post("/")
async def create(name: str) -> RoleSchema:
    pass

@router.get("/{role_id}")
async def get(role_id: int) -> RoleSchema:
    pass

@router.put("/")
async def update(role_id: int, new_name: str) -> RoleSchema:
    pass

@router.delete("/")
async def delete(role_id: int) -> bool:
    pass

@router.get("/all")
async def get_all() -> list[RoleSchema]:
    pass