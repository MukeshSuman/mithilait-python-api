# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordRequestForm

# from app.core.database import SessionLocal
# from app.core.security import verify_password, get_password_hash, create_access_token
# from app.auth.models import User
# from app.auth.schemas import UserCreate, UserOut, Token

# router = APIRouter()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.post("/register", response_model=UserOut)
# async def register(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if db_user:
#         raise HTTPException(
#             status_code=400, detail="Username already registered")
#     hashed_password = get_password_hash(user.password)
#     new_user = User(username=user.username, hashed_password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @router.post("/login", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/me", response_model=UserOut)
# async def me(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login")), db: Session = Depends(get_db)):
#     payload = decode_access_token(token)
#     if payload is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     username = payload.get("sub")
#     user = db.query(User).filter(User.username == username).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# app/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.models import User
from app.auth.schemas import UserCreate, Token, UserOut, UserLoginOut
from app.core.schemas import BaseResponse
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token

router = APIRouter()

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Function to authenticate a user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/register", response_model=BaseResponse[UserLoginOut])
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
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
        role=user.role,
        isActive=True,
        isVerified=False,
        isCompletedProfile=False,
        isDeleted=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.username})
    data = {
        **db_user,
        "access_token": access_token,
        "token_type": "bearer",
    }
    return BaseResponse[UserLoginOut](data=UserLoginOut(**data), message="User registered successfully")
    # return {"access_token": access_token, "token_type": "bearer", "message": "User registered successfully"}


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
    # return {"access_token": access_token, "token_type": "bearer"}
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
