from sqlalchemy.orm import Session
from app.models.book import BookVideoDetail, BookReadingDetail, BookSection
from app.repositories.base_repo import BaseRepository

class BookVideoRepository(BaseRepository[BookVideoDetail]):
    def __init__(self, db: Session):
        super().__init__(BookVideoDetail, db)

class BookReadingRepository(BaseRepository[BookReadingDetail]):
    def __init__(self, db: Session):
        super().__init__(BookReadingDetail, db)

class BookSectionRepository(BaseRepository[BookSection]):
    def __init__(self, db: Session):
        super().__init__(BookSection, db)
