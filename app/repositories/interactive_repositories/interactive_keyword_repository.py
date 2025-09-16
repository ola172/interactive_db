from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.interactive_models.keyword_models import (
    InteractiveKeyWordModel, 
    KeyWordTypeModel, 
    VideoKeywordTypeStyleModel
)
from app.repositories.base_repo import BaseRepository
from app.exceptions.repo_exception import RepoException


class InteractiveKeyWordRepository(BaseRepository[InteractiveKeyWordModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(InteractiveKeyWordModel, db)

    async def get_keywords_by_paragraph_id(self, paragraph_id: UUID) -> Sequence[InteractiveKeyWordModel]:
        try:
            stmt = (
                select(InteractiveKeyWordModel)
                .where(InteractiveKeyWordModel.paragraph_id == paragraph_id)
                .options(selectinload(InteractiveKeyWordModel.type))
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving keywords by paragraph_id",
                additional_info={"error": str(e), "paragraph_id": str(paragraph_id)},
            )


class KeyWordTypeRepository(BaseRepository[KeyWordTypeModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(KeyWordTypeModel, db)

    async def get_by_name(self, name: str) -> KeyWordTypeModel | None:
        try:
            stmt = select(KeyWordTypeModel).where(KeyWordTypeModel.name == name)
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving keyword type by name",
                additional_info={"error": str(e), "name": name},
            )

    async def get_types_with_video_styles(self, video_id: UUID) -> Sequence[KeyWordTypeModel]:
        try:
            stmt = (
                select(KeyWordTypeModel)
                .join(VideoKeywordTypeStyleModel)
                .where(VideoKeywordTypeStyleModel.video_id == video_id)
                .options(selectinload(KeyWordTypeModel.video_styles))
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving keyword types with video styles",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )


class VideoKeywordTypeStyleRepository(BaseRepository[VideoKeywordTypeStyleModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(VideoKeywordTypeStyleModel, db)

    async def get_styles_by_video_id(self, video_id: UUID) -> Sequence[VideoKeywordTypeStyleModel]:
        try:
            stmt = (
                select(VideoKeywordTypeStyleModel)
                .where(VideoKeywordTypeStyleModel.video_id == video_id)
                .options(selectinload(VideoKeywordTypeStyleModel.type))
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving video keyword type styles",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )

    async def get_style_by_video_and_type(self, video_id: UUID, keyword_type_id: UUID) -> VideoKeywordTypeStyleModel | None:
        try:
            stmt = (
                select(VideoKeywordTypeStyleModel)
                .where(
                    VideoKeywordTypeStyleModel.video_id == video_id,
                    VideoKeywordTypeStyleModel.keyword_type_id == keyword_type_id
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving video keyword type style",
                additional_info={
                    "error": str(e), 
                    "video_id": str(video_id),
                    "keyword_type_id": str(keyword_type_id)
                },
            )