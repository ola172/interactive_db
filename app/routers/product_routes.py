# Product-related routes
from fastapi import APIRouter, Depends, Query
from app.container import get_product_service
from app.schemas.product import ProductTypeCreate
from app.services import ProductService

from uuid import UUID
product_router = APIRouter(prefix="/products", tags=["Products"])


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
