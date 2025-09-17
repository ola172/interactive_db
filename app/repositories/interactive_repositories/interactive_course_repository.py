from typing import Sequence, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.constant_manager import ProductType
from app.models import Product, ProductSkill
from app.models.interactive_models.interactive_course_details_model import InteractiveCourseDetailsModel
from app.models.interactive_models.interactive_chapter_model import InteractiveChapterModel
from app.models.interactive_models.interactive_video_model import InteractiveVideoModel
from app.models.interactive_models.keyword_models import VideoKeywordTypeStyleModel, InteractiveKeyWordModel
from app.models.interactive_models.paragraph_model import InteractiveParagraphModel
from app.models.interactive_models.paragraph_words_model import InteractiveWordModel
from app.models.interactive_models.visual_models import VisualItemModel, ChartDataModel
from app.models.skill_objective import ProductObjective
from app.repositories.base_repo import BaseRepository
from app.exceptions.repo_exception import RepoException


class InteractiveCourseDetailsRepository(BaseRepository[InteractiveCourseDetailsModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(InteractiveCourseDetailsModel, db)

    async def get_interactive_course_product(self, product_id: UUID) -> dict[str, Any] | None:
        try:
            stmt = (
                select(
                    Product,
                    Product.average_rating.label("average_rating"),
                    Product.chapter_count.label("chapter_count"),
                    Product.video_count.label("video_count"),
                    Product.skill_count.label("skill_count"),
                    Product.objective_count.label("objective_count"),
                )
                .where(Product.id == product_id)
                .options(
                    selectinload(Product.interactive_course_detail)
                    .selectinload(InteractiveCourseDetailsModel.chapters)
                    .selectinload(InteractiveChapterModel.videos),

                    selectinload(Product.product_skills).selectinload(ProductSkill.skill),

                    selectinload(Product.product_objectives).selectinload(ProductObjective.objective),

                    selectinload(Product.level_obj),
                )
            )

            result = await self.db.execute(stmt)
            row = result.first()

            if not row:
                return None

            product = row.Product

            return {
                "product": product,
                "average_rating": row.average_rating,
                "chapter_count": row.chapter_count,
                "video_count": row.video_count,
                "skill_count": row.skill_count,
                "objective_count": row.objective_count,
            }
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving interactive course product",
                additional_info={"error": str(e), "product_id": str(product_id)},
            )


    async def get_all_interactive_course_product(
            self,
            page: int = 1,
            limit: int = 10,
            category_id: UUID | None = None,
            skill_id: UUID | None = None,
    ) -> list[dict[str, Any]]:
        try:
            stmt = (
                select(
                    Product,
                    Product.average_rating.label("average_rating"),
                    Product.chapter_count.label("chapter_count"),
                    Product.video_count.label("video_count"),
                    Product.skill_count.label("skill_count"),
                    Product.objective_count.label("objective_count"),
                )
                .options(
                    selectinload(Product.interactive_course_detail)
                    .selectinload(InteractiveCourseDetailsModel.chapters)
                    .selectinload(InteractiveChapterModel.videos),
                    selectinload(Product.product_skills).selectinload(ProductSkill.skill),
                    selectinload(Product.product_objectives).selectinload(ProductObjective.objective),
                    selectinload(Product.level_obj),
                )
                .where(Product.type_id == ProductType.INTERACTIVE_COURSES_ID)
                .order_by(Product.average_rating.desc())
                .offset((page - 1) * limit)
                .limit(limit)
            )

            if category_id:
                stmt = stmt.where(Product.category_id == category_id)

            if skill_id:
                stmt = stmt.join(Product.product_skills).where(ProductSkill.skill_id == skill_id)

            result = await self.db.execute(stmt)
            rows = result.all()
            return [
                {
                    "product": row.Product,
                    "average_rating": row.average_rating,
                    "chapter_count": row.chapter_count,
                    "video_count": row.video_count,
                    "skill_count": row.skill_count,
                    "objective_count": row.objective_count,
                }
                for row in rows
            ]
        
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving interactive course products",
                additional_info={
                    "error": str(e),
                    "page": page,
                    "limit": limit,
                    "category_id": str(category_id) if category_id else None,
                    "skill_id": str(skill_id) if skill_id else None,
                    "fixed_type_id": str(ProductType.INTERACTIVE_COURSES_ID),
                },
            )


class InteractiveChapterRepository(BaseRepository[InteractiveChapterModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(InteractiveChapterModel, db)

    async def get_chapters_by_course_id(self, course_id: UUID) -> Sequence[InteractiveChapterModel]:
        try:
            stmt = (
                select(InteractiveChapterModel)
                .where(InteractiveChapterModel.course_id == course_id)
                .order_by(InteractiveChapterModel.view_index.asc())
            )
            result = await self.db.execute(stmt)
            chapters = result.scalars().all()
            return chapters
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving chapters by course_id",
                additional_info={"error": str(e), "course_id": str(course_id)},
            )


class InteractiveVideoRepository(BaseRepository[InteractiveVideoModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(InteractiveVideoModel, db)

    async def get_videos_by_chapter_id(self, chapter_id: UUID) -> Sequence[InteractiveVideoModel]:
        try:
            stmt = (
                select(InteractiveVideoModel)
                .where(InteractiveVideoModel.chapter_id == chapter_id)
                .order_by(InteractiveVideoModel.view_index.asc())
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving videos by chapter_id",
                additional_info={"error": str(e), "chapter_id": str(chapter_id)},
            )

    async def get_video_with_paragraphs(self, video_id: UUID) -> InteractiveVideoModel | None:
        try:
            stmt = (
                select(InteractiveVideoModel)
                .where(InteractiveVideoModel.id == video_id)
                .options(
                    selectinload(InteractiveVideoModel.paragraphs),
                    selectinload(InteractiveVideoModel.type_styles),
                    selectinload(InteractiveVideoModel.paragraphs)
                    .selectinload(InteractiveParagraphModel.paragraph_words)
                    .selectinload(InteractiveWordModel.type),
                    selectinload(InteractiveVideoModel.paragraphs)
                    .selectinload(InteractiveParagraphModel.paragraph_keywords)
                    .selectinload(InteractiveKeyWordModel.type),
                    selectinload(InteractiveVideoModel.paragraphs)
                    .selectinload(InteractiveParagraphModel.paragraph_visual)
                    .selectinload(VisualItemModel.visual_type),
                    selectinload(InteractiveVideoModel.paragraphs)
                    .selectinload(InteractiveParagraphModel.paragraph_visual)
                    .selectinload(VisualItemModel.table),
                    selectinload(InteractiveVideoModel.paragraphs)
                    .selectinload(InteractiveParagraphModel.paragraph_visual)
                    .selectinload(VisualItemModel.chart)
                    .selectinload(ChartDataModel.chart_type),
                    selectinload(InteractiveVideoModel.paragraphs)
                    .selectinload(InteractiveParagraphModel.paragraph_visual)
                    .selectinload(VisualItemModel.image),
                    selectinload(InteractiveVideoModel.type_styles).selectinload(VideoKeywordTypeStyleModel.type),
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving video with paragraphs",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )