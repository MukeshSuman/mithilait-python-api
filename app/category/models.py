from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.core.models import AllMixin


class Category(Base, AllMixin):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
