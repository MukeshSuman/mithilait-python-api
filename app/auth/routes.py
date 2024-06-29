from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.models import User
from app.auth.schemas import UserCreate, Token, UserOut, UserWithToken, Login
from app.core.schemas import BasePaginatedResponse, BaseResponse
from app.auth.service import register_user, login_for_access_token, me, get_all_user, login_user
from typing import Any

from app.role.models import Role


router = APIRouter()

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scheme_name="Login with username and password",
    # scopes={"me": "Get your data", "admin": "Get all data"},
)


@router.post("/register", response_model=BaseResponse[Any])
def register_route(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)


@router.post("/token", response_model=Any)
def login_for_access_token_route(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_for_access_token(form_data, db)


@router.get("/me", response_model=BaseResponse[UserWithToken])
def me_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return me(token, db)


@router.post("/login", response_model=BaseResponse[UserWithToken])
def login_route(login: Login, db: Session = Depends(get_db)):
    return login_user(login, db)


@router.get("/all", response_model=BasePaginatedResponse[Any])
async def get_all_users_route(token: str = Depends(oauth2_scheme), pageNumber: int = 1, pageSize: int = 20, db: Session = Depends(get_db)):
    return get_all_user(pageNumber, pageSize, db)
