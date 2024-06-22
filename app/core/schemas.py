from pydantic import BaseModel
from typing import Any, Generic, TypeVar, Optional
# from pydantic.generics import GenericModel


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
                "message": "Operation completed successfully",
                "data": {"key": "value"}
            }
        }
