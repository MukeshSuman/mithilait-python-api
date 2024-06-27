from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, inspect
from app.core.database import Base
from app.core.models import AllMixin
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class User(Base, AllMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    firstName = Column(String)
    lastName = Column(String)
    isActive = Column(Boolean, default=True)
    isVerified = Column(Boolean, default=False)
    isCompletedProfile = Column(Boolean, default=False)
    hashed_mobile_otp = Column(String, nullable=True)
    hashed_email_otp = Column(String, nullable=True)
    hashed_password = Column(String)
    roleId = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    @hybrid_property
    def roleName(self):
        return self.role.name
    # role = relationship(Promotion, back_populates='sponsor')
    # role = relationship('roles', foreign_keys='users.roleId')
    # friends = relationship('Friend', backref='Friend.friend_id',primaryjoin='User.id==Friend.user_id', lazy='dynamic')

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
