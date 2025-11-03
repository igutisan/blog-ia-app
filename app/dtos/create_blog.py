from typing import Optional
from pydantic import BaseModel

class CreateBlog(BaseModel):
    categoryId: str
    description: str
    imageUrl: Optional[str] = None

    class Config:
        orm_mode = True