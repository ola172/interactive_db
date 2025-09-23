import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from app.container import get_interactive_file_service, get_interactive_image_service
from app.exceptions.custom_exception import CustomHTTPException, CustomException
from app.schemas.interactive_schemas.interactive_request_schemas import (
    FileCreateSchema,
    FileUpdateSchema,
    FileTypeCreateSchema,
    ImageCreateSchema,
    ImageUpdateSchema,
)
from app.services.interactive_file_service import InteractiveFileService
from app.services.interactive_image_service import InteractiveImageService

interactive_file_router = APIRouter(
    prefix="/interactive-files", tags=["Interactive Files"]
)


# File Endpoints

@interactive_file_router.post("/")
async def create_file(
    file: UploadFile = File(...),
    video_id: uuid.UUID = Form(None),
    file_type_id: uuid.UUID = Form(...),
    bucket_name: str = Form("interactive-files"),
    file_service: InteractiveFileService = Depends(get_interactive_file_service),
):
    """
    Create a new file with upload.
    """
    try:
        # Create schema from form data
        file_data = FileCreateSchema(
            video_id=video_id,
            file_type_id=file_type_id,
            bucket_name=bucket_name
        )
        
        result = await file_service.create_file(file_data, file)
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


@interactive_file_router.get("/video/{video_id}")
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