import uuid

from fastapi import APIRouter, Depends, Query

from app.container import get_pathway_service
from app.schemas.pathway_schema import PathwayCreateWithProduct
from app.services.pathway_service import PathwayService

pathway_router = APIRouter(prefix="/pathways", tags=["pathways"])


@pathway_router.post("")
async def create_pathway(
        pathway_request: PathwayCreateWithProduct,
        service: PathwayService = Depends(get_pathway_service)
):
    pathway_id = await service.create_pathway_with_product(pathway_request)
    return {"pathway_id": pathway_id}


@pathway_router.get("/all")
async def get_all_pathways(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        category_id: uuid.UUID | None = None,
        service: PathwayService = Depends(get_pathway_service)):
    results = await service.get_all_pathways(
        page=page,
        limit=limit,
        category_id=category_id
    )
    return {"results": results}


@pathway_router.get("/{pathway_id}")
async def get_pathway(pathway_id: uuid.UUID, service: PathwayService = Depends(get_pathway_service)):
    pathway = await service.get_pathway_by_id(pathway_id)
    return pathway
