from typing import Sequence, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.constant_manager import ProductType
from app.models import Product, ProductSkill
from app.models.course import CourseDetail, Chapter, Video, CourseInstructor
from app.models.skill_objective import ProductObjective
from app.repositories.base_repo import BaseRepository
from app.exceptions.repo_exception import RepoException


class CourseDetailRepository(BaseRepository[CourseDetail]):
    def __init__(self, db: AsyncSession):
        super().__init__(CourseDetail, db)

    async def get_course_product(self, product_id: UUID) -> dict[str, Any] | None:
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
                    # load course → instructors → instructor details
                    selectinload(Product.course_detail)
                    .selectinload(CourseDetail.instructors)
                    .selectinload(CourseInstructor.instructor),

                    # load skills
                    selectinload(Product.product_skills).selectinload(ProductSkill.skill),

                    # load objectives
                    selectinload(Product.product_objectives).selectinload(ProductObjective.objective),

                    # load level relationship
                    selectinload(Product.level_obj),

                    # load chapters + videos
                    selectinload(Product.course_detail)
                    .selectinload(CourseDetail.chapters)
                    .selectinload(Chapter.videos),
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
                detail="Error retrieving course product",
                additional_info={"error": str(e), "product_id": str(product_id)},
            )

    from uuid import UUID

    COURSE_TYPE_ID = UUID("171db108-d3e3-43d9-9153-8692f34deada")

    async def get_all_course_product(
            self,
            page: int = 1,
            limit: int = 10,
            category_id: UUID | None = None,
            instructor_id: UUID | None = None,
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
                    selectinload(Product.course_detail)
                    .selectinload(CourseDetail.instructors)
                    .selectinload(CourseInstructor.instructor),
                    selectinload(Product.product_skills).selectinload(ProductSkill.skill),
                    selectinload(Product.product_objectives).selectinload(ProductObjective.objective),
                    selectinload(Product.level_obj),
                    selectinload(Product.course_detail)
                    .selectinload(CourseDetail.chapters)
                    .selectinload(Chapter.videos),
                )
                # ✅ Always filter by type_id
                .where(Product.type_id == ProductType.COURSES_ID)
                .order_by(Product.average_rating.desc())
                .offset((page - 1) * limit)
                .limit(limit)
            )

            # Filter by category
            if category_id:
                stmt = stmt.where(Product.category_id == category_id)

            # Filter by instructor
            if instructor_id:
                stmt = (
                    stmt.join(Product.course_detail)
                    .join(CourseDetail.instructors)
                    .where(CourseInstructor.instructor_id == instructor_id)
                )

            # Filter by skill
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
                detail="Error retrieving course products",
                additional_info={
                    "error": str(e),
                    "page": page,
                    "limit": limit,
                    "category_id": str(category_id) if category_id else None,
                    "instructor_id": str(instructor_id) if instructor_id else None,
                    "skill_id": str(skill_id) if skill_id else None,
                    "fixed_type_id": str(ProductType.COURSES_ID),
                },
            )

class ChapterRepository(BaseRepository[Chapter]):
    def __init__(self, db: AsyncSession):
        super().__init__(Chapter, db)

    async def get_chapters_by_course_id(self, course_id: UUID) -> Sequence[Chapter]:
        try:
            stmt = (
                select(Chapter)
                .where(Chapter.course_id == course_id)
                .order_by(Chapter.view_index.asc())
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving chapters by course_id",
                additional_info={"error": str(e), "course_id": str(course_id)},
            )


class VideoRepository(BaseRepository[Video]):
    def __init__(self, db: AsyncSession):
        super().__init__(Video, db)

    async def get_videos_by_chapter_id(self, chapter_id: UUID) -> Sequence[Video]:
        try:
            stmt = (
                select(Video)
                .where(Video.chapter_id == chapter_id)
                .order_by(Video.view_index.asc())
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving videos by chapter_id",
                additional_info={"error": str(e), "chapter_id": str(chapter_id)},
            )
