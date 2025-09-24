from typing import Optional
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.container import get_interactive_file_service, get_interactive_image_service
from app.exceptions.custom_exception import CustomHTTPException, CustomException
from app.schemas.interactive_schemas.interactive_request_schemas import (
    FileCreateSchema,
    FileUpdateSchema,
    FileTypeCreateSchema,
    ImageCreateSchema,
    ImageUpdateSchema,
    FileImageTypeEnum,
)
from app.services.interactive_file_service import InteractiveFileService
from app.services.interactive_image_service import InteractiveImageService

interactive_file_router = APIRouter(
    prefix="/interactive-files", tags=["Interactive Files"]
)

# File Type Endpoints

@interactive_file_router.post("/types/")
async def create_file_type(
    file_type_request: FileTypeCreateSchema,
    file_service: InteractiveFileService = Depends(get_interactive_file_service),
):
    """
    Create a new file type.
    """
    try:
        result = await file_service.create_file_type(file_type_request)
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


@interactive_file_router.get("/types/")
async def get_all_file_types(
    file_service: InteractiveFileService = Depends(get_interactive_file_service),
):
    """
    Get all file types.
    """
    try:
        result = await file_service.get_all_file_types()
        return {"file_types": result}
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


@interactive_file_router.get("/types/{name}")
async def get_file_type_by_name(
    name: str,
    file_service: InteractiveFileService = Depends(get_interactive_file_service),
):
    """
    Get a file type by name.
    """
    try:
        result = await file_service.get_file_type_by_name(name)
        if not result:
            raise CustomHTTPException(
                status_code=404,
                detail="File type not found",
                exception_type="NotFound",
                additional_info={"name": name},
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

# File Endpoints

@interactive_file_router.post("/")
async def create_file(
    file: UploadFile = File(...),
    video_id: Optional[str] = Form(None),
    file_type_id: uuid.UUID = Form(...),
    file_service: InteractiveFileService = Depends(get_interactive_file_service),
):
    """
    Create a new file with upload.
    """
    try:
        if not video_id.strip():
            video_id = None
        # Create schema from form data
        file_data = FileCreateSchema(
            video_id=video_id,
            file_type_id=file_type_id,
        )
        
        result = await file_service.create_file(file_data, file)
        return result
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=str(e.detail),
            exception_type=str(e.exception_type),
            additional_info=str(e.additional_info),
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_file_router.get("/{file_id}")
async def get_file(
    file_id: uuid.UUID,
    file_service: InteractiveFileService = Depends(get_interactive_file_service),
):
    """
    Get a file by ID with its images.
    """
    try:
        result = await file_service.get_file(file_id)
        if not result:
            raise CustomHTTPException(
                status_code=404,
                detail="File not found",
                exception_type="NotFound",
                additional_info={"file_id": str(file_id)},
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


@interactive_file_router.get("/{video_id}")
async def get_files_by_video(
    video_id: uuid.UUID,
    file_service: InteractiveFileService = Depends(get_interactive_file_service),
):
    """
    Get all files for a specific video.
    """
    try:
        files = await file_service.get_files_by_video(video_id)
        return {"files": files}
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


@interactive_file_router.put("/{file_id}")
async def update_file(
    file_id: uuid.UUID,
    file_request: FileUpdateSchema,
    file_service: InteractiveFileService = Depends(get_interactive_file_service),
):
    """
    Update a file.
    """
    try:
        result = await file_service.update_file(file_id, file_request)
        if not result:
            raise CustomHTTPException(
                status_code=404,
                detail="File not found",
                exception_type="NotFound",
                additional_info={"file_id": str(file_id)},
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


@interactive_file_router.delete("/{file_id}")
async def delete_file(
    file_id: uuid.UUID,
    file_service: InteractiveFileService = Depends(get_interactive_file_service),
):
    """
    Delete a file and all its images.
    """
    try:
        result = await file_service.delete_file(file_id)
        if not result:
            raise CustomHTTPException(
                status_code=404,
                detail="File not found",
                exception_type="NotFound",
                additional_info={"file_id": str(file_id)},
            )
        return {"message": "File deleted successfully"}
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




# Assist Image Endpoints

@interactive_file_router.post("/{file_id}/images/")
async def create_assist_image(
    file_id: uuid.UUID,
    image: UploadFile = File(...),
    image_title: str = Form(...),
    proposed_image_type: FileImageTypeEnum = Form(...),
    is_protected: bool = Form(False),
    searched_image_url: str = Form(None),
    description: str = Form(None),
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Create a new assist image for a file.
    """
    try:
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


@interactive_file_router.get("/{file_id}/images/")
async def get_assist_images_by_file(
    file_id: uuid.UUID,
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Get all assist images for a specific file.
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


@interactive_file_router.get("/images/{image_id}")
async def get_assist_image(
    image_id: uuid.UUID,
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Get an assist image by ID.
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


@interactive_file_router.put("/images/{image_id}")
async def update_assist_image(
    image_id: uuid.UUID,
    image_request: ImageUpdateSchema,
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Update an assist image.
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


@interactive_file_router.delete("/images/{image_id}")
async def delete_assist_image(
    image_id: uuid.UUID,
    image_service: InteractiveImageService = Depends(get_interactive_image_service),
):
    """
    Delete an assist image.
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