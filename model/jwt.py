from pydantic import BaseModel, Field


class JwtSub(BaseModel):
    sub: str = Field(..., description="ID of verified user")

    def __init__(self, **data) -> None:
        data["sub"] = str(data["sub"])
        super().__init__(**data)