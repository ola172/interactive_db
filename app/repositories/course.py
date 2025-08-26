from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import CourseDetail, Chapter, Video
from app.repositories.base_repo import BaseRepository


class CourseDetailRepository(BaseRepository[CourseDetail]):
    def __init__(self, db: AsyncSession):
        super().__init__(CourseDetail, db)


class ChapterRepository(BaseRepository[Chapter]):
    def __init__(self, db: AsyncSession):
        super().__init__(Chapter, db)


class VideoRepository(BaseRepository[Video]):
    def __init__(self, db: AsyncSession):
        super().__init__(Video, db)
