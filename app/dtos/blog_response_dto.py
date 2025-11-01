from pydantic import BaseModel

class BlogResponseDTO(BaseModel):
    id: str
    # category: str
    description: str
    title: str
    content: str
    seo_description: str

    class Config:
        orm_mode = True