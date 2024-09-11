from fastapi import Depends
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, inspect
from app.core.database import Base, get_db
from app.core.models import AllMixin
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class User(Base, AllMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    email = Column(String(250), index=True)
    firstName = Column(String(250))
    lastName = Column(String(250))
    isActive = Column(Boolean, default=True)
    isVerified = Column(Boolean, default=False)
    isCompletedProfile = Column(Boolean, default=False)
    mobileNumber = Column(String(15))
    hashed_mobile_otp = Column(String(250), nullable=True)
    hashed_email_otp = Column(String(250), nullable=True)
    hashed_password = Column(String(250))
    roleId = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    @hybrid_property
    def roleName(self):
        return self.role.name

    def toDict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            if not key.startswith('_'):
                dict_[key] = getattr(self, key)

        for key, prop in inspect(self.__class__).all_orm_descriptors.items():
            if isinstance(prop, hybrid_property):
                dict_[key] = getattr(self, key)
        if not dict_["roleName"]:
            dict_["roleName"] = "GUEST"
        else:
            dict_["roleName"] = dict_["roleName"].upper()
        return dict_
        # return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
