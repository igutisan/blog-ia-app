from app.dtos.create_blog import CreateBlog
from app.models.blog import BlogModel
from app.models.categories import CategoryModel
from sqlalchemy.orm import Session
from app.services.genia_service import generate_blog_content
import asyncio
import uuid
import json
import re
from typing import List

async def create_blog(
    blog_dto: CreateBlog, user_id: str, db: Session
) -> BlogModel:
    
    try:

        print("Entro al try")
        content_task = asyncio.to_thread(
            generate_blog_content, blog_dto.description
        )

        print("Entro al try2")
        results = await asyncio.gather(content_task)
        generated_content_str = results[0]
        print(generated_content_str)
        try:
            generated_data = json.loads(
                clean_llm_json_response(generated_content_str)
            )
            print(generated_data)
            enhanced_title = generated_data.get("title", "")
            enhanced_content = generated_data.get("body", "")
            enhanced_seo_description = generated_data.get("seoDescription", "")
        except (json.JSONDecodeError, AttributeError):
            enhanced_content = "Could not generate enhanced content."
            enhanced_title = "Could not generate enhanced title."
            enhanced_seo_description = "Could not generate enhanced SEO description."

    except Exception as e:
        print(f"Error calling AI services: {e}")
        enhanced_title = "(AI enhancement failed)"
        enhanced_content = "(AI enhancement failed)"
        enhanced_seo_description = "(AI enhancement failed)"
        return None

    category = db.query(CategoryModel).filter(CategoryModel.name == blog_dto.category).first()
    
    if not category:
        raise ValueError("Category not found")
    
    new_model = BlogModel(
        id=str(uuid.uuid4()),
        category=category,
        description=blog_dto.description,
        title=enhanced_title,
        content=enhanced_content,
        seo_description=enhanced_seo_description,
        user_id=user_id,
    )

    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    return new_model


def get_blogs_by_user(db: Session, user_id: str) -> List[BlogModel]:
    return db.query(BlogModel).filter(BlogModel.user_id == user_id).all()

def get_blogs(db: Session) -> List[BlogModel]:
    return db.query(BlogModel).all()


async def get_blogs_by_category(category_id: str, db: Session) -> List[BlogModel] | None:
    return db.query(BlogModel).filter(CategoryModel.id == category_id).all()

def clean_llm_json_response(raw_response: str) -> str:
    match = re.search(r"```json\s*(\{.*?\})\s*```", raw_response, re.DOTALL)
    if match:
        return match.group(1)

    return raw_response.strip()
