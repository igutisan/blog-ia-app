from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.config.security import verify_password
from app.dtos.login_dto import LoginDTO


def authenticate_user(db: Session, loginDto: LoginDTO) -> UserModel | None:
    user = db.query(UserModel).filter(UserModel.email == loginDto.email).first()
    if not user:
        return None
    if not verify_password(loginDto.password, user.password):
        return None
    return user
