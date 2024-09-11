from sqlalchemy import Column, Integer, String, inspect
from app.core.database import Base
from app.core.models import AllMixin

from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Role(Base, AllMixin):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)

    users = relationship("User", back_populates="role")

    def toDict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            if not key.startswith('_'):
                dict_[key] = getattr(self, key)

        for key, prop in inspect(self.__class__).all_orm_descriptors.items():
            if isinstance(prop, hybrid_property):
                dict_[key] = getattr(self, key)
        return dict_
