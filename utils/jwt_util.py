from datetime import datetime, timezone, timedelta

from jose import jwt

from model.jwt import JwtSub
from settings import JWT


class JwtUtil:
    def __init__(self, jwt_config: JWT) -> None:
        self.jwt_config = jwt_config

    def create_access_token(self, jwt_sub: JwtSub) -> str:
        to_encode = jwt_sub.model_dump()
        expire = datetime.now(timezone.utc) + timedelta(seconds=self.jwt_config.EXPIRES_SECONDS)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, self.jwt_config.SECRET_KEY)
        return encode_jwt
