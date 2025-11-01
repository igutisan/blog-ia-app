from pydantic import BaseModel

class BlogResponseDTO(BaseModel):
    id: str
    topic: str
    title: str
    content: str
    seo_description: str

    class Config:
        orm_mode = True