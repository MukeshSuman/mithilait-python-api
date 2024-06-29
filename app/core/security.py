import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional, Dict, Any, Union

from app.auth.schemas import UserOut

# Configuration settings
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Utility functions for password hashing and verification


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Token models


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def create_access_token(data: UserOut | Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    print('data create_access_token', data)
    # to_encode = data.copy()
    payload = {
        "id": data["id"],
        "username": data["username"],
        "roleId": data["roleId"],
        "email": data["email"],
        "firstName": data["firstName"],
        "lastName": data["lastName"],
        "roleId": data["roleId"],
        "isActive": data["isActive"],
        "isVerified": data["isVerified"],
        "isCompletedProfile": data["isCompletedProfile"],
        "roleName": data["roleName"],
        "mobileNumber": data["mobileNumber"],
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        payload["exp"] = expire
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload["exp"] = expire
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Union[Dict[str, Any], str]:
    # return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    try:
        # Decode the token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
