from pydantic import BaseModel, BeforeValidator
from typing import Any, Generic, TypeVar, Optional, Annotated
from datetime import datetime

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    statusCode: int = 200
    success: bool = True
    message: str = "success"
    data: Optional[T] = None
    error: Optional[Any] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "statusCode": 200,
                "success": True,
                "message": "Operation completed successfully",
                "data": {"key": "value"},
                "error": None,
            }
        }


class BasePaginatedResponse(BaseModel, Generic[T]):
    statusCode: int = 200
    success: bool = True
    message: str = "success"
    items: Optional[T] = None
    pageNumber: int = 1
    pageSize: int = 20
    totalItems: int = 0
    totalPage: int = 0
    error: Optional[Any] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "statusCode": 200,
                "message": "Operation completed successfully",
                "data": [{"key": "value"}],
                "pageNumber": 1,
                "pageSize": 20,
                "totalItems": 0,
                "totalPage": 0
            }
        }


def parse_datetime(value: str):
    print('value', value)
    if value and value.strip():
        try:
            new_date_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            print('new_date_time', new_date_time)
            return new_date_time
        except Exception as e:
            raise ValueError(str(e))
    else:
        return None


date_time = Annotated[datetime | None, BeforeValidator(parse_datetime)]


class BaseTrackTimeMixin(BaseModel):
    createdAt: datetime
    updatedAt: datetime


class BaseSoftDeleteMixin(BaseModel):
    deletedAt: datetime | None = None
    isDeleted: bool = False
    deletedBy: int = 0


class BaseActionByMixin(BaseModel):
    createdBy: int = 0
    updatedBy: int = 0


class BaseAllMixin(BaseTrackTimeMixin, BaseSoftDeleteMixin, BaseActionByMixin):
    pass
