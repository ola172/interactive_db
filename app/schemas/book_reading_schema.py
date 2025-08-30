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
    title: str
    description: str
    language: str
    level: str
    duration: int

    # book details
    author_name: str
    author_bio: Optional[str] = None
    cover_path: Optional[str] = None
    page_count: Optional[int] = None
    reading_time: Optional[int] = None
    readers_count: Optional[int] = 0
    is_new: Optional[bool] = False
    expected_time_completion: Optional[int] = None
    experience_required: Optional[str] = None

    # relations
    sections: Optional[List[BookSectionSchema]] = Field(default=None)
    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)
