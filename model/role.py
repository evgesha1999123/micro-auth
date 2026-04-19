from pydantic import BaseModel


class RoleSchema(BaseModel):
    id_: int
    role_name: str