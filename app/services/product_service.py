from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc

from app.db.models import TrackedProduct
from app.schemas.product import ProductCreate, ProductRead

class ProductService:
    @staticmethod
    async def create_product(data: ProductCreate, session: AsyncSession) -> TrackedProduct:
        await ProductService._ensure_url_unique(session=session, url=data.url)

        product = TrackedProduct(name=data.name, url=data.url)
        
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product
    
    @staticmethod
    async def get_products(
        session: AsyncSession,
        limit: int = 20,
        offset: int = 0,
        sort: str = "id",
    ) -> list[TrackedProduct]:
       
        if limit < 1:
            limit = 1
        if limit > 100:
            limit = 100
        if offset < 0:
            offset = 0


        if sort == "-id":
            order = desc(TrackedProduct.id)
        else:
            order = asc(TrackedProduct.id)

        query = (
            select(TrackedProduct)
            .order_by(order)
            .limit(limit)
            .offset(offset)
        )

        result = await session.execute(query)
        return result.scalars().all()
        
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

    @staticmethod
    async def update_product(product_id: int, data: ProductCreate, session: AsyncSession) -> TrackedProduct:
        product = await ProductService.get_product_by_id(product_id, session)

        if data.name is not None:
            product.name = data.name

        if data.url is not None:
             await ProductService._ensure_url_unique(
                session=session,
                url=data.url,
                exclude_id=product_id,
            )
        product.url = data.url
        
        await session.commit()
        await session.refresh(product)
        return product

    @staticmethod
    async def _ensure_url_unique(
        url: str, 
        session: AsyncSession,
        exclude_id: int | None = None) -> None:

        query = select(TrackedProduct).where(TrackedProduct.url == url)

        if exclude_id is not None:
            query = query.where(TrackedProduct.id != exclude_id)

        result = await session.execute(query)
        existing_product = result.scalar_one_or_none()

        if existing_product is not None:
            raise HTTPException(status_code=400, detail="Product with this URL already exists")