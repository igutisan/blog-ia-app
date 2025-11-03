from pydantic import BaseModel

class CategoryResponseDTO(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True