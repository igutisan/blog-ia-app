from typing import Optional
from pydantic import BaseModel

class CreateBlog(BaseModel):
    category: str
    description: str
    image_url: Optional[str] = None

    class Config:
        orm_mode = True