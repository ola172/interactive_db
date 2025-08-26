from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ProductRepository, ProductTypeRepository
from app.schemas.product import ProductTypeCreate
from app.services.course_service import CourseService


class ProductService:
    def __init__(
        self,
        db: AsyncSession,
        product_repository: ProductRepository,
        product_type_repository: ProductTypeRepository,
        course_service: CourseService
    ):
        self.db = db
        self.product_repository = product_repository
        self.product_type_repository = product_type_repository
        self.course_service = course_service

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
        self, product_type_id: UUID, page: int = 1, limit: int = 10
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
            courses = await self.course_service.get_all_courses(page=page, limit=limit)
            return {"product_type": product_type, "products": courses}

        # For non-course products, use repository with pagination
        products = await self.product_repository.get_all_products_by_type(
            product_type_id
        )
        return {"product_type": product_type, "products": products}
