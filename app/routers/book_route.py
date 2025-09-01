# Product-related routes
import uuid

from fastapi import APIRouter, Depends, Query

from app.container import get_book_service, get_book_video_service
from app.schemas.book_reading_schema import BookCreate
from app.schemas.book_video_schema import BookVideoCreate
from app.services.book_reading_service import BookService
from app.services.book_video_service import BookVideoService

book_router = APIRouter(prefix="/books", tags=["books"])


@book_router.post("/reading")
async def create_book(
        book_request: BookCreate,
        book_service: BookService = Depends(get_book_service)
):
    book_reading_id = await book_service.create_book_reading_product(book_request)
    return {"book_reading_id": book_reading_id}


@book_router.get("/reading/all")
async def get_all_books(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        category_id: uuid.UUID
                     | None = None,
        book_service: BookService = Depends(get_book_service)
):
    """
    Get all reading books with optional pagination and category filtering.
    """
    return await book_service.get_all_reading_books(page=page, limit=limit, category_id=category_id)


@book_router.get("/reading/{product_id}")
async def get_book_by_id(
        product_id: uuid.UUID,
        book_service: BookService = Depends(get_book_service)
):
    return await book_service.get_book_by_product_id(product_id)


@book_router.post("/video")
async def create_video_book(
        video_book_request: BookVideoCreate,
        book_video_service: BookVideoService = Depends(get_book_video_service)
):
    book_video_id = await book_video_service.create_book_video_product(video_book_request)
    return {"book_video_id": book_video_id}


@book_router.get("/video/all")
async def get_all_video_books(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        category_id: uuid.UUID
                     | None = None,
        book_video_service: BookVideoService = Depends(get_book_video_service)
):
    return await book_video_service.get_all_video_books(page=page, limit=limit, category_id=category_id)


@book_router.get("/video/{product_id}")
async def get_video_book_by_id(
        product_id: uuid.UUID,
        book_video_service: BookVideoService = Depends(get_book_video_service)
):
    return await book_video_service.get_book_video_by_product_id(product_id)
