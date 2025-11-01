from pydantic import BaseModel


class ResponseLoginDTO(BaseModel):
    token: str
