from typing import List, Optional
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant_manager import StorageBucket
from app.repositories.interactive_repositories.assist_file_repository import AssistFileModel, FileTypeRepository
from app.repositories.interactive_repositories.assist_image_repository import AssistImageRepository
from app.models.interactive_models.assist_files_model import AssistFileModel, AssistFileTypeModel
from app.schemas.interactive_schemas.interactive_request_schemas import (
    FileCreateSchema,
    FileUpdateSchema,
    FileTypeCreateSchema,
)
from app.services.storage_service import StorageService
from app.exceptions.service_exception import ServiceException


class AssistFileService:
    def __init__(
        self,
        db: AsyncSession,
        file_repo: AssistFileModel,
        file_type_repo: FileTypeRepository,
        assist_image_repo: AssistImageRepository,
        storage_service: StorageService,
    ):
        self.db = db
        self.file_repo = file_repo
        self.file_type_repo = file_type_repo
        self.image_repo = assist_image_repo
        self.storage_service = storage_service

    async def create_file(self, file_data: FileCreateSchema, uploaded_file: UploadFile) -> AssistFileModel:
        try:
            # Upload file to storage
            storage_path, file_url, original_filename = await self.storage_service.upload_file(
                file=uploaded_file,
                bucket_name=StorageBucket.INTERACTIVE_BUCKET,
                folder_prefix=StorageBucket.ASSIST_FILES_FOLDER
            )
            
            # Create file record in database
            file_dict = {
                "file_name": original_filename,
                "video_id": file_data.video_id,
                "file_type_id": file_data.file_type_id,
                "bucket_name": StorageBucket.INTERACTIVE_BUCKET,
                "storage_path": storage_path,
                "file_url": file_url
            }
            
            file = await self.file_repo.create(file_dict)
            await self.db.commit()
            return file
        except Exception as e:
            await self.db.rollback()
            raise ServiceException(
                status_code=500,
                detail="Error creating file",
                additional_info={
                    "error": str(e), 
                    "file_data": file_data.model_dump(),
                    "filename": uploaded_file.filename
                },
            )

    async def get_file(self, file_id: UUID) -> Optional[AssistFileModel]:
        try:
            return await self.file_repo.get_file_with_images(file_id)
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error retrieving file",
                additional_info={"error": str(e), "file_id": str(file_id)},
            )

    async def get_files_by_video(self, video_id: UUID) -> List[AssistFileModel]:
        try:
            return await self.file_repo.get_files_by_video_id(video_id)
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error retrieving files by video",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )

    async def update_file(self, file_id: UUID, file_data: FileUpdateSchema) -> Optional[AssistFileModel]:
        try:
            file_dict = file_data.model_dump(exclude_unset=True)
            if not file_dict:
                raise ServiceException(
                    status_code=400,
                    detail="No data provided for update",
                    additional_info={"file_id": str(file_id)},
                )
            
            file = await self.file_repo.update(file_id, file_dict)
            if file:
                await self.db.commit()
            return file
        except Exception as e:
            await self.db.rollback()
            raise ServiceException(
                status_code=500,
                detail="Error updating file",
                additional_info={"error": str(e), "file_id": str(file_id)},
            )

    async def delete_file(self, file_id: UUID) -> bool:
        try:
            # Get file info first to delete from storage
            file = await self.file_repo.get(file_id)
            if not file:
                return False
            
            # Delete from storage
            if file.storage_path and file.bucket_name:
                self.storage_service.delete_file_from_storage(file.bucket_name, file.storage_path)
            
            # Delete from database (this will cascade delete images)
            result = await self.file_repo.delete_file_and_images(file_id)
            if result:
                await self.db.commit()
            return result
        except Exception as e:
            await self.db.rollback()
            raise ServiceException(
                status_code=500,
                detail="Error deleting file",
                additional_info={"error": str(e), "file_id": str(file_id)},
            )

    async def create_file_type(self, file_type_data: FileTypeCreateSchema) -> AssistFileTypeModel:
        try:
            file_type_dict = file_type_data.model_dump()
            file_type = await self.file_type_repo.create(file_type_dict)
            await self.db.commit()
            return file_type
        except Exception as e:
            await self.db.rollback()
            raise ServiceException(
                status_code=500,
                detail="Error creating file type",
                additional_info={"error": str(e), "file_type_data": file_type_data.model_dump()},
            )

    async def get_file_type_by_name(self, name: str) -> Optional[AssistFileTypeModel]:
        try:
            return await self.file_type_repo.get_by_name(name)
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error retrieving file type by name",
                additional_info={"error": str(e), "name": name},
            )

    async def get_all_file_types(self) -> List[AssistFileTypeModel]:
        try:
            return await self.file_type_repo.get_all()
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error retrieving all file types",
                additional_info={"error": str(e)},
            )