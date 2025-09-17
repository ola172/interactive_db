from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.interactive_models.paragraph_model import InteractiveParagraphModel
from app.models.interactive_models.paragraph_words_model import InteractiveWordModel, WordTypeModel
from app.models.interactive_models.keyword_models import InteractiveKeyWordModel, KeyWordTypeModel
from app.models.interactive_models.visual_models import VisualItemModel, ChartDataModel
from app.repositories.base_repo import BaseRepository
from app.exceptions.repo_exception import RepoException


class InteractiveParagraphRepository(BaseRepository[InteractiveParagraphModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(InteractiveParagraphModel, db)

    async def get_paragraphs_by_video_id(self, video_id: UUID) -> Sequence[InteractiveParagraphModel]:
        try:
            stmt = (
                select(InteractiveParagraphModel)
                .where(InteractiveParagraphModel.video_id == video_id)
                .order_by(InteractiveParagraphModel.view_index.asc())
                .options(
                    selectinload(InteractiveParagraphModel.paragraph_words)
                    .selectinload(InteractiveWordModel.type),
                    selectinload(InteractiveParagraphModel.paragraph_keywords)
                    .selectinload(InteractiveKeyWordModel.type),
                    selectinload(InteractiveParagraphModel.paragraph_visual)
                    .selectinload(VisualItemModel.visual_type),
                    selectinload(InteractiveParagraphModel.paragraph_visual)
                    .selectinload(VisualItemModel.table),
                    selectinload(InteractiveParagraphModel.paragraph_visual)
                    .selectinload(VisualItemModel.chart)
                    .selectinload(ChartDataModel.chart_type),
                    selectinload(InteractiveParagraphModel.paragraph_visual)
                    .selectinload(VisualItemModel.image),
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving paragraphs by video_id",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )

    async def get_paragraph_with_details(self, paragraph_id: UUID) -> InteractiveParagraphModel | None:
        try:
            stmt = (
                select(InteractiveParagraphModel)
                .where(InteractiveParagraphModel.id == paragraph_id)
                .options(
                    selectinload(InteractiveParagraphModel.paragraph_words)
                    .selectinload(InteractiveWordModel.type),
                    selectinload(InteractiveParagraphModel.paragraph_keywords)
                    .selectinload(InteractiveKeyWordModel.type),
                    selectinload(InteractiveParagraphModel.paragraph_visual),
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving paragraph with details",
                additional_info={"error": str(e), "paragraph_id": str(paragraph_id)},
            )


class InteractiveWordRepository(BaseRepository[InteractiveWordModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(InteractiveWordModel, db)

    async def get_words_by_paragraph_id(self, paragraph_id: UUID) -> Sequence[InteractiveWordModel]:
        try:
            stmt = (
                select(InteractiveWordModel)
                .where(InteractiveWordModel.paragraph_id == paragraph_id)
                .order_by(InteractiveWordModel.start_time.asc())
                .options(selectinload(InteractiveWordModel.type))
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving words by paragraph_id",
                additional_info={"error": str(e), "paragraph_id": str(paragraph_id)},
            )


class WordTypeRepository(BaseRepository[WordTypeModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(WordTypeModel, db)

    async def get_by_name(self, name: str) -> WordTypeModel | None:
        try:
            stmt = select(WordTypeModel).where(WordTypeModel.name == name)
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving word type by name",
                additional_info={"error": str(e), "name": name},
            )