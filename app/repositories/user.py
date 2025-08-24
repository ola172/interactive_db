from app.models.user import User
from app.repositories.base_repo import BaseRepository
from sqlalchemy.orm import Session

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
