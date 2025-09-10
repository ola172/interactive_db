import uuid
from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exception import CustomException
from app.exceptions.service_exception import ServiceException
from app.models import ProductCategory
from app.repositories import (
    ProductRepository,
    ProductTypeRepository,
    ProductCategoryRepository,
    ProductRatingRepository,
    SkillRepository,
    ObjectiveRepository,
)
from app.repositories.product import ProductLevelRepository
from app.schemas.product import ProductTypeCreate, ProductCategoryBase
from app.schemas.skills_objectives import SkillObjectiveSchema
from app.services.course_service import CourseService


class ProductService:
    def __init__(
            self,
            db: AsyncSession,
            product_level_repository: ProductLevelRepository,
            product_repository: ProductRepository,
            product_type_repository: ProductTypeRepository,
            product_category_repo: ProductCategoryRepository,
            skill_repository: SkillRepository,
            objective_repository: ObjectiveRepository,
            product_rating_repository: ProductRatingRepository,
            course_service: CourseService,
    ):
        self.db = db
        self.product_repository = product_repository
        self.product_type_repository = product_type_repository
        self.course_service = course_service
        self.product_category_repo = product_category_repo
        self.skill_repository = skill_repository
        self.objective_repository = objective_repository
        self.product_rating_repository = product_rating_repository
        self.product_level_repository = product_level_repository

    async def create_level(self, level_name: str):
        """Create a new product level within a transaction."""
        try:
            async with self.db.begin():
                return await self.product_level_repository.create({"name": level_name})
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create product level",
                additional_info={"error": str(e), "level_name": level_name},
            )

    async def get_all_levels(self) -> Sequence:
        """Fetch all product levels."""
        try:
            return await self.product_level_repository.get_all()
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch product levels",
                additional_info={"error": str(e)},
            )

    async def delete_level(self, level_id: UUID):
        """Delete a product level within a transaction."""
        try:
            async with self.db.begin():
                return await self.product_level_repository.delete(level_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete product level",
                additional_info={"error": str(e), "level_id": str(level_id)},
            )

    async def create_skill(self, skill_data: SkillObjectiveSchema):
        """Create a new skill within a transaction."""
        try:
            async with self.db.begin():
                return await self.skill_repository.create(skill_data.model_dump())
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create skill",
                additional_info={"error": str(e), "skill_data": skill_data.model_dump()},
            )

    async def create_objective(self, objective_data: SkillObjectiveSchema):
        """Create a new objective within a transaction."""
        try:
            async with self.db.begin():
                return await self.objective_repository.create(objective_data.model_dump())
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create objective",
                additional_info={"error": str(e), "objective_data": objective_data.model_dump()},
            )

    async def get_all_skills(self) -> Sequence:
        """Fetch all skills."""
        try:
            return await self.skill_repository.get_all()
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch skills",
                additional_info={"error": str(e)},
            )

    async def get_all_objectives(self) -> Sequence:
        """Fetch all objectives."""
        try:
            return await self.objective_repository.get_all()
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch objectives",
                additional_info={"error": str(e)},
            )

    async def get_all_product_types(self):
        """Fetch all product types."""
        try:
            return await self.product_type_repository.get_all()
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch product types",
                additional_info={"error": str(e)},
            )

    async def delete_product_type(self, product_type_id: UUID):
        """Delete a product type within a transaction."""
        try:
            async with self.db.begin():
                return await self.product_type_repository.delete(product_type_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete product type",
                additional_info={"error": str(e), "product_type_id": str(product_type_id)},
            )

    async def create_product_type(self, product_request: ProductTypeCreate):
        """Create a new product type within a transaction."""
        try:
            async with self.db.begin():
                return await self.product_type_repository.create(product_request.model_dump())
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create product type",
                additional_info={"error": str(e), "product_request": product_request.model_dump()},
            )

    async def get_all_products_by_type(
            self, product_type_id: UUID, page: int = 1, limit: int = 10, category_id: UUID | None = None
    ):
        """Fetch products by type, supporting pagination."""
        try:
            product_type = await self.product_type_repository.get(product_type_id)
            if not product_type:
                return {"product_type": None, "products": []}

            if product_type.name.lower() == "course":
                courses = await self.course_service.get_all_courses(
                    page=page, limit=limit, category_id=category_id
                )
                return {"product_type": product_type, "products": courses}

            products = await self.product_repository.get_all_products_by_type(product_type_id)
            return {"product_type": product_type, "products": products}
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch products by type",
                additional_info={
                    "error": str(e),
                    "product_type_id": str(product_type_id),
                    "page": page,
                    "limit": limit,
                    "category_id": str(category_id) if category_id else None,
                },
            )

    async def get_product_by_id(self, product_id: uuid.UUID):
        """Fetch a product by its ID."""
        try:
            return await self.product_repository.get(product_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch product by ID",
                additional_info={"error": str(e), "product_id": str(product_id)},
            )

    async def get_all_course_categories(self, page: int = 1, limit: int = 10) -> Sequence[ProductCategory]:
        """Fetch all course categories with optional pagination."""
        try:
            return await self.product_category_repo.get_all(page=page, limit=limit)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch course categories",
                additional_info={"error": str(e), "page": page, "limit": limit},
            )

    async def create_product_category(self, product_category: ProductCategoryBase) -> ProductCategory:
        """Create a new course category."""
        try:
            category_data = {
                "name": product_category.name,
                "description": product_category.description,
            }
            async with self.db.begin():
                category = await self.product_category_repo.create(category_data)
            return category
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create product category",
                additional_info={"error": str(e), "category": product_category.model_dump()},
            )

    async def get_all_product_categories(self) -> Sequence[ProductCategory]:
        """Fetch all product categories without pagination."""
        try:
            return await self.product_category_repo.get_all()
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch product categories",
                additional_info={"error": str(e)},
            )

    async def get_product_category_by_id(self, category_id: uuid.UUID) -> ProductCategory | None:
        """Fetch a product category by its ID."""
        try:
            return await self.product_category_repo.get(category_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch product category by ID",
                additional_info={"error": str(e), "category_id": str(category_id)},
            )

    async def get_product_rating(self, product_id: uuid.UUID) -> float | None:
        """Get the average rating for a product."""
        try:
            return await self.product_rating_repository.get_product_rating(product_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch product rating",
                additional_info={"error": str(e), "product_id": str(product_id)},
            )

    async def get_product_rate_and_review(self, product_id: uuid.UUID) -> Sequence:
        """Get all ratings and reviews for a product."""
        try:
            return await self.product_rating_repository.get_product_rate_and_review(product_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch product ratings and reviews",
                additional_info={"error": str(e), "product_id": str(product_id)},
            )