import uuid

from pydantic import BaseModel


class CourseCategoryBase(BaseModel):
    name: str
    description: str

class VideoDetails(BaseModel):
    title: str
    url: str


class ChapterDetails(BaseModel):
    title: str
    description: str
    videos: list[VideoDetails]


class CreateCourse(BaseModel):
    product_type_id: uuid.UUID
    title: str
    description: str
    language: str
    level: str
    duration: int
    chapters: list[ChapterDetails]
    certificate_included: bool = False