from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.dtos.create_blog import CreateBlog
from app.dtos.login_dto import LoginDTO
from app.dtos.response_login_dto import ResponseLoginDTO
from app.services import blog_service
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
from app.models.categories import CategoryModel
from app.dtos.blog_response_dto import BlogResponseDTO
from app.dtos.create_category_dto import CreateCategoryDTO
from app.services.category_service import create_category, get_categories
from app.services.blog_service import create_blog, get_blogs
from app.config.db_connection import engine,Base
from app.dtos.category_reponse_dto import CategoryResponseDTO
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Blog IA API",
    description="API para creacion de blogs con IA",
    version="0.1.0",
)

origins = [
    "http://localhost",
    "http://localhost:8080",   
    "https://midominio.com",   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,         
    allow_methods=["*"],            
    allow_headers=["*"],            
)


@app.post("/register", status_code=201)
def register_user(register_dto: RegisterDTO, db: Session = Depends(get_db)):
    try:
        user = register_user_service(register_dto, db)
        return
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error " + str(e))


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


@app.get("/me")
def login_for_access_token(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user


@app.post("/blogs", status_code=201)
async def create_new_blog(
    blog_dto: CreateBlog,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:

        blog = await create_blog(
            blog_dto, current_user.id, db
        )
        return blog
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/blogs", response_model=List[BlogResponseDTO])
def get_blog(
    db: Session = Depends(get_db)
):
    return get_blogs(db)



@app.get("/blogs/me", response_model=List[BlogResponseDTO])
def get_my_blogs(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return blog_service.get_blogs_by_user(db, user_id=current_user.id)


@app.post("/category", status_code=201)
async def create_new_category(
    category_dto: CreateCategoryDTO,
    db: Session = Depends(get_db)
):
    try:
        category = await create_category(
            category_dto.name, db
        )
        return category
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/categories", response_model=List[CategoryResponseDTO])
async def get_categ(
    db: Session = Depends(get_db),
):
    return await get_categories(db)
