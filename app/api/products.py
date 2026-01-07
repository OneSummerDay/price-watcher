from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.db.models import TrackedProduct
from app.schemas.product import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductRead)
async def create_product(
    data: ProductCreate,
    session: AsyncSession = Depends(get_session)
):
    product = TrackedProduct(name=data.name, url=data.url)

    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product
    
@router.get("/", response_model=list[ProductRead])
async def read_products(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(TrackedProduct))
    products = result.scalars().all()
    return products