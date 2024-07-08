

from typing import Any, Optional
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ErrorResponse(BaseModel):
    statusCode: int
    message: str
    error: str
    type: Optional[str] = None
    detail: Optional[Any] = None
    data: Any = None
    success: bool = False

    class Config:
        from_attributes = True


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Format the pydantic ValidationErrors in a more human-readable way."""
    detail = exc.errors()
    missing = []
    string_type = []
    int_parsing = []
    not_in_list = []
    if detail and isinstance(detail, list):
        for x in detail:
            print(x)
            if x['type'] == "missing":
                missing.append(x['loc'][1])
            elif x['type'] == "string_type":
                string_type.append(x['loc'][1])
            elif x['type'] == "int_parsing":
                int_parsing.append(x['loc'][1])
            else:
                not_in_list.append(x['loc'][1])

    err_msg = ""
    user_msg = "Please check your input and try again"
    if len(missing):
        missing_msg = ', '.join(missing)
        err_msg = f"Required fields are missing: {missing_msg}"
        user_msg = "Required fields are missing"
    elif len(string_type):
        string_type_msg = ', '.join(string_type)
        err_msg = f"Invalid data type: {string_type_msg}"
        user_msg = "Input should be a valid string"
    elif len(int_parsing):
        int_parsing_msg = ', '.join(int_parsing)
        err_msg = f"Invalid data type: {int_parsing_msg}"
        user_msg = "Input should be a valid integer"
    elif len(not_in_list):
        not_in_list_msg = ', '.join(not_in_list)
        err_msg = f"Invalid value: {not_in_list_msg}"
        user_msg = "Input should be a valid value"
    else:
        err_msg = user_msg
    err_response = ErrorResponse(
        statusCode=422,
        message=user_msg,
        error=err_msg,
        type="RequestValidationError",
        detail=exc.errors(),
    )
    return JSONResponse(
        status_code=422,
        content=err_response.model_dump()
    )


def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": exc.detail,
            "error": exc.detail,
            "details": str(exc),
            "data": None,
            "success": False,
            "type": "HTTPException",
        },
    )


def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "statusCode": 500,
            "message": "An unexpected error occurred.",
            "error": "Internal Server Error",
            "data": None,
            "success": False,
            "details": str(exc),
            "type": "Exception",
        },
    )


def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "type": "CustomException",
            "request": str(request.url),
        },
    )
