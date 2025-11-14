from pydantic import BaseModel
from typing import Optional

class BlogResponseDTO(BaseModel):
    id: str
    category: str
    title: str
    content: str
    image_url: Optional[str] = None
    seo_description: str
    author: str
