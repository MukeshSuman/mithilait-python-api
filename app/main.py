import datetime
from typing import Text
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.core.database import engine, Base
from app.auth.routes import router as auth_router
from app.category.routes import router as category_router
from app.role.routes import router as role_router
from app.role.schemas import RoleCreate
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='app/templates')

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

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


# @app.post("/systemInfo")
# def read_root(box: RoleCreate):
#     time_now = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
#     print(box.name)
#     f = open(f"systemInfo/{time_now}.txt", "x")
#     f.write(box.name)
#     f.close()
#     return {"message": "success"}


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request, "message": "Welcome to the FastAPI app", "baseUrl": request.base_url})
    # return {"message": "Welcome to the FastAPI app"}
