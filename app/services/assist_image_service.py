from typing import List, Optional
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant_manager import StorageBucket
from app.repositories.interactive_repositories.assist_image_repository import AssistImageRepository
from app.models.interactive_models.assist_image_model import AssistImageModel, AssistImageTypeEnum
from app.schemas.interactive_schemas.interactive_request_schemas import (
    ImageCreateSchema,
    ImageUpdateSchema,
)
from app.services.storage_service import StorageService
from app.exceptions.service_exception import ServiceException


class AssistImageService:
    def __init__(
        self,
        db: AsyncSession,
        image_repo: AssistImageRepository,
        storage_service: StorageService,
    ):
        self.db = db
        self.image_repo = image_repo
        self.storage_service = storage_service

    async def create_image(self, image_data: ImageCreateSchema, uploaded_image: UploadFile) -> AssistImageModel:
        try:
            # Upload image to storage (uses default bucket "interactive-files")
            storage_path, image_url, original_filename = await self.storage_service.upload_image(
                image=uploaded_image,
                bucket_name=StorageBucket.INTERACTIVE_BUCKET,
                folder_prefix="images"
            )
            
            # Create image record in database
            image_dict = {
                "file_id": image_data.file_id,
                "image_title": image_data.image_title,
                "proposed_image_type": image_data.proposed_image_type,
                "is_protected": image_data.is_protected,
                "original_image_url": image_url,
                "searched_image_url": image_data.searched_image_url,
                "description": image_data.description,
                "bucket_name": StorageBucket.INTERACTIVE_BUCKET,
                "storage_path": storage_path,
                "image_3d_url": image_data.image_3d_url
            }
            
            image = await self.image_repo.create(image_dict)
            await self.db.commit()
            return image
        except Exception as e:
            await self.db.rollback()
            raise ServiceException(
                status_code=500,
                detail="Error creating image",
                additional_info={
                    "error": str(e), 
                    "image_data": image_data.model_dump(),
                    "filename": uploaded_image.filename
                },
            )

    async def get_image(self, image_id: UUID) -> Optional[AssistImageModel]:
        try:
            return await self.image_repo.get(image_id)
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error retrieving image",
                additional_info={"error": str(e), "image_id": str(image_id)},
            )

    async def get_images_by_file(self, file_id: UUID) -> List[AssistImageModel]:
        try:
            return await self.image_repo.get_images_by_file_id(file_id)
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error retrieving images by file",
                additional_info={"error": str(e), "file_id": str(file_id)},
            )

    async def get_images_by_type(
        self, image_type: AssistImageTypeEnum, file_id: Optional[UUID] = None
    ) -> List[AssistImageModel]:
        try:
            return await self.image_repo.get_images_by_type(image_type, file_id)
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error retrieving images by type",
                additional_info={
                    "error": str(e),
                    "image_type": image_type,
                    "file_id": str(file_id) if file_id else None,
                },
            )

    async def get_protected_images(self, file_id: Optional[UUID] = None) -> List[AssistImageModel]:
        try:
            return await self.image_repo.get_protected_images(file_id)
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error retrieving protected images",
                additional_info={
                    "error": str(e),
                    "file_id": str(file_id) if file_id else None,
                },
            )

    async def update_image(self, image_id: UUID, image_data: ImageUpdateSchema) -> Optional[AssistImageModel]:
        try:
            image_dict = image_data.model_dump(exclude_unset=True)
            if not image_dict:
                raise ServiceException(
                    status_code=400,
                    detail="No data provided for update",
                    additional_info={"image_id": str(image_id)},
                )
            
            image = await self.image_repo.update(image_id, image_dict)
            if image:
                await self.db.commit()
            return image
        except Exception as e:
            await self.db.rollback()
            raise ServiceException(
                status_code=500,
                detail="Error updating image",
                additional_info={"error": str(e), "image_id": str(image_id)},
            )

    async def delete_image(self, image_id: UUID) -> bool:
        try:
            # Get image info first to delete from storage
            image = await self.image_repo.get(image_id)
            if not image:
                return False
            
            # Delete from storage if storage info exists
            if image.storage_path and image.bucket_name:
                self.storage_service.delete_file_from_storage(image.bucket_name, image.storage_path)
            
            # Delete from database
            result = await self.image_repo.delete_image(image_id)
            if result:
                await self.db.commit()
            return result
        except Exception as e:
            await self.db.rollback()
            raise ServiceException(
                status_code=500,
                detail="Error deleting image",
                additional_info={"error": str(e), "image_id": str(image_id)},
            )