from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing  import Annotated
import uvicorn
from core.config import settings
from api_v1 import router as router_v1
from items_views import router as items_router
from users.views import router as users_router
from fastapi import APIRouter, Path
from pydantic import BaseModel, EmailStr


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(items_router)
app.include_router(users_router)

router = APIRouter(prefix="/items", tags=["Items"])
router = APIRouter(prefix="/users", tags=["Users"])


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


@app.get("/hello/")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!"}


@app.get("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
