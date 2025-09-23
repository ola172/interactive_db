from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.interactive_models.image_model import ImageModel, ImageTypeEnum
from app.repositories.base_repo import BaseRepository
from app.exceptions.repo_exception import RepoException


class ImageRepository(BaseRepository[ImageModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ImageModel, db)

    async def get_images_by_file_id(self, file_id: UUID) -> List[ImageModel]:
        try:
            stmt = (
                select(ImageModel)
                .where(ImageModel.file_id == file_id)
                .options(selectinload(ImageModel.file))
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving images by file_id",
                additional_info={"error": str(e), "file_id": str(file_id)},
            )

    async def get_images_by_type(
        self, image_type: ImageTypeEnum, file_id: Optional[UUID] = None
    ) -> List[ImageModel]:
        try:
            stmt = select(ImageModel).where(
                ImageModel.proposed_image_type == image_type
            )
            
            if file_id:
                stmt = stmt.where(ImageModel.file_id == file_id)
                
            stmt = stmt.options(selectinload(ImageModel.file))
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving images by type",
                additional_info={
                    "error": str(e), 
                    "image_type": image_type,
                    "file_id": str(file_id) if file_id else None
                },
            )

    async def delete_image(self, image_id: UUID) -> bool:
        try:
            image = await self.get(image_id)
            if not image:
                return False
            
            await self.db.delete(image)
            await self.db.flush()
            return True
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error deleting image",
                additional_info={"error": str(e), "image_id": str(image_id)},
            )

    async def get_protected_images(self, file_id: Optional[UUID] = None) -> List[ImageModel]:
        try:
            stmt = select(ImageModel).where(ImageModel.is_protected == True)
            
            if file_id:
                stmt = stmt.where(ImageModel.file_id == file_id)
                
            stmt = stmt.options(selectinload(ImageModel.file))
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving protected images",
                additional_info={
                    "error": str(e),
                    "file_id": str(file_id) if file_id else None
                },
            )