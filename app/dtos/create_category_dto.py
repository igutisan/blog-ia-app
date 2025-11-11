from pydantic import BaseModel

class CreateCategoryDTO(BaseModel):
    name:str

    class Config:
        orm_mode = True