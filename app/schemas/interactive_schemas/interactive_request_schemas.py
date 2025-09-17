import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class VisualTypeEnum(str, Enum):
    CHART = "chart"
    IMAGE = "image"
    TABLE = "table"


class ChartTypeEnum(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    RADAR = "radar"


# Word and Keyword Request Schemas
class InteractiveWordCreateSchema(BaseModel):
    word_type_id: uuid.UUID  # Reference to WordType by ID
    word: str
    start_time: float
    end_time: float


class KeyWordTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class WordTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class InteractiveKeywordCreateSchema(BaseModel):
    keyword_type_id: uuid.UUID 
    word: str


class InteractiveKeywordUpdateSchema(BaseModel):
    word: Optional[str] = Field(default=None)
    keyword_type_id: Optional[uuid.UUID] = Field(default=None)


class KeyWordTypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class WordTypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class VisualTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class VisualTypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class ChartTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class ChartTypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


# Keyword Type Style Schema for Video
class VideoKeywordTypeStyleUpdateSchema(BaseModel):
    color_light: Optional[str] = Field(default=None)
    color_dark: Optional[str] = Field(default=None)
    shadow_light: Optional[str] = Field(default=None)
    shadow_dark: Optional[str] = Field(default=None)
    size: Optional[int] = Field(default=None)


# Visual Data Request Schemas
class TableDataCreateSchema(BaseModel):
    headers: List[str]
    rows: List[List[str]]
    title: str
    caption: Optional[str]


class ChartDataCreateSchema(BaseModel):
    chart_type_id: uuid.UUID  # Reference to ChartType by ID
    labels: List[str]  # Chart labels
    data: List[float]  # Chart data as list of floats or tuples
    title: str  # Chart title


class ImageDataCreateSchema(BaseModel):
    url: str
    alt_text: Optional[str] = Field(default=None)
    caption: Optional[str] = Field(default=None)


class VisualDataCreateSchema(BaseModel):
    visual_type_id: uuid.UUID
    start_time: float
    table_data: Optional[TableDataCreateSchema] = Field(default=None)
    chart_data: Optional[ChartDataCreateSchema] = Field(default=None)
    image_data: Optional[ImageDataCreateSchema] = Field(default=None)


class VisualDataUpdateSchema(BaseModel):
    visual_type_id: uuid.UUID
    start_time: Optional[float] = Field(default=None)
    table_data: Optional[TableDataCreateSchema] = Field(default=None)
    chart_data: Optional[ChartDataCreateSchema] = Field(default=None)
    image_data: Optional[ImageDataCreateSchema] = Field(default=None)


# Paragraph Request Schemas
class InteractiveParagraphCreateSchema(BaseModel):
    view_index: int
    paragraph_text: str
    start_time: float
    end_time: float
    words: List[InteractiveWordCreateSchema] = Field()
    keywords: List[InteractiveKeywordCreateSchema] = Field(default=[])
    visual_data: Optional[VisualDataCreateSchema] = Field(default=None)


# Video Request Schemas
class InteractiveVideoCreateSchema(BaseModel):
    chapter_id: uuid.UUID
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    url: str
    video_duration: float
    view_index: int
    paragraphs: List[InteractiveParagraphCreateSchema] = Field(description="All paragraphs data is required")


class InteractiveVideoUpdateSchema(BaseModel):
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)
    video_duration: Optional[float] = Field(default=None)  # Changed to float from str
    view_index: Optional[int] = Field(default=None)


# Chapter Request Schemas
class InteractiveChapterCreateSchema(BaseModel):
    course_id: uuid.UUID
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    description: str
    about: Optional[str] = Field(default=None)
    view_index: int


class InteractiveChapterUpdateSchema(BaseModel):
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    about: Optional[str] = Field(default=None)
    view_index: Optional[int] = Field(default=None)


# Course Request Schemas
class InteractiveChapterDetails(BaseModel):
    title: str
    description: str
    about: Optional[str] = Field(default=None)
    view_index: int
    quiz_id: Optional[uuid.UUID] = Field(default=None)


class InteractiveCourseCreateSchema(BaseModel):
    # Product fields (required for creating the product)
    category_id: uuid.UUID
    created_by: Optional[uuid.UUID] = Field(default=None)
    level_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    description: str
    language: str
    duration: str
    cover: Optional[str] = Field(default=None)
    short_video: Optional[str] = Field(default=None)
    
    # Interactive course specific fields
    pre_assessment_id: Optional[uuid.UUID] = Field(default=None)
    final_exam_id: Optional[uuid.UUID] = Field(default=None)
    
    # Related data
    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)
    chapters: Optional[List[InteractiveChapterDetails]] = Field(default=None)


class InteractiveCourseUpdateSchema(BaseModel):
    # Product fields (optional for updates)
    category_id: Optional[uuid.UUID] = Field(default=None)
    level_id: Optional[uuid.UUID] = Field(default=None)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    duration: Optional[str] = Field(default=None)
    cover: Optional[str] = Field(default=None)
    short_video: Optional[str] = Field(default=None)
    
    # Interactive course specific fields
    pre_assessment_id: Optional[uuid.UUID] = Field(default=None)
    final_exam_id: Optional[uuid.UUID] = Field(default=None)
    
    # Related data
    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)