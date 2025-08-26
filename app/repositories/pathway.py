from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pathway import Pathway, PathwayItem
from app.repositories.base_repo import BaseRepository


class PathwayRepository(BaseRepository[Pathway]):
    def __init__(self, db: AsyncSession):
        super().__init__(Pathway, db)


class PathwayItemRepository(BaseRepository[PathwayItem]):
    def __init__(self, db: AsyncSession):
        super().__init__(PathwayItem, db)
