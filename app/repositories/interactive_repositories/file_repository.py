from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.interactive_models.files_model import FileModel
from app.models.interactive_models.file_type_model import FileTypeModel
from app.repositories.base_repo import BaseRepository
from app.exceptions.repo_exception import RepoException


class FileRepository(BaseRepository[FileModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(FileModel, db)

    async def get_files_by_video_id(self, video_id: UUID) -> List[FileModel]:
        try:
            stmt = (
                select(FileModel)
                .where(FileModel.video_id == video_id)
                .options(
                    selectinload(FileModel.file_type),
                    selectinload(FileModel.images)
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving files by video_id",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )

    async def get_file_with_images(self, file_id: UUID) -> Optional[FileModel]:
        try:
            stmt = (
                select(FileModel)
                .where(FileModel.id == file_id)
                .options(
                    selectinload(FileModel.file_type),
                    selectinload(FileModel.images)
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving file with images",
                additional_info={"error": str(e), "file_id": str(file_id)},
            )

    async def delete_file_and_images(self, file_id: UUID) -> bool:
        try:
            file = await self.get(file_id)
            if not file:
                return False
            
            await self.db.delete(file)
            await self.db.flush()
            return True
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error deleting file and images",
                additional_info={"error": str(e), "file_id": str(file_id)},
            )


class FileTypeRepository(BaseRepository[FileTypeModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(FileTypeModel, db)

    async def get_by_name(self, name: str) -> Optional[FileTypeModel]:
        try:
            stmt = select(FileTypeModel).where(FileTypeModel.name == name)
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving file type by name",
                additional_info={"error": str(e), "name": name},
            )