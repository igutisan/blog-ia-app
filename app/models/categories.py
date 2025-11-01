import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.config.db_connection import Base, engine



class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True)
    blogs = relationship("BlogModel", back_populates="category")


# Base.metadata.create_all(bind=engine)