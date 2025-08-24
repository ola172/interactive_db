from sqlalchemy.orm import Session
from app.models.skill import Skill
from app.repositories.base_repo import BaseRepository

class SkillRepository(BaseRepository[Skill]):
    def __init__(self, db: Session):
        super().__init__(Skill, db)
