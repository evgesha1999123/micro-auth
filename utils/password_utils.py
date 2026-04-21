from enum import StrEnum
from passlib.context import CryptContext


class PassHashAlgorythm(StrEnum):
    BCRYPT = "bcrypt"
    ARGON_2 = "argon2"
    PBKDF2_SHA_256 = "pbkdf2_sha256"


class PasswordUtil:
    def __init__(self, algorythm: PassHashAlgorythm):
        self.pwd_context = CryptContext(schemes=[algorythm.value], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

if __name__ == '__main__':
    print(PasswordUtil(PassHashAlgorythm.ARGON_2).get_password_hash("123"))