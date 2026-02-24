from contextlib import asynccontextmanager
from fastapi import FastAPI ,Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from app.db.database import engine, Base
from app.routers.user import user_router
from app.routers.admin import admin_router 
from app.core.config import settings
templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    print("Application shutting down...")


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key.get_secret_value())

@app.get("/register", include_in_schema=False)
def get_register_form(request:Request):
    return templates.TemplateResponse(request,"register.html")

@app.get("/login", include_in_schema=False)
def get_login_form(request:Request):
    return templates.TemplateResponse(request,"login.html")

@app.get("/dashboard", include_in_schema=False)
def get_dashboard(request:Request):
    return templates.TemplateResponse(request,"dashboard.html")

@app.get("/admin-dashboard", include_in_schema=False)
def get_dashboard(request:Request):
    return templates.TemplateResponse(request,"admin-dashboard.html")

@app.get("/profile", include_in_schema=False)
def get_dashboard(request:Request):
    return templates.TemplateResponse(request,"profile.html")


@app.get("/")
async def root():
    return {"message": "App running 🚀"}

app.include_router(user_router,prefix="/api/users", tags=["User"])
app.include_router(admin_router,prefix="/api/admin", tags=["Admin"])