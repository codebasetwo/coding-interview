from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.routes import auth_router
from src.databases.main import init_db
from config import Config
from src.errors import register_errors


description = "An application to help developers practice for technical interviews in python."
name_of_author = "Nnaemeka Nwankwo"
email = "nuaemeka@gmail.com"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server Starting!")
    await init_db()
    yield
    print("Server Stopped!")

app = FastAPI(
    title="Interview Assistant.",
    description=description,
    version="v1",
    contact={
        "email":email,
        "name": name_of_author,

    },
    lifespan=lifespan,
    docs_url=f"{Config.API_PREFIX}/docs",
    redoc_url=f"{Config.API_PREFIX}/redoc"
)


register_errors(app)

# create a home for testing
@app.get("/")
async def home(name: str = "Nnaemeka"):
    return {
        "response": "Succcesful",
        "message": f"Welcome {name} wish you luck in your interview."
        }

app.include_router(auth_router, prefix=f"{Config.API_PREFIX}/auth", tags=["auth"])