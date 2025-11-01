from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.db_connection import Base, engine
import uuid


class BlogModel(Base):
    __tablename__ = "blogs"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    topic = Column(String(50), nullable=False, unique=True)
    title = Column(String(50), nullable=False)
    content = Column(String(150), nullable=False)
    seo_description = Column(String(50), nullable=False)
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="blogs")

Base.metadata.create_all(bind=engine)