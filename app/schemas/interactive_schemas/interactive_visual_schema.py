import uuid
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class VisualTypeResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class VisualTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)


class ChartTypeResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class ChartTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)


class TableDataSchema(BaseModel):
    headers: List[str]
    data: List[List[Any]]
    title: str
    caption: Optional[str] = Field(default=None)


class TableDataResponse(BaseModel):
    id: uuid.UUID
    headers: List[str]
    data: List[List[Any]]
    title: str
    caption: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class ChartDataSchema(BaseModel):
    chart_type_id: uuid.UUID
    data: Dict[str, Any]
    title: str


class ChartDataResponse(BaseModel):
    id: uuid.UUID
    chart_type_id: uuid.UUID
    data: Dict[str, Any]
    title: str
    chart_type: Optional[ChartTypeResponse] = Field(default=None)

    class Config:
        from_attributes = True


class ImageSchema(BaseModel):
    url: str
    title: str
    alt_text: Optional[str] = Field(default=None)


class ImageResponse(BaseModel):
    id: uuid.UUID
    url: str
    title: str
    alt_text: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class VisualItemSchema(BaseModel):
    visual_type_id: uuid.UUID
    paragraph_id: uuid.UUID
    start_time: float
    table_id: Optional[uuid.UUID] = Field(default=None)
    chart_id: Optional[uuid.UUID] = Field(default=None)
    image_id: Optional[uuid.UUID] = Field(default=None)


class VisualItemResponse(BaseModel):
    id: uuid.UUID
    visual_type_id: uuid.UUID
    paragraph_id: uuid.UUID
    start_time: float
    table_id: Optional[uuid.UUID] = Field(default=None)
    chart_id: Optional[uuid.UUID] = Field(default=None)
    image_id: Optional[uuid.UUID] = Field(default=None)
    visual_type: Optional[VisualTypeResponse] = Field(default=None)
    table: Optional[TableDataResponse] = Field(default=None)
    chart: Optional[ChartDataResponse] = Field(default=None)
    image: Optional[ImageResponse] = Field(default=None)

    class Config:
        from_attributes = True


class VisualItemCreateSchema(BaseModel):
    visual_type_id: uuid.UUID
    paragraph_id: uuid.UUID
    start_time: float
    table_id: Optional[uuid.UUID] = Field(default=None)
    chart_id: Optional[uuid.UUID] = Field(default=None)
    image_id: Optional[uuid.UUID] = Field(default=None)


class TableDataCreateSchema(BaseModel):
    headers: List[str]
    data: List[List[Any]]
    title: str
    caption: Optional[str] = Field(default=None)


class ChartDataCreateSchema(BaseModel):
    chart_type_id: uuid.UUID
    data: Dict[str, Any]
    title: str


class ImageCreateSchema(BaseModel):
    url: str
    title: str
    alt_text: Optional[str] = Field(default=None)