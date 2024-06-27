from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.core.models import AllMixin

from sqlalchemy.orm import relationship


class Role(Base, AllMixin):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    users = relationship("User", back_populates="role")
