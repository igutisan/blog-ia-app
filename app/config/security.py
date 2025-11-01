from datetime import datetime, timedelta, timezone
from typing import Annotated
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError
import os
import jwt
from jwt.api_jwt import timezone
from jwt.exceptions import InvalidTokenError
from pydantic.main import BaseModel

ph = PasswordHasher()

# --- Configuración de JWT ---
SECRET_KEY = (
    os.getenv("SECRET_KEY")
    or "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
)
ALGORITHM = os.getenv("ALGORITHM") or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


class Token(BaseModel):
    access_token: str
    token_type: str


def get_password_hash(password: str) -> str:
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except InvalidTokenError:
        raise credentials_exception
