from pydantic import BaseModel

class BlogResponseDTO(BaseModel):
    id: str
    category: str
    title: str
    content: str
    seo_description: str
    author: str
