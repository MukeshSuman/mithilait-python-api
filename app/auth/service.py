from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_db
from app.auth.models import User
from app.auth.schemas import UserCreate, UserOut, UserWithToken, Login
from app.core.schemas import BasePaginatedResponse
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.role.models import Role

from typing import Any


def get_user(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return "User not found"
        temp_user = user.toDict()
        return temp_user
    except Exception as e:
        print(e)
        return str(e)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(password, user.hashed_password):
        return False
    temp_user = user.toDict()
    return temp_user


def register_user(user: UserCreate, db: Session):
    try:
        role = db.query(Role).filter_by(
            id=user.roleId, isDeleted=False).first()
        if not role:
            return f"Role with id {user.roleId} does not exist."
        db_user = db.query(User).filter(
            User.username == user.username, User.isDeleted == False).first()
        if db_user:
            return "Username already registered"
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
        if type(temp_user) is str:
            db.rollback()
            return temp_user

        access_token = create_access_token(data={**temp_user})
        data = {
            **temp_user,
            "token": access_token,
            "tokenType": "bearer",
        }
        finalData = UserWithToken(**data)
        return finalData
    except Exception as e:
        db.rollback()
        print("Exception: register_user", e)
        return e


def login_user(login: Login, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, login.username, login.password)
        if not user:
            return "Invalid username or password"
        access_token = create_access_token(data={**user})
        data = {
            **user,
            "token": access_token,
            "tokenType": "bearer",
        }
        finalData = UserWithToken(**data)
        return finalData
    except Exception as e:
        return e


def me(token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/token")), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        if payload is None:
            return "Invalid token"
        user = get_user(db, payload.get("id"))
        if user is None:
            return "Invalid token"
        data = {
            **user,
            "token": token,
            "tokenType": "bearer",
        }
        finalData = UserWithToken(**data)
        return finalData
    except Exception as e:
        return e


def get_all_user(pageNumber: int = 1, pageSize: int = 20, db: Session = Depends(get_db)):
    try:
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
            "totalPage": totalPages,
            "items": temp_ist
        }
        return BasePaginatedResponse[Any](data=data, message="Users successfully")
    except Exception as e:
        print(e)
        return str(e)
