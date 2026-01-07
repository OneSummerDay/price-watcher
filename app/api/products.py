from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.db.models import TrackedProduct
from app.schemas.product import ProductCreate, ProductRead
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductRead)
async def create_product(
    data: ProductCreate,
    session: AsyncSession = Depends(get_session)
):
    product = await ProductService.create_product(
        data = data,
        session = session)
    return product
    
@router.get("/", response_model=list[ProductRead])
async def read_products(
    session: AsyncSession = Depends(get_session)
):
    products = await ProductService.read_products(session=session)
    return products