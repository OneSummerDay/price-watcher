from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.api.products import router as products_router

app = FastAPI()

app.include_router(products_router)

@app.on_event("startup")
async def on_startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print("STARTUP ERROR:", repr(e))
        raise
