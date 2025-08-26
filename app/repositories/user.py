from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession
                 ):
        super().__init__(User, db)
