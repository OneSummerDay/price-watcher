from fastapi import HTTPException
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
    
    @staticmethod
    async def get_product_by_id(product_id: int, session: AsyncSession) -> TrackedProduct:
        result = await session.execute(
            select(TrackedProduct).where(TrackedProduct.id == product_id)
        )
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
    
    @staticmethod
    async def delete_product(product_id: int, session: AsyncSession) -> None:
        product = await ProductService.get_product_by_id(product_id, session)
        
        await session.delete(product)
        await session.commit()


