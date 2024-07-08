import fastapi.openapi.utils as fu
import datetime
from typing import Text
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.core.database import engine, Base, get_db
from app.auth.routes import router as auth_router
from app.category.routes import router as category_router
from app.core.exceptions import CustomException, custom_exception_handler, general_exception_handler, validation_exception_handler, http_exception_handler
from app.role.routes import router as role_router
from app.role.schemas import RoleCreate
from fastapi.templating import Jinja2Templates
import json
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class ErrorResponse(BaseModel):
    statusCode: int = Field(..., example=422)
    message: str = Field(..., example="message to the user")
    error: str = Field(..., example="message to the developer")
    type: str = Field(..., example="type of error")
    success: bool = Field(..., example=False)
    detail: dict = Field(..., example=[
        {'loc': 'quantity',
         'msg': 'value is not a valid integer',
         'type': 'type_error.integer'}])


# override fastapi 422 schema
fu.validation_error_response_definition = ErrorResponse.schema()

templates = Jinja2Templates(directory='app/templates')

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mithila IT",
    description="Mithila IT API",
    version="1.0.0",
    docs_url="/docs",
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(HTTPSRedirectMiddleware)

# Routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(category_router, prefix="/categories", tags=["Category"])
app.include_router(role_router, prefix="/roles", tags=["Role"])


@app.post("/systemInfo")
def read_root(box: RoleCreate):
    time_now = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
    print(box.name)
    f = open(f"systemInfo/{time_now}.txt", "x")
    f.write(box.name)
    f.close()
    return {"message": "success"}


class BaseTestData(BaseModel):
    name: Text
    rollNo: Text
    className: Text

    class Config:
        from_attributes = True


@app.post("/test-done")
def test_done(textData: BaseTestData):
    with open('weeklyTest.json', 'r+') as f:
        json_data = json.load(f)
        print("json_data", json_data)
        time_now = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        json_data['students'].append(
            {
                "name": textData.name,
                "rollNo": textData.rollNo,
                "className": textData.className,
                "time": time_now
            }
        )
        f.seek(0)
        # json_data[time_now] =
        json.dump(json_data, f, indent=4)
    return {"message": "success"}


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request, "message": "Welcome to the FastAPI app", "baseUrl": request.base_url})
    # return {"message": "Welcome to the FastAPI app"}
