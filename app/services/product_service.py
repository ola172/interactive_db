import uuid
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.models import ProductCategory
from app.repositories import (ProductRepository, ProductTypeRepository, ProductCategoryRepository,
                              ProductRatingRepository,
                              SkillRepository, ObjectiveRepository)
from app.schemas.product import ProductTypeCreate, ProductCategoryBase
from app.schemas.skills_objectives import SkillObjectiveSchema
from app.services.course_service import CourseService


class ProductService:
    def __init__(
        self,
        db: AsyncSession,
        product_repository: ProductRepository,
        product_type_repository: ProductTypeRepository,
        product_category_repo: ProductCategoryRepository,
        skill_repository: SkillRepository,
        objective_repository: ObjectiveRepository,
        product_rating_repository: ProductRatingRepository,
        course_service: CourseService
    ):
        self.db = db
        self.product_repository = product_repository
        self.product_type_repository = product_type_repository
        self.course_service = course_service
        self.product_category_repo = product_category_repo
        self.skill_repository = skill_repository
        self.objective_repository = objective_repository
        self.product_rating_repository = product_rating_repository

    async def create_skill(self, skill_data: SkillObjectiveSchema):
        """
        Create a new skill within a transaction.
        """
        async with self.db.begin():
            return await self.skill_repository.create(skill_data.model_dump())

    async def create_objective(self, objective_data: SkillObjectiveSchema):
        """
        Create a new objective within a transaction.
        """
        async with self.db.begin():
            return await self.objective_repository.create(objective_data.model_dump())

    async def get_all_skills(self) -> Sequence:
        """
        Fetch all skills.
        """
        return await self.skill_repository.get_all()

    async def get_all_objectives(self) -> Sequence:
        """
        Fetch all objectives.
        """
        return await self.objective_repository.get_all()

    async def get_all_product_types(self):
        """
        Fetch all product types.
        """
        return await self.product_type_repository.get_all()

    async def delete_product_type(self, product_type_id: UUID):
        """
        Delete a product type within a transaction.
        """
        async with self.db.begin():
            return await self.product_type_repository.delete(product_type_id)

    async def create_product_type(self, product_request: ProductTypeCreate):
        """
        Create a new product type within a transaction.
        """
        async with self.db.begin():
            return await self.product_type_repository.create(product_request.model_dump())

    async def get_all_products_by_type(
        self, product_type_id: UUID, page: int = 1, limit: int = 10, category_id: UUID | None = None
    ):
        """
        Fetch products by type, supporting pagination.
        Courses are fetched via CourseService to include course details.
        Other product types use ProductRepository.
        """
        product_type = await self.product_type_repository.get(product_type_id)
        if not product_type:
            return {"product_type": None, "products": []}

        if product_type.name.lower() == "course":
            courses = await self.course_service.get_all_courses(page=page, limit=limit,
                                                                category_id=category_id)
            return {"product_type": product_type, "products": courses}

        # For non-course products, use repository with pagination
        products = await self.product_repository.get_all_products_by_type(
            product_type_id
        )
        return {"product_type": product_type, "products": products}

    async def get_product_by_id(self, product_id: uuid.UUID):
        """
        Fetch a product by its ID.
        """
        return await self.product_repository.get(product_id)


    async def get_all_course_categories(
        self, page: int = 1, limit: int = 10
    ) -> Sequence[ProductCategory]:
        """
        Fetch all course categories with optional pagination.
        """
        return await self.product_category_repo.get_all(page=page, limit=limit)

    async def create_product_category(
        self, product_category: ProductCategoryBase
    ) -> ProductCategory:
        """
        Create a new course category.
        Only fields defined in the model are used.
        """
        category_data = {
            "name": product_category.name,
            "description": product_category.description
        }
        async with self.db.begin():
            category = await self.product_category_repo.create(category_data)
        return category

    async def get_all_product_categories(self) -> Sequence[ProductCategory]:
        """
        Fetch all product categories without pagination.
        """
        return await self.product_category_repo.get_all()


    async def get_product_rating(self, product_id: uuid.UUID) -> float | None:
        """
        Get the average rating for a product.
        """
        return await self.product_rating_repository.get_product_rating(product_id)
