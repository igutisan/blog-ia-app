from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.db_connection import get_db
from app.config.security import get_password_hash
from app.dtos.register_dto import RegisterDTO
from app.models.user import UserModel


def register_user(registerDTO: RegisterDTO, db: Session = Depends(get_db)):
    db_user = (
        db.query(UserModel).filter(UserModel.email == registerDTO.email).first()
    )
    if db_user:
        raise ValueError("Email already exists")

    hashed_password = get_password_hash(registerDTO.password)

    new_user = UserModel(
        email=registerDTO.email,
        password=hashed_password, 
        name=registerDTO.name,
        last_name=registerDTO.last_name, 
     )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


