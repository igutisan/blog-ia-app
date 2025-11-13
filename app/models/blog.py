from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.db_connection import Base, engine
import uuid


class BlogModel(Base):
    __tablename__ = "blogs"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    description = Column(String(250), nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(String(1000), nullable=False)
    seo_description = Column(String(250), nullable=False)
    image_url = Column(String(600), nullable=True)
    category_id = Column(String, ForeignKey("categories.id"))
    category = relationship("CategoryModel", back_populates="blogs")
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="blogs")

# Base.metadata.create_all(bind=engine)