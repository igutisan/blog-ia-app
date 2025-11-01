from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.dtos.create_blog import CreateBlog
from app.dtos.login_dto import LoginDTO
from app.dtos.response_login_dto import ResponseLoginDTO
from app.services.user_service import register_user as register_user_service
from app.dtos.register_dto import RegisterDTO
from app.config.db_connection import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.services import auth_service
from app.config.security import create_access_token
from app.auth.dependencies import get_current_user
from app.models.user import UserModel
from typing import List
from app.models.blog import BlogModel
from app.dtos.blog_response_dto import BlogResponseDTO

load_dotenv()

app = FastAPI(
    title="Blog IA API",
    description="API para creacion de blogs con IA",
    version="0.1.0",
)


@app.post("/register", status_code=201)
def register_user(register_dto: RegisterDTO, db: Session = Depends(get_db)):
    try:
        user = register_user_service(register_dto, db)
        return
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    login_dto = LoginDTO(email=form_data.username, password=form_data.password)
    user = auth_service.authenticate_user(db, login_dto)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return ResponseLoginDTO(token=access_token)


@app.post("/blogs", status_code=201)
async def create_new_blog(
    blog_dto: CreateBlog,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        blog = await blog_service.create_blog(
            blog_dto, current_user.id, db
        )
        return blog
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/blogs/me", response_model=List[BlogResponseDTO])
def get_my_blogs(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return blog_service.get_blogs_by_user(db, user_id=current_user.id)
