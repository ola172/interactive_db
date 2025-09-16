import uuid
from sqlalchemy import JSON, UUID, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class VisualTypeModel(Base):
    __tablename__ = "visual_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)      # e.g. chart, image, table
    description = Column(Text, nullable=True)

    visuals = relationship("VisualItemModel", back_populates="visual_type")



class ChartTypeModel(Base):
    __tablename__ = "chart_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)      # e.g. bar, line, pie, radar
    description = Column(Text, nullable=True)

    charts = relationship("ChartDataModel", back_populates="chart_type")


class TableDataModel(Base):
    __tablename__ = "table_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    headers = Column(JSON, nullable=False)   # list of strings
    data = Column(JSON, nullable=False)      # list of lists (rows)
    title = Column(Text, nullable=False)
    caption = Column(Text, nullable=True)

    visual_item = relationship("VisualItemModel", back_populates="table", uselist=False)


class ChartDataModel(Base):
    __tablename__ = "chart_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chart_type_id = Column(UUID(as_uuid=True), ForeignKey("chart_types.id"), nullable=False)
    data = Column(JSON, nullable=False)      # labels + datasets as JSON
    title = Column(String, nullable=False)

    chart_type = relationship("ChartTypeModel", back_populates="charts")
    visual_item = relationship("VisualItemModel", back_populates="chart", uselist=False)


class ImageModel(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(Text, nullable=False)
    title = Column(String, nullable=False)
    alt_text = Column(String, nullable=True)

    visual_item = relationship("VisualItemModel", back_populates="image", uselist=False)


class VisualItemModel(Base):
    __tablename__ = "visual_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    visual_type_id = Column(UUID(as_uuid=True), ForeignKey("visual_types.id"), nullable=False)
    paragraph_id = Column(UUID(as_uuid=True), ForeignKey("interactive_paragraph.id"))
    start_time = Column(Float, nullable=False)

    # references (only one should be filled)
    table_id = Column(UUID(as_uuid=True), ForeignKey("table_data.id"), nullable=True)
    chart_id = Column(UUID(as_uuid=True), ForeignKey("chart_data.id"), nullable=True)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id"), nullable=True)

    # Relationships
    visual_type = relationship("VisualTypeModel", back_populates="visuals")
    table = relationship("TableDataModel", back_populates="visual_item")
    chart = relationship("ChartDataModel", back_populates="visual_item")
    image = relationship("ImageModel", back_populates="visual_item")
    paragraph = relationship("InteractiveParagraphModel", back_populates="paragraph_visual")
