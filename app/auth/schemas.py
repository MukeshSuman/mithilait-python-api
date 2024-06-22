from pydantic import BaseModel

# username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     firstName = Column(String)
#     lastName = Column(String)
#     role = Column(String)
#     isActive = Column(Boolean, default=True)
#     isVerified = Column(Boolean, default=False)
#     isCompletedProfile = Column(Boolean, default=False)
#     hashed_mobile_otp = Column(String, nullable=True)
#     hashed_email_otp = Column(String, nullable=True)
#     hashed_password = Column(String)


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    firstName: str
    lastName: str
    role: str
    # isActive: bool
    # isVerified: bool
    # isCompletedProfile: bool
    # hashed_mobile_otp: str
    # hashed_email_otp: str


class UserOut(UserCreate):
    id: int
    # username: str
    # email: str
    # firstName: str
    # lastName: str
    # role: str
    isActive: bool
    isVerified: bool
    isCompletedProfile: bool

    class Config:
        from_attributes = True


class UserLoginOut(UserOut):
    access_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    token_type: str
