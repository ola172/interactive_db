import uuid
import os
import re
from typing import Optional, Tuple
from fastapi import UploadFile

from app.core.storage import StorageClient
from app.exceptions.service_exception import ServiceException


class StorageService:
    def __init__(self, storage_client: StorageClient):
        self.storage_client = storage_client

    def _generate_unique_filename(self, original_filename: str, prefix: str = "") -> str:
        """Generate a unique filename with UUID prefix"""
        file_extension = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())
        processed_original_filename = re.sub(r'[^A-Za-z0-9\s]', '', original_filename)
        if prefix:
            return f"{prefix}/{unique_id}_{processed_original_filename}.{file_extension}"
        return f"{unique_id}_{processed_original_filename}.{file_extension}"

    async def upload_file(
        self, 
        file: UploadFile, 
        bucket_name: str,
        folder_prefix: str = "files"
    ) -> Tuple[str, str, str]:
        """
        Upload a file to storage and return (storage_path, file_url, original_filename)
        """
        try:
            # Generate unique filename
            unique_filename = self._generate_unique_filename(file.filename, folder_prefix)
            # Read file content
            content = await file.read()
            # Upload to storage
            upload_result = self.storage_client.upload_file(
                bucket_name=bucket_name,
                file_name=unique_filename,
                content=content
            )
            # Get public URL
            file_url = self.storage_client.get_file_url(bucket_name, unique_filename)
            return unique_filename, file_url, file.filename
            
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error uploading file to storage",
                additional_info={
                    "error": str(e),
                    "filename": file.filename,
                    "bucket_name": bucket_name
                },
            )

    async def upload_image(
        self, 
        image: UploadFile, 
        bucket_name: str,
        folder_prefix: str = "images"
    ) -> Tuple[str, str, str]:
        """
        Upload an image to storage and return (storage_path, image_url, original_filename)
        """
        try:
            # Validate image file type
            if not image.content_type or not image.content_type.startswith('image/'):
                raise ServiceException(
                    status_code=400,
                    detail="Invalid file type. Only images are allowed.",
                    additional_info={"content_type": image.content_type},
                )
            
            # Generate unique filename
            unique_filename = self._generate_unique_filename(image.filename, folder_prefix)
            
            # Read image content
            content = await image.read()
            
            # Upload to storage
            upload_result = self.storage_client.upload_file(
                bucket_name=bucket_name,
                file_name=unique_filename,
                content=content
            )
            
            # Get public URL
            image_url = self.storage_client.get_file_url(bucket_name, unique_filename)
            
            return unique_filename, image_url, image.filename
            
        except ServiceException:
            raise
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error uploading image to storage",
                additional_info={
                    "error": str(e),
                    "filename": image.filename,
                    "bucket_name": bucket_name
                },
            )

    def delete_file_from_storage(self, bucket_name: str, storage_path: str) -> bool:
        """
        Delete a file from storage
        """
        try:
            result = self.storage_client.delete_file(bucket_name, storage_path)
            return True
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error deleting file from storage",
                additional_info={
                    "error": str(e),
                    "bucket_name": bucket_name,
                    "storage_path": storage_path
                },
            )

    def get_file_url(self, bucket_name: str, storage_path: str) -> str:
        """
        Get public URL for a file
        """
        try:
            return self.storage_client.get_file_url(bucket_name, storage_path)
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Error getting file URL",
                additional_info={
                    "error": str(e),
                    "bucket_name": bucket_name,
                    "storage_path": storage_path
                },
            )