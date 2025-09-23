import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form

from app.container import get_interactive_image_service
from app.exceptions.custom_exception import CustomHTTPException, CustomException
from app.schemas.interactive_schemas.interactive_request_schemas import (
    ImageCreateSchema,
    ImageUpdateSchema,
    FileImageTypeEnum,
)
from app.services.interactive_image_service import InteractiveImageService
from app.models.interactive_models.image_model import ImageTypeEnum

interactive_image_router = APIRouter(
    prefix="/interactive-images", tags=["Interactive Images"]
)


# Image Endpoints

@interactive_image_router.post("/")
async def create_image(
    image: UploadFile = File(...),
    file_id: uuid.UUID = Form(...),
    image_title: str = Form(...),
    proposed_image_type: FileImageTypeEnum = Form(...),
    is_protected: bool = Form(False),
    searched_image_url: str = Form(None),
    description: str = Form(None),
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Create a new image with upload.
    """
    try:
        # Create schema from form data
        image_data = ImageCreateSchema(
            file_id=file_id,
            image_title=image_title,
            proposed_image_type=proposed_image_type,
            is_protected=is_protected,
            searched_image_url=searched_image_url,
            description=description
        )
        
        result = await image_service.create_image(image_data, image)
        return result
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_image_router.get("/{image_id}")
async def get_image(
    image_id: uuid.UUID,
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Get an image by ID.
    """
    try:
        result = await image_service.get_image(image_id)
        if not result:
            raise CustomHTTPException(
                status_code=404,
                detail="Image not found",
                exception_type="NotFound",
                additional_info={"image_id": str(image_id)},
            )
        return result
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_image_router.get("/file/{file_id}")
async def get_images_by_file(
    file_id: uuid.UUID,
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Get all images for a specific file.
    """
    try:
        images = await image_service.get_images_by_file(file_id)
        return {"images": images}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_image_router.get("/type/{image_type}")
async def get_images_by_type(
    image_type: ImageTypeEnum,
    file_id: Optional[uuid.UUID] = Query(None),
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Get images by type, optionally filtered by file ID.
    """
    try:
        images = await image_service.get_images_by_type(image_type, file_id)
        return {"images": images}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_image_router.get("/protected/")
async def get_protected_images(
    file_id: Optional[uuid.UUID] = Query(None),
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Get protected images, optionally filtered by file ID.
    """
    try:
        images = await image_service.get_protected_images(file_id)
        return {"images": images}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_image_router.put("/{image_id}")
async def update_image(
    image_id: uuid.UUID,
    image_request: ImageUpdateSchema,
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Update an image.
    """
    try:
        result = await image_service.update_image(image_id, image_request)
        if not result:
            raise CustomHTTPException(
                status_code=404,
                detail="Image not found",
                exception_type="NotFound",
                additional_info={"image_id": str(image_id)},
            )
        return result
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_image_router.delete("/{image_id}")
async def delete_image(
    image_id: uuid.UUID,
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Delete an image.
    """
    try:
        result = await image_service.delete_image(image_id)
        if not result:
            raise CustomHTTPException(
                status_code=404,
                detail="Image not found",
                exception_type="NotFound",
                additional_info={"image_id": str(image_id)},
            )
        return {"message": "Image deleted successfully"}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )