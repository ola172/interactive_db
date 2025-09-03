import uuid

from fastapi import APIRouter, Depends, Query

from app.container import get_pathway_service
from app.exceptions.custom_exception import CustomException, CustomHTTPException
from app.schemas.pathway_schema import PathwayCreateWithProduct
from app.services.pathway_service import PathwayService

pathway_router = APIRouter(prefix="/pathways", tags=["pathways"])


@pathway_router.post("")
async def create_pathway(
        pathway_request: PathwayCreateWithProduct,
        service: PathwayService = Depends(get_pathway_service)
):
    try:
        pathway_id = await service.create_pathway_with_product(pathway_request)
        return {"pathway_id": pathway_id}
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


@pathway_router.get("/all")
async def get_all_pathways(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        category_id: uuid.UUID | None = None,
        service: PathwayService = Depends(get_pathway_service)
):
    try:
        results = await service.get_all_pathways(
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


@pathway_router.get("/{pathway_id}")
async def get_pathway(
        pathway_id: uuid.UUID,
        service: PathwayService = Depends(get_pathway_service)
):
    try:
        pathway = await service.get_pathway_by_id(pathway_id)
        return pathway
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
