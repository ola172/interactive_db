from fastapi import APIRouter, Depends
from typing import List
import uuid

from app.schemas.pathway_schema import PathwayCreate, PathwayResponse
from app.services.pathway_service import PathwayService
from app.container import get_pathway_service

router = APIRouter(prefix="/pathways", tags=["pathways"])

@router.post("")
async def create_pathway(
    pathway_request: PathwayCreate,
    service: PathwayService = Depends(get_pathway_service)
):
    return await service.create_pathway(pathway_request)


@router.get("/{pathway_id}", response_model=PathwayResponse)
async def get_pathway(pathway_id: uuid.UUID, service: PathwayService = Depends(get_pathway_service)):
    pathway = await service.get_pathway_by_id(pathway_id)
    return pathway


@router.get("/all", response_model=List[PathwayResponse])
async def get_all_pathways(service: PathwayService = Depends(get_pathway_service)):
    return await service.get_all_pathways()
