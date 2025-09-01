import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.repositories import (
    ProductRepository,
    BookReadingRepository,
    BookSectionRepository,
    ProductSkillRepository,
    ProductObjectiveRepository,
)
from app.schemas.book_reading_schema import BookCreate
from app.models import BookReadingDetail, Product


class BookService:
    def __init__(
        self,
        db,
        product_repo: ProductRepository,
        book_reading_repo: BookReadingRepository,
        book_section_repo: BookSectionRepository,
        product_skill_repo: ProductSkillRepository,
        product_objective_repo: ProductObjectiveRepository,
    ):
        self.db = db
        self.product_repo = product_repo
        self.book_reading_repo = book_reading_repo
        self.book_section_repo = book_section_repo
        self.product_skill_repo = product_skill_repo
        self.product_objective_repo = product_objective_repo

    async def create_book_reading_product(self, book_data: BookCreate) -> uuid.UUID:
        """
        Create a new book product along with reading details,
        sections, skills, objectives, and instructors.
        """
        async with self.db.begin():
            # 1. Create Product
            product = await self.product_repo.create(
                {
                    "type_id": book_data.product_type_id,
                    "category_id": book_data.product_category_id,
                    "title": book_data.title,
                    "description": book_data.description,
                    "language": book_data.language,
                    "level": book_data.level,
                    "duration": book_data.duration,
                }
            )

            # 2. Create BookReadingDetail
            book_detail = await self.book_reading_repo.create(
                {
                    "product_id": product.id,
                    "author_name": book_data.author_name,
                    "author_bio": book_data.author_bio,
                    "cover_path": book_data.cover_path,
                    "page_count": book_data.page_count,
                    "reading_time": book_data.reading_time,
                    "readers_count": book_data.readers_count,
                    "is_new": book_data.is_new,
                    "expected_time_completion": book_data.expected_time_completion,
                    "experience_required": book_data.experience_required,
                }
            )

            # 3. Create Sections
            if book_data.sections:
                for index, section in enumerate(book_data.sections):
                    await self.book_section_repo.create(
                        {
                            "book_id": book_detail.id,
                            "title": section.title,
                            "content": section.content,
                            "stage_index": section.stage_index or (index + 1),
                        }
                    )

            # 4. Add Skills (many-to-many)
            if book_data.skills:
                for skill_id in book_data.skills:
                    await self.product_skill_repo.create(
                        {
                            "product_id": product.id,
                            "skill_id": skill_id,
                        }
                    )

            # 5. Add Objectives (many-to-many)
            if book_data.objectives:
                for obj_id in book_data.objectives:
                    await self.product_objective_repo.create(
                        {
                            "product_id": product.id,
                            "objective_id": obj_id,
                        }
                    )

        return product.id

    async def get_all_reading_books(self, page: int = 1, limit: int = 10, category_id: uuid.UUID | None = None):
        """
        Fetch all reading books.
        """
        return await self.book_reading_repo.get_all_with_details(page=page, limit=limit, category_id=category_id)

    async def get_book_by_product_id(self, product_id: uuid.UUID):
        """
        Fetch one book with product details, sections, skills, and objectives by product_id.
        """
        return await self.book_reading_repo.get_book_with_sections(product_id)
