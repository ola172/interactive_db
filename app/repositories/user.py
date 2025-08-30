from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, UserProduct, UserWaitingList
from app.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)


class UserProductRepository(BaseRepository[UserProduct]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserProduct, db)


class UserWaitingListRepository(BaseRepository[UserWaitingList]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserWaitingList, db)
