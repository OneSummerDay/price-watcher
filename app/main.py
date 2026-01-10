from fastapi import FastAPI

from app.db import init_db
from app.db.base import Base
from app.db.session import engine
from app.api.products import router as products_router

app = FastAPI()

app.include_router(products_router)

@app.on_event("startup")
async def on_startup():
    await init_db()