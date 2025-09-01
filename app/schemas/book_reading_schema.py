import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class BookSectionSchema(BaseModel):
    title: str
    content: str
    stage_index: Optional[int] = Field(default=None)


class BookCreate(BaseModel):
    product_type_id: uuid.UUID
    product_category_id: uuid.UUID
    created_by: uuid.UUID
    title: str
    description: str
    language: str
    level_id: uuid.UUID
    duration: str
    short_video: Optional[str] = None
    cover: Optional[str] = None

    # book details
    author_name: str
    author_bio: Optional[str] = None
    page_count: Optional[int] = None
    reading_time: Optional[int] = None
    is_new: Optional[bool] = False

    # relations
    sections: Optional[List[BookSectionSchema]] = Field(default=None)
    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)
