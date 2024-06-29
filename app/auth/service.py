from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.database import get_db
from app.auth.models import User
from app.auth.schemas import UserCreate, Token, UserOut, UserWithToken, Login
from app.core.schemas import BasePaginatedResponse, BaseResponse
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.role.models import Role

from typing import Any


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).join(Role).first()
    if user is None:
        return None
    temp_user = user.toDict()
    temp_user["roleName"] = user.roleName
    print('temp_user get_user', temp_user)
    return temp_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).join(Role).first()
    if user is None or not verify_password(password, user.hashed_password):
        return False
    temp_user = user.toDict()
    temp_user["roleName"] = user.roleName
    return temp_user


def register_user(user: UserCreate, db: Session):
    print('user register service')
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
        mobileNumber=user.mobileNumber
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    add_user_data = db_user.toDict()
    temp_user = get_user(db, add_user_data["id"])
    print("temp_user", temp_user)
    access_token = create_access_token(data={**temp_user})
    data = {
        **temp_user,
        "token": access_token,
        "tokenType": "bearer",
    }
    print('data', data)
    finalData = UserWithToken(**data)
    return BaseResponse[UserWithToken](data=finalData, message="User registered successfully")


def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={**user})
    data = {
        **user,
        "token": access_token,
        "tokenType": "bearer",
    }
    print('data', data)
    finalData = UserWithToken(**data)
    return {"data": finalData, "statusCode": 200, "error": None, "access_token": access_token, "tokenType": "bearer", "token": access_token, "message": "User logged in successfully"}

    # return BaseResponse[UserWithToken](data=finalData, message="User logged in successfully")


def login_user(login: Login, db: Session = Depends(get_db)):
    user = authenticate_user(db, login.username, login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={**user})
    data = {
        **user,
        "token": access_token,
        "tokenType": "bearer",
    }
    print('data', data)
    finalData = UserWithToken(**data)
    return BaseResponse[UserWithToken](data=finalData, message="User registered successfully")


def me(token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/token")), db: Session = Depends(get_db)):
    print('token', token)
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    print('payload', payload)
    user = get_user(db, payload.get("id"))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    data = {
        **user,
        "token": token,
        "tokenType": "bearer",
    }
    finalData = UserWithToken(**data)
    print('finalData', finalData)
    return BaseResponse[UserWithToken](data=finalData, message="Success")


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
        temp_ist.append(UserOut(**temp_user))

    data = {
        "pageNumber": pageNumber,
        "pageSize": pageSize,
        "totalItems": totalItems,
        "totalPages": totalPages,
        "data": temp_ist
    }

    return BasePaginatedResponse[Any](data=data, message="Users successfully")
