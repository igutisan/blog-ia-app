from pydantic import BaseModel, Field, EmailStr, validator
import re


class RegisterDTO(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico válido del usuario")
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        description="Contraseña entre 8 y 64 caracteres con al menos una mayúscula, una minúscula, un número y un carácter especial",
    )


@validator("password")
def validate_password(cls, value):
    # Debe contener al menos: una minúscula, una mayúscula, un número y un carácter especial
    if not re.search(r"[a-z]", value):
        raise ValueError("La contraseña debe contener al menos una letra minúscula")
    if not re.search(r"[A-Z]", value):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula")
    if not re.search(r"\d", value):
        raise ValueError("La contraseña debe contener al menos un número")
    if not re.search(r"[@$!%*?&]", value):
        raise ValueError(
            "La contraseña debe contener al menos un carácter especial (@, $, !, %, *, ?, &)"
        )
    return value
