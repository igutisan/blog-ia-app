from pydantic import BaseModel

class CreateCategoryDTO(BaseModel):
    id:str

    class Config:
        orm_mode = True