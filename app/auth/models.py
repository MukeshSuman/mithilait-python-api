from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    role = Column(String)
    isActive = Column(Boolean, default=True)
    isVerified = Column(Boolean, default=False)
    isCompletedProfile = Column(Boolean, default=False)
    isDeleted = Column(Boolean, default=False)
    hashed_mobile_otp = Column(String, nullable=True)
    hashed_email_otp = Column(String, nullable=True)
    hashed_password = Column(String)
