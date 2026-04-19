from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

router = APIRouter(prefix="/roles", tags=["Roles"], route_class=DishkaRoute)

@router.post("/")
async def create(name: str) -> None:
    pass

@router.get("/{role_id}")
async def get(role_id: int) -> None:
    pass

@router.put("/")
async def update(role_id: int, name: str) -> None:
    pass

@router.delete("/")
async def delete(role_id: int) -> None:
    pass

@router.get("/all")
async def get_all() -> None:
    pass