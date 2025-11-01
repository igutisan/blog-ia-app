import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.config.db_connection import Base, engine


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    blogs = relationship("BlogModel", back_populates="user")


# Base.metadata.create_all(bind=engine)
