import uuid

from app.repositories import (
    ProductRepository,
    BookVideoDetailsRepository,
    BookVideosRepository,
    ProductSkillRepository,
    ProductObjectiveRepository,
)
from app.schemas.book_video_schema import BookVideoCreate


class BookVideoService:
    def __init__(
            self,
            db,
            product_repo: ProductRepository,
            book_video_details_repo: BookVideoDetailsRepository,
            book_videos_repo: BookVideosRepository,
            product_skill_repo: ProductSkillRepository,
            product_objective_repo: ProductObjectiveRepository,
    ):
        self.db = db
        self.product_repo = product_repo
        self.book_video_details_repo = book_video_details_repo
        self.book_videos_repo = book_videos_repo
        self.product_skill_repo = product_skill_repo
        self.product_objective_repo = product_objective_repo

    async def create_book_video_product(self, video_data: BookVideoCreate) -> uuid.UUID:
        """
        Create a new book product along with video details,
        videos, skills, and objectives.
        """
        async with self.db.begin():
            # 1. Create Product
            product = await self.product_repo.create(
                {
                    "type_id": video_data.product_type_id,
                    "category_id": video_data.product_category_id,
                    "title": video_data.title,
                    "description": video_data.description,
                    "language": video_data.language,
                    "cover": video_data.cover,
                    "created_by": video_data.created_by,
                    "short_video": video_data.short_video,
                    "level_id": video_data.level_id,
                    "duration": video_data.duration,
                }
            )

            # 2. Create BookVideoDetail
            book_video_detail = await self.book_video_details_repo.create(
                {
                    "product_id": product.id,
                    "author_name": video_data.author_name,
                    "expected_time_completion": video_data.expected_time_completion,
                }
            )

            # 3. Create Videos
            if video_data.videos:
                for index, video in enumerate(video_data.videos):
                    await self.book_videos_repo.create(
                        {
                            "book_id": book_video_detail.id,
                            "video_name": video.video_name,
                            "video_duration": video.video_duration,
                            "url": video.url,
                            "view_index": video.view_index or (index + 1),
                        }
                    )

            # 4. Add Skills (many-to-many)
            if video_data.skills:
                for skill_id in video_data.skills:
                    await self.product_skill_repo.create(
                        {
                            "product_id": product.id,
                            "skill_id": skill_id,
                        }
                    )

            # 5. Add Objectives (many-to-many)
            if video_data.objectives:
                for obj_id in video_data.objectives:
                    await self.product_objective_repo.create(
                        {
                            "product_id": product.id,
                            "objective_id": obj_id,
                        }
                    )

        return product.id

    async def get_all_video_books(self, page: int = 1, limit: int = 10, category_id: uuid.UUID | None = None):
        """
        Fetch all video books.
        """
        return await self.book_video_details_repo.get_all_with_details(page=page, limit=limit, category_id=category_id)

    async def get_book_video_by_product_id(self, product_id: uuid.UUID):
        """
        Fetch one video book with product details, videos, skills, and objectives by product_id.
        """
        return await self.book_video_details_repo.get_by_product_id_with_details(product_id)
