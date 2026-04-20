from typing import Optional

from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: Optional[int] = None
    role_name: Optional[str] = None