from pydantic import BaseModel
from app.core.schemas import BaseAllMixin


class RoleCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class RoleOut(BaseAllMixin):
    id: int
    name: str

    class Config:
        from_attributes = True
