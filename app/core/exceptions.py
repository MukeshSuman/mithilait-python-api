

from typing import Any, Optional
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.utils import convert_to_readable, preprocess_for_json


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
    processed_detail_data = preprocess_for_json(detail)
    missing = []
    string_type = []
    int_parsing = []
    not_in_list = []
    value_error = []
    print("step 0 done")
    if detail and isinstance(detail, list):
        print("detail", detail)
        processed_error_data = preprocess_for_json(detail)
        print("processed__error_data", processed_error_data)
        for x in processed_error_data:
            try:
                print("x['type']", x['type'])
                if x['type'] == "missing":
                    missing.append(convert_to_readable(x['loc'][1]))
                elif x['type'] == "string_type":
                    string_type.append(convert_to_readable(x['loc'][1]))
                elif x['type'] == "int_parsing":
                    int_parsing.append(convert_to_readable(x['loc'][1]))
                elif x['type'] == "value_error":
                    value_error.append(convert_to_readable(x['ctx']['error']))
                else:
                    not_in_list.append(convert_to_readable(x['loc'][1]))
            except Exception as e:
                print(e)

    err_msg = ""
    user_msg = "Please check your input and try again"
    print("step 1 done")
    if len(missing):
        missing_msg = ', '.join(missing)
        err_msg = f"Required fields are missing: {missing_msg}"
        user_msg = f"{missing[0]} is required"
    elif len(string_type):
        string_type_msg = ', '.join(string_type)
        err_msg = f"Invalid string: {string_type_msg}"
        user_msg = f"Should be a valid {string_type[0]}"
    elif len(int_parsing):
        int_parsing_msg = ', '.join(int_parsing)
        err_msg = f"Invalid integer: {int_parsing_msg}"
        user_msg = f"Should be a valid {int_parsing[0]}"
    elif len(not_in_list):
        not_in_list_msg = ', '.join(not_in_list)
        err_msg = f"Invalid value: {not_in_list_msg}"
        user_msg = f"Should be a valid {not_in_list[0]}"
    elif len(value_error):
        value_error_msg = ', '.join(value_error)
        err_msg = f"{value_error_msg}"
        user_msg = value_error[0]
    else:
        err_msg = user_msg
    err_response = ErrorResponse(
        statusCode=422,
        message=user_msg,
        error=err_msg,
        type="RequestValidationError",
        detail=processed_detail_data,
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
