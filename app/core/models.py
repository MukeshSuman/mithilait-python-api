from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, func


class TrackTimeMixin:

    createdAt = Column(DateTime, server_default=func.now())

    updatedAt = Column(DateTime, server_default=func.now(),
                       onupdate=datetime.now)


class SoftDeleteMixin:
    deletedAt = Column(DateTime, nullable=True)
    isDeleted = Column(Boolean, default=False)
    deletedBy = Column(Integer, default=0)

    def soft_delete(self, user):
        self.deletedAt = datetime.now()
        self.isDeleted = True
        self.deletedBy = user.id


class ActionByMixin:
    createdBy = Column(Integer, default=0)
    updatedBy = Column(Integer, default=0)

    def set_created_by(self, user=None):
        self.createdBy = user.id | 0

    def set_updated_by(self, user):
        self.updatedBy = user.id


class AllMixin(ActionByMixin, TrackTimeMixin, SoftDeleteMixin):
    pass
