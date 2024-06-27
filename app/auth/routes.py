from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.models import User
from app.auth.schemas import UserCreate, Token, UserOut, UserCreateOut
from app.core.schemas import BasePaginatedResponse, BaseResponse
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from typing import Any

from app.role.models import Role


router = APIRouter()

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Function to authenticate a user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/register", response_model=BaseResponse[UserCreateOut])
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.username == user.username, User.isDeleted == False).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        firstName=user.firstName,
        lastName=user.lastName,
        roleId=user.roleId,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.username})
    data = {
        **db_user.toDict(),
        "token": access_token,
        "tokenType": "bearer",
    }
    finalData = UserCreateOut(**data)
    return BaseResponse[UserCreateOut](data=finalData, message="User registered successfully")


@router.post("/token", response_model=BaseResponse[Token])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return BaseResponse[Token](data=Token(access_token=access_token, token_type="bearer"))


@router.get("/me", response_model=BaseResponse[UserOut])
async def me(token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/token")), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return BaseResponse[UserOut](data=user)


@router.get("/all", response_model=BasePaginatedResponse[Any])
def get_all_user(pageNumber: int = 1, pageSize: int = 20, db: Session = Depends(get_db)):
    offset = (pageNumber - 1) * pageSize
    users_query = db.query(User).join(Role).offset(offset).limit(pageSize)
    users = users_query.all()
    totalItems = db.query(User).count()
    totalPages = (totalItems + pageSize - 1) // pageSize
    temp_ist = []
    for user in users:
        temp_user = user.toDict()
        temp_user["roleName"] = user.roleName
        temp_ist.append(temp_user)

    data = {
        "pageNumber": pageNumber,
        "pageSize": pageSize,
        "totalItems": totalItems,
        "totalPages": totalPages,
        "data": temp_ist
    }

    print("data", data)

    # temp_ist = []
    # user_list = db.query(User).join(Role).all()
    # for user in user_list:
    #     temp_user = user.toDict()
    #     temp_user["roleName"] = user.roleName
    #     temp_ist.append(temp_user)
    # print("temp_ist", temp_ist)
    return BaseResponse[Any](data=data, message="Users successfully")
