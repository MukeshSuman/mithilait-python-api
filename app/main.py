from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.core.database import engine, Base
from app.auth.routes import router as auth_router
from app.category.routes import router as category_router
from app.role.routes import router as role_router


# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

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


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app"}
