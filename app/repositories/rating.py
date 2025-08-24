from sqlalchemy.orm import Session
from app.models.rating import ProductRating
from app.repositories.base_repo import BaseRepository

class ProductRatingRepository(BaseRepository[ProductRating]):
    def __init__(self, db: Session):
        super().__init__(ProductRating, db)
