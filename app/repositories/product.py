from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product, ProductType
from app.repositories.base_repo import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)


class ProductTypeRepository(BaseRepository[ProductType]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductType, db)
