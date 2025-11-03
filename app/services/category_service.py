

from app.models.categories import CategoryModel
from app.config.db_connection import get_db
from typing import List
from sqlalchemy.orm import Session


async def create_category(category_name: str, db: Session) -> CategoryModel | None:
    try:
        new_category = CategoryModel(name=category_name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except Exception as e:
        print(f"Error creating category: {e}")
        return None

async def get_categories(db: Session) -> List[CategoryModel]:
    return db.query(CategoryModel).all()

# async def get_category_by_name(category_id: int, db: Session) -> CategoryModel | None:
#     return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()


