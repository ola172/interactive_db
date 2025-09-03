from uuid import UUID
from fastapi import APIRouter, Depends, Query

from app.container import get_product_service
from app.schemas.product import ProductTypeCreate, ProductCategoryBase
from app.schemas.skills_objectives import SkillObjectiveSchema
from app.services import ProductService
from app.exceptions.custom_exception import CustomException, CustomHTTPException

product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.post("/categories")
async def create_product_category(
        category_request: ProductCategoryBase,
        product_service: ProductService = Depends(get_product_service),
):
    try:
        return await product_service.create_product_category(category_request)
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.get("/categories")
async def read_product_categories(
        product_service: ProductService = Depends(get_product_service),
):
    try:
        categories = await product_service.get_all_product_categories()
        results = [c.__dict__ for c in categories]
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.post("/skills")
async def create_skill(
        skill_request: SkillObjectiveSchema,
        product_service: ProductService = Depends(get_product_service),
):
    try:
        return await product_service.create_skill(skill_request)
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.get("/skills")
async def read_skills(
        product_service: ProductService = Depends(get_product_service),
):
    try:
        skills = await product_service.get_all_skills()
        results = [s.__dict__ for s in skills]
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.post("/objectives")
async def create_objective(
        objective_request: SkillObjectiveSchema,
        product_service: ProductService = Depends(get_product_service),
):
    try:
        return await product_service.create_objective(objective_request)
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.get("/objectives")
async def read_objectives(
        product_service: ProductService = Depends(get_product_service),
):
    try:
        objectives = await product_service.get_all_objectives()
        results = [o.__dict__ for o in objectives]
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.get("/types")
async def read_product_types(
        product_service: ProductService = Depends(get_product_service),
):
    try:
        types = await product_service.get_all_product_types()
        results = [t.__dict__ for t in types]
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.delete("/products/{product_id}")
async def delete_product(
        product_id: UUID,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        return await product_service.delete_product_type(product_id)
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.post("/products_types")
async def create_product_type(
        product_request: ProductTypeCreate,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        return await product_service.create_product_type(product_request)
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.get("/all/{product_type_id}")
async def get_all_products_by_type(
        product_type_id: UUID,
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        category_id: UUID | None = None,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        results = await product_service.get_all_products_by_type(
            product_type_id=product_type_id,
            page=page,
            limit=limit,
            category_id=category_id
        )
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.get("/{product_id}/rating")
async def get_product_rating(
        product_id: UUID,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        results = await product_service.get_product_rating(product_id)
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.post("/levels")
async def create_product_level(
        level_name: str,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        return await product_service.create_level(level_name)
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.get("/levels")
async def read_product_levels(
        product_service: ProductService = Depends(get_product_service),
):
    try:
        levels = await product_service.get_all_levels()
        results = [l.__dict__ for l in levels]
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )


@product_router.delete("/levels/{level_id}")
async def delete_product_level(
        level_id: UUID,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        results = await product_service.delete_level(level_id)
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)}
        )
