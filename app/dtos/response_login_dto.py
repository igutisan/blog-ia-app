from pydantic import BaseModel
from app.dtos.user_dto import UserDTO


class ResponseLoginDTO(BaseModel):
    user: UserDTO 
    token: str
