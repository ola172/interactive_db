import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class InteractiveKeyWordSchema(BaseModel):
    paragraph_id: uuid.UUID
    type_id: uuid.UUID
    word: str


class InteractiveKeyWordResponse(BaseModel):
    id: uuid.UUID
    paragraph_id: uuid.UUID
    type_id: uuid.UUID
    word: str

    class Config:
        from_attributes = True


class KeyWordTypeResponse(BaseModel):
    id: uuid.UUID
    style_id: Optional[uuid.UUID] = Field(default=None)
    name: str

    class Config:
        from_attributes = True


class KeyWordTypeCreateSchema(BaseModel):
    name: str


class VideoKeywordTypeStyleSchema(BaseModel):
    video_id: uuid.UUID
    keyword_type_id: uuid.UUID
    color_light: str
    color_dark: str
    shadow_light: Optional[str] = Field(default=None)
    shadow_dark: Optional[str] = Field(default=None)
    size: int = Field(default=14)


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


class VideoKeywordTypeStyleCreateSchema(BaseModel):
    video_id: uuid.UUID
    keyword_type_id: uuid.UUID
    color_light: str
    color_dark: str
    shadow_light: Optional[str] = Field(default=None)
    shadow_dark: Optional[str] = Field(default=None)
    size: int = Field(default=14)


class InteractiveKeyWordCreateSchema(BaseModel):
    paragraph_id: uuid.UUID
    type_id: uuid.UUID
    word: str


class KeyWordTypeWithStylesResponse(BaseModel):
    id: uuid.UUID
    style_id: Optional[uuid.UUID] = Field(default=None)
    name: str
    video_styles: Optional[List[VideoKeywordTypeStyleResponse]] = Field(default=None)

    class Config:
        from_attributes = True