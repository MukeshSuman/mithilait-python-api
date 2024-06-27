from pydantic import BaseModel

from app.core.schemas import BaseAllMixin


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    firstName: str
    lastName: str
    roleId: int


class UserOut(BaseAllMixin):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    roleId: int = 0
    isActive: bool = False
    isVerified: bool = False
    isCompletedProfile: bool = False
    # role: any = None

    class Config:
        from_attributes = True


class UserCreateOut(UserOut):
    token: str
    tokenType: str


class Token(BaseModel):
    token: str
    tokenType: str
