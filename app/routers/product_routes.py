# Product-related routes
from fastapi import APIRouter, Depends, Query
from app.container import get_product_service
from app.schemas.product import ProductTypeCreate, ProductCategoryBase
from app.schemas.skills_objectives import SkillObjectiveSchema
from app.services import ProductService

from uuid import UUID
product_router = APIRouter(prefix="/products", tags=["Products"])



@product_router.post("/categories",)
async def create_product_category(
    category_request: ProductCategoryBase,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.create_product_category(category_request)

@product_router.get("/categories")
async def read_product_categories(
    product_service: ProductService = Depends(get_product_service),
):
    categories = await product_service.get_all_product_categories()
    return [c.__dict__ for c in categories]


@product_router.post("/skills")
async def create_skill(
    skill_request: SkillObjectiveSchema,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.create_skill(skill_request)


@product_router.get("/skills")
async def read_skills(
    product_service: ProductService = Depends(get_product_service),
):
    skills = await product_service.get_all_skills()
    return [s.__dict__ for s in skills]


@product_router.post("/objectives")
async def create_objective(
    objective_request: SkillObjectiveSchema,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.create_objective(objective_request)

@product_router.get("/objectives")
async def read_objectives(
    product_service: ProductService = Depends(get_product_service),
):
    objectives = await product_service.get_all_objectives()
    return [o.__dict__ for o in objectives]

@product_router.get("/types")
async def read_product_types(
    product_service: ProductService = Depends(get_product_service),
):
    types = await product_service.get_all_product_types()
    return [t.__dict__ for t in types]


@product_router.delete("/products/{product_id}")
async def delete_product(product_id: UUID, product_service: ProductService = Depends(get_product_service)):
    return await product_service.delete_product_type(product_id)

@product_router.post(
    "/products_types",)
async def create_product_type(product_request: ProductTypeCreate, product_service: ProductService = Depends(get_product_service)):
    return await product_service.create_product_type(product_request)


@product_router.get("/all/{product_type_id}")
async def get_all_products_by_type(
    product_type_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.get_all_products_by_type(
        product_type_id=product_type_id,
        page=page,
        limit=limit
    )

@product_router.get("/{product_id}/rating")
async def get_product_rating(
    product_id: UUID,
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.get_product_rating(product_id)