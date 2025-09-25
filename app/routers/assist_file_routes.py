from typing import Optional
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.container import get_assist_file_service
from app.exceptions.custom_exception import CustomHTTPException, CustomException
from app.schemas.interactive_schemas.interactive_request_schemas import (
    FileCreateSchema,
    FileUpdateSchema,
    FileTypeCreateSchema,
)
from app.services.assist_file_service import AssistFileService

assist_file_router = APIRouter(
    prefix="/assist-files", tags=["Assist Files"]
)

# File Type Endpoints

@assist_file_router.post("/types/")
async def create_file_type(
    file_type_request: FileTypeCreateSchema,
    file_service: AssistFileService = Depends(get_assist_file_service),
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


@assist_file_router.get("/types/")
async def get_all_file_types(
    file_service: AssistFileService = Depends(get_assist_file_service),
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


@assist_file_router.get("/types/{name}/")
async def get_file_type_by_name(
    name: str,
    file_service: AssistFileService = Depends(get_assist_file_service),
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

@assist_file_router.post("/")
async def create_file(
    file: UploadFile = File(...),
    video_id: Optional[str] = Form(None),
    file_type_id: uuid.UUID = Form(...),
    file_service: AssistFileService = Depends(get_assist_file_service),
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


@assist_file_router.get("/{file_id}/")
async def get_file(
    file_id: uuid.UUID,
    file_service: AssistFileService = Depends(get_assist_file_service),
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


@assist_file_router.get("/{video_id}/")
async def get_files_by_video(
    video_id: uuid.UUID,
    file_service: AssistFileService = Depends(get_assist_file_service),
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


@assist_file_router.put("/{file_id}/")
async def update_file(
    file_id: uuid.UUID,
    file_request: FileUpdateSchema,
    file_service: AssistFileService = Depends(get_assist_file_service),
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


@assist_file_router.delete("/{file_id}/")
async def delete_file(
    file_id: uuid.UUID,
    file_service: AssistFileService = Depends(get_assist_file_service),
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
