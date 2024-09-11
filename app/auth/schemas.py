from pydantic import BaseModel, Field, field_validator, EmailStr

from app.core.schemas import BaseAllMixin


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20,
                          description="The user's username")
    password: str = Field(min_length=3, max_length=20,
                          description="The user's password")
    email: EmailStr = Field(min_length=3, max_length=50,
                            description="The user's email address")
    firstName: str = Field(min_length=3, max_length=20,
                           description="The user's first name")
    lastName: str = Field(min_length=3, max_length=20,
                          description="The user's last name")
    roleId: int = Field(description="The user's role id")
    mobileNumber: str = Field(
        min_length=9, max_length=15, description="The user's mobile number")

    @field_validator('mobileNumber')
    def validate_mobile_number(cls, value):
        if not value:
            raise ValueError('Mobile number cannot be empty')
        # if not re.match(r'^\+?1?\d{9,15}$', value):
            # raise ValueError('Invalid mobile number format')
        return value

    @field_validator('roleId')
    def validate_role_id(cls, value):
        if value <= 0:
            raise ValueError('Role is invalid')
        return value


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
    roleName: str = "GUEST"
    mobileNumber: str | None = ""

    class Config:
        from_attributes = True


# class UserCreateOut(UserOut):
#     token: str
#     tokenType: str


class UserWithToken(UserOut):
    token: str
    tokenType: str


class Token(BaseModel):
    token: str
    tokenType: str


class Login(BaseModel):
    username: str
    password: str
