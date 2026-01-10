from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.errors import validation_exception_handler
from app.db import init_db
from app.db.base import Base
from app.db.session import engine
from app.api.products import router as products_router

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(products_router)

@app.on_event("startup")
async def on_startup():
    await init_db()