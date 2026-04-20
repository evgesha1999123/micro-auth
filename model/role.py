from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: int
    role_name: str