from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.schemas import UserCreate, UserWithToken, Login
from app.core.schemas import BasePaginatedResponse, BaseResponse
from app.auth.service import register_user, me, get_all_user, login_user
from typing import Any
from app.core.security import oauth2_scheme


router = APIRouter()


@router.post("/register", response_model=BaseResponse[UserWithToken])
def register_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        result = register_user(user, db)
        if type(result) == dict or type(result) == UserWithToken:
            return BaseResponse[UserWithToken](data=result, message="User registered successfully")
        elif type(result) == str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        print('e Exception', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )


@router.post("/token", response_model=Any)
def login_for_access_token_route(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        result = login_user(form_data, db)
        if type(result) == dict or type(result) == UserWithToken:
            print('temp_data', type(result), result.token)
            return {
                "data": result,
                "statusCode": 200,
                "error": None,
                "access_token": result.token,
                "tokenType": result.tokenType,
                "token": result.token,
                "message": "User logged in successfully"
            }
        elif type(result) == str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result,
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        print('e Exception', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=BaseResponse[UserWithToken])
def me_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        result = me(token, db)
        if type(result) == dict or type(result) == UserWithToken:
            return BaseResponse[UserWithToken](data=result, message="Success")
        elif type(result) == str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result,
            )
    except Exception as e:
        print('e Exception', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/login", response_model=BaseResponse[UserWithToken])
def login_route(login: Login, db: Session = Depends(get_db)):
    try:
        result = login_user(login, db)
        if type(result) == dict or type(result) == UserWithToken:
            return BaseResponse[UserWithToken](data=result, message="User logged in successfully")
        elif type(result) == str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result,
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        print('e Exception', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/all", response_model=BasePaginatedResponse[Any])
# token: str = Depends(oauth2_scheme),
async def get_all_users_route(token: str = Depends(oauth2_scheme), pageNumber: int = 1, pageSize: int = 20, db: Session = Depends(get_db)):
    return get_all_user(pageNumber, pageSize, db)
