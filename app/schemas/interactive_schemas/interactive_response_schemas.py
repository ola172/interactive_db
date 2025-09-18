import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from .interactive_request_schemas import VisualTypeEnum, ChartTypeEnum


# Word and Keyword Response Schemas
class KeyWordTypeResponse(BaseModel):
    id: uuid.UUID
    style_id: Optional[uuid.UUID] = Field(default=None)
    name: str

    class Config:
        from_attributes = True


class VideoKeywordTypeStyleResponse(BaseModel):
    id: uuid.UUID
    video_id: uuid.UUID
    keyword_type_id: uuid.UUID
    color_light: str
    color_dark: str
    shadow_light: Optional[str] = Field(default=None)
    shadow_dark: Optional[str] = Field(default=None)
    size: int

    class Config:
        from_attributes = True


class InteractiveWordResponse(BaseModel):
    id: uuid.UUID
    paragraph_id: uuid.UUID
    type_id: uuid.UUID
    word: str
    start_time: float
    end_time: float

    class Config:
        from_attributes = True


class InteractiveKeywordResponse(BaseModel):
    id: uuid.UUID
    paragraph_id: uuid.UUID
    type_id: uuid.UUID
    word: str

    class Config:
        from_attributes = True


# Visual Data Response Schemas


class VisualTypeResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class TableDataResponse(BaseModel):
    id: uuid.UUID
    headers: List[str]
    rows: List[List[str]]
    title: str
    caption: Optional[str]

    class Config:
        from_attributes = True


class ChartDataResponse(BaseModel):
    id: uuid.UUID
    chart_type: ChartTypeEnum
    labels: List[str]
    data: List[float]
    title: str

    class Config:
        from_attributes = True


class ImageDataResponse(BaseModel):
    id: uuid.UUID
    url: str
    alt_text: Optional[str] = Field(default=None)
    caption: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class VisualDataResponse(BaseModel):
    id: uuid.UUID
    visual_type: VisualTypeEnum
    paragraph_id: uuid.UUID
    start_time: float
    table_data: Optional[TableDataResponse] = Field(default=None)
    chart_data: Optional[ChartDataResponse] = Field(default=None)
    image_data: Optional[ImageDataResponse] = Field(default=None)

    class Config:
        from_attributes = True


# Paragraph Response Schemas
class InteractiveParagraphResponse(BaseModel):
    id: uuid.UUID
    video_id: uuid.UUID
    view_index: int
    paragraph_text: str
    start_time: float
    end_time: float
    words: List[InteractiveWordResponse] = Field(default=[])
    keywords: List[InteractiveKeywordResponse] = Field(default=[])
    visual_data: Optional[VisualDataResponse] = Field(default=None)

    class Config:
        from_attributes = True


# Video Response Schemas
class InteractiveVideoResponse(BaseModel):
    id: uuid.UUID
    chapter_id: uuid.UUID
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    url: str
    video_duration: str
    view_index: int
    paragraphs: List[InteractiveParagraphResponse] = Field(default=[])

    class Config:
        from_attributes = True


class InteractiveVideoDetails(BaseModel):
    title: str
    url: str
    video_duration: str
    view_index: Optional[int] = Field(default=None)
    quiz_id: Optional[uuid.UUID] = Field(default=None)


# Chapter Response Schemas
class InteractiveChapterResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    description: str
    about: Optional[str] = Field(default=None)
    view_index: int
    videos: List[InteractiveVideoDetails] = Field(default=[])

    class Config:
        from_attributes = True


# Course Response Schemas
class InteractiveCourseResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    pre_assessment_id: Optional[uuid.UUID] = Field(default=None)
    final_exam_id: Optional[uuid.UUID] = Field(default=None)
    chapters: List[InteractiveChapterResponse] = Field(default=[])

    class Config:
        from_attributes = True
