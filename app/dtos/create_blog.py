from pydantic import BaseModel

class CreateBlog(BaseModel):
    topic: str

    class Config:
        orm_mode = True