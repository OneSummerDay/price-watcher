from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import TrackedProduct
from app.schemas.product import ProductCreate, ProductRead

class ProductService:
    @staticmethod
    async def create_product(data: ProductCreate, session: AsyncSession) -> TrackedProduct:
        product = TrackedProduct(name=data.name, url=data.url)
        
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product
    
    @staticmethod
    async def read_products(session: AsyncSession) -> list[TrackedProduct]:
        result = await session.execute(select(TrackedProduct))
        products = result.scalars().all()
        return products

