from fastapi import Query
from pydantic import BaseModel, BeforeValidator, Field
from typing import Any, Generic, List, TypeVar, Optional, Annotated
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


class BasePaginatedList(BaseModel, Generic[T]):
    items: List[T] = Field(
        [], description='List of items returned in the response following given criteria')
    pageNumber: int = Field(
        1, description='Number of items returned in the response')
    pageSize: int = Field(
        20, description='Number of items returned in the response')
    totalItems: int = Field(0,
                            description='Number of items returned in the response')
    totalPage: int = Field(0,
                           description='Number of pages returned in the response')


# class BasePaginationQuery(BaseModel):
#     pageNumber: int = Query(1, ge=1),
#     pageSize: int = Query(20, ge=1),
#     query: Optional[str] = Query(None, min_length=1, max_length=50),

class PaginatedParams():
    def __init__(
            self,
            pageNumber: int = Query(1, ge=1),
            pageSize: int = Query(20, ge=1),
            query: Optional[str] = Query(None, min_length=1, max_length=50),
            sortBy: Optional[str] = Query(
                "createdAt",
                min_length=1,
                max_length=20,
                description="Sort by id, name, createdAt, updatedAt, etc...",
            ),
            orderBy: Optional[str] = Query(
                "asc",
                regex="^(asc|desc)$",
                description="Order by asc or desc"
            )
    ):
        self.offset = (pageNumber - 1) * pageSize
        self.limit = pageSize
        self.search = query
        self.sortBy = sortBy
        self.orderBy = orderBy
        self.pageNumber = pageNumber
        self.pageSize = pageSize

    def getTotalPages(self, totalItems):
        return (totalItems + self.pageSize - 1) // self.pageSize


class BasePaginatedResponse(BaseModel, Generic[T]):
    statusCode: int = 200
    success: bool = True
    message: str = "success"
    data: BasePaginatedList[T]
    error: Optional[Any] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "statusCode": 200,
                "success": True,
                "message": "Operation completed successfully",
                "data": {
                    "items": [],
                    "pageNumber": 1,
                    "pageSize": 20,
                    "totalItems": 0,
                    "totalPage": 0
                },
                "error": None
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
