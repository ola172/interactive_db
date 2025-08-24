from app.models.product import Product, ProductType
from app.repositories.base_repo import BaseRepository
from sqlalchemy.orm import Session

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(Product, db)

class ProductTypeRepository(BaseRepository[ProductType]):
    def __init__(self, db: Session):
        super().__init__(ProductType, db)
